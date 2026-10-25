# Google search visibility

Canonical page: https://lolworldscalendar.com/
Target phrase: worlds 2026 calendar

The page uses this phrase naturally in its title, visible product name and English introduction. The existing bilingual hero slogan remains unchanged. Its description explains the product rather than repeating keywords. Canonical and Open Graph URLs identify the HTTPS apex. WebSite structured data identifies the real product/creator without claiming rankings or ratings.

The build publishes /robots.txt allowing crawling and advertising /sitemap.xml. The sitemap lists only the canonical home page. It omits invented modification dates and does not submit the subscription ICS or image as separate search landing pages. PL/EN share one URL; separate hreflang URLs are not invented. Most explanatory content is present in initial HTML; match rows and the language switch use JavaScript.

## Owner setup in Google Search Console

1. Add a Domain property for lolworldscalendar.com. Copy the exact TXT verification value Google supplies.
2. In home.pl DNS add TXT for the apex (Host empty in this panel), paste the verification value, keep the default TTL and preserve all A/CNAME records. Return to Search Console and click Verify after DNS propagation. Keep the TXT record after verification.
3. Open Sitemaps and submit https://lolworldscalendar.com/sitemap.xml.
4. Inspect https://lolworldscalendar.com/ using URL Inspection. Run Test live URL, then Request indexing when eligible. Record the actual reported result; successful live fetch is not proof of indexing.
5. Monitor Page indexing and Performance. Indexing and position for the target query are decisions by Google, not guaranteed by metadata or submission. Use a natural Worlds 2026 Calendar link from the owner's portfolio and relevant project mentions to help discovery.

URL-prefix verification by HTML tag is an alternative if preferred; it is not required in addition to verified Domain ownership. Do not add authentication credentials to the repository.

At implementation, public Google index status was not independently established. Search Console verification/submission must be confirmed separately; no ranking, impressions or successful indexing are claimed.

## Confirmed owner-submitted evidence, 2026-10-25

Screenshots show the lolworldscalendar.com Domain property, sitemap Success with one discovered page, URL available to Google and Page can be indexed in the live test, and Indexing requested for the HTTPS homepage. These establish successful submission and crawl eligibility, not actual index inclusion or query position. Next check: indexed URL Inspection result and Performance report. Repeated indexing requests do not increase queue priority.
