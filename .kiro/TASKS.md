# Tasks & Backlog

## In Progress

- [ ] Set up hosting (GitHub Pages recommended — free, simple, free SSL)

## Up Next

- [ ] Add a favicon (small airplane icon or "UKF" initials)
- [ ] Create a `404.html` page
- [ ] Add Open Graph meta tags (`og:title`, `og:description`, `og:image`) to each page for social sharing previews
- [ ] Add `<meta name="description">` to each page for SEO
- [ ] Add a `sitemap.xml`

## Deployment Workflow (to design)

- [ ] Decide on host: GitHub Pages vs Netlify vs S3
- [ ] Set up `rsync --checksum` or CI deploy so only changed files upload
- [ ] Document the full publish workflow: write post → run rebuild-site.py → deploy

## Content Backlog

- [ ] Write and add new RV-8 build posts as work progresses
- [ ] Add a "Lessons Learned" page (inspired by papalimabravo.com)
- [ ] Add a "Tools & Equipment" page
- [ ] Add a "Links" page (other builder sites, EAA resources)
- [ ] Embed YouTube videos in relevant posts once published
- [ ] Add profile photo alt text and caption on about.html

## Design / UX Backlog

- [ ] Review and possibly tweak color scheme (currently: white bg, dark green nav, red accent)
- [ ] Add print stylesheet so posts print cleanly
- [ ] Consider a small airplane ASCII art or SVG in the header for extra vintage feel
- [ ] Review mobile layout on real devices (iPhone, Android, iPad)

## Technical Backlog

- [ ] `rebuild-site.py`: only rewrite files that actually changed (optimization — low priority)
- [ ] `rebuild-site.py`: also regenerate the "Recent Posts" list on `index.html` (top 5 newest)
- [ ] `rebuild-site.py`: add a `--dry-run` flag to preview changes without writing
- [ ] Validate all HTML with W3C validator
- [ ] Add `alt` text audit — ensure all `<img>` tags have meaningful alt text

## Completed

- [x] Design and implement vintage aesthetic (CSS) — white/green/red palette
- [x] Build home page (index.html)
- [x] Build log page (log.html) — by year + by category views
- [x] Build about page (about.html)
- [x] Import all 13 WordPress posts as static HTML with original timestamps
- [x] Responsive layout (mobile/tablet/desktop, sidebar stacks at ≤680px)
- [x] Download all media from WordPress into img/YEAR/post-slug/ folders
- [x] Replace all image placeholders with real photos
- [x] Build hours system: meta tags in posts → auto-updates index.html table
- [x] "Beyond the Build" section for non-build hours (social-flying category)
- [x] rebuild-site.py: auto-generates By Category section in log.html
- [x] rebuild-site.py: auto-generates Categories sidebar in index.html + log.html
- [x] rebuild-site.py: auto-generates "Around This Time" sidebar on every post
- [x] rebuild-site.py: auto-generates prev/next nav with dates on every post
- [x] Organized posts/ and img/ by year/post-slug hierarchy
- [x] Banner image (site logo) on all pages
- [x] Fixed all category labels (removed "Uncategorized")
- [x] Links sidebar only on homepage
- [x] Build Hours table only on homepage
