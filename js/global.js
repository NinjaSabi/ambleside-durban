/* Ambleside — global.js */

document.addEventListener('DOMContentLoaded', () => {

  /* ── NAV SCROLL SHADOW ── */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── MOBILE HAMBURGER ── */
  const burger = document.querySelector('.nav-burger');
  const mobileMenu = document.querySelector('.nav-mobile');
  if (burger && mobileMenu) {
    burger.addEventListener('click', () => {
      const open = mobileMenu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    // Close on nav link click
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        burger.setAttribute('aria-expanded', false);
        document.body.style.overflow = '';
      });
    });
  }

  /* ── SCROLL FADE ANIMATIONS ── */
  const fadeEls = document.querySelectorAll('.fade-up');
  if (fadeEls.length) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          obs.unobserve(e.target);
        }
      });
    }, { threshold: 0.1 });
    fadeEls.forEach(el => obs.observe(el));
  }

  /* ── ACTIVE NAV LINK ── */
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a, .nav-mobile a').forEach(a => {
    if (a.getAttribute('href') === path ||
        (path !== '/' && path.startsWith(a.getAttribute('href')))) {
      a.style.color = 'var(--navy)';
      a.style.fontWeight = '600';
    }
  });

  /* ── HORIZONTAL SCROLL DOTS ── */
  document.querySelectorAll('.cards-scroll').forEach(function(container) {
    var dots = container.nextElementSibling;
    if (!dots || !dots.classList.contains('scroll-dots')) return;
    var items = container.children;
    var count = items.length;

    // Build dots
    dots.innerHTML = '';
    for (var i = 0; i < count; i++) {
      var d = document.createElement('span');
      if (i === 0) d.classList.add('active');
      (function(idx) {
        d.addEventListener('click', function() {
          items[idx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
        });
      })(i);
      dots.appendChild(d);
    }

    // Update active dot on scroll
    container.addEventListener('scroll', function() {
      var scrollLeft = container.scrollLeft;
      var width = container.offsetWidth;
      var active = Math.round(scrollLeft / (width * 0.78));
      dots.querySelectorAll('span').forEach(function(d, i) {
        d.classList.toggle('active', i === active);
      });
    }, { passive: true });
  });

});
