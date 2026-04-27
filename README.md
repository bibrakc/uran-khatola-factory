# Uran Khatola Factory — Website

Static website chronicling the build of a Van's RV-8 homebuilt aircraft.

**Live WordPress (source of truth for content):** https://urankhatolafactory.wordpress.com/  
**Owner:** Bibrak Qamar Chandio (bibrakc@gmail.com)

## Stack

Pure HTML + CSS. No framework, no build step, no JavaScript.  
Host anywhere: GitHub Pages, Netlify, S3 static hosting, etc.

## Structure

```
website/
  style.css              # single stylesheet
  index.html             # home page
  log.html               # build log (by year + by category)
  about.html             # about the builder and project
  rebuild-site.py        # regenerates derived content — run after every new post
  posts/
    2021/                # one .html file per post, grouped by year
    2022/
    2026/
  img/
    common/              # site-wide assets (banner, homepage photos, profile)
    2021/                # per-post images, grouped by year/post-slug/
    2022/
    2026/
```

## Running Locally

```bash
cd website
python3 -m http.server 8080
# open http://localhost:8080
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
6. Add `<img>` tags in the post body.
7. Run `python3 scripts/rebuild-site.py` from the `website/` directory.

That's it. The script handles:
- Build hours table on `index.html`
- By Category section and sidebar on `log.html`
- Categories sidebar on `index.html`
- "Around This Time" sidebar on every post
- Prev/next navigation on every post

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

## Media Workflow (importing from WordPress)

```bash
# 1. Find image URLs in a WordPress post
curl -s "https://urankhatolafactory.wordpress.com/YEAR/MM/DD/post-slug/" \
  | grep -oE 'https://urankhatolafactory\.wordpress\.com/wp-content/uploads/[^"? ]+\.(jpg|jpeg|png|gif|webp)' \
  | sort -u

# 2. Download into the post's image folder
cd website/img/YEAR/post-slug/
curl -sO "https://...full-url-no-query-params..."

# 3. Replace placeholder divs in the post HTML with real <img> tags
```

## Design System

| Token          | Value      | Usage                        |
|----------------|------------|------------------------------|
| `--bg`         | `#ffffff`  | Page background              |
| `--bg-alt`     | `#f0f5f1`  | Sidebar, intro boxes         |
| `--border`     | `#b0a898`  | Borders and dividers         |
| `--text`       | `#1a1a1a`  | Body text                    |
| `--text-muted` | `#5a5a5a`  | Dates, captions, meta        |
| `--accent`     | `#8b1a1a`  | Deep red — highlights        |
| `--link`       | `#1a4a2e`  | Link color                   |
| `--nav-bg`     | `#1a4a2e`  | Nav, footer, sidebar headers |
| `--max-width`  | `860px`    | Content max width            |

Fonts: **Courier New** (nav, meta, headers) + **Georgia** (body).  
Responsive: two-column grid, sidebar stacks below at ≤680px.

## Deployment

Hosted on **GitHub Pages**: https://bibrakc.github.io/uran-khatola-factory/  
Repo: https://github.com/bibrakc/uran-khatola-factory

To publish changes:
```bash
python3 scripts/rebuild-site.py
git add .
git commit -m "description"
git push
```
