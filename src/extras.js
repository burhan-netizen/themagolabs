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
