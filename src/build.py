"""themagolabs.com v3 generator.
  python -I src/build.py          -> dist/     (production)
  python -I src/build.py preview  -> preview/  (self-contained, relative links)"""
import sys, os, re, json, html, shutil
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import SITE, CLIENTS, CATS, TESTIMONIALS, CONCEPTS, PLANS
import words as C
import opts as OPTS
from minis import minis
import trades as TR

MODE = sys.argv[1] if len(sys.argv) > 1 else "prod"
OUT = "preview" if MODE == "preview" else "dist"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(ROOT, "..", "brand-kit", "logos")
TODAY = date(2026, 11, 20).isoformat()
L = json.load(open(os.path.join(BRAND, "_inline.json"), encoding="utf-8"))
CSS = open(os.path.join(ROOT, "src", "site.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "src", "orbit.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "src", "extras.css"), encoding="utf-8").read()
CSS += OPTS.CSS + OPTS.SITE_CSS
JS = open(os.path.join(ROOT, "src", "orbit.js"), encoding="utf-8").read() + open(os.path.join(ROOT, "src", "site.js"), encoding="utf-8").read() + open(os.path.join(ROOT, "src", "extras.js"), encoding="utf-8").read() + OPTS.JS
BY = {c["slug"]: c for c in CLIENTS}
E = lambda s: html.escape(s, quote=True)
def it(s): return re.sub(r"\*(.+?)\*", r"<em>\1</em>", E(s))
def plain(s): return s.replace("*", "")
def svg(key):
    s = re.sub(r' width="\d+" height="\d+"', "", L[key], count=1)
    return s.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)
def icon(n): return svg("icon-" + n).replace('class="dot"', 'class="dot2"')

HEROSHOT = lambda c: ("/assets/work/" + c["src"] + "-hero.webp") if os.path.exists(os.path.join(ROOT, "assets", "work", c["src"] + "-hero.webp")) else ("/assets/work/" + c["src"] + "-card.webp")
FULLSHOT = lambda c: ("/assets/work/" + c["src"] + "-full.webp") if os.path.exists(os.path.join(ROOT, "assets", "work", c["src"] + "-full.webp")) else ("/assets/work/" + c["src"] + ".webp")
WA_SVG = '<svg class="wa-ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
CUR = ["/"]
def depth(p): return len([x for x in p.strip("/").split("/") if x])
def href(p):
    if MODE != "preview": return p
    pre = "../" * depth(CUR[0])
    return pre + "index.html" if p == "/" else pre + p.strip("/") + "/index.html"
def asset(p): return ("../" * depth(CUR[0]) + p.lstrip("/")) if MODE == "preview" else p
def abs_url(p): return SITE["domain"] + p
WA = f"https://wa.me/{SITE['whatsapp']}?text=" + "Hi%20Burhan%2C%20I%20found%20The%20Mago%20Labs%20and%20would%20like%20to%20talk%20about%20a%20website."

# ---------------- shell ----------------
NAV = [("/work/", "Work"), ("/concepts/", "Concepts"), ("/services/", "Services"), ("/about/", "About")]
def header(active):
    items = "".join(f'<li><a href="{href(p)}" aria-label="{n}"{" aria-current=" + chr(34) + "page" + chr(34) if active == p else ""}><span class="roll" aria-hidden="true"><i>{n}<br>{n}</i></span></a></li>' for p, n in NAV)
    m = "".join(f'<li><a href="{href(p)}">{n}<span>0{i}</span></a></li>' for i, (p, n) in enumerate(NAV + [("/testimonials/", "Reviews"), ("/contact/", "Contact")], 1))
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
  <a class="brand" href="{href('/')}" aria-label="The Mago Labs home"><span class="b-ink">{svg('lockup-ink')}</span><span class="b-paper">{svg('lockup-paper')}</span></a>
  <nav aria-label="Main"><ul class="nav">{items}</ul></nav>
  <a class="btn sm desk" href="#contact" data-magnetic>Let's talk</a>
  <button class="menu-btn open" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<div class="mnav" id="mnav" hidden role="dialog" aria-modal="true" aria-label="Menu">
  <div class="top"><a class="brand" href="{href('/')}" aria-label="The Mago Labs home">{svg('lockup-paper')}</a><button class="menu-btn close" type="button">Close</button></div>
  <ul>{m}</ul>
  <a class="btn" href="#contact">Let's talk</a>
  <div class="contact"><a href="{WA}">WhatsApp {SITE['whatsapp_display']}</a><a href="mailto:{SITE['email']}">{SITE['email']}</a></div>
</div>'''

def footer():
    return f'''<footer class="ftr" data-dark><div class="wrap">
  <div class="top">
    <div class="cta"><p>Got a website that should be <em>working harder?</em> Or none at all?</p><div class="links people"><div class="person"><span class="who">Burhan · Founder</span><a href="{WA}">{WA_SVG}WhatsApp Burhan</a><a href="mailto:{SITE['email']}">{SITE['email']}</a></div><div class="person"><span class="who">Priyanka · International</span><a href="https://wa.me/917420819299?text=Hi%20Priyanka%2C%20I%20found%20The%20Mago%20Labs%20and%20would%20like%20to%20talk%20about%20a%20website.">{WA_SVG}WhatsApp Priyanka</a><a href="mailto:priyanka@themagolabs.com">priyanka@themagolabs.com</a></div></div></div>
    <div class="cols">
      <div><p class="fh">Studio</p><ul><li><a href="{href('/work/')}">Work</a></li><li><a href="{href('/concepts/')}">Concepts</a></li><li><a href="{href('/testimonials/')}">Reviews</a></li><li><a href="{href('/about/')}">About</a></li><li><a href="{href('/process/')}">Process</a></li><li><a href="{href('/trades/')}">Trades</a></li><li><a href="{href('/guides/')}">Guides</a></li></ul></div>
      <div><p class="fh">Build</p><ul>{"".join(f'<li><a href="{href("/services/" + k + "/")}">{v["name"]}</a></li>' for k, v in C.SERVICES.items())}</ul></div>
      <div><p class="fh">Talk</p><ul><li><a href="{WA}">WhatsApp</a></li><li><a href="mailto:{SITE['email']}">Email</a></li><li><a href="{SITE['linkedin']}" rel="noopener">LinkedIn</a></li><li><a href="{SITE['instagram']}" rel="noopener">Instagram</a></li><li><a href="{href('/contact/')}">Contact</a></li></ul></div>
    </div>
  </div>
  <p class="word" aria-hidden="true"><em>the</em>Mago Labs<span class="dot"></span></p>
  <div class="bottom"><span>© 2026 The Mago Labs · Built to convert.</span><span><a href="{href('/privacy/')}">Privacy</a> · <a href="{href('/terms/')}">Terms</a></span><span>Websites that pay for themselves</span></div>
</div></footer>
<div class="mcta"><a class="btn" href="#contact">Let's talk</a><a class="btn wa" href="{WA}">{WA_SVG}WhatsApp</a></div>
<div class="curtain" aria-hidden="true"><span class="dot"></span></div>'''

LOADER = '''<div class="loader" aria-hidden="true"><div class="inner">
<svg viewBox="0 0 136 112"><path class="m" stroke="#F2F1EC" stroke-width="1.5" fill="transparent" d="M10 110 L10 50 L34 42.8 L60 72 L86 27.2 L110 20 L110 110 L86 110 L86 55.2 L60 100 L34 70.8 L34 110 Z"/><circle class="ld" r="10" cx="124" cy="11" fill="#10B565"/></svg>
<span class="count">000</span></div></div>'''

PAGES = []
_IMG_RE = re.compile(r'<img\b(?![^>]*\bsrcset=)([^>]*?)\bsrc="(/assets/[^"]+?)\.webp"([^>]*\bloading="lazy"[^>]*)>')
def responsive(doc):
    """Lazy images with a 640px copy get a srcset, so small slots load the small file (sizes=auto picks by rendered width)."""
    def sub(m):
        base = m.group(2)
        small = os.path.join(ROOT, base.lstrip("/") + "-640.webp")
        if not os.path.exists(small): return m.group(0)
        try:
            from PIL import Image as _I
            w = _I.open(os.path.join(ROOT, base.lstrip("/") + ".webp")).width
        except Exception:
            return m.group(0)
        return f'<img{m.group(1)}src="{base}.webp" srcset="{base}-640.webp 640w, {base}.webp {w}w" sizes="auto, 100vw"{m.group(3)}>'
    return _IMG_RE.sub(sub, doc)

FIRST = 'try{if(!sessionStorage.getItem("mago-intro")&&!matchMedia("(prefers-reduced-motion: reduce)").matches){document.documentElement.classList.add("first");setTimeout(function(){document.documentElement.classList.remove("first")},4500)}}catch(e){}'  # homepage only: holds the hero intro while the first-visit loader is up
_HERO_RE = re.compile(r'<h1 class="h-hero">(.*?)</h1>', re.S)
def presplit(doc):
    """Split the home headline into words in the HTML itself, so its rise animation is pure CSS and starts on first paint."""
    def sub(m):
        parts, i = [], 0
        for tok in re.findall(r'<em>.*?</em>|[^\s<]+', m.group(1)):
            parts.append(f'<span class="w"><span style="--i:{i}">{tok}</span></span>'); i += 1
        return '<h1 class="h-hero" data-done="1">' + " ".join(parts) + '</h1>'
    return _HERO_RE.sub(sub, doc)

def page(path, title, desc, body, active=None, schema=None, noindex=False, loader=False):
    CUR[0] = path
    canon = abs_url(path)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    if MODE == "preview":
        css = f"<style>{CSS}</style>"
        libs = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>'
                '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>'
                '<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>')
        js = libs + f"<script>{JS}</script>"
    else:
        import hashlib
        ver = hashlib.sha1((CSS + JS).encode("utf-8")).hexdigest()[:10]
        css = f'<link rel="stylesheet" href="/assets/site.css?v={ver}">'
        js = ('<script src="/assets/vendor/gsap.min.js" defer></script><script src="/assets/vendor/ScrollTrigger.min.js" defer></script>'
              '<script src="/assets/vendor/lenis.min.js" defer></script>' + f'<script src="/assets/site.js?v={ver}" defer></script>')
    ga = ""
    if SITE["ga4"] and MODE != "preview":
        ga = f'<script async src="https://www.googletagmanager.com/gtag/js?id={SITE["ga4"]}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{SITE["ga4"]}");</script>'
    ft = title if "Mago Labs" in title else f"{title} | The Mago Labs"
    head = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(ft)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:type" content="website"><meta property="og:site_name" content="The Mago Labs"><meta property="og:title" content="{E(ft)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{abs_url('/assets/og.png')}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#050505">
<link rel="icon" href="{asset('/favicon.ico')}?v=2" sizes="32x32"><link rel="icon" href="{asset('/favicon.svg')}?v=2" type="image/svg+xml"><link rel="apple-touch-icon" href="{asset('/apple-touch-icon.png')}">
<link rel="preload" href="/assets/fonts/geist-500.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/geist-400.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/newsreader-italic-300.woff2" as="font" type="font/woff2" crossorigin><style>@font-face{{font-family:"Geist";font-weight:400;font-style:normal;font-display:swap;src:url(/assets/fonts/geist-400.woff2) format("woff2")}}@font-face{{font-family:"Geist";font-weight:500;font-style:normal;font-display:swap;src:url(/assets/fonts/geist-500.woff2) format("woff2")}}@font-face{{font-family:"Geist Mono";font-weight:400;font-style:normal;font-display:swap;src:url(/assets/fonts/geist-mono-400.woff2) format("woff2")}}@font-face{{font-family:"Newsreader";font-weight:300;font-style:italic;font-display:swap;src:url(/assets/fonts/newsreader-italic-300.woff2) format("woff2")}}</style>
<script>document.documentElement.classList.add("js");{FIRST if loader else ""}window.MAGO={{whatsapp:"{SITE['whatsapp']}",formEndpoint:"{SITE['form_endpoint']}",formKey:"{SITE.get('form_key', '')}",email:"{SITE['email']}"}};</script>
{css}{ga}{ld}'''
    inner = f'{LOADER if loader else ""}{header(active)}<main id="main">{body}</main>{footer()}{js}'
    if MODE == "preview" and path == "/":
        doc = head.split("\n", 2)[2] + inner
    else:
        doc = f'<!doctype html>\n<html lang="en">\n<head>\n{head}\n</head>\n<body>\n{inner}\n</body>\n</html>\n'
    assert "—" not in doc, f"em dash on {path}"
    out = os.path.join(ROOT, OUT, "404.html") if path == "/404" else os.path.join(ROOT, OUT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(presplit(minis(responsive(doc))))
    PAGES.append((path, noindex))

# ---------------- components ----------------
def sh(label, title, side="", tag="h2"):
    return f'<div class="sh"><span class="lab">{label}</span><{tag} class="h2" data-split>{it(title)}</{tag}>{"<p class=" + chr(34) + "side" + chr(34) + " data-rise>" + side + "</p>" if side else ""}</div>'

def crumbs(*pairs):
    parts = [f'<a href="{href("/")}">Home</a>']
    for p, n in pairs: parts += ["/", f'<a href="{href(p)}">{E(n)}</a>' if p else f"<span>{E(n)}</span>"]
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'
def bc(*pairs):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": abs_url("/")}]
    items += [{"@type": "ListItem", "position": i, "name": n, "item": abs_url(p)} for i, (p, n) in enumerate(pairs, 2)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def rcard(c, i, eager=False):
    return (f'<a class="rcard" href="{href("/work/" + c["slug"] + "/")}" data-cat="{c["cat"]}" data-cursor="View case">'
            f'<div class="shot"><span class="badge live">Live client</span><img src="{asset(HEROSHOT(c))}" alt="Homepage of the website The Mago Labs built for {E(c["name"])}" width="1600" height="1000" loading="{"eager" if eager else "lazy"}" decoding="async"></div>'
            f'<div class="meta"><span class="idx">{i:02d}</span><h3>{E(c["name"])}</h3><p class="res">{c["card"]}</p></div></a>')

def phone(cn, eager=False):
    slug, name, trade, where = cn
    f = slug[:16]
    return (f'<a class="phone" href="https://{slug}.vercel.app/" rel="noopener" data-live="{slug}" data-cursor="Open site" data-long="{asset("/assets/concepts/poster/" + f + "-scroll.webp")}" aria-label="{E(name)}, concept website. Opens the working site.">'
            f'<div class="dev"><span class="badge">Concept</span><div class="scr"><img src="{asset("/assets/concepts/poster/" + f + ".webp")}" alt="Mobile homepage of the concept website for {E(name)}" width="440" height="902" loading="{"eager" if eager else "lazy"}" decoding="async"></div></div>'
            f'<div><h3>{E(name)}</h3><p class="where">{E(trade)} · {E(where)}</p></div></a>')


def index():
    rows = "".join(
        f'<a class="irow" href="{href("/work/" + c["slug"] + "/")}" data-img="{asset("/assets/work/" + c["src"] + "-card.webp")}" data-tag="{E(c["industry"])}">'
        f'<span class="th"><img src="{asset("/assets/work/" + c["src"] + "-card.webp")}" alt="" width="900" height="426" loading="lazy"></span>'
        f'<span class="idx">{i:02d}</span><span class="nm">{E(c["name"])}<span class="dot"></span></span><span class="ind">{E(c["industry"])}</span><span class="rs">{c["card"]}</span></a>'
        for i, c in enumerate(CLIENTS, 1))
    return f'<div class="index" data-index>{rows}<div class="ipreview" aria-hidden="true"><div class="pf"><span class="badge live tag"></span></div></div></div>'

FOUNDER_PHOTOS = [  # (file, caption, place)
    ("sofa", "Hi, I'm Burhan. Pull up a chair.", "Off the clock"),
    ("tiger", "Met a tiger. Asked about his website.", "Close encounters"),
    ("lanterns", "Colour inspiration, collected.", "Lantern street, Vietnam"),
    ("saigon", "Even the city hall has a great hero section.", "Ho Chi Minh City"),
    ("mountains", "Best place to think about your homepage.", "Up in the mountains"),
    ("shoreline", "Ideas arrive on long walks.", "Barefoot, between briefs"),
    ("night-swing", "Where the best headlines get written.", "Late night swing"),
    ("white-arch", "Found the perfect frame. Then built one.", "Whitewashed arches"),
    ("beach-shades", "Wi-Fi optional. Smiles mandatory.", "Beach shack office"),
    ("night-out", "The horns come out when a site goes live.", "Off duty"),
]

def contact(title="Your hardest working hire *starts here.*", sub=""):
    P = OPTS.parts(globals(), False)
    return f'''<section class="contact-sec cx" id="contact" data-dark aria-labelledby="contact-h">
  <div class="cx-glow" aria-hidden="true"></div>
  <div class="wrap"><div class="cx-head"><span class="lab live">Let's talk · reply within one business day</span>
    <h2 class="c-h" id="contact-h">{it(title)}{(" " + E(sub)) if sub else ""}</h2></div>
    <div class="cx-card">{P["d3box"]}</div>
    <div class="d3-alt"><span>Have a website? Free audit. No website yet? Free working preview in 48 hours. No strings, no spam.</span><a href="{WA}">{WA_SVG}Rather chat? WhatsApp Burhan</a></div>
  </div></section>'''

def final(*a, **k):
    return contact(*a, **k)

def logowall():
    from PIL import Image as _I
    cells = ""
    for c in CLIENTS:
        f = os.path.join(ROOT, "assets", "wall2", c["src"] + ".webp")
        if not os.path.exists(f): continue
        w, h = _I.open(f).size
        shape = "wide" if w / h > 3 else ("mid" if w / h > 1.6 else "sq")
        tone = " ink" if c["src"] in ("jaymocivil",) else ""
        res = re.sub(r"<[^>]+>", "", c["card"])
        cells += (f'<a class="lw-cell{tone}" href="{href("/work/" + c["slug"] + "/")}" aria-label="{E(c["name"])}: {E(res)}">'
                  f'<img class="{shape}" src="{asset("/assets/wall2/" + c["src"] + ".webp")}" alt="{E(c["name"])}" width="{w}" height="{h}" loading="lazy">'
                  f'<span class="res">{E(res)}</span></a>')
    cells += '<a class="lw-cell lw-next" href="#contact"><p>Your logo, <em>right here</em><span class="caret"></span></p><span class="ulink">Let\'s talk →</span></a>'
    return f'''<section class="sec lwall"><div class="wrap">{sh("Trusted by " + SITE['businesses'] + " businesses", "Good company *to keep.*", "Clinics, CA firms, contractors, manufacturers. Hover a logo for the result.")}
  <div class="lw-grid" data-stagger>{cells}</div></div></section>'''

def labfloor():
    return OPTS.parts(globals(), False)["a2"]

def process():
    return OPTS.parts(globals(), False)["b3"]

def founder():
    pol = ""
    for f, cap, place in FOUNDER_PHOTOS:
        if not os.path.exists(os.path.join(ROOT, "assets", "founder", f + ".webp")): continue
        pol += f'<figure class="polo"><img src="{asset("/assets/founder/" + f + ".webp")}" alt="Burhan Kapasi, {E(place.lower())}" loading="lazy" draggable="false"><figcaption><em>{E(cap)}</em><span>{E(place)}</span></figcaption></figure>'
    return f'''<section class="sec founder" aria-label="Meet the founder"><div class="wrap"><div class="fd">
  <div class="txt"><span class="lab">Meet the founder</span><h2 data-split>The guy <em>behind the dot.</em></h2>
    <div class="story" data-rise><p>I'm Burhan. I spent eight years inside banks, fintech and insurance, and walked out knowing one thing: people don't buy the best. <em>They buy the one they trust first.</em></p>
    <p>Now I build websites that earn that trust in seconds, for businesses across India, Australia, the USA, the UK and Canada.</p>
    <p>When I'm not building, I'm somewhere new. Lanterns, mountains, long beach walks. Every trip ends up in a website somewhere: a colour, a headline, a feeling.</p></div>
    <div class="facts2" data-rise><div><span class="k">Based in</span><span class="v">Surat, India</span></div><div><span class="k">Clients in</span><span class="v">India · Australia · USA · UK · Canada</span></div>
      <div><span class="k">Before this</span><span class="v">8 years in banking and fintech</span></div><div><span class="k">Recharges by</span><span class="v">Getting lost somewhere new</span></div></div>
    <div class="ctas" data-rise><a class="btn" href="{WA}" data-magnetic>{WA_SVG}Say hi on WhatsApp</a><a class="ulink" href="{href('/about/')}">The full story →</a></div><div class="partner" data-rise><span class="lab">And the other half</span><p class="pn"><b>Priyanka</b> · Co-Founder and Head of International Relations</p><p>I build the websites. Priyanka makes sure our clients overseas are looked after, from the first hello to launch day.</p><div class="pc"><a class="btn" href="https://wa.me/917420819299?text=Hi%20Priyanka%2C%20I%20found%20The%20Mago%20Labs%20and%20would%20like%20to%20talk%20about%20a%20website." data-magnetic>{WA_SVG}WhatsApp Priyanka</a><a class="btn ghost" href="tel:+917420819299" data-magnetic><svg class="btn-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true"><path d="M5 3.5h3.6l1.9 4.8-2.6 1.7a11 11 0 0 0 6.1 6.1l1.7-2.6 4.8 1.9v3.6a1.8 1.8 0 0 1-1.8 1.8A16.7 16.7 0 0 1 3.2 5.3 1.8 1.8 0 0 1 5 3.5z"/></svg>+91 74208 19299</a><a class="btn ghost" href="mailto:priyanka@themagolabs.com" data-magnetic><svg class="btn-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true"><rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 7 9-7"/></svg>Email Priyanka</a></div></div></div>
  <div class="pile-wrap"><div class="stamp" aria-hidden="true"><span><b>{SITE['businesses']}</b>businesses<br>helped</span></div>
    <div class="pile" tabindex="0" role="group" aria-label="Photos of Burhan travelling. Press Enter for the next photo.">{pol}</div>
    <div class="pile-hint"><span class="lab"><span class="dot"></span>Drag or tap to flip through</span><button type="button" class="pile-next">Next photo →</button></div></div>
</div></div></section>'''

def reviews():
    P = OPTS.parts(globals(), False)
    return P["c1"] + f'<script type="application/json" id="op-data">{P["data"]}</script>'

def orbit(clients, label, title):
    cards = ""
    for i, c in enumerate(clients):
        dom = c["url"].replace("https://", "").replace("www.", "").strip("/") if c["url"] else "sales page"
        cards += (f'<li class="ocard" data-name="{E(c["name"])}" data-ind="{E(c["industry"])}" data-where="{E(c["where"])}" data-res="{E(c["card"])}" data-href="{href("/work/" + c["slug"] + "/")}">'
                  f'<a class="olink" href="{href("/work/" + c["slug"] + "/")}" data-cursor="View case" draggable="false"><span class="obar"><i></i><i></i><i></i><b>{E(dom)}</b></span>'
                  f'<img src="{asset(HEROSHOT(c))}" alt="{E(c["name"])} website" width="1600" height="1000" loading="lazy" decoding="async" draggable="false"></a>'
                  f'<span class="oname">{E(c["name"])}<small>{E(c["industry"])}</small></span></li>')
    return f'''<section class="orb-sec" data-dark aria-label="{E(plain(title))}"><div class="orb-stage" tabindex="0" aria-roledescription="carousel" aria-label="Client websites. Use the arrow keys to turn the orbit.">
  <div class="orb-glow" aria-hidden="true"></div><svg class="orb-ring" aria-hidden="true"></svg>
  <div class="orb-head wrap"><span class="lab">{label}</span><h2 data-split>{it(title)}</h2></div>
  <ol class="orb-list">{cards}</ol>
  <div class="orb-info" aria-live="polite"><span class="k"></span><span class="nm t"><span></span></span><span class="rs t"><span></span></span><a class="btn" href="#" data-magnetic>View case</a></div>
  <div class="orb-ui"><span class="cnt" aria-hidden="true"><b>01</b>/ {len(clients):02d}</span><button type="button" class="orb-prev" aria-label="Previous client">←</button><button type="button" class="orb-next" aria-label="Next client">→</button><span class="hint">Scroll or drag to orbit</span></div>
</div></section>'''

def deck(clients, label, title, end_title, end_href, end_label):
    cards = ""
    for i, c in enumerate(clients):
        dom = c["url"].replace("https://", "").replace("www.", "").strip("/") if c["url"] else "sales page"
        meta = "".join(f"<span>{E(x)}</span>" for x in ["Live client", c["industry"], c["where"] or "Design · Build · SEO"])
        cards += (f'<li class="dcard" style="--i:{i}"><a class="dlink" href="{href("/work/" + c["slug"] + "/")}" data-cursor="View case">'
                  f'<span class="dpic"><span class="dshot"><span class="dbar"><i></i><i></i><i></i><b>{E(dom)}</b></span>'
                  f'<span class="dvp"><img src="{asset("/assets/work/" + c["src"] + ".webp")}" alt="Full page screenshot of the {E(c["name"])} website" width="560" height="2275" loading="lazy" decoding="async"></span></span></span>'
                  f'<span class="dmeta">{meta}</span>'
                  f'<span class="drow"><span class="dname">{E(c["name"])}<sup>{i + 1:02d}</sup></span><span class="dres">{c["card"]}</span><span class="darr" aria-hidden="true"><svg class="ext" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M3.5 8.5l5-5M4.5 3.5h4v4"/></svg></span></span>'
                  f'<i class="dsheen"></i><i class="ddim"></i></a></li>')
    n = len(clients) + 1
    cards += (f'<li class="dcard dend" style="--i:{n - 1}"><a class="dlink" href="{href(end_href)}" data-cursor="Open"><span class="lab">{E(end_label)}</span>'
              f'<h3>{it(end_title)}</h3><span class="ulink">Let\'s go →</span><i class="ddim"></i></a></li>')
    return f'''<section class="deck-sec" data-dark aria-label="{E(plain(title))}"><div class="deck-stage">
  <svg class="deck-path" viewBox="0 0 1440 900" preserveAspectRatio="none" aria-hidden="true"><path d="M-40 780 C 260 640, 380 170, 720 210 S 1240 560, 1490 110"/><circle r="7" cx="-40" cy="780"/></svg>
  <div class="deck-back wrap"><span class="lab">{label}</span><h2 data-split>{it(title)}</h2></div>
  <ol class="deck">{cards}</ol>
  <div class="deck-count" aria-hidden="true"><span class="cur">01</span><span>/ {n:02d}</span><span class="hint">Keep scrolling</span></div>
</div></section>'''

def wall():
    cols = [[], [], [], []]
    for i, c in enumerate(CONCEPTS): cols[i % 4].append(phone(c))
    return '<div class="wall"><div class="cols">' + "".join(f'<div class="wc">{"".join(c)}</div>' for c in cols) + "</div></div>"

CNOTE = ('<div class="cnote" data-rise><span class="badge">Concept</span><p><b>Concept builds, not client work.</b> Each is a full working website we designed and wrote for a real trades business, '
         'using their real work and words, to show them what their site could be. Names and logos belong to their owners.</p></div>')

def quote(t, light=False):
    av = f'<img src="{asset("/assets/logos/" + t["src"] + ".webp")}" alt="" width="36" height="30" loading="lazy">' if t["src"] else E("".join(w[0] for w in t["name"].split()[:2]))
    role = ", ".join(x for x in [t["role"], t["company"]] if x)
    link = f'<a href="{href("/work/" + t["case"] + "/")}">{E(role)}</a>' if t["case"] else E(role)
    return (f'<figure class="q"><span class="hd">{E(t["head"])}</span><blockquote>"{E(t["quote"])}"</blockquote>'
            f'<figcaption><span class="av">{av}</span><span class="who">{E(t["name"])}<span>{link}</span></span></figcaption></figure>')

def sticker(top, ring, center, small, link=None):
    tag = "a" if link else "div"
    attr = f' href="{link}" rel="noopener"' if link else ""
    return (f'<{tag} class="sticker"{attr} aria-label="{E(center + " " + small)}"><svg viewBox="0 0 200 200" aria-hidden="true"><defs><path id="c-{abs(hash(ring)) % 9999}" d="M100,100 m-82,0 a82,82 0 1,1 164,0 a82,82 0 1,1 -164,0"/></defs>'
            f'<text><textPath href="#c-{abs(hash(ring)) % 9999}">{E(ring)}</textPath></text></svg><span class="c">{E(center)}<small>{E(small)}</small></span></{tag}>')


def faq(items, dark=False):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}</summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in items) + "</div>"
def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def mq(words):
    s = "".join(f"<span>{w}</span>" for w in words)
    return f'<div class="mq" aria-hidden="true"><div class="in">{s}{s}{s}{s}</div></div>'

def method(steps):
    return '<div class="method"><div class="line"><i></i></div>' + "".join(f'<div class="mstep"><span class="when">{w}</span><h3>{it(t)}</h3><p>{E(d)}</p></div>' for w, t, d in steps) + "</div>"

def stack():
    return '<div class="stack">' + "".join(f'''<a class="scard" style="--i:{i}" href="{href('/services/' + slug + '/')}" data-cursor="Explore"><span class="num">0{i + 1} / 04</span>
<div class="main"><div><h3>{it(h)}</h3><p>{E(d)}</p></div><span class="more ulink">How it works →</span></div><span class="ic">{icon(ic)}</span></a>''' for i, (slug, ic, h, d) in enumerate(C.BUILD)) + "</div>"

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "The Mago Labs", "url": SITE["domain"], "logo": abs_url("/assets/logo.png"),
       "email": SITE["email"], "founder": {"@type": "Person", "name": SITE["founder"]}, "sameAs": [SITE["linkedin"], SITE["instagram"]],
       "aggregateRating": {"@type": "AggregateRating", "ratingValue": SITE["rating"], "reviewCount": SITE["review_count"]}}

def form(kind):
    a = kind == "audit"
    seg = ('<div class="seg" role="radiogroup" aria-label="Do you have a website?"><label><input type="radio" name="has_site" value="yes" checked><span>I have a website</span></label>'
           '<label><input type="radio" name="has_site" value="no"><span>Not yet</span></label></div>') if a else ""
    return f'''<form class="card" data-form="{kind}" data-next="{href('/thank-you/')}" novalidate data-rise>{seg}
<div class="two"><div class="field"><label for="{kind}-name">Your name</label><input id="{kind}-name" name="name" autocomplete="name" data-req><span class="err">Add your name so we know who to reply to.</span></div>
<div class="field"><label for="{kind}-business">Business name</label><input id="{kind}-business" name="business" autocomplete="organization" data-req><span class="err">Add your business name.</span></div></div>
<div class="two"><div class="field"><label for="{kind}-email">Email</label><input id="{kind}-email" name="email" type="email" autocomplete="email" data-req><span class="err">Enter an email like name@business.com.</span></div>
<div class="field"><label for="{kind}-phone">Phone or WhatsApp <span>(optional)</span></label><input id="{kind}-phone" name="phone" type="tel" autocomplete="tel"></div></div>
<div class="field" data-url-field><label for="{kind}-website">Website address</label><input id="{kind}-website" name="website" inputmode="url" placeholder="yourbusiness.com" {"data-req" if a else ""}><span class="err">Add your website, or choose "Not yet".</span></div>
<div class="field"><label for="{kind}-message">{"Anything we should know?" if a else "What do you need?"} <span>(optional)</span></label><textarea id="{kind}-message" name="message"></textarea></div>
<button class="btn" type="submit"><span class="t">{"Get my free audit" if a else "Send it"}</span></button>
<div class="sent" hidden><p><b>One tap left.</b> Send your details to Burhan on WhatsApp, or email them to <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p><a class="btn" href="{WA}">Send on WhatsApp</a></div>
<p class="fine">We reply within one business day. No spam, ever.</p></form>'''

# ================= HOME =================
def build_home():
    H = C.HOME
    feat = ["smile-care-clinic", "darshan-galani-co", "jaymo-civil", "ladson-concrete", "centurion-strategic-ventures", "santosh-timbers", "astrabizz", "solway-energies"]
    rail = "".join(rcard(BY[k], i + 1) for i, k in enumerate(feat))
    tfeat = next(t for t in TESTIMONIALS if t["case"] == "jaymo-civil")
    rest = [t for t in TESTIMONIALS if t is not tfeat]
    row1 = "".join(quote(t, True) for t in rest[:5]); row2 = "".join(quote(t, True) for t in rest[5:])
    body = f'''
<div class="hero-wrap" data-dark><section class="hero" aria-label="Introduction">
  <div class="media">
    <picture><source media="(max-width:760px)" srcset="{asset('/assets/video/hero-poster-mobile.jpg')}"><img class="poster" src="{asset('/assets/video/hero-poster.jpg')}" alt="" width="1600" height="900" fetchpriority="high"></picture>
    <video muted playsinline loop preload="none" aria-hidden="true" style="opacity:0;transition:opacity 1.4s" data-src="{asset('/assets/video/hero.mp4')}" data-src-mobile="{asset('/assets/video/hero-mobile.mp4')}"></video>
    <div class="shade"></div>
  </div>
  <div class="content wrap">
    <h1 class="h-hero">{it(H['h1'])}</h1>
    <div class="row"><p class="lede">{E(H['lede'])}</p>
      <div class="act"><div class="ctas"><a class="btn inv" href="#contact" data-site="yes" data-magnetic>Get a free site audit</a><a class="wa" href="{WA}" data-magnetic>{WA_SVG}WhatsApp us</a></div>
      <p class="nosite">No website yet? <a href="#contact" data-site="no">Get a free preview in 48 hours →</a></p><p class="trust">★ 5.0 on Google · 75+ businesses · India, Australia, USA, UK, Canada</p></div></div>
  </div>
  <div class="scrollcue"><span>Scroll to land</span><i></i></div>
</section></div>

<section class="sec space" data-dark><div class="wrap"><div class="orbit-grid">
  <div class="txt"><span class="lab">{H['orbit_label']}</span><p class="scrub scrub-p" style="margin-top:28px">{E(H['orbit'])}</p></div>
  <div class="viz"><svg class="orbit" viewBox="0 0 400 400" role="img" aria-label="Customers orbit a business; one green dot lands on it">
    <circle class="ring" cx="200" cy="200" r="70"/><circle class="ring" cx="200" cy="200" r="120"/><circle class="ring" cx="200" cy="200" r="172"/>
    <g class="spin1"><circle class="p" cx="270" cy="200" r="5"/><circle class="p" cx="130" cy="200" r="3.5"/></g>
    <g class="spin2"><circle class="p" cx="200" cy="80" r="6"/><circle class="p" cx="315" cy="235" r="4"/><circle class="p" cx="95" cy="260" r="3"/></g>
    <g class="spin3"><circle class="p" cx="372" cy="200" r="4"/><circle class="p" cx="60" cy="110" r="5"/><circle class="p" cx="160" cy="368" r="3.5"/><circle class="p" cx="330" cy="90" r="3"/></g>
    <circle class="core" cx="200" cy="200" r="22"/><circle class="lander" cx="200" cy="200" r="8"/>
    <text x="200" y="250" text-anchor="middle">YOUR BUSINESS</text><text class="landed" x="200" y="266" text-anchor="middle" style="opacity:0;fill:#10B565">+1 CUSTOMER</text>
  </svg><div class="orbit-cap"><span class="lab">Grey: browsing</span><span class="lab" style="color:#10B565">Green: booked</span></div></div>
</div></div></section>

<section class="sec"><div class="wrap">{sh("Lab results", H['proof_h'], "Every number below comes from a live client site. Tap one to see the case.")}
  <div class="proof" data-stagger>
    <a class="pcard big" href="{href('/work/smile-care-clinic/')}" data-cursor="View case"><span class="lab">Dental clinic · patients a day</span><span class="n"><span class="from">25</span><span class="arr">→</span><span class="to" data-count="58" data-from="25">58</span></span><div class="d"><p>A new clinic, within two months of launch. They had to hire more staff to keep up.</p><span class="badge live">Case 01</span></div></a>
    <a class="pcard" href="{href('/work/smile-care-clinic/')}" data-cursor="View case"><span class="lab">Appointment calls</span><span class="n"><span class="to"><span data-count="63">63</span>%</span></span><div class="d"><p>More booking calls in the same two months.</p></div></a>
    <a class="pcard" href="{href('/work/darshan-galani-co/')}" data-cursor="View case"><span class="lab">New clients · 3 months</span><span class="n"><span class="to" data-count="34">34</span></span><div class="d"><p>A CA firm that had never had a website.</p></div></a>
    <div class="pcard"><span class="lab">Businesses helped</span><span class="n">{SITE['businesses']}</span><div class="d"><p>India, Australia, the USA, the UK and Canada.</p></div></div>
    <a class="pcard" href="{SITE['google_reviews']}" rel="noopener" data-cursor="Reviews"><span class="lab">Google rating</span><span class="n">{SITE['rating']}<span style="font-size:.4em">★</span></span><div class="d"><p>From {SITE['review_count']} Google reviews.</p></div></a>
  </div>
</div></section>

{logowall()}

{orbit(CLIENTS, "Live client work · " + str(len(CLIENTS)) + " sites", H['work_h'])}

{mq(["More calls", "More jobs", "More growth", "Built to convert"])}

<section class="split" aria-label="What we believe"><div class="l"><span class="lab">The belief</span><p>{it(H['split_l'])}</p></div><div class="r" data-dark><span class="lab">The point</span><p>{it(H['split_r'])}</p></div></section>

<section class="sec"><div class="wrap">{sh("What we build", H['build_h'], "Four ways we turn a website into your hardest working hire.")}{stack()}</div></section>

{trades_section(" stone")}

{labfloor()}

{process()}

{founder()}

{reviews()}


<section class="sec"><div class="wrap">{sh("Questions", "Straight *answers.*")}{faq(C.FAQ)}</div></section>
{final()}'''
    page("/", C.HOME["title"], C.HOME["desc"], body, loader=True,
         schema=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "The Mago Labs", "url": SITE["domain"]}, faq_schema(C.FAQ)])

# ================= WORK =================
def build_work():
    filt = "".join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in CATS)
    cards = "".join(rcard(c, i + 1, i < 2) for i, c in enumerate(CLIENTS))
    body = f'''
<section class="phero"><div class="wrap">{crumbs(("", "Work"))}
  <h1 class="h-page" data-split>Results, <em>not just pretty pages.</em></h1>
  <p class="lede" data-rise>{len(CLIENTS)} live websites for clinics, accounting firms, contractors, manufacturers and online sellers. Every one started on a blank page. Every one is still live.</p>
  <div class="meta-row" data-rise><div><span class="k">Live sites</span><span class="v">{len(CLIENTS)}</span></div><div><span class="k">Best result</span><span class="v">25 → 58 patients a day</span></div><div><span class="k">Countries</span><span class="v">India · Australia · USA · UK · Canada</span></div><div><span class="k">Google rating</span><span class="v">{SITE['rating']} ★</span></div></div>
</div></section>
{orbit(CLIENTS, "Live client work · " + str(len(CLIENTS)) + " sites", "Every site. *Every result.*")}
<section class="sec space" data-dark style="padding-bottom:110px"><div class="wrap">{sh("From the lab · Concept builds", "And what we'd build *for your trade.*", "Separate from client work.")}{CNOTE}</div>
  {wall()}
  <div class="wrap"><a class="btn inv" href="{href('/concepts/')}" data-magnetic>See all concepts</a></div></section>
{final("Want numbers *like these?*")}'''
    page("/work/", "Work: Live Client Websites and Results", f"{len(CLIENTS)} live client websites and their results, from 25 to 58 patients a day for a dental clinic to 34 new clients in three months for a CA firm.",
         body, active="/work/", schema=[bc(("/work/", "Work"))])

def build_cases():
    for i, c in enumerate(CLIENTS):
        nxt = CLIENTS[(i + 1) % len(CLIENTS)]
        t = next((x for x in TESTIMONIALS if x["case"] == c["slug"]), None)
        meta = [("Client", E(c["name"])), ("Industry", E(c["industry"]))]
        if c["where"]: meta.append(("Location", E(c["where"])))
        meta.append(("Website", f'<a href="{c["url"]}" rel="noopener" data-live="{c["slug"]}">{E(c["url"].replace("https://", "").replace("www.", "").strip("/"))}<svg class="ext" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M3.5 8.5l5-5M4.5 3.5h4v4"/></svg></a>' if c["url"] else "Sales page"))
        md = "".join(f'<div><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in meta)
        built = "".join(f"<li>{E(b)}</li>" for b in c["built"])
        tickets = ""
        if c["tickets"]:
            tickets = '<div class="tickets">' + "".join(
                f'<div class="tk"><span class="lab">{E(l)}</span><div class="row">{(f"<span class=from>{E(f)}</span><span class=arr>→</span>" if f else "")}<span class="to">{E(to)}</span></div><span class="lab">{E(w)}</span></div>'
                for l, f, to, w in c["tickets"]) + "</div>"
        tq = f'<section class="sec space" data-dark><div class="wrap"><div class="feature-q" style="margin:0"><blockquote data-rise>"{E(t["quote"])}"</blockquote><div class="who" data-rise><span>{E(t["name"])}</span><span class="muted">{E(", ".join(x for x in [t["role"], t["company"]] if x))}</span></div></div></div></section>' if t else ""
        visit = f'<a class="btn ghost" href="{c["url"]}" rel="noopener" data-live="{c["slug"]}" data-magnetic>Visit the live site<svg class="ext" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M3.5 8.5l5-5M4.5 3.5h4v4"/></svg></a>' if c["url"] else ""
        dom = c["url"].replace("https://", "").replace("www.", "").strip("/") if c["url"] else "sales page"
        body = f'''
<section class="phero space" data-dark><div class="wrap">{crumbs(("/work/", "Work"), ("", c["short"]))}
  <span class="badge live">Live client · Case {i + 1:02d}</span>
  <h1 class="h-page" data-split style="margin-top:24px">{it(c["headline"])}</h1>
  <div class="meta-row" data-rise>{md}</div>
  <div class="cs-hero-img" data-clip><img src="{asset(HEROSHOT(c))}" alt="Homepage of the {E(c['name'])} website" width="1600" height="1000" fetchpriority="high"></div>
</div></section>
<section class="sec"><div class="wrap"><div class="cs">
  <div class="text">
    <div class="block" data-rise><span class="lab">01 · Before</span><h2>The problem.</h2><p class="body">{E(c["problem"])}</p></div>
    <div class="block" data-rise><span class="lab">02 · Built</span><h2>The website.</h2><ul class="built">{built}</ul></div>
    <div class="block" data-rise><span class="lab">03 · After</span><h2>The result.</h2>{tickets}<p class="body" style="margin-top:{'24px' if tickets else '0'}">{E(c["outcome"])}</p></div>
    <div class="ctas" data-rise>{visit}<a class="btn" href="#contact" data-magnetic>Let's talk</a></div>
  </div>
  <div class="visual"><div class="scrollshot"><div class="bar"><i></i><i></i><i></i><span>{E(dom)}</span></div><div class="vp"><img src="{asset(FULLSHOT(c))}" alt="Full page screenshot of the {E(c['name'])} website" width="1000" height="6000" loading="lazy" decoding="async"></div></div></div>
</div></div></section>
{tq}
<section class="sec tight"><div class="wrap"><a class="next" href="{href('/work/' + nxt['slug'] + '/')}" data-cursor="Next case"><div class="in"><span class="lab">Next case · {E(nxt['name'])}</span><h3>{it(nxt['headline'])}</h3><div class="img"><img src="{asset(HEROSHOT(nxt))}" alt="" width="1600" height="1000" loading="lazy"></div></div></a></div></section>
{final("Want a website *that does this?*")}'''
        page(f"/work/{c['slug']}/", f"{c['name']}: Website Case Study", (f"{c['industry']} case study. {plain(c['headline'])} {c['outcome']}")[:158],
             body, active="/work/", schema=[bc(("/work/", "Work"), (f"/work/{c['slug']}/", c["name"])),
             {"@context": "https://schema.org", "@type": "Article", "headline": f"{c['name']}: {plain(c['headline'])}", "author": {"@type": "Organization", "name": "The Mago Labs"}, "image": abs_url(f"/assets/work/{c['src']}-card.webp"), "datePublished": TODAY}])

def build_concepts():
    body = f'''
<section class="phero space" data-dark><div class="wrap">{crumbs(("", "Concepts"))}
  <span class="badge">Concept builds · not client work</span>
  <h1 class="h-page" data-split style="margin-top:24px">What we'd build <em>for your trade.</em></h1>
  <p class="lede" data-rise style="color:#DAD8D0">{len(CONCEPTS)} working websites for roofers, concreters, earthmovers, glaziers, landscapers and more. Each one sounds like the business it was made for. Hover to scroll a site, tap to open it.</p>
  <div style="margin-top:40px">{CNOTE}</div>
</div>
<div class="wrap" style="margin-top:72px"><div class="grid-phones" data-stagger>{"".join(phone(c, i < 4) for i, c in enumerate(CONCEPTS))}</div></div></section>
<section class="sec"><div class="wrap">{sh("Why concepts", "See your site *before you pay.*")}
  <div class="grid3" data-stagger>
    <div class="col"><span class="num">01</span><h3 class="h3">Real work, real words.</h3><p>Each concept uses the business's own photos, services and reviews, so it shows what their site could actually be.</p></div>
    <div class="col"><span class="num">02</span><h3 class="h3">Zero repeats.</h3><p>A roofer in Brisbane doesn't talk like a tiler in California. Their websites don't either.</p></div>
    <div class="col"><span class="num">03</span><h3 class="h3">Yours in 48 hours.</h3><p>Send us your Instagram or a few photos. We'll send back a working preview of your own site, free.</p></div>
  </div></div></section>
{final("See your own site *in 48 hours.*", "Tell us about your business or send your Instagram. We'll send back a working preview of your new website within 48 hours, free.")}'''
    page("/concepts/", "Concept Websites For Trades and Contractors", f"{len(CONCEPTS)} concept websites for roofers, concreters, earthmovers and other trades. Working sites, clearly marked as concepts, not client work.",
         body, active="/concepts/", schema=[bc(("/concepts/", "Concepts"))])

def build_testimonials():
    body = f'''
<section class="phero"><div class="wrap">{crumbs(("", "Reviews"))}
  <h1 class="h-page" data-split>In their <em>own words.</em></h1>
  <div style="display:flex;gap:40px;align-items:center;flex-wrap:wrap;margin-top:40px"><p class="lede" data-rise>{len(TESTIMONIALS)} reviews from clinics, accounting firms, contractors, consultants and manufacturers. Each links to the work behind it.</p>{sticker("", "Rated 5.0 on Google · " + str(SITE['review_count']) + " reviews · ", SITE['rating'], "Google", SITE['google_reviews'])}</div>
</div></section>
<section class="sec tight light" style="padding-top:0"><div class="wrap"><div class="qgrid" data-stagger>{"".join(quote(t, True) for t in TESTIMONIALS)}</div></div></section>
{final()}'''
    page("/testimonials/", "Client Reviews", f"{len(TESTIMONIALS)} client reviews of The Mago Labs, rated {SITE['rating']} on Google.", body, schema=[bc(("/testimonials/", "Reviews")), ORG])

def industry_cards():
    out = ""
    for slug, name, tags, text in C.INDUSTRY_CARDS:
        link = (href(slug) if slug.startswith("/") else href("/industries/" + slug + "/")) if slug else "#contact"
        more = "Explore" if slug else "Let's talk"
        out += (f'<a class="col ind" href="{link}" data-cursor="{more}"><span class="tags">{E(tags)}</span><h3 class="h3">{E(name)}</h3>'
                f'<p>{E(text)}</p><span class="more">{more} →</span></a>')
    return out

def trades_section(tone=""):
    cards = "".join(f'<a class="tlink" href="{href(h)}"><span class="t">{E(n)}</span><span class="go" aria-hidden="true">→</span></a>' for h, n in C.TRADE_LINKS)
    cards += f'<a class="tlink all" href="{href("/trades/")}"><span class="t">Every trade we build for</span><span class="go" aria-hidden="true">→</span></a>'
    ctry = " · ".join(f'<a class="ulink" href="{href(h)}">{E(n)}</a>' for h, n in C.COUNTRY_LINKS)
    return (f'<section class="sec{tone}"><div class="wrap">{sh("Built for trades", "Websites for *your trade.*", "Roofers, concreters, civil crews and every trade in between. Pick yours to see what we would build.")}'
            f'<div class="tlinks t9" data-stagger>{cards}</div><p class="tmore ctry"><span>Trade websites by country:</span> {ctry} · <a class="ulink" href="{href("/guides/")}">Free guides</a></p></div></section>')

def build_services():
    inds = industry_cards()
    body = f'''
<section class="phero"><div class="wrap">{crumbs(("", "Services"))}<span class="lab kw">Website design services</span>
  <h1 class="h-page" data-split>Websites built to <em>bring in work.</em></h1>
  <p class="lede" data-rise>Everything we make has one job: turn someone who's never heard of you into someone who calls.</p>
  <div class="ctas" data-rise><a class="btn" href="#contact" data-magnetic>Let's talk</a><a class="btn ghost" href="{href('/work/')}" data-magnetic>See the work</a></div>
</div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap">{stack()}</div></section>
<section class="sec stone"><div class="wrap">{sh("By industry", "Built for how *your customers* choose.")}<div class="grid3" data-stagger>{inds}</div></div></section>
{trades_section()}
{final()}'''
    page("/services/", "Website Design and Development Services", "Website design, development, redesign, local SEO, Google Business Profile and copywriting, built around the calls, bookings and jobs that pay you.",
         body, active="/services/", schema=[bc(("/services/", "Services"))])
    for slug, s in C.SERVICES.items():
        inc = "".join(f"<li>{E(x)}</li>" for x in s["included"])
        cases = "".join(rcard(BY[k], i + 1) for i, k in enumerate(s["cases"]))
        others = "".join(f'<a class="ulink" href="{href("/services/" + k + "/")}">{v["name"]} →</a>' for k, v in C.SERVICES.items() if k != slug)
        others += "".join(f'<a class="ulink" href="{href(h)}">{E(n)} →</a>' for h, n in C.SERVICE_MORE.get(slug, []))
        body = f'''
<section class="phero"><div class="wrap">{crumbs(("/services/", "Services"), ("", s["name"]))}<span class="lab kw">{E(s["kw"])}</span>
  <h1 class="h-page" data-split>{it(s["h1"])}</h1>
  <p class="lede" data-rise>{E(s["intro"])}</p>
  <div class="ctas" data-rise><a class="btn" href="#contact" data-magnetic>Let's talk</a><a class="btn ghost" href="{href('/work/')}" data-magnetic>See the work</a></div>
</div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap"><div class="formgrid"><div class="intro"><span class="lab">What you get</span><h2 class="h2" data-split>Everything it needs. <em>Nothing it doesn't.</em></h2></div><ul class="checks" style="grid-column:7/span 6" data-stagger>{inc}</ul></div></div></section>
<section class="sec dark" data-dark><div class="wrap">{sh("How it works", "Four steps. *No surprises.*")}{method(C.METHOD)}</div></section>
<section class="sec"><div class="wrap">{sh("Proof", "Work like this. *For real clients.*")}<div class="wgrid">{cases}</div></div></section>
<section class="sec tight"><div class="wrap">{sh("Questions", "Straight *answers.*")}{faq(s["faq"])}<div class="ctas" style="margin-top:48px;gap:28px">{others}</div></div></section>
{final()}'''
        page(f"/services/{slug}/", s["title"], s["desc"], body, active="/services/",
             schema=[bc(("/services/", "Services"), (f"/services/{slug}/", s["name"])), faq_schema(s["faq"]),
                     {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "provider": {"@type": "Organization", "name": "The Mago Labs"}}])

def build_industries():
    cards = industry_cards()
    body = f'''<section class="phero"><div class="wrap">{crumbs(("", "Industries"))}<span class="lab kw">Websites by industry</span><h1 class="h-page" data-split>For businesses that <em>live on enquiries.</em></h1>
<p class="lede" data-rise>Contractors, clinics, firms, manufacturers, agents and online stores. Different buyers, same goal: more calls.</p></div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap"><div class="grid3" data-stagger>{cards}</div></div></section>{trades_section(" stone")}{final()}'''
    page("/industries/", "Website Design by Industry", "Custom websites for contractors and trades, clinics, professional firms, manufacturers, real estate agents and online stores.", body, schema=[bc(("/industries/", "Industries"))])
    for k, v in C.INDUSTRIES.items():
        pts = "".join(f'<div class="col"><h3 class="h3">{E(a)}</h3><p>{E(b)}</p></div>' for a, b in v["points"])
        cases = "".join(rcard(BY[x], i + 1) for i, x in enumerate(v["cases"]))
        tq = [t for t in TESTIMONIALS if t["case"] in v["cases"]][:3]
        qs = f'<section class="sec light"><div class="wrap">{sh("Reviews", "From clients *in your field.*")}<div class="qgrid" data-stagger>{"".join(quote(t, True) for t in tq)}</div></div></section>' if tq else ""
        extra = f'''<section class="sec space" data-dark style="padding-bottom:110px"><div class="wrap">{sh("From the lab · Concept builds", "More trade sites *we've designed.*")}{CNOTE}</div>{wall()}</section>''' if k == "home-services" else ""
        body = f'''
<section class="phero"><div class="wrap">{crumbs(("/industries/", "Industries"), ("", v["name"]))}<span class="lab kw">{E(v["kw"])}</span><h1 class="h-page" data-split>{it(v["h1"])}</h1><p class="lede" data-rise>{E(v["intro"])}</p>
<div class="ctas" data-rise><a class="btn" href="#contact" data-magnetic>Let's talk</a></div></div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap"><div class="grid3" data-stagger>{pts}</div></div></section>
<section class="sec stone"><div class="wrap">{sh("Live client work", "Built for businesses *like yours.*")}<div class="wgrid">{cases}</div></div></section>
{extra}{qs}{final()}'''
        page(f"/industries/{k}/", v["title"], v["desc"], body, schema=[bc(("/industries/", "Industries"), (f"/industries/{k}/", v["name"]))])

def build_pricing():
    plans = "".join(f'''<div class="plan{' pop' if p['pop'] else ''}"><div class="tag"><span>Live in {p['days']}</span>{'<b>Most chosen</b>' if p['pop'] else ''}</div><h3>{p['name']}</h3>
<div class="price"><small>From</small>${p['price']}</div><p class="for">{E(p['for_'])}</p><ul>{"".join(f"<li>{E(x)}</li>" for x in p['items'])}</ul><a class="btn" href="#contact">Let's talk</a></div>''' for p in PLANS)
    fq = [("Are there monthly fees?", "No. You pay once. Hosting is included for life for standard business websites, under fair use."),
          ("How do payments work?", "Half to start, half at launch."),
          ("What happens after year one?", "Leave it running at no cost, send changes at $30 an hour, or edit it yourself for free."),
          ("Can the price change?", "No. The quote is fixed and in writing before we start."),
          ("Who owns it?", "You. Domain in your name, code in your hands.")]
    body = f'''
<section class="phero"><div class="wrap">{crumbs(("", "Pricing"))}<h1 class="h-page" data-split>Pay once. <em>Own it.</em></h1>
<p class="lede" data-rise>Four fixed packages. No monthly rent on your own website. A year of changes on us.</p></div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap"><div class="plans" data-stagger>{plans}</div>
<p class="muted" style="margin-top:20px;font-size:14.5px">Prices in USD. Every project gets a fixed written quote first. Add-ons: ongoing SEO, Google Business Profile, copywriting, social media and paid ads.</p></div></section>
<section class="sec stone"><div class="wrap"><div class="facts" data-stagger>
  <div class="fact ink"><span class="lab">Hosting</span><span class="big">$0<span style="font-size:.4em">/mo</span></span><p>Included for life. Fair use.</p></div>
  <div class="fact"><span class="lab">Ownership</span><span class="big">100%</span><p>Domain and code in your name.</p></div>
  <div class="fact"><span class="lab">Support</span><span class="big">1 yr</span><p>Changes and fixes on us for the first year.</p></div></div></div></section>
<section class="sec tight"><div class="wrap">{sh("Questions", "About *the money.*")}{faq(fq)}</div></section>
{final("Not sure which *package fits?*", "Start with a free audit. We'll tell you what your site needs and quote it exactly. No obligation.")}'''
    offers = [{"@type": "Offer", "name": p["name"], "price": p["price"].replace(",", ""), "priceCurrency": "USD"} for p in PLANS]
    page("/pricing/", "Website Pricing: Pay Once, From $999", "Four fixed website packages from $999. Pay once, no monthly fees, hosting included, you own everything. Live in 5 to 28 days.",
         body, active="/pricing/", schema=[bc(("/pricing/", "Pricing")), faq_schema(fq), {"@context": "https://schema.org", "@type": "Service", "name": "Custom websites", "provider": {"@type": "Organization", "name": "The Mago Labs"}, "offers": offers}])

def build_process():
    body = f'''<section class="phero"><div class="wrap">{crumbs(("", "Process"))}<h1 class="h-page" data-split>Four steps. <em>Live in weeks.</em></h1>
<p class="lede" data-rise>You keep running your business. We handle the rest, and you see everything before it goes live.</p></div></section>
<section class="sec dark" data-dark><div class="wrap">{method(C.METHOD)}</div></section>
<section class="sec"><div class="wrap">{sh("What we need from you", "Almost *nothing.*")}<div class="grid3" data-stagger>
<div class="col"><span class="num">01</span><h3 class="h3">Five minutes.</h3><p>A quick chat about your business and who you sell to.</p></div>
<div class="col"><span class="num">02</span><h3 class="h3">Your photos.</h3><p>Real work, real team, real premises. Your Instagram is often enough.</p></div>
<div class="col"><span class="num">03</span><h3 class="h3">Your opinion.</h3><p>Two rounds of changes are included. Tell us what you think.</p></div></div></div></section>{final()}'''
    page("/process/", "How We Work", "From your numbers to launch in 5 to 28 days. Fixed quote, design approval before build, a year of support.", body, schema=[bc(("/process/", "Process"))])

def build_about():
    ch = "".join(f'<div class="chap" data-rise><span class="lab">{E(a)}</span><p>{it(b)}</p></div>' for a, b in C.ABOUT)
    body = f'''<section class="phero"><div class="wrap">{crumbs(("", "About"))}<h1 class="h-page" data-split>Led by the founder. <em>Obsessed with results.</em></h1>
<p class="lede" data-rise>The Mago Labs is a small studio led by its founder, Burhan Kapasi. You talk to the person doing the work, from the first message to launch day and after.</p></div></section>
<section class="sec tight" style="padding-top:0"><div class="wrap"><div class="about"><div class="pic" data-clip><img src="{asset('/assets/img/burhan-sofa.webp')}" alt="Burhan Kapasi, founder of The Mago Labs, smiling in an armchair" width="768" height="878" loading="lazy"></div>
<div class="story">{ch}<div class="ctas" data-rise><a class="btn" href="#contact" data-magnetic>Let's talk</a><a class="btn ghost" href="{SITE['linkedin']}" rel="noopener" data-magnetic>Burhan on LinkedIn</a></div><div class="partner" data-rise><span class="lab">Co-Founder</span><p class="pn"><b>Priyanka</b> · Co-Founder and Head of International Relations</p><p>Burhan builds the websites. Priyanka makes sure our clients overseas are looked after, from the first hello to launch day.</p><div class="pc"><a class="btn" href="https://wa.me/917420819299?text=Hi%20Priyanka%2C%20I%20found%20The%20Mago%20Labs%20and%20would%20like%20to%20talk%20about%20a%20website." data-magnetic>{WA_SVG}WhatsApp Priyanka</a><a class="btn ghost" href="tel:+917420819299" data-magnetic><svg class="btn-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true"><path d="M5 3.5h3.6l1.9 4.8-2.6 1.7a11 11 0 0 0 6.1 6.1l1.7-2.6 4.8 1.9v3.6a1.8 1.8 0 0 1-1.8 1.8A16.7 16.7 0 0 1 3.2 5.3 1.8 1.8 0 0 1 5 3.5z"/></svg>+91 74208 19299</a><a class="btn ghost" href="mailto:priyanka@themagolabs.com" data-magnetic><svg class="btn-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true"><rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 7 9-7"/></svg>Email Priyanka</a></div></div></div></div></div></section>
<section class="sec dark" data-dark><div class="wrap">{sh("Three rules", "How we *work.*")}<div class="grid3" data-stagger>
<div class="col"><span class="num">01</span><h3 class="h3">Outcome first.</h3><p>A website is judged by the calls, bookings and jobs it brings in.</p></div>
<div class="col"><span class="num">02</span><h3 class="h3">Numbers beat adjectives.</h3><p>We measure before and after, and we show you. Ours too.</p></div>
<div class="col"><span class="num">03</span><h3 class="h3">Yours to keep.</h3><p>No contracts that trap you, no monthly rent, no hostage domains.</p></div></div></div></section>{final()}'''
    page("/about/", "About The Mago Labs", "A website studio led by its founder. Burhan Kapasi designs and builds websites that bring in calls, bookings and jobs.", body, active="/about/",
         schema=[bc(("/about/", "About")), {"@context": "https://schema.org", "@type": "Person", "name": SITE["founder"], "jobTitle": "Founder", "worksFor": {"@type": "Organization", "name": "The Mago Labs"}, "sameAs": [SITE["linkedin"]]}])

def build_forms():
    body = f'''<section class="phero"><div class="wrap">{crumbs(("", "Free site audit"))}<div class="formgrid solo"><div class="intro">
<h1 class="h-page" data-split style="font-size:clamp(44px,6vw,104px)">Where is your site <em>losing customers?</em></h1>
<p class="lede" data-rise>We go through your website the way a customer does: on a phone, in a hurry. You get a short, plain English list of what's costing you enquiries and what to fix first.</p>
<ul class="checks" data-stagger><li>Free. No strings.</li><li>A reply within one business day</li><li>No site yet? A free working preview in 48 hours</li></ul></div></div></div></section>{contact("Tell us about *your site.*")}'''
    page("/free-audit/", "Free Website Audit", "Find out exactly where your website loses customers. A free, plain English audit from The Mago Labs.", body)
    body = f'''<section class="phero"><div class="wrap">{crumbs(("", "Contact"))}<div class="formgrid solo"><div class="intro">
<h1 class="h-page" data-split style="font-size:clamp(44px,6vw,104px)">Let's talk about <em>your website.</em></h1>
<p class="lede" data-rise>You talk directly to Burhan, the founder. Answer six quick questions below, or email or WhatsApp him directly.</p>
<ul class="checks" data-stagger><li><span>WhatsApp: <a class="ulink" href="{WA}">{SITE['whatsapp_display']}</a></span></li><li><span>Email: <a class="ulink" href="mailto:{SITE['email']}">{SITE['email']}</a></span></li><li><span>Working with businesses in India, Australia, the USA, the UK and Canada</span></li><li><span>International enquiries: Priyanka, <span style="white-space:nowrap">Co-Founder</span>. <a class="ulink" href="mailto:priyanka@themagolabs.com">priyanka@themagolabs.com</a> · <a class="ulink" href="tel:+917420819299">+91 74208 19299</a> (call or <a class="ulink" href="https://wa.me/917420819299">WhatsApp</a>)</span></li></ul></div></div></div></section>{contact("Six quick questions. *Then we talk.*")}'''
    page("/contact/", "Contact", "Talk directly to the founder of The Mago Labs on WhatsApp or email. Reply within one business day.", body, schema=[bc(("/contact/", "Contact"))])
    body = f'''<section class="phero space" data-dark style="min-height:80vh"><div class="wrap"><span class="dot" style="width:18px;height:18px"></span>
<h1 class="h-page" data-split style="margin-top:28px">Got it. <em>You've landed.</em></h1>
<p class="lede" data-rise style="color:#DAD8D0">Burhan will look at your business and reply within one business day. If you asked for a preview, you'll see it within 48 hours.</p>
<div class="ctas" data-rise><a class="btn inv" href="{href('/work/')}" data-magnetic>See the work while you wait</a><a class="btn ghost" href="{WA}">WhatsApp</a></div></div></section>
<script>window.dataLayer=window.dataLayer||[];dataLayer.push({{event:"conversion_thank_you"}});</script>'''
    page("/thank-you/", "Thank You", "Thanks for getting in touch.", body, noindex=True)

def build_options():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import opts
    opts.build(globals())

def build_legal():
    pv = f'''<p class="note">Plain English draft. Have it checked against the laws where you sell before launch.</p><h2>What we collect</h2><p>When you use a form or message us: your name, business, email, phone, website address and message.</p>
<h2>How we use it</h2><p>Only to reply, prepare your audit or quote, and do the work you ask for. We never sell your details.</p><h2>Analytics</h2><p>We may use analytics to see which pages help. Where the law requires it, we ask first.</p>
<h2>Your rights</h2><p>Ask to see, correct or delete your details any time: <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>'''
    tm = f'''<p class="note">Plain English draft. Have it checked by a lawyer before launch.</p><h2>Quotes and payment</h2><p>Every project starts with a fixed written quote. Payment is half to start and half at launch.</p>
<h2>Ownership</h2><p>Once paid in full, you own the design, content and code. Your domain is registered in your name.</p><h2>Changes and support</h2><p>Two rounds of revisions and one year of free support for small changes. After that, changes are quoted when you ask for them, or you can edit the site yourself.</p>
<h2>Hosting</h2><p>Included for standard business websites under fair use. Unusual traffic or storage may need a paid plan, always agreed first.</p><h2>Contact</h2><p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>'''
    for p, t, h, x in [("/privacy/", "Privacy Policy", "Privacy", pv), ("/terms/", "Terms of Service", "Terms", tm)]:
        page(p, t, f"{t} for The Mago Labs.", f'<section class="phero"><div class="wrap">{crumbs(("", h))}<h1 class="h-page" data-split>{h}<em>.</em></h1><div class="legal" style="margin-top:48px">{x}</div></div></section>')
    page("/404", "Lost in space", "This page does not exist.", f'''<section class="phero space" data-dark style="min-height:90vh"><div class="wrap"><span class="lab">Error 404</span>
<h1 class="h-page" data-split style="margin-top:24px">Lost <em>in space.</em></h1><p class="lede" data-rise style="color:#DAD8D0">This page drifted out of orbit. Let's get you back.</p>
<div class="ctas" data-rise><a class="btn inv" href="{href('/')}">Back to home</a><a class="btn ghost" href="{href('/work/')}">See the work</a></div></div></section>''', noindex=True)

# ================= RUN =================
os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
for n in os.listdir(os.path.join(ROOT, OUT)):
    q = os.path.join(ROOT, OUT, n); shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)
shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(ROOT, OUT, "assets"),
                ignore=shutil.ignore_patterns("vendor") if MODE == "preview" else None)
for b in [build_home, build_work, build_cases, build_concepts, build_testimonials, build_services, build_industries, lambda: TR.build_all(globals()), build_process, build_about, build_forms, build_legal]:
    b()
png = os.path.join(BRAND, "png")
shutil.copy(os.path.join(ROOT, "src", "favicon.ico"), os.path.join(ROOT, OUT, "favicon.ico"))  # transparent mark, no box
shutil.copy(os.path.join(ROOT, "src", "favicon.svg"), os.path.join(ROOT, OUT, "favicon.svg"))  # switches colour for dark tabs
shutil.copy(os.path.join(png, "apple-touch-icon.png"), os.path.join(ROOT, OUT, "apple-touch-icon.png"))
shutil.copy(os.path.join(png, "lockup-ink-2000.png"), os.path.join(ROOT, OUT, "assets", "logo.png"))
shutil.copy(os.path.join(ROOT, "src", "og.png"), os.path.join(ROOT, OUT, "assets", "og.png"))
if MODE != "preview":
    open(os.path.join(ROOT, OUT, "assets", "site.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(ROOT, OUT, "assets", "site.js"), "w", encoding="utf-8").write(JS)
    urls = [p for p, ni in PAGES if not ni]
    open(os.path.join(ROOT, OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "\n".join(f"  <url><loc>{abs_url(p)}</loc><lastmod>{TODAY}</lastmod></url>" for p in urls) + "\n</urlset>\n")
    open(os.path.join(ROOT, OUT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    open(os.path.join(ROOT, OUT, "vercel.json"), "w", encoding="utf-8").write(json.dumps({"cleanUrls": True, "trailingSlash": True, "headers": [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]}, indent=2))
print(MODE, "pages:", len(PAGES))
