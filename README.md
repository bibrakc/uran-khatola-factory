# Uran Khatola Factory

Static website chronicling the build of a Van's RV-8 homebuilt aircraft.

**Live site:** https://bibrakc.github.io/uran-khatola-factory/  
**Owner:** Bibrak Qamar Chandio (bibrakc@gmail.com)

## Stack

Pure HTML + CSS. No framework, no build step, no JavaScript.

## Structure

```
/                          # repo root = site root
  style.css                # single stylesheet
  index.html               # home page
  log.html                 # build log (by year + by category)
  flying.html              # flying log index
  about.html               # about the builder and project
  aircraft.html            # RV-8 aircraft page
  404.html                 # custom not found page
  scripts/
    rebuild-site.py        # regenerates derived content (run after every new post)
  posts/
    2021/                  # one .html file per post, grouped by year
    2022/
    2026/                  # build log posts + flying posts for 2026
  img/
    common/                # site-wide assets (banner, homepage photos, profile)
    2021/                  # per-post images, grouped by year/post-slug/
    2022/
    2026/                  # build log posts + flying posts for 2026
  workshop/                # build planning notes (open source, drawings excluded)
    AGENT.md               # AI builder assist instructions
    empennage/
      README.md
      horizontal-stabilizer.md
      vertical-stabilizer.md
      rudder.md
      elevators.md
      drawings/            # drawing PNGs, excluded from git (Van's copyright)
```

## Running Locally

```bash
python3 -m http.server 8080
# open http://localhost:8080
# on phone (same WiFi): http://YOUR_LOCAL_IP:8080
```

## Adding a New Post

1. Copy any existing post as a template (e.g. `posts/2026/attended-fiberglass-workshop.html`).
2. Save as `posts/YEAR/post-slug.html`.
3. Update: `<title>`, `<h1>` inside `.post-header`, and body content.
4. Set the required meta tags in `<head>`:
   ```html
   <meta name="build-date"     content="YYYY-MM-DD">
   <meta name="build-category" content="Category Name">
   <meta name="build-hours"    content="X.X" data-category="category-key">
   <!-- add data-bucket="other" if hours should NOT count toward build total -->
   ```
5. Download post images into `img/YEAR/post-slug/` (see Media section below).
6. Add `<img>` tags in the post body wrapped in `<a class="img-link">` for tap-to-zoom.
7. Add the post entry to the By Year section of `log.html` manually.
8. Run `python3 scripts/rebuild-site.py` from the repo root.

The script handles:
- Build hours table on `index.html`
- Recent posts list on `index.html`
- By Category section and sidebar on `log.html`
- Categories sidebar on `index.html`
- "Around This Time" sidebar on every post
- Prev/next navigation on every post
- NEW! badge on the most recent post

## Hours Categories

| `data-category` key  | Display label        | Bucket  |
|----------------------|----------------------|---------|
| `workshop`           | Workshop             | build   |
| `research-education` | Research & Education | build   |
| `empennage`          | Empennage            | build   |
| `wings`              | Wings                | build   |
| `fuselage`           | Fuselage             | build   |
| `firewall-forward`   | Firewall Forward     | build   |
| `finishing`          | Finishing            | build   |
| `social-flying`      | Flying & Social      | other   |

New categories auto-appear in the table. Add `data-bucket="other"` to exclude from build total.

## Clickable Images

All post images are wrapped in `<a class="img-link">` so tapping opens the full-size image in a new tab. Use this pattern:

```html
<a href="../../img/YEAR/post-slug/photo.jpg" target="_blank" class="img-link">
  <img src="../../img/YEAR/post-slug/photo.jpg" alt="description">
</a>
<p class="img-caption">Caption text.</p>
```

## Media Workflow (importing from WordPress)

```bash
# 1. Find image URLs in a WordPress post
curl -s "https://urankhatolafactory.wordpress.com/YEAR/MM/DD/post-slug/" \
  | grep -oE 'https://urankhatolafactory\.wordpress\.com/wp-content/uploads/[^"? ]+\.(jpg|jpeg|png|gif|webp)' \
  | sort -u

# 2. Download into the post's image folder
cd img/YEAR/post-slug/
curl -sO "https://...full-url-no-query-params..."
```

## Design System

| Token          | Value      | Usage                        |
|----------------|------------|------------------------------|
| `--bg`         | `#ffffff`  | Page background              |
| `--bg-alt`     | `#f0f5f1`  | Sidebar, intro boxes         |
| `--border`     | `#b0a898`  | Borders and dividers         |
| `--text`       | `#1a1a1a`  | Body text                    |
| `--text-muted` | `#5a5a5a`  | Dates, captions, meta        |
| `--accent`     | `#8B6914`  | Dark gold, highlights       |
| `--link`       | `#1a4a2e`  | Link color                   |
| `--nav-bg`     | `#1a4a2e`  | Nav, footer, sidebar headers |
| `--max-width`  | `860px`    | Content max width            |

Fonts: **Courier New** (nav, meta, headers) + **Georgia** (body).  
Responsive: two-column grid, sidebar stacks below at ≤680px. Images tap-to-zoom on mobile.

## Flying Section

Flying posts live in `posts/YEAR/` alongside build log posts, but are listed in `flying.html` (not `log.html`). They are **not** tracked by `rebuild-site.py`.

To add a new flying post:
1. Create `posts/YEAR/post-slug.html` using an existing flying post as template.
2. Add images to `img/YEAR/post-slug/`.
3. Add an entry to `flying.html` under the correct year heading manually.
4. No need to run `rebuild-site.py`.

## Workshop (AI Builder Assist)

The `workshop/` folder contains build planning notes generated with AI assistance. See the blog post: [Building with an AI Co-Builder](https://bibrakc.github.io/uran-khatola-factory/posts/2026/building-with-an-ai-co-builder.html).

The drawing PNG files (`workshop/empennage/drawings/`) are excluded from git as they are derived from Van's Aircraft copyrighted plans.

## Deployment

```bash
python3 scripts/rebuild-site.py
git add .
git commit -m "description"
git push
```
