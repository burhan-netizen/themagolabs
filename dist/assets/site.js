/* Orbit gallery: client sites orbit a tilted ring like planets. Scroll (desktop, pinned),
   drag, arrows, keys or a click on a back card turn the orbit; the front card opens its case.
   Without JS it is a plain grid of linked cards. */
window.MAGO_ORBIT = function (G, ST) {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.orb-sec').forEach(function (sec) {
    var stage = sec.querySelector('.orb-stage');
    var cards = Array.prototype.slice.call(sec.querySelectorAll('.ocard'));
    var n = cards.length; if (n < 3) return;
    sec.classList.add('orb-js');
    var info = sec.querySelector('.orb-info'), cnt = sec.querySelector('.orb-ui .cnt b');
    var ring = sec.querySelector('.orb-ring'), glow = sec.querySelector('.orb-glow');
    var step = Math.PI * 2 / n;
    var scrollT = 0, dragT = 0, rot = 0, front = -1, W, H, cx, cy, Rx, Ry, cw, ch;
    var desktop = innerWidth > 900;

    function measure() {
      lastRot = null;
      W = stage.clientWidth; H = stage.clientHeight; desktop = innerWidth > 900;
      if (desktop) { cx = W * .6; cy = H * .45; Rx = Math.min(W * .44, 760); Ry = H * .17; cw = Math.min(W * .31, 520); }
      else { cx = W * .5; cy = H * .36; Rx = W * .4; Ry = H * .08; cw = W * .62; }
      ch = cw * 426 / 900 + 24;
      sec.style.setProperty('--cw', cw + 'px');
      if (glow) { glow.style.setProperty('--gx', cx + 'px'); glow.style.setProperty('--gy', cy + 'px'); }
      if (ring) {
        ring.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
        ring.innerHTML = '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + Rx + '" ry="' + Ry + '"/>' +
          '<ellipse class="d" cx="' + cx + '" cy="' + cy + '" rx="' + Rx * 1.35 + '" ry="' + Ry * 1.35 + '"/>' +
          '<ellipse class="d" cx="' + cx + '" cy="' + cy + '" rx="' + Rx * .6 + '" ry="' + Ry * .6 + '"/>' +
          '<circle r="6" cx="' + cx + '" cy="' + cy + '"/>';
      }
    }

    function setInfo(i) {
      var c = cards[i], d = c.dataset;
      cards.forEach(function (x, j) { x.classList.toggle('front', j === i); x.querySelector('a').tabIndex = j === i ? 0 : -1; });
      cnt.textContent = String(i + 1).padStart(2, '0');
      info.querySelector('.k').textContent = d.ind + (d.where ? ' · ' + d.where : '');
      info.querySelector('.nm > span').textContent = d.name;
      info.querySelector('.rs > span').innerHTML = d.res;
      var b = info.querySelector('.btn'); b.href = d.href; b.setAttribute('aria-label', b.textContent.trim() + ': ' + d.name);
      if (G && !reduce) G.fromTo(info.querySelectorAll('.t > span'), { yPercent: 105 }, { yPercent: 0, duration: .7, stagger: .05, ease: 'power3.out', overwrite: true });
    }

    /* only redraw while on screen and still moving; a settled orbit costs nothing */
    var onScreen = true, lastRot = null;
    new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; }, { rootMargin: '200px 0px' }).observe(stage);
    function frame() {
      requestAnimationFrame(frame);
      var target = scrollT + dragT;
      rot += (target - rot) * (reduce ? 1 : .085);
      if (!onScreen || (lastRot !== null && Math.abs(rot - lastRot) < 1e-5)) return;
      lastRot = rot;
      for (var i = 0; i < n; i++) {
        var th = i * step + rot, s = Math.sin(th), c = Math.cos(th);
        var depth = (c + 1) / 2;
        var sc = .2 + .8 * Math.pow(depth, 2.6);
        var x = cx + s * Rx - cw / 2, y = cy + c * Ry - ch / 2;
        var el = cards[i];
        el.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0) scale(' + sc.toFixed(3) + ')';
        el.style.zIndex = Math.round(depth * 100);
        el.style.opacity = (.08 + .92 * Math.pow(depth, 1.7)).toFixed(3);
        el.style.setProperty('--dim', (.75 - .75 * Math.pow(depth, 1.5)).toFixed(2)); /* dark veil instead of a brightness filter: same look, cheaper, readable for screen readers */
      }
      var f = ((Math.round(-rot / step) % n) + n) % n;
      if (f !== front) { front = f; setInfo(f); }
    }

    function goTo(i) {
      var cur = -(scrollT + dragT) / step, diff = i - cur;
      diff = ((diff % n) + n + n / 2) % n - n / 2;
      dragT -= diff * step;
    }

    measure();
    addEventListener('resize', measure);

    /* scroll drives the orbit on desktop (pinned) */
    if (desktop && G && ST) {
      ST.create({ trigger: stage, start: 'top top', end: function () { return '+=' + Math.round(n * innerHeight * .42); }, pin: true, scrub: true,
        refreshPriority: 1, invalidateOnRefresh: true, anticipatePin: 1,
        onUpdate: function (s) { scrollT = -s.progress * (n - 1) * step; } });
    } else if (!reduce) {
      /* phones: drift slowly while on screen */
      var vis = false;
      new IntersectionObserver(function (es) { vis = es[0].isIntersecting; }).observe(stage);
      (function drift() { if (vis && !dragging) dragT -= .0016; requestAnimationFrame(drift); })();
    }

    /* drag to spin */
    var dragging = false, sx = 0, sd = 0, moved = 0;
    stage.addEventListener('pointerdown', function (e) { dragging = true; moved = 0; sx = e.clientX; sd = dragT; });
    addEventListener('pointermove', function (e) { if (!dragging) return; var dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); dragT = sd + dx / (Rx * 1.2); });
    addEventListener('pointerup', function () { if (!dragging) return; dragging = false; if (moved > 6) goTo(((Math.round(-(scrollT + dragT) / step) % n) + n) % n); });

    /* clicks: back cards rotate to the front, the front card opens its case */
    cards.forEach(function (c, i) {
      c.addEventListener('click', function (e) {
        if (moved > 6 || i !== front) { e.preventDefault(); e.stopPropagation(); if (moved <= 6) goTo(i); }
      }, true);
    });
    sec.querySelector('.orb-prev').addEventListener('click', function () { goTo((front - 1 + n) % n); });
    sec.querySelector('.orb-next').addEventListener('click', function () { goTo((front + 1) % n); });
    stage.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo((front + 1) % n); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo((front - 1 + n) % n); }
    });
    requestAnimationFrame(frame);
  });
};
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
    lenis = new Lenis({ lerp: .14, smoothWheel: true, wheelMultiplier: 1 }); window.MAGO_LENIS = lenis;
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
  /* calls reveal() once, as the loader starts lifting (or straight away when there is no loader) */
  function intro(reveal) {
    var fired = false, done = function () { if (!fired) { fired = true; reveal(); } };
    var seen = false; try { seen = sessionStorage.getItem('mago-intro'); } catch (e) {}
    if (!loader || !motion || seen) { done(); return; }
    try { sessionStorage.setItem('mago-intro', '1'); } catch (e) {}
    loader.classList.add('on');
    var safety = setTimeout(function () { loader.style.display = 'none'; done(); }, 4200);
    var path = $('.loader .m'), dotEl = $('.loader .ld'), count = $('.loader .count');
    var len = path.getTotalLength();
    G.set(path, { strokeDasharray: len, strokeDashoffset: len, fill: 'transparent' });
    G.set(dotEl, { attr: { cx: 60, cy: 40 }, opacity: 0 });
    var o = { v: 0 };
    var tl = G.timeline({ onComplete: function () { clearTimeout(safety); } });
    tl.to(o, { v: 100, duration: 1.4, ease: 'power2.inOut', onUpdate: function () { count.textContent = String(Math.round(o.v)).padStart(3, '0'); } }, 0)
      .to(path, { strokeDashoffset: 0, duration: 1.1, ease: 'power2.inOut' }, 0)
      .to(path, { fill: '#F2F1EC', duration: .35 }, 1.0)
      .to(dotEl, { opacity: 1, attr: { cx: 124, cy: 11 }, duration: .55, ease: 'back.out(2)' }, 1.05)
      .call(done, null, 1.75)
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
  var hdr = $('.hdr'), last = 0, darkSecs = $$('[data-dark]'), mctaEl = $('.mcta'), hdrQueued = false;
  function hdrUpdate() {
    hdrQueued = false;
    var y = window.scrollY;
    hdr.classList.toggle('solid', y > 40);
    hdr.classList.toggle('hide', y > 500 && y > last && !document.body.classList.contains('menu-open'));
    last = y;
    var probe = 40, dark = false;
    for (var di = 0; di < darkSecs.length && !dark; di++) { var r = darkSecs[di].getBoundingClientRect(); if (r.top <= probe && r.bottom > probe) dark = true; }
    hdr.classList.toggle('on-dark', dark);
    if (mctaEl) mctaEl.classList.toggle('on', y > innerHeight * .8);
  }
  addEventListener('scroll', function () { if (!hdrQueued) { hdrQueued = true; requestAnimationFrame(hdrUpdate); } }, { passive: true }); hdrUpdate();

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
    var curRun = false;
    function curLoop() {
      cx += (mx - cx) * .2; cy += (my - cy) * .2; cur.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)';
      if (Math.abs(mx - cx) + Math.abs(my - cy) > .3) requestAnimationFrame(curLoop); else curRun = false;
    }
    addEventListener('pointermove', function (e) { mx = e.clientX; my = e.clientY; cur.classList.add('ready'); if (!curRun) { curRun = true; requestAnimationFrame(curLoop); } }, { passive: true });
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
        $('.tag', pv).textContent = r.dataset.tag; pv.classList.toggle('on', true); ts = 1; wake();
      });
    });
    var pvRun = false;
    function wake() { if (!pvRun) { pvRun = true; requestAnimationFrame(loop); } }
    idx.addEventListener('pointerleave', function () { pv.classList.toggle('on', false); ts = .7; wake(); });
    addEventListener('pointermove', function (e) { tx = e.clientX; ty = e.clientY; if (pv.classList.contains('on')) wake(); }, { passive: true });
    function loop() {
      var dx = tx - x; x += dx * .12; y += (ty - y) * .12; s += (ts - s) * .12;
      var rot = reduce ? 0 : Math.max(-8, Math.min(8, dx * .04));
      pv.style.transform = 'translate(' + (x + 40) + 'px,' + (y - 20) + 'px) translate(0,-50%) rotate(' + rot + 'deg) scale(' + s + ')';
      if (Math.abs(dx) + Math.abs(ty - y) + Math.abs(ts - s) * 100 > .3) requestAnimationFrame(loop); else pvRun = false;
    }
    wake();
  });

  /* ---------- pause decorative CSS animations in sections that are off screen ---------- */
  if ('IntersectionObserver' in window) {
    var offIO = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('anim-off', !(e.isIntersecting && e.intersectionRatio > 0)); }); }, { rootMargin: '0px' });
    $$('main > section, main > div, .ftr').forEach(function (s) { offIO.observe(s); });
  }

  if (!motion) { document.documentElement.classList.add('static'); return; }

  /* ================== GSAP SCENES ================== */
  function scenes() {
    if (window.MAGO_ORBIT) window.MAGO_ORBIT(G, ST);
    /* hero: kinetic headline, then video shrinks into a card as you scroll */
    var hero = $('.hero');
    if (hero) {
      /* the headline rise, the copy and the video zoom are CSS animations (see .h-hero in extras.css) */
      var heroMedia = $('.hero .media');
      heroTl = true;
      G.timeline({ scrollTrigger: { trigger: '.hero-wrap', start: 'top top', end: 'bottom top', scrub: true,
          onUpdate: function (s) { heroMedia.classList.toggle('shrunk', s.progress > .02); } } })
        .to(heroMedia, { scale: .9, ease: 'none' }, 0)
        .to('.hero .content', { yPercent: -18, opacity: 0, ease: 'none' }, 0)
        .to('.hud', { opacity: 0, ease: 'none' }, 0);
    }
    /* inner page heroes */
    $$('[data-split]').forEach(function (el) {
      var w = split(el);
      if (el.closest('.hero')) { G.set(el, { visibility: 'visible' }); return; }
      var inView = el.getBoundingClientRect().top < innerHeight;
      G.from(w, { yPercent: 115, rotate: 3, duration: 1.1, stagger: .05, ease: 'power4.out', delay: inView ? .25 : 0, immediateRender: true,
        onComplete: function () { $$('.w', el).forEach(function (x) { x.classList.add('open'); }); },
        scrollTrigger: inView ? null : { trigger: el, start: 'top 85%' } });
      G.set(el, { visibility: 'visible' });
    });
    /* fades */
    $$('[data-rise]').forEach(function (el) {
      G.from(el, { y: 50, opacity: 0, duration: 1.1, ease: 'power3.out', immediateRender: true, scrollTrigger: { trigger: el, start: 'top 90%' } });
      G.set(el, { visibility: 'visible' });
    });
    $$('[data-stagger]').forEach(function (g) {
      G.from(g.children, { y: 60, opacity: 0, duration: 1, stagger: .08, ease: 'power3.out', immediateRender: true, scrollTrigger: { trigger: g, start: 'top 85%' } });
      G.set(g, { visibility: 'visible' });
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
      var dir = i % 2 ? 1 : -1, x = 0, w = el.scrollWidth / 2, boost = 0, on = false;
      ST.create({ trigger: el, start: 'top bottom', end: 'bottom top', onToggle: function (s) { on = s.isActive; }, onUpdate: function (s) { boost = Math.min(Math.abs(s.getVelocity()) / 300, 8); } });
      G.ticker.add(function () { if (!on) return; x += dir * (1.6 + boost); boost *= .94; if (x <= -w) x += w; if (x > 0) x -= w; el.style.transform = 'translate3d(' + x + 'px,0,0)'; });
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
  var heroTl = null;
  scenes();
  intro(function () {
    document.documentElement.classList.remove('first');
    if (!heroTl) return;
    setTimeout(function () { $$('.hero h1 .w').forEach(function (w) { w.classList.add('open'); }); }, 1700);
  });
})();
/* v4 interactions. Each block checks for its own markup and degrades to a static, usable page. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  var cfg = window.MAGO || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function track(n, p) { try { (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: n }, p || {})); } catch (e) {} }

  /* ---------- in-page anchors (+ preselect the contact path) ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]'); if (!a) return;
    var id = a.getAttribute('href').slice(1); var t = id && document.getElementById(id); if (!t) return;
    e.preventDefault();
    var mode = a.getAttribute('data-site');
    if (mode) { document.dispatchEvent(new CustomEvent('mago:site', { detail: mode })); }
    var y = t.getBoundingClientRect().top + scrollY - 20;
    if (window.MAGO_LENIS) window.MAGO_LENIS.scrollTo(y, { duration: 1.4 }); else scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
    setTimeout(function () { var f = $('#contact input[name="name"]'); if (f && id === 'contact') f.focus({ preventScroll: true }); }, reduce ? 0 : 1300);
  });

  /* ---------- logo wall spotlight ---------- */
  $$('.lw-grid').forEach(function (g) {
    if (!fine) return;
    g.addEventListener('pointermove', function (e) {
      var r = g.getBoundingClientRect(); g.style.setProperty('--mx', (e.clientX - r.left) + 'px'); g.style.setProperty('--my', (e.clientY - r.top) + 'px');
      var c = e.target.closest('.lw-cell'); if (c) { var cr = c.getBoundingClientRect(); c.style.setProperty('--x', (e.clientX - cr.left) + 'px'); c.style.setProperty('--y', (e.clientY - cr.top) + 'px'); }
    });
  });

  /* ---------- concept lab floor: lanes drift, speed up with scroll ---------- */
  var lanes = $$('.lane');
  if (lanes.length && !reduce) {
    var boost = 0, lastY = scrollY, vis = false;
    var floor = $('.floor');
    new IntersectionObserver(function (es) { vis = es[0].isIntersecting; }).observe(floor);
    addEventListener('scroll', function () { boost = Math.min(Math.abs(scrollY - lastY) * .35, 14); lastY = scrollY; }, { passive: true });
    var st = lanes.map(function (l, i) { return { el: l, x: i % 2 ? -l.scrollWidth / 4 : 0, dir: i % 2 ? 1 : -1, speed: [.55, .75, .45][i % 3], paused: false }; });
    st.forEach(function (s) { s.el.addEventListener('pointerenter', function () { s.paused = true; }); s.el.addEventListener('pointerleave', function () { s.paused = false; }); });
    (function loop() {
      if (vis) st.forEach(function (s) {
        if (s.paused) return;
        var half = s.el.scrollWidth / 2;
        s.x += s.dir * (s.speed + boost * .5);
        if (s.x <= -half) s.x += half; if (s.x > 0) s.x -= half;
        s.el.style.transform = 'translate3d(' + s.x + 'px,0,0)';
      });
      boost *= .92;
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- process: active step, rolling counter, travelling dot ---------- */
  var proc = $('.proc');
  if (proc) {
    var steps = $$('.pstep', proc), roll = $('.proc .big .roll span'), bar = $('.proc .bar i');
    var path = $('.proc .path'), fill = $('.proc .path i'), dot = $('.proc .path b'), right = $('.proc .right');
    function setStep(i) {
      steps.forEach(function (s, j) { s.classList.toggle('on', j === i); });
      if (roll) roll.style.transform = 'translateY(' + (-i * .82) + 'em)';
      if (bar) bar.style.transform = 'scaleX(' + ((i + 1) / steps.length) + ')';
    }
    if ('IntersectionObserver' in window) {
      var pio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) setStep(steps.indexOf(e.target)); }); }, { rootMargin: '-45% 0px -45% 0px' });
      steps.forEach(function (s) { pio.observe(s); });
    }
    setStep(0);
    function pathUpdate() {
      var r = right.getBoundingClientRect(), mid = innerHeight * .5;
      var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      fill.style.transform = 'scaleY(' + p + ')';
      dot.style.transform = 'translateY(' + (p * (r.height - 13)) + 'px)';
    }
    addEventListener('scroll', pathUpdate, { passive: true }); pathUpdate();
  }

  /* ---------- founder photo pile: drag or tap to toss the top photo to the back ---------- */
  $$('.pile').forEach(function (pile) {
    var cards = $$('.polo', pile);
    var order = cards.slice();
    function layout(anim) {
      order.forEach(function (c, i) {
        var rot = parseFloat(c.dataset.rot);
        c.style.zIndex = String(order.length - i);
        c.style.transition = anim ? 'transform .7s cubic-bezier(.2,.8,.2,1)' : 'none';
        c.style.transform = 'translate(' + (i * 3) + 'px,' + (i * 4) + 'px) rotate(' + rot + 'deg) scale(' + (1 - Math.min(i, 4) * .02) + ')';
      });
    }
    cards.forEach(function (c, i) { c.dataset.rot = ((i * 37) % 13 - 6).toFixed(1); });
    layout(false);
    function toss(dx, dy) {
      var top = order[0];
      top.style.transition = reduce ? 'none' : 'transform .55s cubic-bezier(.3,.6,.2,1)';
      top.style.transform = 'translate(' + (dx * 6) + 'px,' + (dy * 3 - 60) + 'px) rotate(' + (dx > 0 ? 28 : -28) + 'deg)';
      setTimeout(function () { order.push(order.shift()); layout(true); }, reduce ? 0 : 420);
      track('founder_photo_toss');
    }
    var drag = null;
    pile.addEventListener('pointerdown', function (e) {
      var c = e.target.closest('.polo'); if (c !== order[0]) return;
      drag = { x: e.clientX, y: e.clientY, dx: 0, dy: 0 }; c.setPointerCapture(e.pointerId); c.style.transition = 'none';
    });
    pile.addEventListener('pointermove', function (e) {
      if (!drag) return; drag.dx = e.clientX - drag.x; drag.dy = e.clientY - drag.y;
      order[0].style.transform = 'translate(' + drag.dx + 'px,' + drag.dy + 'px) rotate(' + (parseFloat(order[0].dataset.rot) + drag.dx * .06) + 'deg)';
    });
    pile.addEventListener('pointerup', function () {
      if (!drag) return; var d = drag; drag = null;
      if (Math.abs(d.dx) > 90 || Math.abs(d.dy) > 120) toss(d.dx || 1, d.dy);
      else if (Math.abs(d.dx) < 6 && Math.abs(d.dy) < 6) toss(1, 0);
      else layout(true);
    });
    var nb = pile.parentNode.querySelector('.pile-next'); if (nb) nb.addEventListener('click', function () { toss(1, 0); });
    pile.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') { e.preventDefault(); toss(1, 0); } });
  });

  /* ---------- reviews showcase ---------- */
  var rvData = $('#rv-data');
  if (rvData) {
    var R = JSON.parse(rvData.textContent), stage = $('.rv-stage'), btns = $$('.rv-list button');
    var cur = 0, t0 = 0, paused = false, DUR = 8000;
    function show(i, user) {
      cur = i; var r = R[i];
      btns.forEach(function (b, j) { b.setAttribute('aria-selected', String(j === i)); $('.pg', b).style.transform = 'scaleX(0)'; });
      $('.hd', stage).textContent = r.head;
      var q = $('blockquote', stage);
      q.innerHTML = '<span class="qm">“</span>' + r.quote.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '<span class="qm">”</span>';
      $('.who .p', stage).innerHTML = r.name + '<span>' + r.role + '</span>';
      $('.who .lg', stage).innerHTML = r.logo ? '<img src="' + r.logo + '" alt="">' : r.initials;
      var l = $('.who a', stage); if (r.href) { l.hidden = false; l.href = r.href; } else l.hidden = true;
      if (window.gsap && !reduce) gsap.fromTo([q, $('.who', stage)], { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .7, stagger: .08, ease: 'power3.out' });
      t0 = performance.now();
      if (user) track('review_select', { index: i });
    }
    btns.forEach(function (b, i) { b.addEventListener('click', function () { show(i, true); }); });
    var sec = $('.rv-sec'), inView = false;
    sec.addEventListener('pointerenter', function () { paused = true; }); sec.addEventListener('pointerleave', function () { paused = false; t0 = performance.now() - parseFloat(btns[cur].dataset.el || 0); });
    new IntersectionObserver(function (es) { inView = es[0].isIntersecting; }).observe(sec);
    show(0);
    if (!reduce) (function tick(now) {
      if (inView && !paused) {
        var el = now - t0; btns[cur].dataset.el = el;
        $('.pg', btns[cur]).style.transform = 'scaleX(' + Math.min(1, el / DUR) + ')';
        if (el >= DUR) show((cur + 1) % R.length);
      } else t0 = now - parseFloat(btns[cur].dataset.el || 0);
      requestAnimationFrame(tick);
    })(performance.now());
  }

  /* ---------- mad-lib contact ---------- */
  $$('form.madlib').forEach(function (f) {
    var at = $('.site-at', f);
    function sync() { var v = $('input[name="has_site"]:checked', f); if (at) at.hidden = !v || v.value !== 'yes'; }
    $$('input[name="has_site"]', f).forEach(function (r) { r.addEventListener('change', sync); }); sync();
    $$('input[data-grow]', f).forEach(function (i) {
      var grow = function () { i.style.width = Math.max(i.placeholder.length * .55, i.value.length * .58 + 1) + 'em'; };
      i.addEventListener('input', grow); grow();
    });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var need = ['name', 'business', 'reach'], miss = [];
      var hs = $('input[name="has_site"]:checked', f); if (hs && hs.value === 'yes') need.push('website');
      need.forEach(function (n) { var i = $('[name="' + n + '"]', f), w = i.closest('.fill'); var bad = !i.value.trim(); w.classList.toggle('bad', bad); if (bad) miss.push(i); });
      var err = $('.err', f);
      if (miss.length) { err.classList.add('on'); miss[0].focus(); return; }
      err.classList.remove('on');
      var goals = $$('input[name="goal"]:checked', f).map(function (g) { return g.value; });
      var d = { name: $('[name=name]', f).value.trim(), business: $('[name=business]', f).value.trim(), website: $('[name=website]', f).value.trim(),
        has_site: hs ? hs.value : '', goals: goals.join(', '), reach: $('[name=reach]', f).value.trim(), page: location.pathname, form: 'madlib' };
      track('generate_lead', { form: 'madlib', has_site: d.has_site });
      var lines = ['Hi Burhan, I\'m ' + d.name + ' from ' + d.business + '.'];
      lines.push(d.has_site === 'yes' ? 'My website: ' + d.website + '. I\'d like a free site audit.' : 'I don\'t have a website yet. I\'d love a free preview.');
      if (d.goals) lines.push('I want more: ' + d.goals + '.');
      lines.push('Reach me at: ' + d.reach);
      var done = $('.done', f), send = $('.send', f);
      function fallback() { $('a.btn', done).href = 'https://wa.me/' + cfg.whatsapp + '?text=' + encodeURIComponent(lines.join('\n')); send.hidden = true; done.classList.add('on'); $('a.btn', done).focus(); }
      if (cfg.formEndpoint) fetch(cfg.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { if (r.ok) { send.hidden = true; done.querySelector('p').textContent = 'Got it. You\'ll hear from Burhan within one business day.'; $('a.btn', done).hidden = true; done.classList.add('on'); } else fallback(); }).catch(fallback);
      else fallback();
    });
  });
})();

/* ---------- footer word: scale to fill the row exactly, dot included ---------- */
(function () {
  var w = document.querySelector('.ftr .word'); if (!w) return;
  var dot = w.querySelector('.dot');
  function fit() {
    w.style.fontSize = '100px';
    var r = w.getBoundingClientRect(), target = r.width; if (!target) return;
    var first = w.firstChild && w.firstChild.nodeType === 1 ? w.firstChild : w;
    var left = first.getBoundingClientRect().left, right = (dot || w).getBoundingClientRect().right;
    var used = right - left; if (used <= 0) return;
    w.style.fontSize = Math.floor(100 * target * 0.97 / used * 10) / 10 + 'px';
  }
  fit(); addEventListener('resize', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();

document.addEventListener('DOMContentLoaded',function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var _d=$('#op-data');var DATA=_d?JSON.parse(_d.textContent):{concepts:[],reviews:[]};
function msg(o){return ['Hi Burhan, I\'m '+(o.name||'')+(o.business?' from '+o.business:'')+'.',
 o.has==='no'?'I don\'t have a website yet. I\'d like the free 48-hour preview.':'I have a website'+(o.website?' at '+o.website:'')+'. I\'d like the free audit.',
 o.goals&&o.goals.length?'I want more '+o.goals.join(', ')+'.':'', o.msg||'', 'Reach me at '+(o.reach||'')+'.'].filter(Boolean).join('\n');}
function wa(o){var n=(window.MAGO&&MAGO.whatsapp)||'';return 'https://wa.me/'+n+'?text='+encodeURIComponent(msg(o));}
function sendMail(o){var M=window.MAGO||{},ep=M.formEndpoint;
 var subj='New enquiry: '+(o.business||o.name||'website')+(o.has==='no'?' (no website yet)':'');
 if(!ep){location.href='mailto:'+(M.email||'')+'?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(msg(o));return Promise.resolve('mailto');}
 var body={name:o.name||'',business:o.business||'',has_website:o.has==='no'?'no':'yes',website:o.website||'',wants_more:(o.goals||[]).join(', '),contact:o.reach||'',company_site:($('input[name=company_site]')||{}).value||'',message:msg(o),subject:subj,_subject:subj,page:location.pathname};
 if(M.formKey)body.access_key=M.formKey;
 return fetch(ep,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(body)}).then(function(r){if(!r.ok)throw new Error(r.status);return 'sent'});}
function loadLong(ph){var l=$('img.long',ph);if(l&&!l.src)l.src=l.dataset.src;}
$$('.o-ph').forEach(function(ph){ph.addEventListener('pointerenter',function(){loadLong(ph)});ph.addEventListener('focus',function(){loadLong(ph)});});

/* A1 parallax columns */
$$('.a1-view').forEach(function(v){var cols=$$('.a1-col',v),sp=[-320,220,-420,160];
 function f(){var r=v.getBoundingClientRect(),p=(innerHeight-r.top)/(innerHeight+r.height);p=Math.max(0,Math.min(1,p));
  cols.forEach(function(c,i){c.style.transform='translate3d(0,'+((p-.5)*sp[i%4]*(innerWidth<900?.6:1)).toFixed(1)+'px,0)'});}
 if(!reduce){addEventListener('scroll',f,{passive:true});addEventListener('resize',f);f();}});

/* A2 centre stage */
$$('.a2').forEach(function(sec){var st=$('.a2-stage',sec),ph=$$('.o-ph',st),n=ph.length,i=0,t=null;
 function lay(){ph.forEach(function(p,k){var d=k-i;if(d>n/2)d-=n;if(d<-n/2)d+=n;var a=Math.abs(d),sm=innerWidth<700;
  p.style.transform='translateX('+(d*(sm?58:68))+'%) scale('+(1-Math.min(a,3)*.17)+')';p.style.zIndex=20-a;p.style.opacity=a>(sm?1:2)?0:1;p.style.filter='brightness('+(1-a*.32)+')';
  p.classList.toggle('c',d===0);var s=$('.o-scr',p);if(d===0){loadLong(p);setTimeout(function(){s.classList.add('on')},500)}else s.classList.remove('on');p.tabIndex=d===0?0:-1;});
  var c=DATA.concepts[i];$('.a2-info b',sec).textContent=c.name;$('.a2-info span',sec).textContent=c.trade+' · '+c.where;$('.a2-ctl .n',sec).textContent=String(i+1).padStart(2,'0')+' / '+n;$('.a2-bar .live',sec).href=c.url;}
 function go(k){i=(k+n)%n;lay();}
 function auto(){clearInterval(t);if(!reduce)t=setInterval(function(){go(i+1)},4200);}
 $('.prev',sec).onclick=function(){go(i-1);auto()};$('.next',sec).onclick=function(){go(i+1);auto()};
 ph.forEach(function(p,k){p.addEventListener('click',function(e){if(k!==i){e.preventDefault();go(k);auto();}});});
 var x0=null;st.addEventListener('pointerdown',function(e){x0=e.clientX});st.addEventListener('pointerup',function(e){if(x0===null)return;var dx=e.clientX-x0;x0=null;if(Math.abs(dx)>50){go(i+(dx<0?1:-1));auto();}});
 st.addEventListener('pointerenter',function(){clearInterval(t)});st.addEventListener('pointerleave',auto);
 lay();auto();addEventListener('resize',lay);});

/* A3 index + phone */
$$('.a3').forEach(function(sec){var bs=$$('.a3-list button',sec),imgs=$$('.a3-ph img.base',sec),long=$('.a3-ph img.long',sec),scr=$('.a3-ph .o-scr',sec);
 function set(k){bs.forEach(function(b,j){b.setAttribute('aria-selected',j===k)});imgs.forEach(function(im,j){im.classList.toggle('on',j===k)});
  var c=DATA.concepts[k];scr.classList.remove('on');long.style.transition='none';long.style.transform='';long.src=c.long;void long.offsetWidth;long.style.transition='';
  setTimeout(function(){scr.classList.add('on')},350);$('.a3-ph .meta b',sec).textContent=c.name;$('.a3-ph .meta a',sec).href=c.url;}
 bs.forEach(function(b,k){b.addEventListener('mouseenter',function(){set(k)});b.addEventListener('focus',function(){set(k)});b.addEventListener('click',function(){set(k)});});
 set(0);});

/* B1 horizontal track */
$$('.b1').forEach(function(sec){if(innerWidth<900||!window.gsap||!window.ScrollTrigger||reduce)return;gsap.registerPlugin(ScrollTrigger);
 var tr=$('.b1-track',sec),bar=$('.b1-prog i',sec);var dist=function(){return tr.scrollWidth-innerWidth};
 gsap.to(tr,{x:function(){return -dist()},ease:'none',scrollTrigger:{trigger:$('.b1-pin',sec),pin:true,start:'top top',end:function(){return '+='+dist()},scrub:.6,invalidateOnRefresh:true,onUpdate:function(s){bar.style.width=(s.progress*100)+'%'}}});});

/* B2 journey line */
$$('.b2').forEach(function(sec){var f=$('.b2-line .f',sec),dot=$('.b2-line .dot',sec),cs=$$('.b2-c',sec);
 function u(){if(innerWidth<900){cs.forEach(function(c){c.classList.add('on')});return;}var r=sec.getBoundingClientRect(),p=-r.top/(r.height-innerHeight);p=Math.max(0,Math.min(1,p));
  var w=(p*1.08)*100;w=Math.min(100,w);f.style.width=w+'%';dot.style.left=w+'%';cs.forEach(function(c,k){c.classList.toggle('on',w>=k*25+2)});}
 addEventListener('scroll',u,{passive:true});addEventListener('resize',u);u();});

/* B3 accordion */
$$('.b3').forEach(function(sec){var rows=$$('.b3-row',sec),ss=$$('.b3-card .s',sec),big=$('.b3-card .big',sec),i=0,anim=null,user=false;
 function set(k){i=k;rows.forEach(function(r,j){r.classList.toggle('on',j===k);$('button',r).setAttribute('aria-expanded',j===k)});ss.forEach(function(s,j){s.classList.toggle('on',j===k)});big.textContent='0'+(k+1);
  if(anim)anim.cancel();var bar=$('.bar i',rows[k]);if(!user&&!reduce&&bar.animate){anim=bar.animate([{transform:'scaleX(0)'},{transform:'scaleX(1)'}],{duration:5200,easing:'linear'});anim.onfinish=function(){set((i+1)%rows.length)};}}
 rows.forEach(function(r,k){$('button',r).addEventListener('click',function(){user=true;set(k)})});
 var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){set(i);io.disconnect()}},{threshold:.4});io.observe(sec);set(0);if(anim)anim.pause();});

/* C1 big quote */
$$('.c1').forEach(function(sec){var T=DATA.reviews,i=0,t=null,dots=$$('.c1-dots button',sec);
 function show(k){sec.classList.add('out');setTimeout(function(){i=(k+T.length)%T.length;var r=T[i];
  $('.c1-q',sec).textContent='“'+r.quote+'”';var L=r.quote.length;$('.c1-q',sec).style.fontSize=L>260?'clamp(20px,1.9vw,27px)':L>160?'clamp(22px,2.4vw,34px)':L>90?'clamp(26px,3vw,44px)':'';$('.c1-q',sec).style.maxWidth=L>160?'40ch':'';$('.c1-res',sec).textContent=r.head;$('.c1-who',sec).innerHTML='<b></b>, <span></span>';$('.c1-who b',sec).textContent=r.name;$('.c1-who span',sec).textContent=r.role;
  var lg=$('.c1-logo',sec);lg.innerHTML=r.logo?'<img alt="">':'';if(r.logo){$('img',lg).src=r.logo;$('img',lg).alt=r.company;}
  dots.forEach(function(d,j){d.setAttribute('aria-current',j===i)});sec.classList.remove('out');},reduce?0:420);}
 function auto(){clearInterval(t);if(!reduce)t=setInterval(function(){show(i+1)},5000);}
 $('.prev',sec).onclick=function(){show(i-1);auto()};$('.next',sec).onclick=function(){show(i+1);auto()};
 dots.forEach(function(d,j){d.onclick=function(){show(j);auto()}});
 var sw=$('.c1-swipe',sec),x0=null,y0=0;sw.addEventListener('pointerdown',function(e){x0=e.clientX;y0=e.clientY});
 sw.addEventListener('pointerup',function(e){if(x0===null)return;var dx=e.clientX-x0,dy=e.clientY-y0;x0=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)){show(i+(dx<0?1:-1));auto();}});
 sw.addEventListener('pointercancel',function(){x0=null});
 sec.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')clearInterval(t)});sec.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')auto()});
 dots.forEach(function(d,j){d.setAttribute('aria-current',j===0)});
 var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting)auto();else clearInterval(t)})});io.observe(sec);});

/* C3 rail drag + arrows */
$$('.c3').forEach(function(sec){var r=$('.c3-rail',sec),down=false,x0=0,s0=0,moved=false;
 r.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;moved=false;x0=e.clientX;s0=r.scrollLeft;r.classList.add('drag')});
 addEventListener('pointermove',function(e){if(!down)return;var d=e.clientX-x0;if(Math.abs(d)>4)moved=true;r.scrollLeft=s0-d});
 addEventListener('pointerup',function(){if(!down)return;down=false;r.classList.remove('drag')});
 var step=function(){return ($('.c3-card',r).offsetWidth+20)};
 $('.prev',sec).onclick=function(){r.scrollBy({left:-step(),behavior:'smooth'})};$('.next',sec).onclick=function(){r.scrollBy({left:step(),behavior:'smooth'})};});

/* D1 chat */
$$('.d1').forEach(function(sec){var log=$('.d1-log',sec),form=$('.d1-in',sec),inp=$('input',form),o={goals:[]},k=0;
 var Q=[{key:'name',q:'Hi! I\'m Burhan. What should I call you?',ph:'Your name'},
  {key:'business',q:function(){return 'Nice to meet you, '+o.name+'. What\'s your business called?'},ph:'Business name'},
  {key:'has',q:'Do you have a website yet?',ch:[['yes','Yes, I do'],['no','Not yet']]},
  {key:'website',q:'What\'s the address? I\'ll take a look before we talk.',ph:'yourbusiness.com',skip:function(){return o.has==='no'}},
  {key:'goals',q:'What do you want more of? Pick any.',multi:['calls','bookings','enquiries','sales']},
  {key:'reach',q:'Last one. Best email or phone to reach you?',ph:'Email or phone'}];
 function say(t,who){var m=document.createElement('div');m.className='d1-m '+who;m.textContent=t;log.appendChild(m);log.scrollTop=log.scrollHeight;return m;}
 function typing(cb){var m=document.createElement('div');m.className='d1-m bot typing';m.innerHTML='<i></i><i></i><i></i>';log.appendChild(m);log.scrollTop=log.scrollHeight;setTimeout(function(){m.remove();cb()},reduce?0:750);}
 function ask(){while(Q[k]&&Q[k].skip&&Q[k].skip())k++;var s=Q[k];if(!s)return done();
  typing(function(){say(typeof s.q==='function'?s.q():s.q,'bot');
   if(s.ch||s.multi){form.classList.add('off');var w=document.createElement('div');w.className='d1-opts';
    (s.ch||s.multi.map(function(g){return [g,g]})).forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c[1];b.setAttribute('aria-pressed','false');w.appendChild(b);
     b.onclick=function(){if(s.ch){o[s.key]=c[0];w.remove();say(c[1],'me');k++;ask();}else{var on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on);}};});
    if(s.multi){var d=document.createElement('button');d.type='button';d.textContent='Done →';d.style.background='var(--go)';d.style.color='#04130B';w.appendChild(d);
     d.onclick=function(){o.goals=$$('button[aria-pressed=true]',w).map(function(b){return b.textContent});if(!o.goals.length)o.goals=['calls'];w.remove();say(o.goals.join(', '),'me');k++;ask();};}
    log.appendChild(w);log.scrollTop=log.scrollHeight;}
   else{form.classList.remove('off');inp.placeholder=s.ph;inp.value='';if(sec.dataset.seen)inp.focus({preventScroll:true});}});}
 form.addEventListener('submit',function(e){e.preventDefault();var v=inp.value.trim();if(!v)return;var s=Q[k];o[s.key]=v;say(v,'me');inp.value='';k++;form.classList.add('off');ask();});
 function done(){typing(function(){say('Perfect. '+(o.has==='no'?'I\'ll send your free preview within 48 hours.':'I\'ll send your free audit within one business day.')+' Tap below to send this to me on WhatsApp.','bot');
  var a=document.createElement('a');a.className='op-btn go';a.style.alignSelf='flex-start';a.style.marginTop='6px';a.href=wa(o);a.target='_blank';a.rel='noopener';a.textContent='Send on WhatsApp';log.appendChild(a);log.scrollTop=log.scrollHeight;});}
 var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){sec.dataset.seen=1;ask();io.disconnect();}},{threshold:.35});io.observe(sec);});

/* D2 split card */
$$('.d2').forEach(function(sec){var f=$('form',sec),url=$('.d2-url',sec);
 function sync(){url.hidden=$('input[name=has]:checked',f).value==='no'}$$('input[name=has]',f).forEach(function(r){r.onchange=sync});sync();
 f.addEventListener('submit',function(e){e.preventDefault();var bad=false;['name','reach'].forEach(function(n){var el=f.elements[n];var b=!el.value.trim();el.setAttribute('aria-invalid',b);if(b)bad=true;});
  $('.d-err',f).textContent=bad?'Add your name and an email or phone so we know who to reply to.':'';if(bad)return;
  var o={name:f.elements.name.value.trim(),business:f.elements.business.value.trim(),has:$('input[name=has]:checked',f).value,website:f.elements.website.value.trim(),goals:$$('input[name=goal]:checked',f).map(function(x){return x.value}),reach:f.elements.reach.value.trim(),msg:f.elements.msg.value.trim()};
  $('.d2-done a',sec).href=wa(o);f.style.display='none';$('.d2-done',sec).style.display='block';});});

/* D3 one at a time */
$$('.d3-box').forEach(function(sec){var st=$$('.d3-step',sec),i=0,o={goals:[]},bar=$('.d3-prog i',sec),lab=$('.d3-prog .c',sec);
 function vis(k){return !(st[k].dataset.key==='website'&&o.has==='no')}
 function show(k,foc){i=k;st.forEach(function(s,j){s.classList.toggle('on',j===k)});var tot=st.length-2;bar.style.width=(Math.min(k,tot)/tot*100)+'%';lab.textContent=k>tot?'Sent':k===tot?'Review':(String(k+1)+' of '+tot);
  var inp=$('input',st[k]);if(inp&&foc!==false)setTimeout(function(){inp.focus({preventScroll:true})},50);if(st[k].dataset.key==='sum')sum();}
 function next(){var s=st[i],key=s.dataset.key,inp=$('input',s);if(inp){var v=inp.value.trim();if(!v&&inp.required){inp.setAttribute('aria-invalid','true');inp.focus();return;}o[key]=v;}
  var k=i+1;while(k<st.length&&!vis(k))k++;show(k);}
 function back(){var k=i-1;while(k>0&&!vis(k))k--;show(Math.max(0,k));}
 function sum(){var rows=[['Name',o.name],['Business',o.business],['Website',o.has==='no'?'Not yet':(o.website||'Yes')],['Wants more',(o.goals.length?o.goals:['calls']).join(', ')],['Reach at',o.reach]];
  $('.d3-sum',sec).innerHTML=rows.map(function(r){return '<div><span></span><b></b></div>'}).join('');$$('.d3-sum div',sec).forEach(function(d,j){$('span',d).textContent=rows[j][0];$('b',d).textContent=rows[j][1]||'-'});$$('.d3-wa',sec).forEach(function(a){a.href=wa(o)});}
 $$('.d3-step input',sec).forEach(function(inp){inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();next();}})});
 $$('.next',sec).forEach(function(b){b.onclick=next});$$('.back',sec).forEach(function(b){b.onclick=back});
 $$('.d3-ch',sec).forEach(function(w){var s=w.closest('.d3-step'),multi=s.dataset.key==='goals';$$('button',w).forEach(function(b){b.onclick=function(){
  if(multi){b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!=='true');o.goals=$$('button[aria-pressed=true]',w).map(function(x){return x.dataset.v});}
  else{$$('button',w).forEach(function(x){x.setAttribute('aria-pressed',x===b)});o[s.dataset.key]=b.dataset.v;setTimeout(next,reduce?0:260);}}})});
 document.addEventListener('mago:site',function(e){o.has=e.detail;$$('.d3-step[data-key=has] button',sec).forEach(function(b){b.setAttribute('aria-pressed',b.dataset.v===e.detail)});});
 var sb=$('.d3-send',sec),stt=$('.d3-status',sec);
 if(sb)sb.addEventListener('click',function(){if(!o.goals.length)o.goals=['calls'];sb.disabled=true;stt.textContent='Sending...';
  sendMail(o).then(function(how){stt.textContent='';try{(window.dataLayer=window.dataLayer||[]).push({event:'generate_lead',form:'contact',has_site:o.has||'yes',via:how})}catch(e){}
   if(how==='sent'){var k=st.length-1;show(k,false);}else{sb.disabled=false;stt.textContent='Your email app should open with the message ready. Nothing opened? Use WhatsApp instead.';}})
  .catch(function(){sb.disabled=false;stt.textContent='That didn\'t go through. Please try again, or send it on WhatsApp.';});});
 show(0,false);});
});
