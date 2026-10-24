# Build log

## 2026-10-23 — Audit

- Inspected sync.py, template.html, both original tests and deployment workflow, README, empty production state and the seven existing commits.
- Baseline: 6 tests executed; 5 passed, one failed because it searched a folded ICS description without unfolding it. This prevented the deployment job from reaching synchronization.
- After the previously configured API domain became available, authenticated live getLeagues/getSchedule requests succeeded: Worlds league `98767975604431411`, 160 raw events across pages, 46 normalized matches in October/November 2026. A request without the website key returned 403; authenticated requests returned 200.
- Native Git read succeeded. GitHub API and public Pages requests were denied by the environment network proxy, so repository Pages settings, Actions runs and public output could not be inspected.

## 2026-10-23 — Reliability and interface changes

- Fixed the folded-description assertion, added 11 reliability tests, normalized CR/LF in ICS text, rejected other-league rows and empty current-season responses, and added atomic per-file writes after complete rendering.
- Added optional --state/--site CLI paths, ignored generated files, separate CI, main-branch deployment triggers and job timeouts.
- Added author metadata, kept explicit independent-fan branding, displayed translated match status and hardened language preferences against disabled/invalid browser storage.
- Added AGENTS.md, this log, decisions and current status. No personal website code was changed.
- Verified 17/17 unit tests. Failure-path checks confirmed API/empty-source/render failures preserve existing outputs and state. Interrupted temporary writes preserve the previous destination.
- Live local generation produced 46 events. Real Chromium checks passed at mobile (390px) and desktop widths in Europe/Warsaw and America/New_York: PL/EN, saved preference, exact local times, match counts, no horizontal overflow, webcal link, HTTP ICS response and clipboard content. Disabled localStorage did not break rendering or language selection.
- Tests use fixtures only in tests; the production snapshot is generated only by authenticated live API requests.
- Saved additional network requirements for api.github.com and marsellewoczko.github.io alongside the existing esports-api.lolesports.com rule. Draft saving alone does not apply policy or publish the environment.

## 2026-10-23 — Remote delivery and confirmed deployment blocker

- Generated the tracked production snapshot directly from the live API: 46 events. Verified output event count, CRLF line endings and the 75-octet folding limit.
- Committed and pushed [`dfd1ae0`](https://github.com/marsellewoczko/worlds-2026-calendar/commit/dfd1ae0314046564e9fca8e0e88dcebc17d6969e) to main with a normal fast-forward push; remote SHA was verified.
- GitHub API and Pages became reachable after network settings propagation. [Tests run 39913285145](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39913285145) completed successfully.
- [Publish run 39913285142](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39913285142) passed tests, live schedule generation and snapshot persistence. It failed at configure-pages; artifact upload and deployment were skipped.
- Repository is public, default branch main. GET Pages configuration returned 404. Attempted authorized activation using POST /repos/marsellewoczko/worlds-2026-calendar/pages with build_type=workflow; GitHub denied the integration with HTTP 403 (Resource not accessible by integration). No settings were changed by that failed request.
- Both public HTML and calendar.ics returned HTTP 404. Deployment cannot be claimed. Detailed downloadable Actions logs were inaccessible on a separate logs hostname, but the run/job API exposed the failed step and all preceding outcomes.
- Required owner action: Settings → Pages → Build and deployment → Source: GitHub Actions; then manually run the publish workflow on main or rerun the failed job. README contains the acceptance checklist. Calendar-account acceptance remains unrun.

## 2026-10-23 — Owner activated Pages

- Owner supplied screenshots showing GitHub Actions saved as the Pages source and manual workflow dispatch.
- Verified through GitHub API: build_type=workflow, https_enforced=true, expected public URL.
- Manual publish run [39916652277](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39916652277) is queued for a runner, with no steps started at this observation. Public HTML/ICS still return 404 pending first deployment. The prior activation blocker is resolved.

- Follow-up API observation: run advanced to waiting on github-pages, still without started steps. Environment policy allows main, has no reviewers and wait_timer=0; current_user_can_approve=false. No protection settings were weakened or changed.

## 2026-10-24 — Public deployment verified

- Latest five publish runs completed successfully. Latest inspected [run 40091990593](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40091990593) was triggered by schedule and passed every step, including tests, live synchronization, snapshot persistence, upload and Pages deployment. Run timestamps: 13:58:02–13:58:22 Europe/Warsaw.
- Public page https://marsellewoczko.github.io/worlds-2026-calendar/ and calendar.ics both returned HTTP 200. Parsed embedded HTML events and public ICS: the same 46 identities, 46 unique UIDs, resolved template, author credit and valid 75-octet line folding.
- Fetched and fast-forwarded the local checkout to retain automatic upstream schedule updates before documentation changes. No application code changed in this verification session.
- Previous Pages activation and waiting blockers are resolved. Actual Google/Apple/Outlook account subscriptions remain untested; this check proves public availability and successful scheduled deployment, not client refresh behavior.

## 2026-10-24 — Scores inside calendar notes

- Added explicit API gameWins extraction for completed/inProgress matches. Completed matches require a valid series-winning score. Missing, malformed or unstarted results do not become invented scores.
- ICS DESCRIPTION now includes bilingual final-result labels or Live with the last successful observation time (UTC) and a last-sync disclaimer. SUMMARY remains unchanged and contains no score; the schedule interface does not display scores.
- Live observations update timestamp and SEQUENCE so subscribers can see when the score was fetched. Final results remain stable until corrected. Missing results for unchanged teams/state retain the previous verified score and timestamp; a missing final result is never inferred from a prior live score.
- All 26 unit tests passed, including 9 new score tests. Live local API build produced 46 matches with 14 final-score descriptions and no scores in event summaries. No live matches were available in that source snapshot; live-note behavior is unit tested, not claimed as observed in production.
- Deployment of this change will be verified separately after pushing; provider refresh remains outside the server's control.
