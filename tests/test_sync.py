from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import patch
import sync

def fixture(mid="11", name="TBD", start="2026-10-23T15:00:00Z"):
    return {"type":"match","startTime":start,"blockName":"Swiss","match":{"id":mid,"teams":[{"code":name},{"code":"G2"}],"strategy":{"count":1}}}

class CalendarTests(TestCase):
    def test_stable_uid_and_updates(self):
        now = datetime(2026,10,23,tzinfo=timezone.utc)
        first,_ = sync.merge({},[fixture()],now)
        later,_ = sync.merge(first,[fixture(name="T1",start="2026-10-23T16:00:00Z")],now)
        self.assertEqual(first["11"]["sequence"],0)
        self.assertEqual(later["11"]["sequence"],1)
        self.assertIn("UID:worlds2026-riot-11@marsellewoczko.com",sync.make_ics(later))
        self.assertIn("Created by Marsel Lewoczko",sync.make_ics(later).replace("\r\n ", ""))

    def test_empty_api_fails_closed(self):
        with self.assertRaises(RuntimeError):
            sync.merge({},[],datetime(2026,10,23,tzinfo=timezone.utc))

    def test_preserves_previous_games(self):
        now=datetime(2026,10,23,tzinfo=timezone.utc)
        state,_=sync.merge({},[fixture()],now)
        state,_=sync.merge(state,[fixture(mid="12")],now)
        self.assertEqual(len(state),2)

    def test_unicode_folding(self):
        for row in sync.folded("SUMMARY:" + "🔥"*40).split("\r\n"):
            self.assertLessEqual(len(row.encode()),75)

    def test_html_escaped(self):
        now=datetime(2026,10,23,tzinfo=timezone.utc)
        state,_=sync.merge({},[fixture(name="</script><script>alert(1)</script>")],now)
        page=sync.make_html(state,now)
        self.assertNotIn("</script><script>alert(1)",page)
        self.assertIn("marsellewoczko.com",page)

    def test_external_season_rejected(self):
        with self.assertRaises(RuntimeError):
            sync.merge({},[fixture(start="2027-10-23T15:00:00Z")],datetime(2026,10,23,tzinfo=timezone.utc))

class ReliabilityTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 23, tzinfo=timezone.utc)

    def test_unchanged_event_keeps_sequence_and_timestamp(self):
        first, _ = sync.merge({}, [fixture()], self.now)
        second, changes = sync.merge(first, [fixture()], datetime(2026, 10, 24, tzinfo=timezone.utc))
        self.assertEqual(first, second)
        self.assertEqual(changes, 0)

    def test_cancellation_updates_existing_uid(self):
        first, _ = sync.merge({}, [fixture()], self.now)
        event = fixture()
        event['state'] = 'canceled'
        later, _ = sync.merge(first, [event], self.now)
        text = sync.make_ics(later)
        self.assertIn('STATUS:CANCELLED', text)
        self.assertIn('SEQUENCE:1', text)
        self.assertEqual(text.count('BEGIN:VEVENT'), 1)
        self.assertIn('UID:worlds2026-riot-11@marsellewoczko.com', text)

    def test_offset_dates_normalized_to_utc_and_estimated_duration(self):
        event = fixture(start='2026-10-23T17:00:00+02:00')
        event['match']['strategy']['count'] = 5
        state, _ = sync.merge({}, [event], self.now)
        text = sync.make_ics(state)
        self.assertIn('DTSTART:20261023T150000Z', text)
        self.assertIn('DTEND:20261023T200000Z', text)
        with self.assertRaises(ValueError):
            sync.parse_time('2026-10-23T15:00:00')

    def test_crlf_cannot_inject_ical_properties(self):
        state, _ = sync.merge({}, [fixture(name='T1\r\nSTATUS:CANCELLED')], self.now)
        text = sync.make_ics(state)
        self.assertNotIn('\r\nSTATUS:CANCELLED', text)
        self.assertIn('T1\\nSTATUS:CANCELLED', text)

    def test_empty_current_source_fails_even_with_previous_events(self):
        state, _ = sync.merge({}, [fixture()], self.now)
        with self.assertRaises(RuntimeError):
            sync.merge(state, [], self.now)

    def test_other_league_and_malformed_rows_rejected(self):
        event = fixture()
        event['league'] = {'slug': 'lec'}
        for bad in (event, None, [], {'type': 'show'}, fixture(start='bad')):
            self.assertIsNone(sync.normalized(bad))

    def test_window_boundaries(self):
        self.assertIsNotNone(sync.normalized(fixture(start='2026-10-01T00:00:00Z')))
        self.assertIsNone(sync.normalized(fixture(start='2026-12-01T00:00:00Z')))

    def test_overlapping_schedule_pages_deduplicated(self):
        first = {'events': [fixture()], 'pages': {'older': 'older'}}
        older = {'events': [fixture(), fixture(mid='12')], 'pages': {}}
        with patch.object(sync, 'get', side_effect=[{'schedule': first}, {'schedule': older}]):
            self.assertEqual(len(sync.download('worlds')), 2)

    def test_invalid_schedule_page_fails_closed(self):
        with patch.object(sync, 'get', return_value={'schedule': {'events': None}}):
            with self.assertRaises(RuntimeError):
                sync.download('worlds')

    def test_run_preserves_files_on_api_empty_or_render_failure(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state, _ = sync.merge({}, [fixture()], self.now)
            import json
            state_path = root / 'events.json'
            state_path.write_text(json.dumps(state))
            site = root / 'site'
            site.mkdir()
            (site / 'index.html').write_text('old html')
            (site / 'calendar.ics').write_text('old feed')
            original = {p: p.read_bytes() for p in (state_path, site/'index.html', site/'calendar.ics')}
            with patch.object(sync, 'STATE', state_path), patch.object(sync, 'SITE', site), patch.object(sync, 'league_id', return_value='worlds'):
                with patch.object(sync, 'download', side_effect=RuntimeError('API unavailable')):
                    with self.assertRaises(RuntimeError):
                        sync.run()
                with patch.object(sync, 'download', return_value=[]):
                    with self.assertRaises(RuntimeError):
                        sync.run()
                with patch.object(sync, 'download', return_value=[fixture(name='T1')]), patch.object(sync, 'make_html', side_effect=ValueError('bad template')):
                    with self.assertRaises(ValueError):
                        sync.run()
            for path, content in original.items():
                self.assertEqual(path.read_bytes(), content)

    def test_atomic_write_failure_preserves_destination_and_cleans_temp(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'events.json'
            target.write_bytes(b'old')
            with patch('os.fsync', side_effect=OSError('disk failure')):
                with self.assertRaises(OSError):
                    sync.atomic_write(target, b'new')
            self.assertEqual(target.read_bytes(), b'old')
            self.assertEqual(list(Path(directory).iterdir()), [target])

class ScoreNotesTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 24, 12, 0, tzinfo=timezone.utc)

    def scored(self, state='completed', scores=(3, 2)):
        event = fixture(name='T1')
        event['state'] = state
        event['match']['strategy']['count'] = 5
        for team, score in zip(event['match']['teams'], scores):
            team['result'] = {'gameWins': score}
        return event

    def unfolded(self, state):
        return sync.make_ics(state).replace('\r\n ', '')

    def test_final_score_is_in_description_only(self):
        state, _ = sync.merge({}, [self.scored()], self.now)
        text = self.unfolded(state)
        summary = next(row for row in text.split('\r\n') if row.startswith('SUMMARY:'))
        self.assertEqual(summary, 'SUMMARY:T1 vs G2 | Worlds 2026 (Bo5)')
        self.assertIn('Wynik końcowy / Final result: T1 3–2 G2', text)
        self.assertNotIn('Live:', text)

    def test_live_score_has_observation_timestamp(self):
        state, _ = sync.merge({}, [self.scored('inProgress', (1, 2))], self.now)
        text = self.unfolded(state)
        self.assertIn('Live: T1 1–2 G2', text)
        self.assertIn('Last fetched: 2026-10-24 12:00 UTC', text)
        self.assertIn('not a real-time feed', text)
        self.assertNotIn('Final result:', text)

    def test_live_refresh_and_final_update_keep_same_uid(self):
        first, _ = sync.merge({}, [self.scored('inProgress', (1, 2))], self.now)
        later = datetime(2026, 10, 24, 12, 30, tzinfo=timezone.utc)
        refreshed, _ = sync.merge(first, [self.scored('inProgress', (1, 2))], later)
        final, _ = sync.merge(refreshed, [self.scored()], later)
        self.assertEqual(refreshed['11']['sequence'], 1)
        self.assertEqual(final['11']['sequence'], 2)
        self.assertIn('Last fetched: 2026-10-24 12:30 UTC', self.unfolded(refreshed))
        self.assertNotIn('score_checked_at', final['11'])
        for state in (first, refreshed, final):
            self.assertIn('UID:worlds2026-riot-11@marsellewoczko.com', self.unfolded(state))

    def test_final_score_is_stable_and_corrections_increment_sequence(self):
        first, _ = sync.merge({}, [self.scored()], self.now)
        same, count = sync.merge(first, [self.scored()], datetime(2026, 10, 25, tzinfo=timezone.utc))
        self.assertEqual(same, first)
        self.assertEqual(count, 0)
        corrected, _ = sync.merge(same, [self.scored(scores=(2, 3))], self.now)
        self.assertEqual(corrected['11']['sequence'], 1)
        self.assertIn('Final result: T1 2–3 G2', self.unfolded(corrected))

    def test_unstarted_and_missing_results_do_not_invent_scores(self):
        event = self.scored('unstarted', (0, 0))
        self.assertNotIn('score', sync.normalized(event))
        for team in event['match']['teams']:
            team.pop('result')
        for state in ('inProgress', 'completed'):
            event['state'] = state
            normalized = sync.normalized(event)
            self.assertNotIn('score', normalized)

    def test_invalid_and_incomplete_final_scores_are_omitted(self):
        for scores in ((None, 1), ('3', 1), (True, 1), (-1, 3), (4, 1), (0, 0), (2, 1), (3, 3)):
            with self.subTest(scores=scores):
                self.assertNotIn('score', sync.normalized(self.scored(scores=scores)))

    def test_explicit_live_zero_zero_is_valid(self):
        self.assertEqual(sync.normalized(self.scored('inProgress', (0, 0)))['score'], [0, 0])

    def test_temporarily_missing_results_keep_score_without_fresh_timestamp(self):
        first, _ = sync.merge({}, [self.scored('inProgress', (1, 2))], self.now)
        event = self.scored('inProgress')
        for team in event['match']['teams']:
            team.pop('result')
        later, count = sync.merge(first, [event], datetime(2026, 10, 24, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(later, first)
        self.assertEqual(count, 0)
        self.assertIn('Last fetched: 2026-10-24 12:00 UTC', self.unfolded(later))

    def test_old_live_score_is_not_presented_as_final_when_final_result_missing(self):
        first, _ = sync.merge({}, [self.scored('inProgress', (1, 2))], self.now)
        event = self.scored()
        event['match']['teams'][0].pop('result')
        final, _ = sync.merge(first, [event], self.now)
        self.assertNotIn('score', final['11'])
        self.assertNotIn('Final result:', self.unfolded(final))
