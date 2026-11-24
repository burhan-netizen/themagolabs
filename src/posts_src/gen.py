"""Turns the post sources into src/posts/*.json (run before build.py).

Sources:
  posts_src/[a-z]_*.py   the first 11 guides (POSTS lists), published 2026-11-24
  posts_src/daily/*.py   one file per daily post, named YYYY-MM-DD-slug.py, defining POST = dict(...)
See BLOG.md in the repo root for the post format and the daily routine.
"""
import json, os, re, glob, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "posts")
sys.path.insert(0, HERE)
from extra import EXTRA

def load(f):
    spec = importlib.util.spec_from_file_location(re.sub(r"\W", "_", os.path.basename(f)[:-3]), f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

CORE_DATE = "2026-11-24"
posts = []
for f in sorted(glob.glob(os.path.join(HERE, "[a-z]_*.py"))):
    posts += load(f).POSTS
for p in posts:
    p["html"] += EXTRA.get(p["slug"], "")
order = ["is-hipages-worth-it", "is-checkatrade-worth-it", "are-local-services-ads-worth-it", "customer-ghosted-after-quote",
         "how-to-deal-with-time-wasters", "should-you-charge-for-quotes", "how-to-get-more-customers", "how-to-get-google-reviews", "slow-season", "how-to-get-paid-on-time"]
posts.sort(key=lambda p: order.index(p["slug"]))
kick = {"Leads and ads": order[:3], "Quotes": order[3:6], "Getting work": order[6:9], "Getting paid": order[9:]}
for k, ks in kick.items():
    for p in posts:
        if p["slug"] in ks: p.setdefault("kicker", k)
for p in posts: p.setdefault("date", CORE_DATE)

daily = []
for f in sorted(glob.glob(os.path.join(HERE, "daily", "*.py"))):
    p = load(f).POST
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.py$", os.path.basename(f))
    assert m, f"daily file must be named YYYY-MM-DD-slug.py: {f}"
    p.setdefault("date", m.group(1)); p.setdefault("slug", m.group(2))
    daily.append(p)

angi_src = [os.path.join(HERE, "angi.json")]
angi = json.load(open(angi_src[0])) if angi_src else None
content = json.load(open(os.path.join(HERE, "..", "trades_content.json")))
def plain(s): return s.replace("*", "")
allp = posts + daily
titles = {p["slug"]: plain(p["h1"]) for p in allp}
titles["is-angi-worth-it"] = "Is Angi worth it for contractors? The real cost per job."
def link(x):
    if x.startswith("/"):
        if x in content: return {"href": x, "title": content[x]["blocks"][0]["h1"], "text": ""}
        x = x.strip("/").split("/")[-1]
    return {"href": f"/guides/{x}/", "title": titles[x], "text": ""}

MONTHS = "January February March April May June July August September October November December".split()
def month(d): y, m, _ = d.split("-"); return f"{MONTHS[int(m) - 1]} {y}"
CTA = {"type": "cta", "eyebrow": "Your turn", "title": "Send us your Instagram. We will show you your website.", "text": "Within 48 hours you get a working preview of your new site, free and with no strings."}

def to_json(p):
    return {"path": f"/guides/{p['slug']}/", "group": "work", "kicker": p["kicker"], "date": p["date"], "card": p["card"], "title": p["title"], "desc": p["desc"], "blocks": [
        {"type": "hero", "h1": p["h1"], "eyebrow": f"Guide / {month(p['date'])}", "lede": p["lede"], "ticks": p["ticks"]},
        {"type": "guide", "html": p["html"]},
        {"type": "list", "eyebrow": "Do this now", "title": "Your checklist.", "lede": "", "items": p["checklist"]},
        {"type": "faq", "eyebrow": "Quick answers", "title": "Common questions.", "lede": "", "items": [{"q": q, "a": a} for q, a in p["faq"]]},
        {"type": "links", "eyebrow": "Keep reading", "title": "More guides.", "lede": "", "items": [link(x) for x in p["links"]]}, CTA]}

for f in glob.glob(os.path.join(OUT, "*.json")): os.remove(f)
if angi:
    angi.update(kicker="Leads and ads", date=CORE_DATE)
    angi["blocks"] = [b for b in angi["blocks"] if b["type"] not in ("links", "cta")] + [
        {"type": "links", "eyebrow": "Keep reading", "title": "More guides.", "lede": "", "items": [link(x) for x in ["is-hipages-worth-it", "is-checkatrade-worth-it", "are-local-services-ads-worth-it", "how-to-get-more-customers"]]}, CTA]
    json.dump(angi, open(os.path.join(OUT, f"{CORE_DATE}-00-is-angi-worth-it.json"), "w"), ensure_ascii=False, indent=1)
for i, p in enumerate(posts):
    json.dump(to_json(p), open(os.path.join(OUT, f"{CORE_DATE}-{i + 1:02d}-{p['slug']}.json"), "w"), ensure_ascii=False, indent=1)
for p in daily:
    json.dump(to_json(p), open(os.path.join(OUT, f"{p['date']}-{p['slug']}.json"), "w"), ensure_ascii=False, indent=1)
print(f"generated {len(posts) + 1 + len(daily)} posts ({len(daily)} daily)")
