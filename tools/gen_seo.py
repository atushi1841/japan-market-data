# -*- coding: utf-8 -*-
"""Programmatic SEO ジェネレータ。

使い方:
    cd /mnt/d/Project2/apify-sales-funnel/tools
    python3 gen_seo.py            # 生成のみ
    python3 gen_seo.py --check    # 生成 + HTML構文/リンク検証

生成物:
    ../<slug>.html        ランディングページ
    ../sitemap.xml
    ../robots.txt
index.html への内部リンク追加は別途行う（既存ページを壊さないため）。
"""
import html
import json
import os
import re
import sys
import datetime

BASE = "https://atushi1841.github.io/japan-market-data"
SITE_NAME = "Japan Market Data"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_pages_1 import PAGES as P1, PROFILE  # noqa: E402
from seo_pages_2 import PAGES as P2  # noqa: E402

# 2026-10-11 実在確認の結果、除外したページ:
#   yahoo-auctions-japan-data      -> actorが [DEPRECATED]（actor-deprecated を実ページで確認）
#   japan-used-car-price-data      -> goo-net actor が HTTP 404（ストア未公開）
#   japan-used-car-market-data     -> 同上
DROP = {"yahoo-auctions-japan-data", "japan-used-car-price-data", "japan-used-car-market-data"}

PAGES = [p for p in (P1 + P2) if p["slug"] not in DROP]
BY_SLUG = {p["slug"]: p for p in PAGES}

CSS = """  :root{--bg:#0f1115;--card:#1a1d24;--fg:#e8eaed;--acc:#ff6b35;--muted:#a0a7b1;--line:#2a2e37}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);line-height:1.6}
  .wrap{max-width:960px;margin:0 auto;padding:32px 20px}
  header{border-bottom:1px solid var(--line);padding-bottom:24px;margin-bottom:28px}
  h1{font-size:2rem;line-height:1.25;margin-bottom:12px}
  h1 em{color:var(--acc);font-style:normal}
  p.lead{color:var(--muted);font-size:1.05rem;max-width:760px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;margin:24px 0}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}
  .card h2{font-size:1.15rem;margin-bottom:8px}
  .card p{color:var(--muted);font-size:.95rem}
  .card .url{display:inline-block;margin-top:12px;color:var(--acc);text-decoration:none;font-weight:600;border:1px solid var(--acc);padding:8px 14px;border-radius:8px;font-size:.9rem}
  .card .url:hover{background:var(--acc);color:#0f1115}
  h3{padding-top:24px;font-size:1.25rem}
  .note{background:var(--card);border-left:4px solid var(--acc);padding:16px;border-radius:8px;margin:20px 0;color:var(--muted);font-size:.95rem}
  footer{border-top:1px solid var(--line);margin-top:40px;padding-top:20px;color:var(--muted);font-size:.85rem}
  a{color:var(--acc)}
  code{background:#262a33;padding:1px 6px;border-radius:4px;font-size:.9em}
  .crumbs{color:var(--muted);font-size:.85rem;margin-bottom:18px}
  .crumbs a{color:var(--muted)}
  .body p{margin:14px 0;color:#d5d9df}
  .cta{margin:22px 0}
  .cta .url{display:inline-block;margin:6px 10px 6px 0;color:var(--acc);text-decoration:none;font-weight:600;border:1px solid var(--acc);padding:9px 16px;border-radius:8px;font-size:.95rem}
  .cta .url:hover{background:var(--acc);color:#0f1115}
  table.fields{width:100%;border-collapse:collapse;margin:16px 0;font-size:.92rem}
  table.fields th,table.fields td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
  table.fields th{color:var(--muted);font-weight:600;width:34%}
  table.fields td code{white-space:nowrap}
  ul.tick{margin:14px 0 14px 20px;color:#d5d9df}
  ul.tick li{margin:7px 0}
  dl.faq{margin:14px 0}
  dl.faq dt{font-weight:600;margin-top:16px}
  dl.faq dd{color:var(--muted);margin:6px 0 0 0}
  pre{background:#0b0d11;border:1px solid var(--line);border-radius:8px;padding:14px;overflow-x:auto;margin:16px 0}
  pre code{background:none;padding:0;font-size:.85em;color:#c9d1d9}
  ul.related{margin:14px 0 14px 20px}
  ul.related li{margin:6px 0}"""

FOOTER = ("""    Independent utility publisher. All scrapers target retail storefronts and respect published terms; """
          """output is pricing/listing data only (no personal seller data). Prices in JPY unless converted.""")


def actor_id(url: str) -> str:
    """apify.com/user/actor → user~actor （ApifyのActor ID表記）"""
    m = re.match(r"https://apify\.com/([^/]+)/([^/?#]+)", url)
    return f"{m.group(1)}~{m.group(2)}" if m else ""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(p: dict) -> str:
    slug = p["slug"]
    canon = f"{BASE}/{slug}.html"
    actor_name, actor_url = p["actor"]
    aid = actor_id(actor_url)

    fields_rows = "\n".join(
        f"      <tr><th><code>{esc(k)}</code></th><td>{esc(v)}</td></tr>" for k, v in p["fields"])
    uses = "\n".join(f"      <li>{esc(u)}</li>" for u in p["use_cases"])
    faq_dl = "\n".join(
        f"      <dt>{esc(q)}</dt>\n      <dd>{esc(a)}</dd>" for q, a in p["faq"])
    rel = "\n".join(
        f'      <li><a href="{s}.html">{esc(BY_SLUG[s]["h1"])}</a></li>'
        for s in p["related"] if s in BY_SLUG)
    intro = "\n".join(f'    <p>{esc(t)}</p>' for t in p["intro"])

    if aid:
        run_note = (f'    <p class="note"><strong>Starting a run:</strong> call the Apify API with the actor id '
                    f'<code>{esc(aid)}</code>, or press <em>Start</em> on the actor page and download the dataset. '
                    f'Check the actor page for its exact input schema — a run is scoped by the search terms you '
                    f'supply, and billing is per result returned (roughly <code>$0.002 per item</code>).</p>')
        curl = (f'curl -X POST "https://api.apify.com/v2/acts/{aid}/runs?token=$APIFY_TOKEN" \\\n'
                f'  -H "Content-Type: application/json" \\\n'
                f'  -d \'{{"searchTerms": ["your", "search", "terms"]}}\'')
    else:
        run_note = ('    <p class="note"><strong>Starting a run:</strong> pick the actor for your marketplace from the '
                    'publisher page, then start it from the Apify console or the API. Billing is per result returned '
                    '(roughly <code>$0.002 per item</code>), so a scoped search stays cheap.</p>')
        curl = ('curl "https://api.apify.com/v2/datasets/$DATASET_ID/items?token=$APIFY_TOKEN&format=json"')

    ld_app = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": p["h1"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Cloud (Apify)",
        "description": p["desc"],
        "url": canon,
        "offers": {"@type": "Offer", "price": "0.002", "priceCurrency": "USD",
                   "description": "Pay per result; roughly $0.002 per item returned."},
        "publisher": {"@type": "Organization", "name": SITE_NAME},
    }
    ld_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{canon}">
<style>
{CSS}
</style>
<script type="application/ld+json">{json.dumps(ld_app, ensure_ascii=False, separators=(',', ':'))}</script>
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False, separators=(',', ':'))}</script>
</head>
<body>
<div class="wrap">
  <p class="crumbs"><a href="./">{SITE_NAME}</a> &rsaquo; {esc(p['h1'])}</p>
  <header>
    <h1>{esc(p['h1'])}</h1>
  </header>

  <div class="body">
{intro}
  </div>

  <div class="cta">
    <a class="url" href="{actor_url}">{esc(actor_name)} &rarr;</a>
    <a class="url" href="{PROFILE[1]}">All Japanese market scrapers &rarr;</a>
  </div>

  <h3>What you get</h3>
  <table class="fields">
    <tbody>
{fields_rows}
    </tbody>
  </table>
  <p class="note">Field names follow the actor's dataset schema and can differ slightly between actors — check the actor page for the exact input and output schema before wiring it into a pipeline.</p>

  <h3>Use cases</h3>
  <ul class="tick">
{uses}
  </ul>

  <h3>How a run works</h3>
{run_note}
  <pre><code>{esc(curl)}</code></pre>

  <h3>FAQ</h3>
  <dl class="faq">
{faq_dl}
  </dl>

  <h3>Related</h3>
  <ul class="related">
{rel}
      <li><a href="blog/mandarake-price-tracking.html">Mandarake price tracking</a></li>
      <li><a href="blog/dlsite-price-tracking.html">DLsite price tracking</a></li>
  </ul>

  <footer>
{FOOTER}
  </footer>
</div>
</body>
</html>
"""


def write_sitemap(today: str) -> None:
    urls = [f"{BASE}/"]
    urls += [f"{BASE}/{p['slug']}.html" for p in PAGES]
    for extra in ("blog/mandarake-price-tracking.html", "blog/dlsite-price-tracking.html",
                  "blog/goo-net-used-car-export-data.html"):
        if os.path.exists(os.path.join(ROOT, extra)):
            urls.append(f"{BASE}/{extra}")
    body = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == f"{BASE}/" else "0.7"
        body.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>")
    body.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(body) + "\n")
    return len(urls)


def write_robots() -> None:
    txt = "User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n"
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)


def check() -> list:
    """HTML構文チェック + 内部リンク切れチェック"""
    from html.parser import HTMLParser
    problems = []
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack = []

        def handle_starttag(self, tag, attrs):
            if tag not in VOID:
                self.stack.append(tag)

        def handle_endtag(self, tag):
            if tag in VOID:
                return
            if not self.stack or self.stack[-1] != tag:
                self.errors.append(f"unbalanced </{tag}>")
            else:
                self.stack.pop()

        errors = []

    targets = [f"{p['slug']}.html" for p in PAGES] + ["index.html"]
    for name in targets:
        path = os.path.join(ROOT, name)
        src = open(path, encoding="utf-8").read()
        par = P()
        par.errors = []
        par.feed(src)
        if par.errors:
            problems.append(f"{name}: {par.errors[:3]}")
        if par.stack:
            problems.append(f"{name}: unclosed {par.stack[:5]}")
        # 内部リンク切れ
        for href in re.findall(r'href="([^"#]+)"', src):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            tgt = os.path.normpath(os.path.join(ROOT, href))
            if not os.path.exists(tgt):
                problems.append(f"{name}: broken link -> {href}")
    return problems


def main() -> int:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    for p in PAGES:
        with open(os.path.join(ROOT, f"{p['slug']}.html"), "w", encoding="utf-8") as fh:
            fh.write(render(p))
    n = write_sitemap(today)
    write_robots()
    print(f"generated: {len(PAGES)} pages, sitemap urls={n}, robots.txt")
    if "--check" in sys.argv:
        problems = check()
        if problems:
            print("PROBLEMS:")
            for x in problems:
                print("  -", x)
            return 1
        print("check: OK (html balance + internal links)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
