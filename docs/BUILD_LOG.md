# Build log

Entries record observations at the time of each step. Historical waiting states and failed checks are followed by their later resolution; see PROJECT_STATUS.md for current readiness.

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

- Score-note implementation committed as [d5e5272](https://github.com/marsellewoczko/worlds-2026-calendar/commit/d5e527249224f73647683758b014fcd7f82f6307). [CI 40093593704](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40093593704) and [publish run 40093593688](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40093593688) succeeded. This push regenerated and published the feed immediately, without waiting for the scheduled run.
- Compared public ICS fetched before and after publication: all 46 UIDs and titles unchanged; 14 final-result descriptions added with increased event SEQUENCE. Public example: KC 3–2 C9 in DESCRIPTION only. Verified UTF-8 folding remains within 75 octets. Public feed is refreshed; calendar-provider caches cannot be forced from this repository.

## 2026-10-24 — Source only on website, easier copy editing

- Removed Schedule source from ICS DESCRIPTION and removed the LoL Esports URL property. Website footer retains source attribution and the link.
- Added an event format version so this text change increments existing event SEQUENCE once with stable UIDs; otherwise unchanged completed events could keep their old notes in calendar clients. A migration test verifies the update happens only once.
- Reformatted PL/EN translation entries to one field per line without changing copy, and added docs/EDITING_TEXTS.md with the GitHub editing workflow, field map, metadata locations and deployment steps.
- All 27 unit tests passed; Node syntax check passed for the website script. A live local build retains scores, removes the source URL from ICS and retains the source link on the website. Remote deployment verification pending.

- [Publish run 40095901623](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40095901623) and CI succeeded. Public ICS returns 200 with no LoL Esports source URL, still includes final scores, preserves all 46 UIDs and increases SEQUENCE for every event. Public page retains the source link. Source cleanup is deployed.
- Discussed a possible future recap-link feature after creator permission, potentially without score notes to avoid spoilers. No recap integration, contact or score removal has been performed.

## 2026-10-24 — Colorful buttons and simplified subscription heading

- Removed the subscription eyebrow element (Your calendar, always up to date). Preserved owner's latest PL/EN copy.
- Subscription buttons now use gold, mint and lavender backgrounds with dark text; language buttons are also colored. Added visible keyboard focus outlines.
- Real Chromium smoke checks passed for mobile/desktop, PL/EN, two timezones, clipboard and disabled storage. Verified the eyebrow is absent and all three subscription button backgrounds differ. Deployment pending.

## 2026-10-24 — Score first, credit last in calendar notes

- Moved final/live score to the beginning of DESCRIPTION, followed by match details; moved author credit to the last line after a blank line, including events without scores.
- Bumped event format version to 3 so existing subscriptions receive the reordered note. Titles and UIDs remain unchanged.
- All 28 tests passed, including description ordering for final, live and unstarted matches. Publication pending together with colored buttons.

- Both updates published successfully in run [40118658048](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40118658048). Public HTML confirms colored button CSS and absent eyebrow; public ICS confirms 15 final/live score notes at the beginning and every author credit last after a blank line.

## 2026-10-24 — Author credit in the first screen

- Added Created by Marsel Lewoczko under the hero heading with a link to https://marsellewoczko.com. Existing footer credit remains.
- Chromium confirms correct credit/link fully within the initial viewport at 390×844 and 1280×900. Existing PL/EN, timezones, clipboard and blocked-storage smoke checks pass. Publication pending.

- Publication succeeded in run [40118790938](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40118790938); public HTML confirms the hero credit is present.

## 2026-10-24 — Explain calendar contents and score notes

- Added a PL/EN explanation before the schedule: title/teams/format, local times, estimated endings, scores in notes, Live observation timestamps and provider refresh delays.
- Added a clearly labeled illustrative event outside the actual schedule/feed. Its sample score is collapsed until the visitor opens the example notes. Warned that calendar apps may preview notes.
- Real Chromium smoke checks passed; PL/EN illustration labeling, initially collapsed sample score and mobile layout verified. Publication pending.

- Publish run 40119461125 succeeded; public HTML confirms the calendar-contents section is present.

## 2026-10-24 — Actual calendar screenshot

- Replaced the text-only illustrative event with the owner-supplied calendar screenshot in the explanation section. The image is behind a labeled spoiler disclosure, scales to mobile widths and has PL/EN alt text.
- Added image copying to the site build and asset changes to the deployment trigger. Kept the original supplied image unchanged.
- All 28 tests passed; a live build copied the image. Chromium smoke and screenshot checks passed in PL/EN at mobile/desktop widths, including loaded image dimensions, collapsed initial state and no overflow. Publication pending.

- Publication run 40120568995 succeeded. Public HTML references the screenshot, and the public JPEG returns HTTP 200 (130089 bytes).

## 2026-10-24 — Replacement screenshot

- Replaced the calendar screenshot with the newly supplied original (906×1280). Updated declared dimensions and image URL version so browsers fetch the replacement. Existing spoiler disclosure and captions are unchanged. Publication pending.

- Replacement screenshot verified in Chromium at 390px/1280px. Publication run 40120806327 succeeded; downloaded public image matches the new upload byte for byte.

## 2026-10-25 — Custom domain configuration

- Owner purchased/activated lolworldscalendar.com, set four apex A records for GitHub Pages and www CNAME to marsellewoczko.github.io. Screenshots show correct records and successful GitHub DNS validation.
- Automatic Pages configuration attempt was denied (integration HTTP 403); owner saved custom domain through GitHub UI.
- GitHub API confirms cname and approved certificate for apex/www; https_enforced=false at observation. Legacy page and ICS requests returned 301 to matching custom-domain paths over HTTP. Full new-domain requests hit this environment's proxy CONNECT 403, not an observed origin failure.
- Saved additive new-domain network requirements preserving existing rules. Updated README URLs. No application/UID changes, and no claim that existing calendar clients followed redirects. Owner action and remaining checks recorded in PROJECT_STATUS.md.

## 2026-10-25 — Custom domain migration verified

- Owner enabled HTTPS enforcement. GitHub API confirms https_enforced=true and an approved certificate for apex/www.
- Direct HTTPS HTML and ICS returned 200. www and both legacy GitHub Pages page/feed URLs returned 301 to matching HTTPS apex paths and successfully resolved to 200.
- Parsed public HTML and ICS: same 46 unique source identities, original UID namespace retained, generated subscription URL uses the new origin. No application changes were needed for the domain switch.
- Cloud network access is now available. Actual subscribed calendar-client refresh has not been independently observed; owner acceptance remains. README already points to the new canonical sharing/feed addresses.

## 2026-10-25 — Updated hero wording

- Changed default/EN hero to Every match / in your calendar. and PL to Wszystkie mecze / w Twoim kalendarzu. Kept explicit line break, second-line emphasis and author credit.
- Chromium checks passed for exact PL/EN text and no horizontal overflow at 390px and 1280px. Publication pending.

- Publish run 40183890349 succeeded; public HTML at https://lolworldscalendar.com/ contains both requested headline variants.

## 2026-10-25 — Remove dash punctuation from site copy

- Rephrased EN/PL subscription instructions without dashes, removed dash separators from page/social titles, replaced fan-made with fan, and replaced loading dashes with ellipses. Source match names and supplied screenshot remain unchanged.
- Chromium verified updated EN/PL hero, lead, instructions and disclaimer without dash characters and no overflow at mobile/desktop widths. Publication pending.

- Publish run 40184234185 succeeded; updated copy is verified in public HTML at https://lolworldscalendar.com/.

## 2026-10-25 — Search discovery for custom domain

- Public audit: homepage returned 200 with no noindex/X-Robots-Tag restriction; robots.txt and sitemap.xml returned 404. Google indexing was not independently established.
- Added canonical HTTPS apex, descriptive title/description targeting Worlds 2026 Calendar, Open Graph URL/site metadata and factual WebSite structured data. Kept the owner's hero wording unchanged; visible header and English introduction now identify the product naturally.
- Added root robots.txt and sitemap.xml to the build, with static-file deployment triggers and no invented sitemap modification date. Added an integration test for emitted crawl metadata and calendar output. All 29 tests passed.
- Live local build and Chromium smoke checks passed: PL/EN, mobile/desktop, local times, clipboard, storage fallback, valid structured data and SEO metadata. Publication pending.
- Owner is creating a Domain property in Search Console; TXT verification and submission remain manual external steps. Documented the workflow in SEARCH_VISIBILITY.md. No ranking/indexing claims.

- SEO publish run 40186069064 and CI succeeded. Verified public homepage title/canonical plus HTTP 200 for robots.txt and sitemap.xml. Owner obtained a Domain TXT verification value and was given home.pl entry instructions. Verification and indexing request remain unconfirmed; no credential or verification value was stored in repository documentation.

## 2026-10-25 — Search Console submission confirmed

- Owner supplied screenshots for the correct lolworldscalendar.com Domain property: sitemap Success, 1 discovered page, live homepage available to Google/page can be indexed, and Indexing requested.
- Recorded completed owner verification/submission steps in project status and search documentation. One discovered page is expected for the single-page sitemap; matches are not separate landing pages.
- Actual inclusion in Google Search, ranking for worlds 2026 calendar, impressions and traffic remain unconfirmed. Next step is monitoring indexed URL Inspection and Performance; no application changes or extra tests were necessary for this documentation-only update.

## 2026-10-25 — Google index inclusion confirmed

- Owner provided Search Console URL Inspection evidence for https://lolworldscalendar.com/: URL is on Google, Page is indexed, successful fetch by Googlebot smartphone, crawling/indexing allowed and HTTPS served.
- Google-selected canonical is the inspected HTTPS apex, matching the declared canonical. Sitemap association is shown.
- Updated status and search documentation. This establishes a publicly deployed product indexed by Google; no query ranking, traffic or user-adoption metrics are inferred. Next step: monitor Search Console Performance for the target query, impressions and clicks. Documentation-only change, no application tests needed.

## 2026-10-25 — FAQ, initial HTML schedule and public repository review

- Added seven PL/EN FAQ entries below the schedule and a subscription-section fragment link. Google subscription, Apple/Outlook, timezone, event updates, refresh cadence, spoilers and independent/free status are covered. No additional product routes were created; single-page requirement is saved in AGENTS.md.
- Initial HTML includes escaped match rows, UTC labels, event count and subscription URL. JavaScript replaces rows with local times. Added tests for correct UTC timestamps, title spoiler avoidance and source escaping; all 31 tests passed.
- Chromium smoke checks passed for mobile/desktop, PL/EN, timezone conversion, clipboard and blocked storage. Specific checks passed for FAQ anchor, keyboard disclosure and seven translated questions. With JavaScript disabled, 46 UTC events, correct count/timezone, usable FAQ and feed link were verified.
- Reviewed public repository contents and scanned 19 tracked files plus 145 reachable historical blobs for common private-key/token patterns. No matches or tracked environment/credential files found. No TODO/FIXME/debug leftovers found. Intentional technical comments, tests and the public LoL Esports website key remain. This was a targeted review, not a full security audit.
- Updated README and replaced accumulated status fragments with a concise current report. BUILD_LOG preserves earlier observations with a note distinguishing historical states from current readiness. No history rewrite or deletion of prior records was performed.

- CI and publish run [40199501228](https://github.com/marsellewoczko/worlds-2026-calendar/actions/runs/40199501228) succeeded. Public HTML returned 200 and contained all 46 initial UTC event rows, seven FAQ questions and correct initial timezone/count with no schedule placeholder. The single-page changes are deployed.

## 2026-10-27 — Link calendar notes back to the product

- Replaced the final Created by author line in ICS notes with Imported from https://lolworldscalendar.com/. A full HTTPS URL allows calendar clients to recognize the link without HTML-specific extensions. Website author branding is unchanged.
- Incremented event format version from 3 to 4 so existing events receive the changed text with stable UIDs and increased SEQUENCE.
- All 31 unit/integration tests passed. A live local API build produced 46 notes ending with the new source link. Verified one-time sequence migration on the saved 46 events. Deployment verification follows publication.

- Publish run 40476579855 succeeded. Public HTTPS ICS returned 200; all 46 notes now end with Imported from https://lolworldscalendar.com/. Compared with the previous saved snapshot, UIDs remain unchanged and all SEQUENCE values increased. No Created by text remains in the feed. Calendar-provider refresh timing is outside the server’s control.

## 2026-10-28 — Updated preview with current imported-from footer

- Replaced the preview with the owner's latest cropped TES vs HLE screenshot (940×1280), preserving the supplied original. Updated image dimensions and URL version for cache refresh.
- Updated PL/EN alt text and explanation to describe the source website link visible at the bottom, matching current event notes. The image stays behind the existing spoiler disclosure.
- Chromium checks passed in PL/EN at mobile/desktop widths: new image loads at its actual dimensions, disclosure works, schedule row count is preserved and no horizontal overflow occurs. Publication pending.
