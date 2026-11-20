/* Work deck: pinned stage, cards fly in and stack, the green dot travels a dotted path.
   Called from site.js scenes() so it is created before other triggers. Without GSAP the
   deck is a vertical list of sticky cards, which is also the phone layout. */
window.MAGO_DECK = function (G, ST) {
  document.querySelectorAll('.deck-sec').forEach(function (sec) {
    var cards = Array.prototype.slice.call(sec.querySelectorAll('.dcard'));
    var n = cards.length;
    if (!n) return;
    if (innerWidth <= 900 || !G || !ST) {
      if (!('IntersectionObserver' in window)) return;
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.target.classList.toggle('is-on', e.isIntersecting); });
      }, { threshold: .6 });
      cards.forEach(function (c) { io.observe(c); });
      return;
    }
    sec.classList.add('deck-js');
    var stage = sec.querySelector('.deck-stage');
    var path = sec.querySelector('.deck-path path');
    var dot = sec.querySelector('.deck-path circle');
    var len = path.getTotalLength();
    var count = sec.querySelector('.deck-count .cur');
    G.set(cards, { xPercent: -50, yPercent: -50, transformOrigin: '50% 100%' });

    var tl = G.timeline({
      scrollTrigger: {
        trigger: stage, start: 'top top', pin: true, scrub: 1, refreshPriority: 1, invalidateOnRefresh: true, anticipatePin: 1,
        end: function () { return '+=' + Math.round(n * innerHeight * .8); },
        onUpdate: function (s) {
          var k = Math.max(0, Math.min(n - 1, Math.floor(s.progress * n * 1.02) - 0));
          count.textContent = String(k + 1).padStart(2, '0');
          cards.forEach(function (c, j) { c.classList.toggle('is-on', j === k); });
          var pt = path.getPointAtLength(s.progress * len);
          dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y);
        }
      }
    });
    tl.to(sec.querySelector('.deck-back'), { scale: .9, opacity: .28, ease: 'none', duration: n }, 0);
    cards.forEach(function (c, i) {
      var fx = (i - (n - 1) / 2) * 16;
      tl.fromTo(c,
        { y: function () { return innerHeight * 1.05; }, x: 180, rotation: 9 },
        { y: -i * 5, x: fx, rotation: i % 2 ? .7 : -.7, ease: 'power3.out', duration: 1 }, i);
      for (var j = 0; j < i; j++) {
        var d = i - j;
        tl.to(cards[j].querySelector('.ddim'), { opacity: Math.min(.72, d * .24), ease: 'none', duration: 1 }, i);
        tl.to(cards[j], { scale: 1 - Math.min(.14, d * .04), ease: 'none', duration: 1 }, i);
      }
    });
    tl.to({}, { duration: .6 });
  });
};
