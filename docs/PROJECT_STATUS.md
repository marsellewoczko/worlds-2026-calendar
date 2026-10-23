# Project status — 2026-10-23

## Verified

- Python 3.12 standard-library synchronization; live Worlds API returned 46 current-season matches.
- Stable IDs, sequence updates, explicit cancellations, UTC offsets, escaped/folded ICS, preserved prior records and failure-safe output generation: 17 tests pass.
- Real Chromium: PL/EN, mobile/desktop, Warsaw/New York local times, clipboard, subscription URLs and disabled browser storage pass.
- Local page and ICS generated from live source. The generated site is ignored; data/events.json is the durable real-source snapshot.

## Deployment and limits

- Workflow targets GitHub Pages and runs at minutes 7 and 37, on manual request and relevant main changes. Schedule delivery and subscriber refresh cadence are not guaranteed.
- Code commit [`dfd1ae0`](https://github.com/marsellewoczko/worlds-2026-calendar/commit/dfd1ae0314046564e9fca8e0e88dcebc17d6969e) is pushed to `main`. [GitHub CI](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39913285145) passed.
- [Deployment run](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39913285142) passed tests, live sync and state persistence, then failed at `actions/configure-pages@v5`; upload and deploy were skipped.
- Pages is not enabled: GET /pages and both public HTML/ICS return 404. Attempting to enable it through GitHub API returned `403 Resource not accessible by integration`. This integration cannot activate Pages, despite reporting repository admin permission. Public MVP is **not deployed**.
- No Google/Apple/Outlook account subscription has been manually tested. No personal portfolio implementation was changed.
- Unofficial API availability, upstream ID changes and stale or missing source data remain risks. Omitted games are retained; explicit complete cancellation records update status. Estimated end times are disclosed.

## Next step

Owner action: in Settings → Pages → Build and deployment set Source to GitHub Actions. Then run the publish workflow manually on main (or rerun the failed deployment). Verify public HTML/ICS, and perform real subscriptions in Google Calendar, Apple Calendar and Outlook. Network access to GitHub API/Pages is now working; activation permission is the remaining deployment blocker.
