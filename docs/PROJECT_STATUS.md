# Project status — 2026-10-23

## Verified

- Python 3.12 standard-library synchronization; live Worlds API returned 46 current-season matches.
- Stable IDs, sequence updates, explicit cancellations, UTC offsets, escaped/folded ICS, preserved prior records and failure-safe output generation: 17 tests pass.
- Real Chromium: PL/EN, mobile/desktop, Warsaw/New York local times, clipboard, subscription URLs and disabled browser storage pass.
- Local page and ICS generated from live source. The generated site is ignored; data/events.json is the durable real-source snapshot.

## Deployment and limits

- Workflow targets GitHub Pages and runs at minutes 7 and 37, on manual request and relevant main changes. Schedule delivery and subscriber refresh cadence are not guaranteed.
- Public deployment, Pages settings and Actions results are **unverified**: the cloud network proxy denied GitHub API and the Pages hostname. Successful Git access does not prove Pages configuration.
- No Google/Apple/Outlook account subscription has been manually tested. No personal portfolio implementation was changed.
- Unofficial API availability, upstream ID changes and stale or missing source data remain risks. Omitted games are retained; explicit complete cancellation records update status. Estimated end times are disclosed.

## Next step

Apply the saved network settings, inspect the deployed Actions run and verify public HTML/ICS. If Pages is not enabled, follow README deployment instructions. Then perform real subscriptions in the three supported calendar clients and record results. Code push and deployment evidence is recorded in BUILD_LOG.md as available.
