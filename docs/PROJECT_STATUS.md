# Project status — 2026-10-24

## Verified

- Python 3.12 standard-library synchronization; live Worlds API returned 46 current-season matches.
- Stable IDs, sequence updates, explicit cancellations, UTC offsets, escaped/folded ICS, preserved prior records and failure-safe output generation: 28 tests pass.
- Real Chromium: PL/EN, mobile/desktop, Warsaw/New York local times, clipboard, subscription URLs and disabled browser storage pass.
- Local page and ICS generated from live source. The generated site is ignored; data/events.json is the durable real-source snapshot.

- Score-note change is deployed and publicly verified: 14 real final scores appear only in ICS descriptions; all 46 UIDs and titles are preserved. Updated result events have increased SEQUENCE values. Live snapshots include a fetch timestamp (unit tested; no in-progress matches in the inspected source snapshot).

- Source removal from calendar notes is deployed and publicly verified: all 46 UIDs preserved, SEQUENCE increased for all events, scores retained, source attribution remains on the website. Text editing instructions: [EDITING_TEXTS.md](EDITING_TEXTS.md).

## Deployment and limits

- Workflow targets GitHub Pages and runs at minutes 7 and 37, on manual request and relevant main changes. Schedule delivery and subscriber refresh cadence are not guaranteed.
- Code commit [`dfd1ae0`](https://github.com/marsellewoczko/worlds-2026-calendar/commit/dfd1ae0314046564e9fca8e0e88dcebc17d6969e) is pushed to `main`. [GitHub CI](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39913285145) passed.
- Public deployment is verified. [Scheduled run 40091990593](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40091990593), created 2026-10-24 at 13:58:02 Europe/Warsaw, completed successfully at 13:58:22: tests, live sync, state persistence, artifact upload and Pages deployment all passed. The five latest runs returned success.
- Public HTML and calendar.ics both return HTTP 200. Both contain the same 46 source event identities; ICS UIDs are unique and folded lines stay within 75 octets. Previous Pages activation/waiting blockers are resolved.
- No Google/Apple/Outlook account subscription has been manually tested. No personal portfolio implementation was changed.
- Unofficial API availability, upstream ID changes and stale or missing source data remain risks. Omitted games are retained; explicit complete cancellation records update status. Estimated end times are disclosed.

## Next step

Perform actual URL subscriptions in Google Calendar, Apple Calendar and Outlook, then verify provider refresh after a genuine source update. Keep monitoring the unofficial API and scheduled sync; do not assume provider refresh is immediate.

## Possible future enhancement

Explore creator-authorized match recap links. A version without score notes is a proposal for spoiler-free recap viewing, not an implemented change. No creator contact or permission is claimed.

- Latest UI update: colored calendar/language buttons and removed subscription eyebrow; real-browser checks passed, publication pending.

- Note layout update: score first, author credit last after a blank line; 28 tests passed, deployment pending.
