# Agent Context — Uran Khatola Factory Website

This file gives an AI agent everything it needs to work on this project without prior conversation history.

## Project Summary

A static personal website for Bibrak Qamar Chandio, who is building a **Van's RV-8 homebuilt aircraft** in his garage in Cupertino, California. The site chronicles the build with blog-style posts, a build hours tracker, and links to social media.

- **WordPress source:** https://urankhatolafactory.wordpress.com/
- **Owner/author:** Bibrak Qamar Chandio (`bibrakc@gmail.com`)
- **Social:** YouTube, Facebook, Instagram (all `urankhatolafactory`)

## Tech Stack

- Pure HTML5 + CSS3. No JavaScript, no framework, no build tool.
- Single stylesheet: `website/style.css`
- All pages are self-contained `.html` files.
- `website/rebuild-site.py` — run after every new post to regenerate derived content.

## Design System

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#ffffff` | Page background (white) |
| `--bg-alt` | `#f0f5f1` | Sidebar, intro boxes (light green tint) |
| `--border` | `#b0a898` | All borders and dividers |
| `--text` | `#1a1a1a` | Body text |
| `--text-muted` | `#5a5a5a` | Dates, captions, meta |
| `--accent` | `#8b1a1a` | Deep red — borders, hover, highlights |
| `--link` | `#1a4a2e` | Link color |
| `--nav-bg` | `#1a4a2e` | Nav, footer, sidebar headers (dark forest green) |
| `--max-width` | `860px` | Content max width |

**Fonts:** Courier New (nav, meta, headers) + Georgia serif (body).  
**Aesthetic:** Vintage 2000s homebuilder website. No animations, no gradients, flat layout.  
**Responsive:** Two-column grid (main + 220px sidebar). Sidebar stacks below main at ≤680px.  
**Header:** White background with banner image + site title in green. Red bottom border.

## File Map

```
website/
  style.css
  index.html          home — intro, 5 recent posts, hours sidebar, categories, links
  log.html            build log — by year + by category (both on same page)
  about.html          about Bibrak and the RV-8 project
  rebuild-site.py     regenerates: hours table, categories, Around This Time, prev/next nav
  img/
    common/           banner, homepage photos, profile photo
    2021/post-slug/   per-post images
    2022/post-slug/
    2026/post-slug/
  posts/
    2021/             10 posts
    2022/             1 post
    2026/             2 posts
```

### All Posts (newest first)

| File | Date | Category |
|---|---|---|
| posts/2026/attended-fiberglass-workshop.html | 2026-03-25 | Research & Education |
| posts/2026/back-to-building.html | 2026-02-19 | Planning |
| posts/2022/horizontal-stabilizer-update-2.html | 2022-03-19 | Empennage |
| posts/2021/horizontal-stabilizer-update-1.html | 2021-12-01 | Empennage |
| posts/2021/empennage-inventoried.html | 2021-10-27 | Empennage |
| posts/2021/finished-the-practice-flap-kit.html | 2021-10-20 | Research & Education |
| posts/2021/became-a-pilot-today.html | 2021-09-25 | Flying & Social |
| posts/2021/a-beauty-came-to-kbmg.html | 2021-08-30 | Flying & Social |
| posts/2021/marks-rv7.html | 2021-08-30 | Flying & Social |
| posts/2021/getting-to-know-tools.html | 2021-07-11 | Planning |
| posts/2021/update-on-empennage-crating-date.html | 2021-05-12 | Planning |
| posts/2021/homebuilthelp-rv7-rudder-workshop-dvd.html | 2021-05-11 | Planning |
| posts/2021/ordered-the-empennage-kit.html | 2021-04-26 | Planning |

## HTML Conventions

### Required meta tags in every post `<head>`
```html
<meta name="build-date"     content="YYYY-MM-DD">
<meta name="build-category" content="Category Name">
<meta name="build-hours"    content="X.X" data-category="category-key">
<!-- add data-bucket="other" to exclude from build total (e.g. social-flying) -->
```

### Post header block
```html
<div class="post-header">
  <h1>Post Title</h1>
  <div class="post-meta">
    <span>&#128197; Month D, YYYY</span>
    <span>&#128193; Category</span>
    <span>&#9201; X hrs logged</span>
  </div>
</div>
```

### Image (real photo)
```html
<img src="../../img/YEAR/post-slug/filename.jpg" alt="description">
<p class="img-caption">Caption text.</p>
```

### Markers managed by rebuild-site.py (do not edit manually)
```html
<div class="post-nav" id="post-nav"></div>
<div class="sidebar-section" id="recent-posts"></div>
```

### Nav — mark the active page
```html
<li><a href="../../log.html" class="active">Build Log</a></li>
```

### Path depths
- Top-level pages (`index.html`, `log.html`, `about.html`): `style.css`, `img/common/...`
- Posts (`posts/YEAR/post.html`): `../../style.css`, `../../img/...`

## How to Add a New Post

1. Copy `posts/2026/attended-fiberglass-workshop.html` as a template.
2. Save as `posts/YEAR/kebab-case-title.html`.
3. Update: `<title>`, `<h1>`, post-meta (date, category, hours), body content.
4. Set the four meta tags (build-date, build-category, build-hours, optionally data-bucket).
5. Download images into `img/YEAR/post-slug/` and add `<img>` tags.
6. Leave `post-nav` and `recent-posts` divs as empty markers.
7. Run `python3 scripts/rebuild-site.py` from `website/`.
8. Add the post to the By Year section of `log.html` manually (the script handles By Category).
9. Update the 5 recent posts list on `index.html` if it's in the top 5.

## rebuild-site.py — What It Does

Run: `python3 scripts/rebuild-site.py` from `website/`

Scans all posts for meta tags and regenerates:
1. **Build Hours table** in `index.html` — sums `build-hours` by `data-category`
2. **Beyond the Build table** in `index.html` — categories with `data-bucket="other"`
3. **By Category section** in `log.html` — grouped by `build-category`, sorted newest first
4. **Categories sidebar** in `log.html` and `index.html` — counts per category with anchor links
5. **"Around This Time" sidebar** on every post — 2 newer + self + 2 older posts
6. **Prev/Next nav** on every post — with date and title, Option D style

## Hours Categories

| `data-category` | Display label | Bucket |
|---|---|---|
| `workshop` | Workshop | build |
| `research-education` | Research & Education | build |
| `empennage` | Empennage | build |
| `wings` | Wings | build |
| `fuselage` | Fuselage | build |
| `firewall-forward` | Firewall Forward | build |
| `finishing` | Finishing | build |
| `social-flying` | Flying & Social | other |

New categories auto-appear. Labels auto-format from key if not in `CATEGORY_LABELS` dict.  
New `data-bucket="other"` categories auto-appear in "Beyond the Build" section.

## Current Build Hours (RV-8 only)

| Category | Hours |
|---|---|
| Workshop | 4 |
| Research & Education | 31 |
| **Total** | **35** |
| Flying & Social (beyond build) | 5.17 |

## External Links

- Van's RV-8: https://www.vansaircraft.com/rv-8/
- EAA: https://www.eaa.org/
- HomebuiltHelp: https://homebuilthelp.com
- YouTube: https://www.youtube.com/channel/UCkw7kZ2sxUoKswTp_emBPEg
- Facebook: https://www.facebook.com/urankhatolafactory
- Instagram: https://www.instagram.com/urankhatolafactory/
- LinkedIn: https://www.linkedin.com/in/bibrak-qamar-chandio-6444b51b/
