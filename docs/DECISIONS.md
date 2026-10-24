# Technical decisions

## 2026-10-23 — Small static product with a scheduled sync

Retain Python 3.12, the standard library, GitHub Actions and GitHub Pages. A database or continuously running backend adds cost and operational work without helping a twice-hourly calendar refresh. Runtime has no third-party dependencies. Playwright is optional development tooling.

## 2026-10-23 — Verify the source, preserve real data

Use the public LoL Esports website's `getLeagues` and paginated `getSchedule` endpoints. Live requests authenticated with the existing public website key returned the Worlds league and 46 October/November 2026 matches during this session. This is an undocumented API, not a guaranteed service. A private API integration or alternate source has not been established. No fictional production events are allowed.

Fail synchronization when no usable current-season events arrive, even when a previous snapshot exists. Preserve omitted historic matches rather than interpreting missing rolling-page entries as cancellations. Explicit cancellation states update the existing event. A source identity change still needs manual review; matching games heuristically by teams/time could merge distinct matches.

## 2026-10-23 — Stable subscriptions and bounded writes

Retain source-derived UID, UTC times, per-event SEQUENCE and LAST-MODIFIED. Unchanged data preserves both sequence and modification time. Estimated durations depend on Bo1/Bo3/Bo5 and are disclosed. ICS uses CRLF and UTF-8 octet folding; tests must unfold logical lines before matching descriptions. Normalize CR/LF in source text to prevent property injection.

Render all output before replacing files and use temporary files plus atomic replacement per file. This prevents truncated individual outputs; it is not a multi-file transaction. The deployment job stops on any failure, so partial local output is never uploaded by a failed sync. A previously deployed Pages site remains served. Optional CLI paths isolate local development from the production state file.

## 2026-10-23 — Deployment and validation boundaries

Test pull requests and pushes independently of production credentials. Trigger deployment on relevant main-branch code changes, manual requests and the existing 30-minute schedule. Exclude snapshot-only commits from the push trigger to avoid recursion. Keep deployment serialized; never force-push after a state-commit conflict.

Calendar apps decide refresh frequency. Generated subscription URLs and ICS semantics are browser/unit tested; actual Google, Apple and Outlook account subscriptions remain a manual acceptance check. Do not claim these clients or public deployment have been verified without evidence.

## 2026-10-24 — Spoiler-free titles, scores in notes

Keep event titles and visible website rows free of scores. Put explicit series game wins only in ICS DESCRIPTION, so opening match details reveals the result. Use bilingual labels because one shared calendar feed serves both languages. Live scores show an observation timestamp and are explicitly snapshots from the scheduled sync, not real-time scoring. Refreshing that timestamp deliberately increments SEQUENCE; final results do not change on every poll. Never interpret absent result fields as zero.

## 2026-10-24 — Source attribution and event text revisions

Per owner request, retain LoL Esports attribution/link on the website and remove it from calendar notes and the ICS URL property. Add a persisted event format version to trigger exactly one SEQUENCE increment for an event text format change; keep UIDs unchanged. Future rendered event changes should bump this version so existing subscribers can receive them even when source match data is unchanged.
