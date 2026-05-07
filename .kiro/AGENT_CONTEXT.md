# Agent Context — Uran Khatola Factory Website

This file gives an AI agent everything it needs to work on this project without prior conversation history.

## Project Summary

A static personal website for Bibrak Qamar Chandio, who is building a **Van's RV-8 homebuilt aircraft** in his garage in Cupertino, California. The site chronicles the build and flying adventures.

- **Live site:** https://bibrakc.github.io/uran-khatola-factory/
- **Repo:** https://github.com/bibrakc/uran-khatola-factory
- **Owner/author:** Bibrak Qamar Chandio (`bibrakc@gmail.com`)
- **Social:** YouTube, Facebook, Instagram (all `urankhatolafactory`)

## Deployment

Hosted on **GitHub Pages** from the `main` branch, root folder.
```bash
python3 scripts/rebuild-site.py   # regenerate derived content
git add .
git commit -m "description"
git push
```

## Tech Stack

Pure HTML5 + CSS3. No JavaScript, no framework, no build tool.  
Single stylesheet: `style.css` at repo root.  
`scripts/rebuild-site.py` — run after every new build log post.

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

**Fonts:** Courier New (nav, meta, headers) + Georgia (body).  
**Responsive:** Two-column grid, sidebar stacks at ≤680px. Images tap-to-zoom (wrapped in `<a class="img-link">`).  
**No em dashes** in prose. Rephrase sentences instead.

## File Map

```
/                          # repo root = site root
  style.css
  index.html               # home
  log.html                 # build log (by year + by category)
  flying.html              # flying log index
  about.html
  aircraft.html
  404.html
  scripts/
    rebuild-site.py
  posts/
    2021/                  # build log posts
    2022/
    2026/                  # build log posts + flying posts for 2026
      flights-pre-2026.html   # flying post
  img/
    common/                # banner, homepage photos, profile
    2021/post-slug/
    2022/post-slug/
    2026/post-slug/
  workshop/                # AI builder assist notes (open source, drawings excluded)
    AGENT.md
    empennage/
```

## Navigation Structure

All pages have this nav (in order):
```
Home | Build Log | Aircraft | About | Flying | YouTube | Facebook
```

- **Flying** links to `flying.html` (top-level pages) or `../../flying.html` (posts)
- Mark the active page with `class="active"` on the relevant `<a>` tag

## Two Types of Posts

### 1. Build Log Posts (go in `posts/YEAR/`)
Tracked by `rebuild-site.py`. Require meta tags. Appear in `log.html` and `index.html`.

Required meta tags:
```html
<meta name="build-date"     content="YYYY-MM-DD">
<meta name="build-category" content="Category Name">
<meta name="build-hours"    content="X.X" data-category="category-key">
<!-- add data-bucket="other" to exclude from build total -->
```

After adding: run `python3 scripts/rebuild-site.py` and add entry to `log.html` By Year section manually.

### 2. Flying Posts (go in `posts/YEAR/`, listed in `flying.html`)
NOT tracked by `rebuild-site.py`. Add entry to `flying.html` manually under the correct year heading.

Use `data-bucket="other"` on hours meta if logging flying time.

## Image Conventions

- Images live in `img/YEAR/post-slug/` matching the post filename
- All content images wrapped in `<a class="img-link">` for tap-to-zoom:
```html
<a href="../../img/YEAR/post-slug/photo.jpg" target="_blank" class="img-link">
  <img src="../../img/YEAR/post-slug/photo.jpg" alt="description">
</a>
<p class="img-caption">Caption text.</p>
```
- Site-wide assets (banner, profile, gifs) in `img/common/`

## Path Depths

- Top-level pages: `style.css`, `img/common/...`, `flying.html`, `log.html`
- Posts in `posts/YEAR/`: `../../style.css`, `../../img/...`, `../../flying.html`, `../../log.html`

## Markers Managed by rebuild-site.py (do not edit manually in build log posts)

```html
<div class="post-nav" id="post-nav"></div>
<div class="sidebar-section" id="recent-posts"></div>
```

## rebuild-site.py — What It Does

Scans build log posts only (not flying posts). Regenerates:
1. Build Hours + Beyond the Build tables in `index.html`
2. Recent posts list in `index.html`
3. By Category section + sidebar in `log.html`
4. Categories sidebar in `index.html`
5. "Around This Time" sidebar on every build log post
6. Prev/Next nav on every build log post
7. NEW! badge on most recent post

## All Posts (newest first)

| File | Date | Category | Type |
|---|---|---|---|
| posts/2026/flights-pre-2026.html | 2026-05-06 | Flying & Social | Flying |
| posts/2026/building-with-an-ai-co-builder.html | 2026-05-04 | Research & Education | Build Log |
| posts/2026/experimented-with-stewart-systems-primer.html | 2026-05-02 | Research & Education | Build Log |
| posts/2026/attended-fiberglass-workshop.html | 2026-03-25 | Research & Education | Build Log |
| posts/2026/back-to-building.html | 2026-02-19 | Planning | Build Log |
| posts/2022/horizontal-stabilizer-update-2.html | 2022-03-19 | Empennage | Build Log |
| posts/2021/horizontal-stabilizer-update-1.html | 2021-12-01 | Empennage | Build Log |
| posts/2021/empennage-inventoried.html | 2021-10-27 | Empennage | Build Log |
| posts/2021/finished-the-practice-flap-kit.html | 2021-10-20 | Research & Education | Build Log |
| posts/2021/became-a-pilot-today.html | 2021-09-25 | Flying & Social | Build Log |
| posts/2021/a-beauty-came-to-kbmg.html | 2021-08-30 | Flying & Social | Build Log |
| posts/2021/marks-rv7.html | 2021-08-30 | Flying & Social | Build Log |
| posts/2021/getting-to-know-tools.html | 2021-07-11 | Planning | Build Log |
| posts/2021/update-on-empennage-crating-date.html | 2021-05-12 | Planning | Build Log |
| posts/2021/homebuilthelp-rv7-rudder-workshop-dvd.html | 2021-05-11 | Planning | Build Log |
| posts/2021/ordered-the-empennage-kit.html | 2021-04-26 | Planning | Build Log |

## Current Build Hours

| Category | Hours |
|---|---|
| Workshop | 4 |
| Research & Education | 38 |
| **Total** | **42** |
| Flying & Social (beyond build) | 5.17 |

## External Links

- Van's RV-8: https://www.vansaircraft.com/rv-8/
- EAA Chapter 20: https://www.eaa20.org/
- YouTube: https://www.youtube.com/channel/UCkw7kZ2sxUoKswTp_emBPEg
- Facebook: https://www.facebook.com/urankhatolafactory
- Instagram: https://www.instagram.com/urankhatolafactory/
