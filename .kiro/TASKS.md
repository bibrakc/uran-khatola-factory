# Tasks & Backlog

## Up Next

- [ ] Make `rebuild-site.py` regenerate `sitemap.xml` from the post files (it is maintained by hand and has fallen behind before)
- [ ] Fix the `flying.html` regex in `rebuild-site.py` so new flying posts are added automatically
- [ ] Add a missing-caption pass: a few photos in `flights-pre-2026.html` have no caption (second sunset photo, two Mount Hood photos, second Fueling photo, second checkride photo)
- [ ] Confirm dates for photos left without a month and year in `flights-pre-2026.html`: Taylorcraft, "Autumn over Indiana", KBMG to KLWV solo cross-country, "Fueling the C172"
- [ ] Add a favicon animation or improve the favicon
- [ ] Add `<meta name="description">` to `flying.html`
- [ ] Fill in the placeholder pages (`wings.html`, `fuselage.html`, `firewall-forward.html`, `finishing.html`, `avionics.html`) as the build reaches them

## Content Backlog

- [ ] "Build Stats" sidebar on `index.html` (kit sections received, parts reordered, rivets driven, workshops attended, tools acquired). Manually maintained, Courier New, styled like the hours table
- [ ] More RV-8 build posts as work progresses
- [ ] More flying posts (Mooney search, cross-country trips)
- [ ] "Lessons Learned" page (inspired by papalimabravo.com)
- [ ] "Tools & Equipment" page
- [ ] "Links" page (other builder sites, EAA resources)
- [ ] Profile photo alt text and caption on `about.html`

## Design / UX Backlog

- [ ] Print stylesheet so posts print cleanly
- [ ] Review mobile layout on real devices (iPhone, Android, iPad)
- [ ] Tag pages (tags are decorative links to `#` today, nothing reads them). Only worth it with many posts per topic

## Technical Backlog

- [ ] `rebuild-site.py`: only rewrite files that changed
- [ ] `rebuild-site.py`: `--dry-run` flag
- [ ] Validate all HTML with the W3C validator
- [ ] Audit `alt` text on all `<img>` tags
- [ ] Optional: custom domain

## Completed (summary)

- Vintage static site: home, build log (By Year and By Category), about, aircraft, books, 404, favicon
- All WordPress posts imported with original dates and media, organized as `posts/YEAR/` and `img/YEAR/post-slug/`
- Hours system driven by post meta tags, including multi-category posts and the "Beyond the Build" bucket
- `rebuild-site.py`: hours tables, recent posts, categories, Around This Time, prev/next, NEW! badge
- Flying section (`flying.html`) with posts: Before 2026, Oshkosh AirVenture 2026, Complex Endorsement
- SEO: sitemap, robots.txt, Open Graph tags, canonical URLs, Google Search Console verification
- Workshop folder (AI builder assist) and the "Building with an AI Co-Builder" post
- Month and year added to flying post photo captions
- Hosted on GitHub Pages with SSH push
