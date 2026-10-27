# Project status — 2026-10-27

## Product

- One canonical page: https://lolworldscalendar.com/. Feed: https://lolworldscalendar.com/calendar.ics.
- PL/EN interface, calendar subscription, local match times, source attribution, author credit and screenshot explanation. Match results appear in ICS notes, not in event titles or visible schedule rows.
- Stable UIDs/SEQUENCE, explicit cancellations and last successful data preserved on source/render failure. Estimated end times and refresh limitations are disclosed.
- Published update adds seven PL/EN FAQ entries on the same page and initial HTML schedule rows in UTC. JavaScript upgrades UTC times to the browser timezone. A fragment link reaches FAQ without creating another page.

## Verification

- Python 3.12 standard-library runtime. All 31 unit/integration tests pass, including UTC initial rows, escaping source text, update identity and error paths.
- Chromium checks pass on mobile/desktop: PL/EN, local times, clipboard, blocked storage, FAQ anchor/keyboard interaction. With JavaScript disabled, 46 source matches, UTC labels, FAQ disclosure and subscription URL remain available.
- Production page and ICS return HTTPS 200. Latest publish run 40199501228 succeeded; public raw HTML contains 46 UTC event rows and seven FAQ questions. Legacy GitHub Pages URLs and www redirect to the canonical HTTPS domain. Deployment evidence for the latest update is recorded in BUILD_LOG.md.
- Search Console owner evidence confirms sitemap Success, URL is on Google, Page is indexed and correct canonical. Query rankings, impressions and traffic have not been established.

## Public repository review

- Reviewed tracked source, templates, tests, workflows and documentation, and scanned 145 reachable historical blobs for common credential patterns. No matches, tracked .env/credential files, TODO/FIXME markers or debug statements were found.
- The LoL Esports public website API key is intentional and is not a personal credential. Technical comments, test fixtures and public development documentation are retained. Pattern-based checks do not establish a comprehensive security audit.
- README describes the deployed product; historical intermediate results remain in BUILD_LOG.md with an explicit note that they are observations at that time.

## Limits and next steps

- Unofficial source availability, changed source IDs, calendar-provider refresh cadence and estimated durations remain limitations. A URL subscription is required instead of one-time import.
- Actual Google/Apple/Outlook account refresh is a user acceptance check. Creator-authorized recap links and removing score notes are proposals only; no creator permission or integration is claimed.
- Monitor scheduled sync and Search Console Performance. Keep FAQ, instructions and schedule together on this single page.

- Latest note change: Imported from https://lolworldscalendar.com/ replaces author credit in ICS only. Version 4 refreshes existing events; 31 tests and live local generation passed.
