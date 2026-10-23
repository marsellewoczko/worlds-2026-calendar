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
        self.assertIn("Created by Marsel Lewoczko",sync.make_ics(later))

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
