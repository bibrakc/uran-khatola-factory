# Agent Context: Uran Khatola Factory Website

This file gives an AI agent what it needs to work on this project without prior conversation history. Read it first. `README.md` has the same technical detail in a human-oriented form.

## Project Summary

A static personal website for Bibrak Qamar Chandio, who is building a **Van's RV-8 homebuilt aircraft** in his garage in Cupertino, California. The site covers the build and his flying.

- **Live site:** https://bibrakc.github.io/uran-khatola-factory/
- **Repo:** https://github.com/bibrakc/uran-khatola-factory (branch `main`, GitHub Pages from the root folder)
- **Owner/author:** Bibrak Qamar Chandio (`bibrakc@gmail.com`)
- **Social:** YouTube, Facebook, Instagram (all `urankhatolafactory`)

## Working Rules (from the owner, follow these)

1. **Do not push until the owner says so.** Commit only when asked. He often asks to amend the last commit and force-push (use `--force-with-lease`) or to squash into one commit, to avoid noisy history.
2. **Commit messages describe the content added.** Do not mention style fixes such as em-dash removal.
3. **No em dashes in prose.** Rephrase the sentence. A `&mdash;` in the footer and a `|` in titles are fine.
4. **Plain, simple, minimal writing in the owner's voice.** No flowery or cringe language. Fix typos and commas, but do not add content he did not say. Ask for missing facts instead of inventing them.
5. **Every content image needs a caption.**
6. **Use "Mathieu"** (French spelling). Other names in use: Shujauddin Saqib Siddiqui (Oshkosh trip), Siddique (Houston ferry trip), Thomas (EAA 20 technical counselor), Carl, Mike (lead pilot, RV-6A), Paul (KSQL, Mooney M20C), Sergey (flight instructor).
7. **Never mention sleep or hours of sleep** anywhere on the site.
8. **Post date = the day the post is written**, formatted `YYYY-MM-DD` in the meta tag.
9. **Leave `wings.html` alone.** It has gone missing from the working tree once with no known cause. If `git status` shows it deleted, restore it with `git checkout -- wings.html`.
10. Do not use `pip --break-system-packages` or venvs. Use the system tools (`pdftotext`, `pdftoppm`, PIL).

## Tech Stack

Pure HTML5 + CSS3. No JavaScript, no framework, no build tool. One stylesheet: `style.css`. `scripts/rebuild-site.py` regenerates the derived parts of the site.

## Design System

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#ffffff` | Page background |
| `--bg-alt` | `#f0f5f1` | Sidebar, intro boxes |
| `--border` | `#b0a898` | Borders and dividers |
| `--text` | `#1a1a1a` | Body text |
| `--text-muted` | `#5a5a5a` | Dates, captions, meta |
| `--accent` | `#8B6914` | Dark gold |
| `--link` | `#1a4a2e` | Link color |
| `--nav-bg` | `#1a4a2e` | Nav, footer, sidebar headers |
| `--max-width` | `860px` | Content max width |

Fonts: Courier New (nav, meta, headers) and Georgia (body). Two-column grid, sidebar stacks at 680px and below.

## File Map

```
/                          repo root = site root
  index.html               home (hours tables, recent posts, links)
  log.html                 build log (By Year + By Category)
  flying.html              flying post index
  books.html               reading list (single page, 10 books)
  about.html  aircraft.html  404.html
  wings.html fuselage.html firewall-forward.html finishing.html avionics.html   placeholder pages
  style.css
  sitemap.xml  robots.txt  googled5b43998e0486be9.html   SEO, Search Console verification
  scripts/rebuild-site.py
  posts/YEAR/post-slug.html
  img/common/              site-wide assets (banner, new.gif, favicons, books/<book>/)
  img/YEAR/post-slug/      per-post images; folder name equals the post filename
  workshop/                AI builder assist notes (open source; empennage/drawings/ is gitignored, Van's copyright)
```

Navigation on every page, in this order: `Home | Build Log | Aircraft | About | Flying`. Mark the current page with `class="active"`. Books is linked from the "Links" sidebar on `index.html`.

Path depth: top-level pages use `style.css` and `img/...`. Posts in `posts/YEAR/` use `../../style.css` and `../../img/...`.

## Two Kinds of Posts

Both live in `posts/YEAR/`. The easiest templates are `posts/2026/osh-2026.html` (flying) and `posts/2026/horizontal-and-vertical-stablizers-done.html` (build).

**Build log post.** Listed in `log.html` and counted in the build hours table.

**Flying post.** Add `<meta name="post-type" content="flying">`. Listed in `flying.html`. It does not appear in `log.html`.

Required `<head>` meta tags (both kinds):
```html
<meta name="build-date"     content="YYYY-MM-DD">
<meta name="build-category" content="Category Name">    <!-- plain &, e.g. "Research & Education" -->
<meta name="build-hours"    content="X.X" data-category="category-key">
```
- Flying posts use `data-category="social-flying" data-bucket="other"` and the category "Flying & Social". Their hours show under "Beyond the Build", not the build total.
- A post can count hours in several categories with several `build-hours` tags, each with its own `data-category`. It then appears under each category.
- The visible meta block shows date, category and hours (`&#9201; X hrs logged`). Keep it in sync with the tags.
- Keep the empty `<div class="post-nav" id="post-nav"></div>` and `<div class="sidebar-section" id="recent-posts"></div>`. The script fills them.
- The tag block uses `<div class="tags">` (not `post-tags`). The tags are decorative links to `#`, no page reads them. Use only a few meaningful tags.

## Adding a Post (checklist)

1. Copy a template, save as `posts/YEAR/slug.html`. Update `<title>`, `<h1>`, meta tags, description, body.
2. Put images in `img/YEAR/slug/`. Resize like the existing ones: about 1536x2048 (or 2048x1536), roughly 500 KB to 1 MB each. Recompress anything larger (PIL, quality about 82) before adding it. The read tool fails on very large images.
3. Wrap each image and add a caption:
   ```html
   <a href="../../img/YEAR/slug/photo.jpg" target="_blank" class="img-link">
     <img src="../../img/YEAR/slug/photo.jpg" alt="description">
   </a>
   <p class="img-caption">Caption. Month Year.</p>
   ```
4. **Caption dates.** End the caption with the month and year, as in "Approaching San Carlos (KSQL) over the salt fields, October 2026." Leave captions that already carry a full date alone. Find dates in the photo EXIF (`DateTimeOriginal`). If a photo has no date, ask the owner. Do not guess.
5. Place photos next to the part of the story they illustrate. Avoid dumping them at the end.
6. Build log post only: add an entry to the By Year section of `log.html` by hand.
7. Flying post: `rebuild-site.py` tries to update `flying.html`, but its regex often does not match. Check that the post is listed under the right year, newest first, and add it by hand if not.
8. Add the new URL to `sitemap.xml`. It is maintained by hand and was missing several posts before.
9. Run `python3 scripts/rebuild-site.py` from the repo root.
10. Review `git status`, then wait for the owner before committing or pushing.

## What rebuild-site.py Does

Scans all posts. Regenerates:
1. Build Hours and "Beyond the Build" tables in `index.html`
2. "Recent Posts" list in `index.html` (the heading must stay "Recent Posts"; includes flying posts)
3. By Category section and sidebar in `log.html`, and the Categories sidebar in `index.html`
4. "Around This Time" sidebar and prev/next nav on build posts
5. NEW! badge (`img/common/new.gif`) on the newest post
6. `flying.html` list (see step 7 above)

It does not touch `sitemap.xml` or the By Year list in `log.html`.

## Photos and Privacy

Many photos carry GPS EXIF data, and it is published as-is. The owner decided not to strip it. Do not strip GPS unless he asks. Note that recompressing with PIL drops EXIF, which is a side effect to be aware of.

## Videos

YouTube Shorts and some videos show Error 153 on localhost. Use the full iframe embed code from YouTube including `?si=`. It works on the live site.

## Hours and Posts

Do not copy hour totals or post lists into docs, they go stale. The source of truth is the `build-*` meta tags in the posts, the tables in `index.html`, `log.html` and `flying.html`.

## External Links

- Van's RV-8: https://www.vansaircraft.com/rv-8/
- EAA Chapter 20: https://www.eaa20.org/
- YouTube: https://www.youtube.com/channel/UCkw7kZ2sxUoKswTp_emBPEg
- Facebook: https://www.facebook.com/urankhatolafactory
- Instagram: https://www.instagram.com/urankhatolafactory/
