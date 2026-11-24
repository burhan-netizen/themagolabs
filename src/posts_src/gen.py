"""Turns posts_src/*.py into src/posts/NN-slug.json (run before build.py)."""
import json, os, re, glob, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "posts")
posts = []
for f in sorted(glob.glob(os.path.join(HERE, "[a-z]_*.py"))):
    spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    posts += m.POSTS
import sys; sys.path.insert(0, HERE); from extra import EXTRA
for p in posts: p["html"] += EXTRA.get(p["slug"], "")
angi = json.load(open(glob.glob(os.path.join(OUT, "*is-angi-worth-it.json"))[0]))
order = ["is-angi-worth-it", "is-hipages-worth-it", "is-checkatrade-worth-it", "are-local-services-ads-worth-it", "customer-ghosted-after-quote",
         "how-to-deal-with-time-wasters", "should-you-charge-for-quotes", "how-to-get-more-customers", "how-to-get-google-reviews", "slow-season", "how-to-get-paid-on-time"]
content = json.load(open(os.path.join(HERE, "..", "trades_content.json")))
def plain(s): return re.sub(r"\*", "", s)
titles = {p["slug"]: plain(p["h1"]) for p in posts}
titles["is-angi-worth-it"] = plain(angi["blocks"][0]["h1"])
def link(x):
    if x.startswith("/"): return {"href": x, "title": content[x]["blocks"][0]["h1"], "text": ""}
    return {"href": f"/guides/{x}/", "title": titles[x], "text": ""}
CTA = {"type": "cta", "eyebrow": "Your turn", "title": "Send us your Instagram. We will show you your website.", "text": "Within 48 hours you get a working preview of your new site, free and with no strings."}
for f in glob.glob(os.path.join(OUT, "*.json")): os.remove(f)
angi["blocks"] = [b for b in angi["blocks"] if b["type"] != "links"][:-1] + [{"type": "links", "eyebrow": "Keep reading", "title": "More guides.", "lede": "", "items": [link(x) for x in ["is-hipages-worth-it", "is-checkatrade-worth-it", "are-local-services-ads-worth-it", "how-to-get-more-customers"]]}, CTA]
out = {"is-angi-worth-it": angi}
for p in posts:
    out[p["slug"]] = {"path": f"/guides/{p['slug']}/", "group": "work", "card": p["card"], "title": p["title"], "desc": p["desc"], "blocks": [
        {"type": "hero", "h1": p["h1"], "eyebrow": "Guide / Updated November 2026", "lede": p["lede"], "ticks": p["ticks"]},
        {"type": "guide", "html": p["html"]},
        {"type": "list", "eyebrow": "Do this now", "title": "Your checklist.", "lede": "", "items": p["checklist"]},
        {"type": "faq", "eyebrow": "Quick answers", "title": "Common questions.", "lede": "", "items": [{"q": q, "a": a} for q, a in p["faq"]]},
        {"type": "links", "eyebrow": "Keep reading", "title": "More guides.", "lede": "", "items": [link(x) for x in p["links"]]}, CTA]}
assert set(out) == set(order), set(out) ^ set(order)
K = {"Leads and ads": order[:4], "Quotes": order[4:7], "Getting work": order[7:10], "Getting paid": order[10:]}
for lab, ks in K.items():
    for k in ks: out[k]["kicker"] = lab
for i, k in enumerate(order):
    json.dump(out[k], open(os.path.join(OUT, f"{i+1:02d}-{k}.json"), "w"), ensure_ascii=False, indent=1)
# checks: no em dashes, no hyphenated words in prose, desc lengths
for k, v in out.items():
    txt = json.dumps(v, ensure_ascii=False)
    bad = re.findall(r"[—–]", txt) + re.findall(r"(?<![\w/#\"])[A-Za-z]+-[A-Za-z]+(?![\w/\".])", re.sub(r'(href|id)=\\"[^\\]*\\"', "", txt))
    print(f"{k:34} title {len(v['title']):3} desc {len(v['desc']):3}", "ISSUES:" if bad else "", bad[:6])
