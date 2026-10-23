# Worlds 2026 Live Calendar

Fan-made, automatically updated League of Legends Worlds 2026 calendar by **Marsel Lewoczko**.

- **Website (after deployment):** https://marsellewoczko.github.io/worlds-2026-calendar/
- **Subscribable iCalendar feed (after deployment):** https://marsellewoczko.github.io/worlds-2026-calendar/calendar.ics
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
