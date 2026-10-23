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
