#!/usr/bin/env python3
"""
rebuild-site.py
Scans all post HTML files for metadata and regenerates derived content:
  - Build hours tables in index.html (from build-hours meta tags)
  - By Category section in log.html (from build-category + build-date meta tags)
  - Categories sidebar in log.html and index.html

Usage:
    python3 rebuild-site.py

Run this from the website/ directory after adding or editing any post.
"""

import os
import re

WEBSITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML   = os.path.join(WEBSITE_DIR, "index.html")
LOG_HTML     = os.path.join(WEBSITE_DIR, "log.html")

# ── Post metadata collection ───────────────────────────────────────────────

def collect_posts():
    posts = []
    cat_re   = re.compile(r'<meta name="build-category" content="([^"]+)"', re.IGNORECASE)
    date_re  = re.compile(r'<meta name="build-date" content="([^"]+)"', re.IGNORECASE)
    h1_re    = re.compile(r'<div class="post-header">\s*<h1>([^<]+)</h1>', re.DOTALL)
    hours_re = re.compile(r'<meta name="build-hours" content="([0-9.]+)"', re.IGNORECASE)
    type_re  = re.compile(r'<meta name="post-type" content="([^"]+)"', re.IGNORECASE)

    for root, dirs, files in os.walk(os.path.join(WEBSITE_DIR, "posts")):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, WEBSITE_DIR).replace("\\", "/")
            content  = open(abs_path).read()
            cat_m, date_m, h1_m = cat_re.search(content), date_re.search(content), h1_re.search(content)
            if not (cat_m and date_m and h1_m):
                continue
            hours_m = hours_re.search(content)
            type_m  = type_re.search(content)
            posts.append({
                "title":     h1_m.group(1).strip(),
                "path":      rel_path,
                "date":      date_m.group(1),
                "category":  cat_m.group(1),
                "hours":     float(hours_m.group(1)) if hours_m else 0,
                "post_type": type_m.group(1).strip().lower() if type_m else "build",
            })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts

def _cat_slug(cat):
    return "cat-" + re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')

def _fmt_date(iso):
    from datetime import datetime
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %-d, %Y")

def _cats_ordered(posts):
    seen, cats = set(), {}
    for p in posts:
        c = p["category"]
        cats.setdefault(c, []).append(p)
    return cats

def build_category_section(posts):
    cats = _cats_ordered(posts)
    html = ""
    anchor_map = {}
    for cat, cat_posts in cats.items():
        slug = _cat_slug(cat)
        anchor_map[cat] = slug
        html += f'\n    <h3 id="{slug}" class="log-section">{cat} '
        html += f'<span style="font-weight:normal; color:var(--text-muted); font-size:0.85rem;">({len(cat_posts)})</span></h3>\n'
        html += '    <ul class="post-list">\n'
        for p in cat_posts:
            html += f'      <li>\n        <span class="post-date">{_fmt_date(p["date"])}</span>\n'
            html += f'        <a href="{p["path"]}">{p["title"]}</a>\n      </li>\n'
        html += '    </ul>\n'
    return html, anchor_map

def update_log(posts, anchor_map):
    content = open(LOG_HTML).read()
    # Sidebar categories
    items = "".join(
        f'        <li><a href="#{anchor_map.get(c, _cat_slug(c))}">{c}</a> ({len(ps)})</li>\n'
        for c, ps in _cats_ordered(posts).items()
    )
    content = re.sub(
        r'<h3>Categories</h3>\s*<ul>.*?</ul>',
        f'      <h3>Categories</h3>\n      <ul>\n{items}      </ul>',
        content, flags=re.DOTALL
    )
    # By Category section body
    cat_html, _ = build_category_section(posts)
    content = re.sub(
        r'(<!-- ── BY CATEGORY[^\n]*\n).*?(?=\n  </main>)',
        r'\1' + cat_html,
        content, flags=re.DOTALL
    )
    open(LOG_HTML, "w").write(content)
    print("log.html categories updated.")

def update_recent_posts(posts):
    """For each post, inject a sidebar showing the 2 before + 2 after it chronologically."""
    for i, post in enumerate(posts):
        # window: up to 2 newer, self, up to 2 older (posts is newest-first)
        start = max(0, i - 2)
        end   = min(len(posts), i + 3)
        window = posts[start:end]

        abs_path = os.path.join(WEBSITE_DIR, post["path"])
        post_dir = os.path.dirname(abs_path)

        items = ""
        for p in window:
            rel = os.path.relpath(os.path.join(WEBSITE_DIR, p["path"]), post_dir).replace("\\", "/")
            marker = " &laquo;" if p["path"] == post["path"] else ""
            items += f'        <li><a href="{rel}">{p["title"]}</a>{marker}</li>\n'

        block = (f'<div class="sidebar-section" id="recent-posts">\n'
                 f'      <h3>Around This Time</h3>\n'
                 f'      <ul>\n{items}      </ul>\n    </div>')

        c = open(abs_path).read()
        new = re.sub(r'<div class="sidebar-section" id="recent-posts">.*?</div>',
                     block, c, flags=re.DOTALL)
        if new != c:
            open(abs_path, "w").write(new)

    print(f"Recent posts updated for {len(posts)} posts.")


def update_post_nav(posts):
    """Inject prev/next nav with dates into every post. posts is newest-first."""
    def fmt_short(iso):
        from datetime import datetime
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%b %-d, %Y")

    for i, post in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i < len(posts) - 1 else None

        abs_path = os.path.join(WEBSITE_DIR, post["path"])
        post_dir = os.path.dirname(abs_path)

        def rel(t):
            return os.path.relpath(os.path.join(WEBSITE_DIR, t["path"]), post_dir).replace("\\", "/")

        left = (f'<a href="{rel(older)}">&larr; {fmt_short(older["date"])}<br>'
                f'<span style="font-size:0.9em;">{older["title"]}</span></a>') if older else ''
        right = (f'<a href="{rel(newer)}" style="text-align:right; display:block;">'
                 f'{fmt_short(newer["date"])} &rarr;<br>'
                 f'<span style="font-size:0.9em;">{newer["title"]}</span></a>') if newer else ''

        nav = f'<div class="post-nav" id="post-nav">\n      {left}\n      {right}\n    </div>'
        c = open(abs_path).read()
        new = re.sub(r'<div class="post-nav" id="post-nav">.*?</div>', nav, c, flags=re.DOTALL)
        if new != c:
            open(abs_path, "w").write(new)

    print(f"Post nav updated for {len(posts)} posts.")




def update_index_recent_posts(posts):
    """Rewrite the top-5 recent posts list on index.html."""
    top5 = posts[:5]
    items = ""
    for i, p in enumerate(top5):
        badge = '<img src="img/common/new.gif" alt="NEW!" style="vertical-align:middle; height:1.2em; margin-right:4px;"> ' if i == 0 else ""
        items += "      <li>\n"
        items += f'        <span class="post-date">{_fmt_date(p["date"])}</span>\n'
        items += f'        <a href="{p["path"]}">{badge}{p["title"]}</a>\n'
        items += f'        <span class="post-cat">{p["category"]}</span>\n'
        items += "      </li>\n"
    new_block = '<h2>Recent Build Log Entries</h2>\n    <ul class="post-list">\n' + items + "    </ul>"
    c = open(INDEX_HTML).read()
    import re as _re
    new = _re.sub(r'<h2>Recent Build Log Entries</h2>\s*<ul class="post-list">.*?</ul>',
                 new_block, c, flags=_re.DOTALL)
    if new != c:
        open(INDEX_HTML, "w").write(new)
        print("index.html recent posts updated.")
    else:
        print("index.html recent posts: no changes needed.")

def update_index_categories(posts, anchor_map):
    content = open(INDEX_HTML).read()
    items = "".join(
        f'        <li><a href="log.html#{anchor_map.get(c, _cat_slug(c))}">{c}</a> ({len(ps)})</li>\n'
        for c, ps in _cats_ordered(posts).items()
    )
    new_content = re.sub(
        r'<h3>Categories</h3>\s*<ul>.*?</ul>',
        f'      <h3>Categories</h3>\n      <ul>\n{items}      </ul>',
        content, flags=re.DOTALL
    )
    if new_content != content:
        open(INDEX_HTML, "w").write(new_content)
        print("index.html categories updated.")
    else:
        print("index.html categories: no changes needed.")

# Human-readable labels for each category key
CATEGORY_LABELS = {
    "workshop":           "Workshop",
    "research-education": "Research & Education",
    "empennage":          "Empennage",
    "wings":              "Wings",
    "fuselage":           "Fuselage",
    "firewall-forward":   "Firewall Forward",
    "finishing":          "Finishing",
    "social-flying":      "Flying & Social",
}

# Preferred display order (unknown categories appended at end)
CATEGORY_ORDER = [
    "workshop",
    "research-education",
    "empennage",
    "wings",
    "fuselage",
    "firewall-forward",
    "finishing",
]

def collect_hours():
    totals = {}
    meta_re = re.compile(
        r'<meta\s+name="build-hours"\s+content="([0-9.]+)"\s+data-category="([^"]+)"',
        re.IGNORECASE
    )
    for root, dirs, files in os.walk(os.path.join(WEBSITE_DIR, "posts")):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            content = open(path).read()
            for m in meta_re.finditer(content):
                hours = float(m.group(1))
                cat   = m.group(2).strip().lower()
                totals[cat] = totals.get(cat, 0) + hours
    return totals

# Categories excluded from the build total (shown separately below)
# No longer needed as a hardcoded set — driven by data-bucket="other" in posts

def collect_hours():
    totals  = {}   # cat -> hours
    buckets = {}   # cat -> "build" | "other"
    meta_re = re.compile(
        r'<meta\s+name="build-hours"\s+content="([0-9.]+)"\s+data-category="([^"]+)"(?:\s+data-bucket="([^"]+)")?',
        re.IGNORECASE
    )
    for root, dirs, files in os.walk(os.path.join(WEBSITE_DIR, "posts")):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            content = open(path).read()
            for m in meta_re.finditer(content):
                hours  = float(m.group(1))
                cat    = m.group(2).strip().lower()
                bucket = (m.group(3) or "build").strip().lower()
                totals[cat]  = totals.get(cat, 0) + hours
                buckets[cat] = bucket
    return totals, buckets

def build_table_html(totals, buckets):
    build_cats  = [c for c in CATEGORY_ORDER if c in totals and buckets.get(c) != "other"]
    build_cats += sorted(c for c in totals if c not in CATEGORY_ORDER and buckets.get(c) != "other")
    extra_cats  = [c for c in totals if buckets.get(c) == "other"]

    # Build hours table
    build_rows = ""
    grand_total = 0
    for cat in build_cats:
        hrs = totals[cat]
        grand_total += hrs
        label = CATEGORY_LABELS.get(cat, cat.replace("-", " ").title())
        hrs_str = str(int(hrs)) if hrs == int(hrs) else str(hrs)
        build_rows += f"        <tr><td>{label}</td><td>{hrs_str}</td></tr>\n"
    total_str = str(int(grand_total)) if grand_total == int(grand_total) else str(grand_total)
    build_rows += f"        <tr><td><strong>Total</strong></td><td><strong>{total_str}</strong></td></tr>"
    build_section = f"      <table class=\"hours-table\">\n{build_rows}\n      </table>"

    # Beyond the Build section
    other_section = ""
    if extra_cats:
        other_rows = ""
        for cat in extra_cats:
            hrs = totals[cat]
            label = CATEGORY_LABELS.get(cat, cat.replace("-", " ").title())
            hrs_str = str(int(hrs)) if hrs == int(hrs) else str(hrs)
            other_rows += f"        <tr><td>{label}</td><td>{hrs_str}</td></tr>\n"
        other_section = (
            f"\n    </div>\n\n    <div class=\"sidebar-section\">\n"
            f"      <h3>Beyond the Build</h3>\n"
            f"      <table class=\"hours-table\">\n{other_rows}      </table>"
        )

    return build_section + other_section

def update_index(table_html):
    content = open(INDEX_HTML).read()
    # Remove any existing NEW badges first
    content = re.sub(r'\s*<span class="badge-new">NEW!</span>', '', content)
    # Replace Build Hours section + any immediately following Beyond the Build section
    new_content = re.sub(
        r'(<h3>Build Hours</h3>\s*)<table class="hours-table">.*?</table>'
        r'\s*</div>'
        r'(\s*<div class="sidebar-section">\s*<h3>Beyond the Build</h3>.*?</table>\s*</div>)?',
        lambda m: f'<h3>Build Hours</h3>\n      {table_html}\n    </div>',
        content,
        flags=re.DOTALL
    )
    if new_content == content:
        print("No changes needed.")
        return
    open(INDEX_HTML, "w").write(new_content)
    print("index.html hours table updated.")

def update_flying_log(posts):
    """Regenerate the year-grouped post list in flying.html from posts with post_type=flying."""
    flying = [p for p in posts if p.get("post_type") == "flying"]
    if not flying:
        return

    # Group by year
    years = {}
    for p in flying:
        y = p["date"][:4]
        years.setdefault(y, []).append(p)

    html = ""
    for year in sorted(years.keys(), reverse=True):
        html += f'\n    <h2 id="{year}">{year}</h2>\n    <ul class="post-list">\n'
        for p in years[year]:
            html += f'      <li>\n'
            html += f'        <span class="post-date">{_fmt_date(p["date"])}</span>\n'
            html += f'        <a href="{p["path"]}">{p["title"]}</a>\n'
            html += f'        <span class="post-cat">{p["category"]}</span>\n'
            html += f'      </li>\n'
        html += '    </ul>\n'

    flying_html = os.path.join(WEBSITE_DIR, "flying.html")
    content = open(flying_html).read()
    new_content = re.sub(
        r'(<p[^>]*>Flying logs.*?</p>\s*).*?(?=\s*</main>)',
        r'\1' + html,
        content, flags=re.DOTALL
    )
    if new_content != content:
        open(flying_html, "w").write(new_content)
        print(f"flying.html updated ({len(flying)} flying posts).")
    else:
        print("flying.html: no changes needed.")


if __name__ == "__main__":
    totals, buckets = collect_hours()
    if not totals:
        print("No build-hours meta tags found in any post.")
    else:
        print("Hours found:")
        for cat, hrs in totals.items():
            label  = CATEGORY_LABELS.get(cat, cat)
            bucket = buckets.get(cat, "build")
            print(f"  [{bucket}] {label}: {hrs}")
        table_html = build_table_html(totals, buckets)
        update_index(table_html)

    posts = collect_posts()
    build_posts  = [p for p in posts if p.get("post_type") != "flying"]
    print(f"\nPosts found: {len(posts)} ({len(build_posts)} build, {len(posts)-len(build_posts)} flying)")
    _, anchor_map = build_category_section(build_posts)
    update_log(build_posts, anchor_map)
    update_index_recent_posts(posts)  # all posts including flying
    update_index_categories(build_posts, anchor_map)
    update_recent_posts(build_posts)
    update_post_nav(build_posts)
    update_flying_log(posts)

    # Add NEW! badge (GIF) to the most recent post in index.html and log.html
    if build_posts:
        posts = build_posts
        newest_path = posts[0]["path"]
        badges = {
            INDEX_HTML: '<img src="img/common/new.gif" alt="NEW!" style="vertical-align:middle; height:1.2em; margin-right:4px;"> ',
            LOG_HTML:   '<img src="img/common/new.gif" alt="NEW!" style="vertical-align:middle; height:1.2em; margin-right:4px;"> ',
        }
        for html_path, badge in badges.items():
            c = open(html_path).read()
            # Remove any existing badges
            c = re.sub(r'<span class="badge-new">NEW!</span>\s*', '', c)
            c = re.sub(r'<img src="[^"]*new\.gif"[^>]*>\s*', '', c)
            # Add badge to first link to newest post
            c = c.replace(f'href="{newest_path}">', f'href="{newest_path}">{badge}', 1)
            open(html_path, "w").write(c)
        print(f"NEW! badge added to: {posts[0]['title']}")
