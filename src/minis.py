"""Mini visuals for card sections (option A).

Every <div|a class="col"> card in a .grid3 gets a small illustration above its heading,
chosen by the heading text. Real material where it exists: client site screenshots,
concept-site posters and the brand-kit icons. Used by build.py on every page it writes.
"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# brand-kit icons, stroke switched to currentColor so they follow the card's text colour
ICONS = {
    "call": '<path d="M5 3.5h3.6l1.9 4.8-2.6 1.7a11 11 0 0 0 6.1 6.1l1.7-2.6 4.8 1.9v3.6a1.8 1.8 0 0 1-1.8 1.8A16.7 16.7 0 0 1 3.2 5.3 1.8 1.8 0 0 1 5 3.5z"/>',
}

def _ic(name, cls="mv-ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" aria-hidden="true">{ICONS[name]}</svg>'

def _img(src, cls=""):
    return f'<img class="{cls}" src="{src}" alt="" loading="lazy" decoding="async">'

P = "/assets/concepts/poster/"
W = "/assets/work/"

def _photos():
    return ('<div class="mv mv-photos">' + "".join(_img(P + n + ".webp") for n in ("cnbconcreting", "canfieldconcrete", "rteearthmoving")) + '</div>')

def _buttons():
    return (f'<div class="mv mv-dark mv-buttons"><span class="pill solid">{_ic("call")}Call now</span><span class="pill line">Get a quote</span></div>')

def _map(label="Your service area"):
    return f'<div class="mv mv-map"><i class="ring r2"></i><i class="ring"></i><i class="pin"></i><span class="cap">{label}</span></div>'

def _booking():
    days = "".join(f'<span class="d{" on" if i == 2 else ""}"><b>{d}</b>{n}</span>' for i, (d, n) in enumerate([("Mon", 12), ("Tue", 13), ("Wed", 14), ("Thu", 15)]))
    return f'<div class="mv mv-booking"><div class="days">{days}</div><div class="slot"><i></i>10:30 · Booked</div></div>'

def _reviews():
    return '<div class="mv mv-reviews"><div class="score">5.0<span>★★★★★</span></div><div class="mv-lines"><i></i><i></i><i class="s"></i></div></div>'

def _credential():
    return '<div class="mv mv-cred"><div class="seal"><span>Est.</span>Qualified</div><div class="mv-lines"><i></i><i></i><i class="s"></i></div></div>'

def _list():
    rows = "".join(f'<span><i></i>{t}<b>→</b></span>' for t in ("Audit and assurance", "Tax planning", "Advisory"))
    return f'<div class="mv mv-list">{rows}</div>'

def _form():
    return '<div class="mv mv-form"><span class="f"></span><span class="f"></span><span class="send">Send enquiry</span></div>'

def _ticket():
    return '<div class="mv mv-dark mv-ticket"><span class="from">25</span><span class="arr">→</span><span class="to">58<i></i></span><span class="cap">Patients a day · 2 months after launch</span></div>'

def _chart():
    bars = "".join(f'<i style="height:{h}%"></i>' for h in (22, 30, 41, 55, 72, 92))
    return f'<div class="mv mv-chart"><div class="bars">{bars}<b></b></div><span class="cap">Before → after, measured</span></div>'

def _domain():
    return '<div class="mv mv-domain"><span class="url"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="5" y="10" width="14" height="10"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>yourbusiness.com</span><span class="cap">Domain and code in your name</span></div>'

def _clock(txt, cap):
    return f'<div class="mv mv-dark mv-clock"><span class="big">{txt}</span><span class="cap">{cap}</span></div>'

def _phone_grid():
    tiles = "".join(_img(P + n + ".webp") for n in ("kittcrete", "aceroofing", "gblandscaping", "lgndconcrete", "dandnconcreting", "viproofing"))
    return f'<div class="mv mv-phone"><div class="screen">{tiles}</div></div>'

def _chat():
    return '<div class="mv mv-chat"><span class="b them">Can the logo be bigger?</span><span class="b us">Done. Take a look.</span></div>'

def _poster_quote():
    return f'<div class="mv mv-pq">{_img(P + "njcivilgroup.webp")}<span class="mv-quote">“Their own photos, services and reviews.”</span></div>'

def _variety():
    return '<div class="mv mv-variety">' + "".join(_img(P + n + ".webp") for n in ("schellshock", "empireglassinc", "handydandys")) + '</div>'

def _shot(src):
    return f'<div class="mv mv-shot">{_img(src)}</div>'

def _listing():
    return '<div class="mv mv-listing"><div class="card"><span class="ph"></span><span class="t">3 bed · 2 bath</span><span class="pill"><i></i>Viewing Sat 11:00</span></div></div>'

def _store():
    return f'<div class="mv mv-shot">{_img(W + "momrise-card.webp")}</div>'

KIND = {
    # industry page points
    "Real work": _photos, "One tap away": _buttons, "On the map": _map,
    "Booking first": _booking, "Trust in seconds": _reviews, "Found nearby": lambda: _map("Patients nearby"),
    "Credibility": _credential, "Clarity": _list, "Enquiries": _form,
    # about: how we work
    "Outcome first.": _ticket, "Numbers beat adjectives.": _chart, "Yours to keep.": _domain,
    # process: what we need
    "Five minutes.": lambda: _clock("5 min", "One quick chat"), "Your photos.": _phone_grid, "Your opinion.": _chat,
    # concepts: why concepts
    "Real work, real words.": _poster_quote, "Zero repeats.": _variety, "Yours in 48 hours.": lambda: _clock("48h", "Your preview, free"),
    # industry overview cards: real client sites
    "Contractors and trades": lambda: _shot(W + "jaymocivil-hero-640.webp"),
    "Clinics and healthcare": lambda: _shot(W + "drmihirshah-hero-640.webp"),
    "Professional services": lambda: _shot(W + "darshangalani-hero-640.webp"),
    "Manufacturers and B2B": lambda: _shot(W + "prabhakarprocessors-hero-640.webp"),
    "Real estate": _listing,
    "Online stores": _store,
}

_CARD = re.compile(r'(<(?:div|a) class="col[^"]*"[^>]*>)((?:(?!</?(?:div|a)\b).)*?)(<h3 class="h3">)(.*?)(</h3>)', re.S)

def minis(doc):
    """Insert the matching mini visual at the top of each column card that doesn't have one yet."""
    def sub(m):
        title = re.sub(r"<[^>]+>", "", m.group(4)).replace("&#x27;", "'").strip()
        fn = KIND.get(title)
        if not fn or 'class="mv' in m.group(2):
            return m.group(0)
        return m.group(1) + fn() + m.group(2) + m.group(3) + m.group(4) + m.group(5)
    return _CARD.sub(sub, doc)
