/* Rendile Travels — interactions */
(function () {
  'use strict';

  /* ---- Year in footer ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Sticky header shadow ---- */
  var header = document.getElementById('header');
  var onScroll = function () {
    if (header) header.classList.toggle('scrolled', window.scrollY > 20);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile nav ---- */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---- Scroll reveal ---- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el, i) {
      // small stagger for siblings
      el.style.transitionDelay = (Math.min(i % 4, 3) * 0.08) + 's';
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- Testimonial slider ---- */
  var track = document.getElementById('reviewsTrack');
  var dotsWrap = document.getElementById('reviewsDots');
  if (track && dotsWrap) {
    var slides = Array.prototype.slice.call(track.querySelectorAll('.review'));
    var current = 0;
    var timer;

    slides.forEach(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Show review ' + (i + 1));
      if (i === 0) b.classList.add('is-active');
      b.addEventListener('click', function () { go(i); reset(); });
      dotsWrap.appendChild(b);
    });
    var dots = Array.prototype.slice.call(dotsWrap.children);

    function go(n) {
      slides[current].classList.remove('is-active');
      dots[current].classList.remove('is-active');
      current = (n + slides.length) % slides.length;
      slides[current].classList.add('is-active');
      dots[current].classList.add('is-active');
    }
    function next() { go(current + 1); }
    function start() { timer = setInterval(next, 6000); }
    function reset() { clearInterval(timer); start(); }
    start();
  }

  /* ---- Inquiry form (front-end demo handling) ---- */
  var form = document.getElementById('inquiryForm');
  var note = document.getElementById('formNote');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.querySelector('#name');
      var email = form.querySelector('#email');
      if (!name.value.trim() || !email.value.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value)) {
        showNote('Please add your name and a valid email so we can reach you.', false);
        return;
      }
      var firstName = name.value.trim().split(' ')[0];
      var submitBtn = form.querySelector('button[type=submit]');
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
      // Submit to Netlify Forms (notifies bookings@rendiletravels.com).
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      }).then(function (r) {
        if (!r.ok) throw new Error('bad status');
        showNote('Thank you, ' + firstName + '! Your travel designer will be in touch within one business day.', true);
        form.reset();
      }).catch(function () {
        showNote('Sorry — something went wrong. Please email us directly at bookings@rendiletravels.com.', false);
      }).finally(function () {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Send my enquiry'; }
      });
    });
  }
  function showNote(msg, ok) {
    if (!note) return;
    note.hidden = false;
    note.textContent = msg;
    note.style.background = ok ? 'rgba(62,155,156,.14)' : 'rgba(179,56,28,.12)';
    note.style.color = ok ? '#2E7B7C' : '#B3381C';
  }

  /* ---- Newsletter (demo) ---- */
  var news = document.getElementById('newsletterForm');
  if (news) {
    news.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = news.querySelector('input');
      input.value = '';
      input.placeholder = 'You’re on the list — thank you!';
    });
  }
})();

/* ---- Hero video montage (East Africa) ---- */
(function () {
  'use strict';
  var a = document.getElementById('heroVidA');
  var b = document.getElementById('heroVidB');
  if (!a || !b) return;

  // Women's wellness-retreat montage (self-hosted Pexels clips, free to use, no credit needed):
  // friends walking the beach -> yoga at sunset -> safari drive -> elephant -> friends at dusk
  var clips = [
    'assets/videos/hero-1-beach.mp4',
    'assets/videos/hero-2-yoga.mp4',
    'assets/videos/hero-3-safari.mp4',
    'assets/videos/hero-4-elephant.mp4',
    'assets/videos/hero-5-friends.mp4'
  ];

  // Respect reduced-motion, data-saver, and small screens (keep the poster image instead).
  var mq = window.matchMedia || function () { return { matches: false }; };
  var reduce = mq('(prefers-reduced-motion: reduce)').matches;
  var small = mq('(max-width: 767px)').matches;
  var saveData = (navigator.connection && navigator.connection.saveData) || false;
  if (reduce || small || saveData) return;

  var cur = a, nxt = b, i = 0, timer;
  var HOLD = 7000; // cap each clip so every scene appears within one short loop
  function safePlay(el) { var p = el.play(); if (p && p.catch) p.catch(function () {}); }
  function load(el, idx) { el.src = clips[idx]; el.load(); }
  function schedule() { clearTimeout(timer); timer = setTimeout(advance, HOLD); }

  function advance() {
    clearTimeout(timer);
    i = (i + 1) % clips.length;
    nxt.classList.add('is-on');
    safePlay(nxt);
    cur.classList.remove('is-on');
    var old = cur; cur = nxt; nxt = old;
    setTimeout(function () {
      try { old.pause(); } catch (e) {}
      load(nxt, (i + 1) % clips.length); // preload the following clip while hidden
    }, 1500);
    schedule();
  }

  a.addEventListener('ended', advance);
  b.addEventListener('ended', advance);
  a.addEventListener('error', advance);
  b.addEventListener('error', advance);

  // Reveal the first clip the instant it can paint (quick fade), so the poster image
  // isn't lingering — the hero effectively "starts on the video".
  var started = false;
  function revealFirst() {
    if (started) return;
    started = true;
    cur.style.transition = 'opacity .3s ease';
    cur.classList.add('is-on');
    setTimeout(function () { cur.style.transition = ''; }, 450); // restore slow crossfade for later clips
    schedule();
  }
  cur.addEventListener('playing', revealFirst);
  cur.addEventListener('loadeddata', revealFirst);

  load(cur, 0);
  safePlay(cur);
  load(nxt, 1); // preload second clip
})();

/* ---- Prefill "Trip of interest" from ?trip= ---- */
(function () {
  'use strict';
  var el = document.getElementById('trip');
  if (!el) return;
  try {
    var t = new URLSearchParams(window.location.search).get('trip');
    if (t) {
      el.value = t;
      // also seed the message so the enquiry is clearly about this trip
      var msg = document.getElementById('message');
      if (msg && !msg.value) msg.value = "I'd like to enquire about the " + t + '.';
    }
  } catch (e) {}
})();

/* ---- 2027 calendar: filter retreats by region (buttons + region tiles) ---- */
(function () {
  'use strict';
  var grid = document.getElementById('calendarGrid');
  if (!grid) return;
  var cards = grid.querySelectorAll('.retreat');
  var btns = document.querySelectorAll('.cal-filter');
  function apply(region) {
    cards.forEach(function (c) {
      var show = region === 'all' || c.getAttribute('data-region') === region;
      c.classList.toggle('is-hidden', !show);
      if (show) c.classList.add('in');
    });
    btns.forEach(function (b) { b.classList.toggle('is-active', b.getAttribute('data-filter') === region); });
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-filter')); });
  });
  document.querySelectorAll('a.dest[data-region]').forEach(function (a) {
    a.addEventListener('click', function () { apply(a.getAttribute('data-region')); });
  });
})();
