"""Quality gate for posts. Run after gen.py and build.py. Exits 1 on any error.

Usage: python3 posts_src/check.py [slug ...]   (no slugs = check every post)
"""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, ".."); DIST = os.path.join(SRC, "..", "dist")
only = set(sys.argv[1:])
errors, warns = [], []
posts = {}
for f in sorted(glob.glob(os.path.join(SRC, "posts", "*.json"))):
    p = json.load(open(f)); slug = p["path"].strip("/").split("/")[-1]
    if slug in posts: errors.append(f"duplicate slug {slug}")
    posts[slug] = p
# no slug may clash with a migrated guide
for path in json.load(open(os.path.join(SRC, "trades_content.json"))):
    s = path.strip("/").split("/")[-1]
    if path.startswith("/guides/") and s in posts: errors.append(f"{s} clashes with an existing guide")

def text(html): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
for slug, p in posts.items():
    if only and slug not in only: continue
    e = lambda m: errors.append(f"{slug}: {m}")
    blob = json.dumps(p, ensure_ascii=False)
    if re.search(r"[—–]", blob): e("contains an em or en dash")
    if not 30 <= len(p["title"]) <= 60: e(f"title is {len(p['title'])} chars (30 to 60)")
    if not 120 <= len(p["desc"]) <= 158: e(f"description is {len(p['desc'])} chars (120 to 158)")
    if not p.get("kicker"): e("missing kicker")
    b = {x["type"]: x for x in p["blocks"]}
    if "*" not in b["hero"]["h1"]: e("h1 needs an *italic part*")
    html = b["guide"]["html"]
    words = len(text(html).split())
    if p.get("date", "") > "2026-11-24" and words < 900: e(f"article is {words} words (900 minimum for daily posts)")
    h2 = re.findall(r'<h2 id="([^"]+)">', html)
    if len(h2) < 5: e(f"only {len(h2)} h2 sections (5 minimum)")
    if len(h2) != len(set(h2)): e("duplicate h2 ids")
    if "<h1" in html: e("no h1 inside the article")
    if len(b["faq"]["items"]) < 4: e("needs at least 4 FAQs")
    if len(b["list"]["items"]) < 6: e("checklist needs at least 6 items")
    # hyphenated words in prose (links and ids excluded)
    prose = text(re.sub(r'(href|id)="[^"]*"', "", html)) + " " + " ".join([p["title"], p["desc"], b["hero"]["lede"]] + [f["q"] + " " + f["a"] for f in b["faq"]["items"]])
    hy = sorted(set(re.findall(r"\b[A-Za-z]+-[A-Za-z]+\b", prose)))
    if hy: e(f"hyphenated words, rewrite without hyphens: {hy[:8]}")
    if re.search(r"\btradies?\b", prose, re.I) and not re.search(r"hipages|australia|new zealand|\bnz\b", slug + p["title"], re.I):
        warns.append(f"{slug}: uses 'tradie' outside an Australia or New Zealand post")
    for h in re.findall(r'href="(/[^"#?]*)"', html) + [i["href"] for i in b["links"]["items"]]:
        if not os.path.exists(os.path.join(DIST, h.strip("/"), "index.html")): e(f"broken link {h}")
    if not os.path.exists(os.path.join(DIST, "guides", slug, "index.html")): e("page was not built (run gen.py then build.py)")
for w in warns: print("WARN ", w)
for x in errors: print("ERROR", x)
print(f"checked {len(only) or len(posts)} posts: {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
