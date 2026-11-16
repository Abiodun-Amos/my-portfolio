/* Amos Abiodun portfolio: interactions. No libraries. */
(function () {
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };

  /* header: solid after scrolling, hides on the way down, returns on the way up */
  var header = $('.header'), bar = $('.progress'), lastY = 0;
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) {
      header.classList.toggle('is-stuck', y > 40);
      header.classList.toggle('is-hidden', y > 500 && y > lastY);
    }
    if (bar) {
      var max = doc.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    }
    lastY = y;
    parallax(y);
    timeline();
  }

  /* gentle parallax for elements marked data-speed */
  var pEls = $$('[data-speed]');
  function parallax() {
    if (reduce || window.innerWidth < 700) return;
    pEls.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var mid = r.top + r.height / 2 - window.innerHeight / 2;
      el.style.translate = '0 ' + (mid * parseFloat(el.dataset.speed)).toFixed(1) + 'px';
    });
  }

  /* timeline line fills as you scroll past it */
  var tl = $('.tl'), tlFill = $('.tl__fill');
  function timeline() {
    if (!tl || !tlFill) return;
    var r = tl.getBoundingClientRect();
    var done = Math.min(Math.max((window.innerHeight * 0.6 - r.top) / r.height, 0), 1);
    tlFill.style.height = (done * (r.height - 12)) + 'px';
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { onScroll(); ticking = false; }); }
  }, { passive: true });
  onScroll();

  /* size the giant hero name so it always spans the hero, whatever font has loaded */
  function fitName() {
    var n = $('.hero__name'); if (!n) return;
    var spans = $$('span', n); if (!spans.length) return;
    n.style.fontSize = '';
    var w = spans[spans.length - 1].getBoundingClientRect().right - spans[0].getBoundingClientRect().left;
    var box = n.clientWidth;
    if (!w || !box) return;
    var size = parseFloat(getComputedStyle(n).fontSize) * (box * 0.94) / w;
    var cap = (n.parentElement.clientHeight || 900) * 0.62;
    n.style.fontSize = Math.min(size, cap, 640) + 'px';
  }
  fitName();
  window.addEventListener('resize', fitName);
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(fitName);

  /* reveal on scroll */
  var revealEls = $$('.reveal, .clip');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* number counters: the final value is already in the page, this counts up to it */
  var counters = $$('[data-count]');
  if ('IntersectionObserver' in window && !reduce) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        co.unobserve(e.target);
        var el = e.target, end = parseInt(el.dataset.count, 10), t0 = null, dur = 1600;
        function step(t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - p, 4);
          el.textContent = Math.round(end * eased);
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* light / dark theme switch, remembered on this device */
  $$('.theme-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('aa-theme', next); } catch (err) {}
      b.setAttribute('aria-label', next === 'light' ? 'Switch to dark mode' : 'Switch to light mode');
    });
  });

  /* mobile menu */
  var drawer = $('.drawer');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    doc.body.style.overflow = open ? 'hidden' : '';
    $$('[data-menu]').forEach(function (b) { b.setAttribute('aria-expanded', open ? 'true' : 'false'); });
  }
  $$('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () { setDrawer(b.dataset.menu === 'open'); });
  });

  /* expertise rows */
  $$('.xp__head').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var row = btn.closest('.xp__row'), open = !row.classList.contains('is-open');
      row.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  function openFromHash() {
    var id = location.hash.replace('#', '');
    if (!id) return;
    var row = doc.getElementById(id);
    if (row && row.classList.contains('xp__row')) {
      row.classList.add('is-open');
      var b = $('.xp__head', row); if (b) b.setAttribute('aria-expanded', 'true');
      setTimeout(function () { row.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); }, 300);
    }
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);

  /* filters for projects and gallery */
  $$('.filters').forEach(function (group) {
    var targets = $$(group.dataset.target);
    $$('button', group).forEach(function (btn) {
      btn.addEventListener('click', function () {
        $$('button', group).forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        var f = btn.dataset.filter;
        targets.forEach(function (t) {
          var show = f === 'all' || (t.dataset.cat || '').split(' ').indexOf(f) > -1;
          t.hidden = !show;
          if (show) t.classList.add('in');
        });
      });
    });
  });

  /* lightbox for gallery and certificates */
  var lb = $('.lb'), shots = $$('[data-full]'), idx = 0, lastFocus = null;
  function visibleShots() { return shots.filter(function (s) { return !s.hidden; }); }
  function show(i) {
    var list = visibleShots(); if (!list.length) return;
    idx = (i + list.length) % list.length;
    var s = list[idx];
    $('.lb__stage img', lb).src = s.dataset.full;
    $('.lb__stage img', lb).alt = s.dataset.caption || '';
    $('.lb__foot p', lb).textContent = s.dataset.caption || '';
    $('.lb__count', lb).textContent = (idx + 1) + ' / ' + list.length;
  }
  function closeLb() {
    lb.classList.remove('is-open'); doc.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  if (lb) {
    shots.forEach(function (s) {
      s.addEventListener('click', function () {
        lastFocus = s; show(visibleShots().indexOf(s));
        lb.classList.add('is-open'); doc.body.style.overflow = 'hidden';
        $('[data-lb="close"]', lb).focus();
      });
    });
    $('[data-lb="close"]', lb).addEventListener('click', closeLb);
    $('[data-lb="prev"]', lb).addEventListener('click', function () { show(idx - 1); });
    $('[data-lb="next"]', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__stage')) closeLb(); });
  }
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (lb && lb.classList.contains('is-open')) closeLb(); setDrawer(false); }
    if (lb && lb.classList.contains('is-open')) {
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    }
  });

  /* contact form: builds the message, then the visitor sends it by WhatsApp or email */
  var form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = $('#cf-name').value.trim(), email = $('#cf-email').value.trim();
      var topic = $('#cf-topic').value, msg = $('#cf-message').value.trim();
      var text = 'Hello Amos,\n\n' + msg + '\n\nTopic: ' + topic + '\nFrom: ' + name + (email ? ' (' + email + ')' : '');
      var box = $('#sendbox');
      $('#send-preview').textContent = text;
      $('#send-wa').href = 'https://wa.me/2348086130089?text=' + encodeURIComponent(text);
      $('#send-gmail').href = 'https://mail.google.com/mail/?view=cm&fs=1&to=abiodunamos59@gmail.com&su=' + encodeURIComponent(topic + ' enquiry from ' + name) + '&body=' + encodeURIComponent(text);
      $('#send-mail').href = 'mailto:abiodunamos59@gmail.com?subject=' + encodeURIComponent(topic + ' enquiry from ' + name) + '&body=' + encodeURIComponent(text);
      box.hidden = false;
      box.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    });
    var copy = $('#send-copy');
    if (copy) copy.addEventListener('click', function () {
      var t = $('#send-preview').textContent;
      function done(ok) { copy.textContent = ok ? 'Copied' : 'Select the text and copy it'; setTimeout(function () { copy.textContent = 'Copy message'; }, 2200); }
      try { navigator.clipboard.writeText(t).then(function () { done(true); }, function () { done(false); }); } catch (err) { done(false); }
    });
  }

  /* page transition: curtain slides in before moving to another page of the site */
  var curtain = $('.curtain');
  if (curtain && !reduce) {
    doc.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a') : null;
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      var href = a.getAttribute('href') || '';
      if (!/^[a-z0-9-]+\.html(#[\w-]+)?$/i.test(href)) return;
      e.preventDefault();
      setDrawer(false);
      curtain.classList.add('is-in');
      setTimeout(function () { window.location.href = href; }, 430);
    });
    window.addEventListener('pageshow', function (e) { if (e.persisted) curtain.classList.remove('is-in'); });
  }

  /* cursor ring on devices with a mouse */
  var cursor = $('.cursor');
  if (cursor && window.matchMedia('(hover: hover) and (pointer: fine)').matches && !reduce) {
    var cx = 0, cy = 0, tx = 0, ty = 0;
    doc.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; cursor.classList.add('is-on'); }, { passive: true });
    doc.addEventListener('mouseleave', function () { cursor.classList.remove('is-on'); });
    doc.addEventListener('mouseover', function (e) {
      var hit = e.target.closest ? e.target.closest('a, button, input, select, textarea') : null;
      cursor.classList.toggle('is-link', !!hit && !hit.matches('input, select, textarea'));
    });
    (function loop() {
      cx += (tx - cx) * 0.2; cy += (ty - cy) * 0.2;
      cursor.style.transform = 'translate(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px)';
      requestAnimationFrame(loop);
    })();
  }

  /* back to top */
  $$('.totop').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
  });
})();
