/* The Mago Labs v3 motion. Uses GSAP + ScrollTrigger + Lenis when present.
   Every effect is optional: without JS, or with reduced motion, the page is complete and static. */
(function () {
  var cfg = window.MAGO || {};
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  var G = window.gsap, ST = window.ScrollTrigger;
  var motion = !reduce && G && ST;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  window.dataLayer = window.dataLayer || [];
  function track(n, p) { try { dataLayer.push(Object.assign({ event: n }, p || {})); } catch (e) {} }
  if (motion) G.registerPlugin(ST);

  /* ---------- smooth scroll ---------- */
  var lenis = null;
  if (motion && window.Lenis && fine) {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true }); window.MAGO_LENIS = lenis;
    lenis.on('scroll', ST.update);
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
  }

  /* ---------- word splitting ---------- */
  function split(el) {
    if (el.dataset.done) return el.querySelectorAll('.w > span');
    el.dataset.done = 1;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span'); w.className = 'w';
            var i = document.createElement('span'); i.textContent = part;
            w.appendChild(i); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && !n.classList.contains('dot') && !n.classList.contains('w')) {
          if (n.tagName === 'EM') { var w = document.createElement('span'); w.className = 'w'; n.parentNode.insertBefore(w, n); var i = document.createElement('span'); w.appendChild(i); i.appendChild(n); }
          else walk(n);
        }
      });
    })(el);
    return el.querySelectorAll('.w > span');
  }

  /* ---------- loader (once per session, home only) ---------- */
  var loader = $('.loader');
  function intro(done) {
    var seen = false; try { seen = sessionStorage.getItem('mago-intro'); } catch (e) {}
    if (!loader || !motion || seen) { done(); return; }
    try { sessionStorage.setItem('mago-intro', '1'); } catch (e) {}
    loader.classList.add('on');
    var safety = setTimeout(function () { loader.style.display = 'none'; done(); done = function () {}; }, 4200);
    var path = $('.loader .m'), dotEl = $('.loader .ld'), count = $('.loader .count');
    var len = path.getTotalLength();
    G.set(path, { strokeDasharray: len, strokeDashoffset: len, fill: 'transparent' });
    G.set(dotEl, { attr: { cx: 60, cy: 40 }, opacity: 0 });
    var o = { v: 0 };
    var tl = G.timeline({ onComplete: function () { clearTimeout(safety); done(); } });
    tl.to(o, { v: 100, duration: 1.4, ease: 'power2.inOut', onUpdate: function () { count.textContent = String(Math.round(o.v)).padStart(3, '0'); } }, 0)
      .to(path, { strokeDashoffset: 0, duration: 1.1, ease: 'power2.inOut' }, 0)
      .to(path, { fill: '#F2F1EC', duration: .35 }, 1.0)
      .to(dotEl, { opacity: 1, attr: { cx: 124, cy: 11 }, duration: .55, ease: 'back.out(2)' }, 1.05)
      .to(loader, { yPercent: -100, duration: .9, ease: 'power4.inOut' }, 1.75)
      .set(loader, { display: 'none' });
  }

  /* ---------- page transitions ---------- */
  var curtain = $('.curtain');
  if (motion && curtain) {
    /* reveal runs as a CSS animation so it never depends on the JS frame loop */
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      var h = a.getAttribute('href') || '';
      if (a.target === '_blank' || a.hasAttribute('download') || /^(https?:|mailto:|tel:|#)/.test(h) || a.closest('form')) return;
      e.preventDefault();
      var go = function () { location.href = a.href; };
      curtain.classList.add('cover');
      setTimeout(go, 560);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) { curtain.classList.remove('cover'); } });
  }

  /* ---------- header: colour over dark sections, hide on scroll down ---------- */
  var hdr = $('.hdr'), last = 0;
  function hdrUpdate() {
    var y = window.scrollY;
    hdr.classList.toggle('solid', y > 40);
    hdr.classList.toggle('hide', y > 500 && y > last && !document.body.classList.contains('menu-open'));
    last = y;
    var probe = 40, dark = false;
    $$('[data-dark]').forEach(function (s) { var r = s.getBoundingClientRect(); if (r.top <= probe && r.bottom > probe) dark = true; });
    hdr.classList.toggle('on-dark', dark);
    var mcta = $('.mcta'); if (mcta) mcta.classList.toggle('on', y > innerHeight * .8);
  }
  addEventListener('scroll', hdrUpdate, { passive: true }); hdrUpdate();

  /* ---------- mobile menu ---------- */
  var mbtn = $('.menu-btn.open'), mnav = $('#mnav');
  function setMenu(open) {
    mnav.hidden = !open; mbtn.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('menu-open', open);
    if (lenis) open ? lenis.stop() : lenis.start();
    document.documentElement.style.overflow = open ? 'hidden' : '';
    if (open) {
      var c = $('.close', mnav); c.focus();
      if (motion) G.from($$('li a', mnav), { yPercent: 60, opacity: 0, stagger: .05, duration: .6, ease: 'power3.out' });
    } else mbtn.focus();
  }
  if (mbtn && mnav) {
    mbtn.addEventListener('click', function () { setMenu(true); });
    $('.close', mnav).addEventListener('click', function () { setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !mnav.hidden) setMenu(false); });
    mnav.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var els = $$('a,button', mnav), f = els[0], l = els[els.length - 1];
      if (e.shiftKey && document.activeElement === f) { e.preventDefault(); l.focus(); }
      else if (!e.shiftKey && document.activeElement === l) { e.preventDefault(); f.focus(); }
    });
  }

  /* ---------- custom cursor + magnetic ---------- */
  if (fine && !reduce) {
    var cur = document.createElement('div'); cur.className = 'cursor'; cur.innerHTML = '<span></span>';
    document.body.appendChild(cur);
    var lab = cur.firstChild, mx = -100, my = -100, cx = -100, cy = -100;
    addEventListener('pointermove', function (e) { mx = e.clientX; my = e.clientY; cur.classList.add('ready'); }, { passive: true });
    (function loop() { cx += (mx - cx) * .2; cy += (my - cy) * .2; cur.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)'; requestAnimationFrame(loop); })();
    document.addEventListener('pointerover', function (e) {
      var t = e.target.closest && e.target.closest('[data-cursor]');
      if (t) { lab.textContent = t.getAttribute('data-cursor'); cur.classList.add('big'); }
      else if (e.target.closest && e.target.closest('a,button,input,textarea,summary,label')) { cur.classList.remove('big'); cur.classList.add('hide'); }
      else { cur.classList.remove('big', 'hide'); }
    });
    document.addEventListener('pointerleave', function () { cur.classList.remove('ready'); });
    if (G) $$('[data-magnetic]').forEach(function (b) {
      b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); G.to(b, { x: (e.clientX - r.left - r.width / 2) * .3, y: (e.clientY - r.top - r.height / 2) * .35, duration: .4, ease: 'power3.out' }); });
      b.addEventListener('pointerleave', function () { G.to(b, { x: 0, y: 0, duration: .7, ease: 'elastic.out(1,.4)' }); });
    });
  }

  /* ---------- videos: start after load, pause when hidden, still frame for reduced motion ---------- */
  var av1 = (function () { try { return document.createElement('video').canPlayType('video/mp4; codecs="av01.0.08M.10"') === 'probably'; } catch (e) { return false; } })();
  $$('video[data-src]').forEach(function (v) {
    if (reduce) return;
    var small = matchMedia('(max-width: 760px)').matches;
    var src = small && v.dataset.srcMobile ? v.dataset.srcMobile : v.dataset.src;
    if (av1) src = src.replace(/\.mp4$/, '-av1.mp4');
    var start = function () {
      v.muted = true; v.defaultMuted = true; v.playsInline = true;
      v.setAttribute('muted', ''); v.setAttribute('playsinline', ''); v.setAttribute('webkit-playsinline', '');
      v.src = src; v.load();
      v.addEventListener('playing', function () { v.style.opacity = 1; }, { once: true });
      var visible = false, armed = false;
      var EV = ['touchstart', 'pointerdown', 'scroll', 'keydown'];
      var go = function () { if (!visible) return; var pr = v.play(); if (pr && pr.catch) pr.catch(arm); };
      /* phones in low-power or data-saver mode refuse autoplay: start on the first touch or scroll instead */
      var once = function () { EV.forEach(function (e) { window['remove' + 'EventListener'](e, once, true); }); armed = false; go(); };
      function arm() { if (armed) return; armed = true; EV.forEach(function (e) { addEventListener(e, once, { capture: true, passive: true }); }); }
      var io = new IntersectionObserver(function (es) { es.forEach(function (en) { visible = en.isIntersecting; if (visible) go(); else v.pause(); }); });
      io.observe(v);
      document.addEventListener('visibilitychange', function () { if (!document.hidden) go(); });
    };
    if (document.readyState === 'complete') setTimeout(start, 200); else addEventListener('load', function () { setTimeout(start, 200); });
  });

  /* ---------- forms ---------- */
  $$('form[data-form]').forEach(function (form) {
    var urlField = $('[data-url-field]', form);
    function sync() { var v = $('input[name="has_site"]:checked', form); if (urlField) urlField.hidden = v && v.value === 'no'; }
    $$('input[name="has_site"]', form).forEach(function (s) { s.addEventListener('change', sync); }); sync();
    form.addEventListener('submit', function (e) {
      e.preventDefault(); var ok = true;
      $$('[data-req]', form).forEach(function (inp) {
        var w = inp.closest('.field'); if (w.closest('[hidden]')) { w.classList.remove('invalid'); return; }
        var v = inp.value.trim(), bad = !v; if (!bad && inp.type === 'email') bad = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
        w.classList.toggle('invalid', bad); if (bad && ok) { inp.focus(); ok = false; }
      });
      if (!ok) return;
      var d = {}; new FormData(form).forEach(function (v, k) { d[k] = v; }); d.form = form.dataset.form; d.page = location.pathname;
      track('generate_lead', { form: d.form });
      var btn = $('button[type="submit"]', form); btn.disabled = true; btn.lastChild.textContent = 'Sending...';
      function fallback() {
        var lines = ['Hi Burhan, ' + (d.form === 'audit' ? 'I would like a free site audit.' : 'I would like to talk about a website.')];
        ['name', 'business', 'website', 'email', 'phone'].forEach(function (k) { if (d[k]) lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ': ' + d[k]); });
        if (d.message) lines.push(d.message);
        var p = $('.sent', form); $('a.btn', p).href = 'https://wa.me/' + cfg.whatsapp + '?text=' + encodeURIComponent(lines.join('\n'));
        p.hidden = false; btn.hidden = true; $('a.btn', p).focus();
      }
      if (cfg.formEndpoint) fetch(cfg.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { r.ok ? (location.href = form.dataset.next) : fallback(); }).catch(fallback);
      else fallback();
    });
  });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a'); if (!a) return; var h = a.getAttribute('href') || '';
    if (h.indexOf('mailto:') === 0) track('email_click'); else if (h.indexOf('wa.me') > -1) track('whatsapp_click');
    else if (a.dataset.live) track('live_site_click', { site: a.dataset.live });
  });

  /* ---------- filters ---------- */
  $$('.filters button').forEach(function (b, _, all) {
    b.addEventListener('click', function () {
      var f = b.dataset.f; all.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      $$('[data-cat]').forEach(function (c) { c.hidden = !(f === 'all' || c.dataset.cat === f); });
      if (ST) ST.refresh();
    });
  });

  /* ---------- concept phones: load long image on first hover ---------- */
  $$('.phone[data-long]').forEach(function (p) {
    function load() { if (p.dataset.l || reduce) return; p.dataset.l = 1; var i = new Image(); i.className = 'long'; i.alt = ''; i.src = p.dataset.long; $('.scr', p).appendChild(i); }
    p.addEventListener('pointerenter', load); p.addEventListener('focus', load);
  });

  /* ---------- drag to scroll ---------- */
  $$('[data-drag]').forEach(function (row) {
    var down = false, sx = 0, sl = 0, moved = 0;
    row.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = 0; sx = e.clientX; sl = row.scrollLeft; });
    addEventListener('pointermove', function (e) { if (!down) return; var dx = e.clientX - sx; moved = Math.abs(dx); if (moved > 4) row.classList.add('dragging'); row.scrollLeft = sl - dx; });
    addEventListener('pointerup', function () { if (!down) return; down = false; setTimeout(function () { row.classList.remove('dragging'); }, 0); });
  });

  /* client index: screenshot follows the cursor and swaps per row */
  $$('[data-index]').forEach(function (idx) {
    var pv = $('.ipreview', idx); if (!pv || !fine) return;
    var imgs = {}, cur = null, x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y, s = .7, ts = .7;
    $$('.irow', idx).forEach(function (r) {
      var src = r.dataset.img, im = new Image(); im.src = src; im.alt = ''; $('.pf', pv).appendChild(im); imgs[src] = im;
      r.addEventListener('pointerenter', function () {
        if (cur) cur.classList.toggle('cur', false);
        cur = imgs[src]; cur.classList.toggle('cur', true);
        $('.tag', pv).textContent = r.dataset.tag; pv.classList.toggle('on', true); ts = 1;
      });
    });
    idx.addEventListener('pointerleave', function () { pv.classList.toggle('on', false); ts = .7; });
    addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    (function loop() {
      var dx = tx - x; x += dx * .12; y += (ty - y) * .12; s += (ts - s) * .12;
      var rot = reduce ? 0 : Math.max(-8, Math.min(8, dx * .04));
      pv.style.transform = 'translate(' + (x + 40) + 'px,' + (y - 20) + 'px) translate(0,-50%) rotate(' + rot + 'deg) scale(' + s + ')';
      requestAnimationFrame(loop);
    })();
  });

  if (!motion) { document.documentElement.classList.add('static'); return; }

  /* ================== GSAP SCENES ================== */
  function scenes() {
    if (window.MAGO_ORBIT) window.MAGO_ORBIT(G, ST);
    /* hero: kinetic headline, then video shrinks into a card as you scroll */
    var hero = $('.hero');
    if (hero) {
      var words = split($('.hero h1'));
      var tl = G.timeline({ delay: .1 });
      tl.from(words, { yPercent: 115, rotate: 4, duration: 1.2, stagger: .07, ease: 'power4.out' })
        .from('.hero .row > *, .hud', { y: 24, opacity: 0, duration: .9, stagger: .08, ease: 'power3.out' }, '-=.8')
        .from('.hero .media', { scale: 1.15, duration: 2.2, ease: 'power3.out' }, 0);
      G.timeline({ scrollTrigger: { trigger: '.hero-wrap', start: 'top top', end: 'bottom top', scrub: true } })
        .to('.hero .media', { scale: .9, borderRadius: 28, ease: 'none' }, 0)
        .to('.hero .content', { yPercent: -18, opacity: 0, ease: 'none' }, 0)
        .to('.hud', { opacity: 0, ease: 'none' }, 0);
    }
    /* inner page heroes */
    $$('[data-split]').forEach(function (el) {
      var w = split(el);
      if (el.closest('.hero')) return;
      var inView = el.getBoundingClientRect().top < innerHeight;
      G.from(w, { yPercent: 115, rotate: 3, duration: 1.1, stagger: .05, ease: 'power4.out', delay: inView ? .25 : 0,
        scrollTrigger: inView ? null : { trigger: el, start: 'top 85%' } });
    });
    /* fades */
    $$('[data-rise]').forEach(function (el) {
      G.from(el, { y: 50, opacity: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%' } });
    });
    $$('[data-stagger]').forEach(function (g) {
      G.from(g.children, { y: 60, opacity: 0, duration: 1, stagger: .08, ease: 'power3.out', scrollTrigger: { trigger: g, start: 'top 85%' } });
    });
    /* word-by-word scrub */
    $$('.scrub').forEach(function (el) {
      var ws = split(el); $$('.w', el).forEach(function (w) { w.classList.add('sw'); });
      G.to($$('.sw', el), { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 75%', end: 'bottom 45%', scrub: true } });
    });
    /* orbit: green dot lands on the core as you scroll */
    var lander = $('.orbit .lander');
    if (lander) {
      G.timeline({ scrollTrigger: { trigger: '.orbit', start: 'top 80%', end: 'center 40%', scrub: 1 } })
        .fromTo(lander, { attr: { cx: 372, cy: 120 } }, { attr: { cx: 200, cy: 200 }, ease: 'power2.in' })
        .to('.orbit .core', { attr: { r: 30 }, ease: 'back.out(3)' }, '>-0.1')
        .to('.orbit .landed', { opacity: 1 }, '<');
    }
    /* image clip reveal */
    $$('[data-clip]').forEach(function (el) {
      G.fromTo(el, { clipPath: 'inset(18% 10% 18% 10% round 24px)' }, { clipPath: 'inset(0% 0% 0% 0% round 20px)', ease: 'none', scrollTrigger: { trigger: el, start: 'top 95%', end: 'top 35%', scrub: true } });
      var img = el.querySelector('img'); if (img) G.fromTo(img, { scale: 1.25 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 95%', end: 'bottom top', scrub: true } });
    });
    /* odometer counts (HTML holds the final numbers) */
    $$('[data-count]').forEach(function (el) {
      var to = parseFloat(el.dataset.count), from = parseFloat(el.dataset.from || 0), o = { v: from };
      G.to(o, { v: to, duration: 1.8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 85%' }, onUpdate: function () { el.textContent = Math.round(o.v); } });
    });
    /* pinned horizontal work rail (desktop) */
    var rail = $('.rail[data-pin]');
    if (rail && innerWidth > 900) {
      var dist = function () { return rail.scrollWidth - innerWidth; };
      G.to(rail, { x: function () { return -dist(); }, ease: 'none', scrollTrigger: { trigger: '.rail-sec', start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1,
        onUpdate: function (s) { G.set('.railbar i', { scaleX: s.progress }); } } });
    }
    /* split statement: halves slide in */
    var sp = $('.split');
    if (sp) {
      var ltxt = split($('.split .l p')), rtxt = split($('.split .r p'));
      G.timeline({ scrollTrigger: { trigger: sp, start: 'top 70%', end: 'top 10%', scrub: 1 } })
        .from('.split .l', { xPercent: -30, ease: 'none' }, 0).from('.split .r', { xPercent: 30, ease: 'none' }, 0)
        .from(ltxt, { yPercent: 110, stagger: .05, ease: 'none' }, 0).from(rtxt, { yPercent: 110, stagger: .05, ease: 'none' }, .15);
    }
    /* stacked cards scale back as the next arrives */
    var cards = $$('.scard');
    if (cards.length && innerWidth > 760) cards.forEach(function (c, i) {
      if (i === cards.length - 1) return;
      G.to(c, { scale: .92 + i * .015, filter: 'brightness(.82)', ease: 'none', scrollTrigger: { trigger: cards[i + 1], start: 'top 85%', end: 'top 20%', scrub: true } });
    });
    /* method line draws */
    var ml = $('.method .line i');
    if (ml) G.fromTo(ml, { scaleX: 0 }, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: '.method', start: 'top 80%', end: 'bottom 60%', scrub: true } });
    /* scroll-velocity marquees */
    $$('.mq .in').forEach(function (el, i) {
      var dir = i % 2 ? 1 : -1, x = 0, w = el.scrollWidth / 2, boost = 0;
      ST.create({ trigger: el, start: 'top bottom', end: 'bottom top', onUpdate: function (s) { boost = Math.min(Math.abs(s.getVelocity()) / 300, 8); } });
      G.ticker.add(function () { x += dir * (1.6 + boost); boost *= .94; if (x <= -w) x += w; if (x > 0) x -= w; el.style.transform = 'translate3d(' + x + 'px,0,0)'; });
    });
    /* case study screenshot scrolls with the page */
    $$('.scrollshot').forEach(function (s) {
      var img = $('.vp img', s), vp = $('.vp', s);
      G.to(img, { y: function () { return -(img.offsetHeight - vp.offsetHeight); }, ease: 'none', scrollTrigger: { trigger: s.closest('.cs') || s, start: 'top 20%', end: 'bottom 80%', scrub: 1, invalidateOnRefresh: true } });
    });
    /* concept wall: columns drift in opposite directions */
    if (innerWidth > 900) $$('.wall').forEach(function (w) {
      $$('.wc', w).forEach(function (c, i) {
        var amt = [-220, 180, -300, 140][i % 4];
        G.fromTo(c, { y: -amt * .5 }, { y: amt, ease: 'none', scrollTrigger: { trigger: w, start: 'top bottom', end: 'bottom top', scrub: true } });
      });
    });
    /* client index rows rise in */
    $$('[data-index]').forEach(function (idx) {
      G.from($$('.irow', idx), { y: 40, opacity: 0, duration: .9, stagger: .05, ease: 'power3.out', clearProps: 'opacity,transform', scrollTrigger: { trigger: idx, start: 'top 85%' } });
    });
    /* footer word */
    var fw = $('.ftr .word');
    if (fw) G.from(fw, { y: 70, opacity: 0, duration: 1.3, ease: 'power4.out', clearProps: 'transform,opacity', scrollTrigger: { trigger: fw, start: 'top 95%' } });
    /* parallax media */
    $$('[data-parallax]').forEach(function (el) {
      G.fromTo(el, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: el.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    ST.sort(); addEventListener('load', function () { ST.refresh(); });
  }
  intro(scenes);
})();
