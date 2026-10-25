# Worlds 2026 Live Calendar

Fan-made, automatically updated League of Legends Worlds 2026 calendar by **Marsel Lewoczko**.

- **Website:** https://lolworldscalendar.com/
- **Subscribable iCalendar feed:** https://lolworldscalendar.com/calendar.ics
- **Author and projects:** https://marsellewoczko.com

Includes a bilingual PL/EN responsive website with local match times, stable event identities, and links to add the calendar to Apple Calendar, Outlook, and Google Calendar.

## Activate deployment

1. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Repo **Actions → Sync and publish Worlds 2026 calendar → Run workflow**.
3. Check the workflow logs, website and ICS feed; a successful first sync requires LoL Esports' website API to return actual Worlds 2026 fixtures.
4. Repo **Settings → Actions → General → Workflow permissions**: select **Read and write permissions** if the workflow cannot save updated data/events.json.

Automatic sync runs approximately every 30 minutes when GitHub delivers scheduled workflows. Subscribers' calendar apps refresh at their own cadence; do not use one-time ICS import.

## Implementation

`sync.py` fetches Worlds matches from LoL Esports' undocumented web endpoint `getLeagues` and paginated `getSchedule`, keeps only 2026-10/11 match data, and persists event IDs in `data/events.json`. It updates existing calendar events by keeping their iCalendar UID and raising SEQUENCE when anything changes. If source/API fails or a first run has zero Worlds fixtures, it stops instead of publishing made-up matches.

`template.html` defines the landing page; its EN/PL language toggle is independent of the bilingual personal portfolio proposed at marsellewoczko.com.

### Caveats

- This is an independent community project, not endorsed by Riot Games.
- The LoL Esports website API is unofficial and can change, restrict traffic, or become unavailable. Never assume availability until the first live workflow succeeds.
- Calendar end times are estimates, and updates in Apple/Google/Outlook are not instantaneous.
- Historic events in the state file remain even if omitted from rolling schedule pages; cancellation and changed identities may require manual review.
- GitHub Pages must be activated in repository settings before the addresses above work.

### Run local unit tests

```bash
python -m unittest discover -s tests -v
```

MIT license. All Riot Games marks remain the property of their respective owners.

## Development and verification

Use Python **3.12** (matching CI). Runtime dependencies: none.

```bash
python -B -m unittest discover -s tests -v
python -B sync.py --state .local/events.json --site .local/site
python -B -m http.server 8000 --directory .local/site
```

The local paths keep development output separate from the durable production snapshot. Running `python sync.py` without overrides updates `data/events.json` and generates `site/`. Only real matches returned by the API enter the production snapshot. `LOL_ESPORTS_API_KEY` optionally overrides the public website key; `WORLDS_LEAGUE_ID` optionally overrides league discovery. Do not commit secret values.

Optional real-browser checks (requires Playwright and a Chromium installation):

```bash
python -m pip install playwright
python -B tools/browser_smoke.py http://127.0.0.1:8000 --chromium /usr/bin/chromium
```

This checks mobile/desktop layout, local match times in two timezones, PL/EN, clipboard, subscription links and restricted browser storage. Test fixtures never populate the production schedule. No third-party Python package is needed for the scheduled sync or unit tests.

## Deployment acceptance checklist

1. In **Settings → Pages**, choose **GitHub Actions** as the source. No custom domain is required.
2. In **Settings → Actions → General**, enable Actions. If saving the snapshot is denied, allow **Read and write permissions** where repository/organization policy permits it.
3. In **Settings → Environments → github-pages**, allow deployments from `main`; resolve any required reviewer gate deliberately.
4. Open **Actions → Sync and publish Worlds 2026 calendar → Run workflow**, select `main`. Tests, sync, snapshot commit and Pages deployment must all succeed. Relevant code pushes to `main` also trigger this workflow; snapshot commits do not trigger a deployment loop.
5. Request both public URLs above. Confirm HTML displays real matches and `calendar.ics` returns HTTP 200 with `BEGIN:VCALENDAR`, stable `UID` values and current events. A source failure must leave the previously deployed site and committed snapshot intact.
6. Subscribe using the URL (never a one-time file import): Google Calendar → **Other calendars → From URL**; Apple Calendar → **New Calendar Subscription**; Outlook web → **Add calendar → Subscribe from web**. Verify the same UID is updated after a genuine upstream change. Refresh frequency is controlled by each provider; do not claim instant synchronization.

The generator uses UTC in ICS; the page formats times in the visitor's local timezone. Explicit cancellation states are published as `STATUS:CANCELLED`. Missing matches are retained because rolling source pages are not cancellation notices. If upstream changes a match ID or omits cancellation details, manual review may be needed. Empty or unusable current-season API data fails the job rather than silently republishing a stale feed as fresh. Render/API failures keep the previous local outputs; deployment stops before uploading a failed build. Individual output replacements are atomic, not a transaction across all files.

See [project status](docs/PROJECT_STATUS.md), [build log](docs/BUILD_LOG.md) and [technical decisions](docs/DECISIONS.md) for verified progress and remaining acceptance checks.


Scores appear only in calendar event notes (ICS DESCRIPTION), never in event titles or visible schedule rows. Completed matches show **Wynik końcowy / Final result**; ongoing matches show **Live**, the last successful fetch time in UTC and a reminder that the score is a sync snapshot. These are series game wins from the source, not individual-game kills. Missing results are not invented. Refresh your subscribed calendar to fetch changes when your provider allows it; the server cannot force Google/Apple/Outlook refreshes.

Teksty strony PL/EN możesz zmieniać w `template.html`, w sekcji `const strings`. Zobacz [instrukcję edycji tekstów](docs/EDITING_TEXTS.md).


Custom domain migration: `lolworldscalendar.com` is configured in GitHub Pages. DNS uses the four GitHub Pages A records and a `www` CNAME to `marsellewoczko.github.io`. Custom Actions deployment uses the Pages setting; it does not require a CNAME file in the artifact. Keep existing UID values unchanged. The legacy GitHub Pages URLs issue 301 redirects to the corresponding new paths; actual provider handling must be checked. HTTPS enforcement and end-to-end checks are tracked in docs/PROJECT_STATUS.md.
