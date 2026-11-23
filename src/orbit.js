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
      var b = info.querySelector('.btn'); b.href = d.href; b.setAttribute('aria-label', 'View the ' + d.name + ' case study');
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
        el.style.filter = 'brightness(' + (.25 + .75 * Math.pow(depth, 1.5)).toFixed(2) + ')';
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
