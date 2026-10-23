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
- The owner enabled Pages with GitHub Actions. GitHub API now confirms build_type=workflow and enforced HTTPS. [Manual publish run 39916652277](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/39916652277) has advanced from queued to waiting on the github-pages environment; no job steps have started. Public HTML/ICS still return 404, so deployment is not yet confirmed.
- No Google/Apple/Outlook account subscription has been manually tested. No personal portfolio implementation was changed.
- Unofficial API availability, upstream ID changes and stale or missing source data remain risks. Omitted games are retained; explicit complete cancellation records update status. Estimated end times are disclosed.

## Next step

Wait for manual publish run 39916652277 to complete, then verify public HTML/ICS and perform real subscriptions in Google Calendar, Apple Calendar and Outlook. Pages activation is complete; GitHub environment release is currently pending. The environment allows main, has no reviewers and no wait timer; API reports current_user_can_approve=false, so no specific owner approval action is established.
