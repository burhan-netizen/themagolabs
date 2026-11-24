"""Pages moved over from trades.magolabs.in: trades, countries, guides and two services.

Content lives in trades_content.json (already cleaned: studio voice is "we", no prices, no hyphens).
Rendered with the site's own components so the pages match the rest of themagolabs.com.
REDIRECTS maps every old trades.magolabs.in path to its new home here.
"""
import json, os, re, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = json.load(open(os.path.join(HERE, "trades_content.json"), encoding="utf-8"))

TRADES = ["concreters", "excavation", "roofers", "builders", "landscapers", "plumbers", "electricians", "hvac",
          "painters", "tilers", "glaziers", "handymen"]
COUNTRIES = [("usa", "USA"), ("canada", "Canada"), ("australia", "Australia"), ("uk", "UK"), ("new-zealand", "New Zealand")]

# every old trades.magolabs.in URL -> its new path on themagolabs.com
REDIRECTS = {
    "/": "/", "/about/": "/about/", "/contact/": "/contact/", "/faq/": "/process/", "/how-it-works/": "/process/",
    "/pricing/": "/free-audit/", "/privacy/": "/privacy/", "/terms/": "/terms/", "/work/": "/concepts/",
    "/services/": "/services/", "/services/website-design/": "/services/website-design/", "/services/local-seo/": "/services/local-seo/",
    "/services/google-business-profile/": "/services/google-business-profile/", "/services/copywriting/": "/services/copywriting/",
    "/services/social-media/": "/services/", "/services/ai-receptionist/": "/services/",
    "/trades/": "/trades/", "/guides/": "/guides/", "/work/jaymocivil/": "/work/jaymo-civil/",
}
for t in TRADES: REDIRECTS[f"/trades/{t}/"] = f"/trades/{t}/"
for c, _ in COUNTRIES: REDIRECTS[f"/{c}/"] = f"/{c}/"
for p in CONTENT:
    if p.startswith("/guides/"): REDIRECTS[p] = p

def map_href(href, base):
    """Resolve an old relative link against the page it was on, then send it to its new home."""
    if not href or href.startswith(("http", "mailto:", "tel:", "#")):
        return href
    parts = [x for x in base.strip("/").split("/") if x]
    for seg in href.split("#")[0].split("/"):
        if seg in ("", "."): continue
        if seg == "..":
            if parts: parts.pop()
        else: parts.append(seg)
    path = "/" + "/".join(parts) + ("/" if parts else "")
    if path.startswith("/work/") and path not in REDIRECTS: return "/concepts/"
    return REDIRECTS.get(path)

# hand written descriptions where price removal left the original too thin
DESC = {
    "/usa/": "Contractor website design for US trades: built for local search, fast on phones, with tap to call and quote forms. Send your Instagram, get a free preview in 48 hours.",
    "/canada/": "Contractor websites for Canadian trades, built to rank locally and turn searches into calls. You own the site. Send your Instagram for a free preview in 48 hours.",
    "/australia/": "Websites for Australian trades and contractors that rank locally and make the phone ring. You own the site. Send your Instagram, get a free preview in 48 hours.",
    "/uk/": "Websites for UK tradespeople that show up in local search and turn visitors into calls. You own the site. Send your Instagram, get a free preview in 48 hours.",
    "/new-zealand/": "Websites for New Zealand trades that rank locally and win more jobs. Fast, mobile first and yours to keep. Send your Instagram, see a free preview in 48 hours.",
    "/guides/website-cost-usa/": "What a contractor website costs in the USA in 2026: typical market price ranges, what drives the cost, hidden monthly fees and what you should get for your money.",
    "/guides/website-cost-canada/": "What a contractor website costs in Canada in 2026: typical market price ranges, what changes the price, monthly fees to watch for and what a good build includes.",
    "/guides/website-cost-australia/": "What a trade website costs in Australia in 2026: typical market price ranges, what drives the cost, ongoing fees to watch for and what a good build includes.",
    "/guides/website-cost-uk/": "What a tradesperson website costs in the UK in 2026: typical market price ranges, what changes the price, monthly fees to avoid and what a good build includes.",
    "/guides/website-cost-new-zealand/": "What a trade website costs in New Zealand in 2026: typical market price ranges, what drives the cost, ongoing fees to watch for and what a good build includes.",
    "/services/google-business-profile/": "Google Business Profile setup or cleanup for trades: categories, areas, photos, reviews. Quoted up front, and linked to your site free with every build.",
}

def build_all(G):
    E, it, href, page, sh, crumbs, bc, faq, faq_schema, final, process, phone, icon = (
        G["E"], G["it"], G["href"], G["page"], G["sh"], G["crumbs"], G["bc"], G["faq"], G["faq_schema"],
        G["final"], G["process"], G["phone"], G["icon"])
    CONCEPTS = {c[0]: c for c in G["CONCEPTS"]}
    WA, WA_SVG = G["WA"], G["WA_SVG"]

    def md(s, base):
        """Inline markers from the extractor: **bold**, *em*, [text](href)."""
        out = E(s)
        def link(m):
            h = map_href(_html.unescape(m.group(2)), base)
            return f'<a class="ulink" href="{href(h)}">{m.group(1)}</a>' if h else m.group(1)
        out = re.sub(r"\[([^\]]+)\]\(([^)]*)\)", link, out)
        out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
        out = re.sub(r"\*(.+?)\*", r"<em>\1</em>", out)
        return out

    def plain(s):
        return re.sub(r"\*+", "", re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s))

    def brand(s):
        s = re.sub(r"\s*\|\s*Mago Labs\s*$", " | The Mago Labs", s)
        return re.sub(r"(?<![Tt]he )\bMago Labs\b", "the Mago Labs", s).replace("| the Mago Labs", "| The Mago Labs")

    ICON_RULES = [("enquiry", r"quote|form|estimate|enquir|inquir"), ("call", r"\bcall|phone|emergenc|tap"),
                  ("booking", r"book|schedul|timeline|process|calendar|appointment"), ("local", r"area|suburb|town|count(y|ies)|map|local|region|city"),
                  ("seo", r"google|search|seo|found|rank"), ("reviews", r"review|trust|before and after|gallery|photo|proof|portfolio"),
                  ("secure", r"licen|insur|warrant|guarantee|safe|accredit|certif"), ("speed", r"fast|speed|quick|minute"),
                  ("mobile", r"mobile|screen|phone-first|instagram|social"), ("growth", r"grow|bigger|more jobs|commercial|crew|team"),
                  ("pricing", r"price|cost|financ|money|budget")]
    def pick_icon(t, used):
        for name, rx in ICON_RULES:
            if re.search(rx, t, re.I) and name not in used: return name
        for name in ("code", "growth", "speed", "seo", "local", "reviews"):
            if name not in used: return name
        return "code"

    def hero(b, base, trail, kw=None):
        eyebrow = kw or b.get("eyebrow", "")
        ticks = "".join(f"<li>{E(t)}</li>" for t in b.get("ticks", []))
        card = b.get("card") or {}
        if "on this page" in card.get("label", "").lower(): card = {}
        aside = ""
        if card.get("items") and not re.search(r"[$£€]\s?\d", card.get("big", "") + " ".join(card["items"])):
            if "type" in card.get("label", "").lower() or "search" in card.get("label", "").lower():
                first, rest = card["items"][0], card["items"][1:]
                aside = (f'<aside class="tq" data-rise aria-label="{E(card["label"])}"><span class="lab">{E(card["label"])}</span>'
                         f'<div class="tq-bar"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg><span>{E(first)}</span><i class="caret"></i></div>'
                         f'<ul>{"".join(f"<li>{E(x)}</li>" for x in rest)}</ul><p>{E(card.get("note", ""))}</p></aside>')
            else:
                aside = (f'<aside class="tq tq-plain" data-rise><span class="lab">{E(card["label"])}</span>'
                         f'<p class="tq-big">{E(card.get("note") or card.get("big", ""))}</p><ul class="tq-list">{"".join(f"<li>{E(x)}</li>" for x in card["items"])}</ul></aside>')
        return (f'<section class="phero thero"><div class="wrap"><div class="thero-grid"><div>{crumbs(*trail)}'
                f'<span class="lab kw">{E(eyebrow)}</span><h1 class="h-page" data-split>{it(b["h1"])}</h1>'
                f'<p class="lede" data-rise>{md(b.get("lede", ""), base)}</p>'
                f'<div class="ctas" data-rise><a class="btn" href="#contact" data-site="no" data-magnetic>Get a free preview</a>'
                f'<a class="btn ghost" href="{WA}" data-magnetic>{WA_SVG}WhatsApp us</a></div>'
                f'{f"<ul class=ticks data-rise>{ticks}</ul>" if ticks else ""}</div>{aside}</div></div></section>')

    def render(b, base, alt):
        t = b["type"]; tone = " stone" if alt else ""
        head = sh(E(b.get("eyebrow") or ""), b.get("title") or "", md(b.get("lede", ""), base)) if b.get("title") else ""
        if t == "split":
            paras = [p for p in b.get("paras", []) if p]
            if not paras: return ""
            lead, rest = paras[0], paras[1:]
            card = b.get("card") or {}
            aside = ""
            if card.get("items") and not re.search(r"[$£€]\s?\d", card.get("big", "") + " ".join(card["items"])):
                aside = f'<aside class="tq tq-plain"><span class="lab">{E(card["label"])}</span><ul class="tq-list">{"".join(f"<li>{E(x)}</li>" for x in card["items"])}</ul></aside>'
            return (f'<section class="sec{tone}"><div class="wrap tsplit"><div class="tprose"><p class="tlead" data-rise>{md(lead, base)}</p>'
                    f'{"".join(f"<p data-rise>{md(p, base)}</p>" for p in rest)}</div>{aside}</div></section>')
        if t == "cards":
            used, cards = set(), ""
            for i, c in enumerate(b["items"]):
                ic = pick_icon(c["title"] + " " + c["text"], used); used.add(ic)
                cards += (f'<div class="col tcard"><div class="mv mv-icon"><span class="tic">{icon(ic)}</span><span class="tno">{i + 1:02d}</span></div>'
                          f'<h3 class="h3">{E(c["title"])}</h3><p>{md(c["text"], base)}</p></div>')
            return f'<section class="sec{tone}"><div class="wrap">{head}<div class="grid3" data-stagger>{cards}</div></div></section>'
        if t == "list":
            items = "".join(f'<li><span class="n">{i + 1:02d}</span>{md(x, base)}</li>' for i, x in enumerate(b["items"]))
            cls = "pmap" if not base.startswith("/guides/") else "pmap qlist"
            return f'<section class="sec{tone}"><div class="wrap">{head}<ol class="{cls}" data-stagger>{items}</ol></div></section>'
        if t == "work":
            phones = ""
            for i, w in enumerate(b["items"]):
                slug = (w.get("href") or "").strip("/").split("/")[-1]
                if slug in CONCEPTS: phones += phone(CONCEPTS[slug])
            if not phones: return ""
            return (f'<section class="sec{tone}"><div class="wrap">{head or sh("Built for trades like yours", "Live sites. *Open them on your phone.*")}'
                    f'<div class="grid-phones" data-stagger>{phones}</div><p class="tmore"><a class="ulink" href="{href("/concepts/")}">See every concept site</a></p></div></section>')
        if t == "links":
            seen, cards = set(), ""
            for l in b["items"]:
                h = map_href(l.get("href"), base)
                if not h or h in seen or h == base or h == "/free-audit/": continue
                seen.add(h)
                desc = f'<span class="d">{E(l["text"])}</span>' if l.get("text") else ""
                cards += f'<a class="tlink" href="{href(h)}"><span class="t">{E(l["title"])}</span>{desc}<span class="go" aria-hidden="true">→</span></a>'
            if not cards: return ""
            head = head or sh("Keep exploring", "Related *pages.*")
            return f'<section class="sec{tone}"><div class="wrap">{head}<div class="tlinks" data-stagger>{cards}</div></div></section>'
        if t == "faq":
            items = [(plain(i["q"]), plain(i["a"])) for i in b["items"] if i["q"] and i["a"]]
            if not items: return ""
            FAQS.extend(items)
            return f'<section class="sec{tone} tight"><div class="wrap">{head}{faq(items)}</div></section>'
        if t == "guide":
            h = b["html"]
            h = re.sub(r'<article[^>]*>', '', h).replace("</article>", "")
            h = re.sub(r'\sclass="[^"]*"', "", h)
            h = re.sub(r'href="([^"]+)"', lambda m: f'href="{href(map_href(_html.unescape(m.group(1)), base) or "/guides/")}"' if not m.group(1).startswith(("http", "#", "mailto")) else m.group(0), h)
            h = re.sub(r"(?<![Tt]he )\bMago Labs\b", "the Mago Labs", h)
            toc = "".join(f'<li><a href="#{i}">{_html.unescape(re.sub("<[^>]+>", "", x))}</a></li>' for i, x in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', h))
            return (f'<section class="sec gsec"><div class="wrap gwrap"><aside class="gtoc"><span class="lab">On this page</span><ol>{toc}</ol></aside>'
                    f'<article class="gprose">{h}</article></div></section>')
        if t == "unknown":
            if "How it works" in b.get("text", "") or "Day 1" in b.get("text", ""):
                return process()
            return ""
        return ""

    def build(path, trail, schema_trail, kw=None, extra_schema=None):
        d = CONTENT[path]
        FAQS.clear()
        blocks = d["blocks"]
        hero_b = next(b for b in blocks if b["type"] == "hero")
        body = hero(hero_b, path, trail, kw)
        alt = False; final_t = None
        for b in blocks:
            if b is hero_b: continue
            if b["type"] == "cta":
                final_t = b.get("title"); continue
            if b["type"] == "unknown" and not ("How it works" in b.get("text", "") or "Day 1" in b.get("text", "")): continue
            out = render(b, path, alt)
            if out: body += out; alt = not alt
        ft = final_t or "Send us your Instagram. *We'll show you your website.*"
        if "*" not in ft:
            ft = re.sub(r"^(.*?[.!?])\s+(.+)$", r"\1 *\2*", ft)
        body += final(ft)
        desc = DESC.get(path) or brand(d["desc"] or "")
        if re.search(r"[$£€]\s?\d", desc):
            desc = re.sub(r"\s*from\s+[^,.]*[$£€][\d,]+[^,.]*[,.]?", ".", desc).replace("..", ".").strip()
        if len(desc) > 158: desc = desc[:155].rsplit(" ", 1)[0] + "."
        schema = [bc(*schema_trail)]
        if FAQS: schema.append(faq_schema(list(FAQS)))
        if extra_schema: schema.append(extra_schema)
        page(path, brand(d["title"]), desc, body, schema=schema)

    FAQS = []
    # hubs first so their links resolve to real pages
    build("/trades/", [("", "Trades")], [("/trades/", "Trades")], kw="Websites for trades and contractors")
    for t in TRADES:
        name = CONTENT[f"/trades/{t}/"]["blocks"][0].get("eyebrow", "").replace("Websites for ", "").strip() or t.title()
        build(f"/trades/{t}/", [("/trades/", "Trades"), ("", name[:1].upper() + name[1:])], [("/trades/", "Trades"), (f"/trades/{t}/", name[:1].upper() + name[1:])])
    for c, label in COUNTRIES:
        build(f"/{c}/", [("", label)], [(f"/{c}/", label)])
    build("/guides/", [("", "Guides")], [("/guides/", "Guides")], kw="Guides for trades and contractors")
    for p in CONTENT:
        if p.startswith("/guides/") and p != "/guides/":
            d = CONTENT[p]; title = re.sub(r"\s*\|.*$", "", d["title"]).strip()
            art = {"@context": "https://schema.org", "@type": "Article", "headline": title[:110], "author": {"@type": "Person", "name": "Burhan Kapasi"},
                   "publisher": {"@type": "Organization", "name": "The Mago Labs"}, "mainEntityOfPage": G["abs_url"](p)}
            build(p, [("/guides/", "Guides"), ("", title[:48] + ("…" if len(title) > 48 else ""))], [("/guides/", "Guides"), (p, title)], extra_schema=art)
    for s, n in (("google-business-profile", "Google Business Profile"), ("copywriting", "Copywriting")):
        build(f"/services/{s}/", [("/services/", "Services"), ("", n)], [("/services/", "Services"), (f"/services/{s}/", n)])
