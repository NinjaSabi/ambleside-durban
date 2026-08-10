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
    mobileMenu.setAttribute('aria-modal', 'true');
    const focusables = () => mobileMenu.querySelectorAll('a[href]');
    const closeMenu = (returnFocus) => {
      mobileMenu.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      if (returnFocus) burger.focus();
    };
    const openMenu = () => {
      mobileMenu.classList.add('open');
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
      const f = focusables();
      if (f.length) f[0].focus();
    };
    burger.addEventListener('click', () => {
      if (mobileMenu.classList.contains('open')) closeMenu(true); else openMenu();
    });
    // Close on nav link click (keep focus on the page the link loads)
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => closeMenu(false));
    });
    // Escape closes; Tab is trapped inside the open menu
    mobileMenu.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { closeMenu(true); return; }
      if (e.key !== 'Tab') return;
      const f = focusables();
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ── SCROLL FADE ANIMATIONS ── */
  const fadeEls = document.querySelectorAll('.fade-up, .heading-reveal');
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
      var d = document.createElement('button');
      d.type = 'button';
      d.setAttribute('aria-label', 'Go to item ' + (i + 1) + ' of ' + count);
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
      dots.querySelectorAll('button').forEach(function(d, i) {
        d.classList.toggle('active', i === active);
      });
    }, { passive: true });
  });

});

/* ── PAGE-TRANSITION FADE (progressive enhancement) ──
   Skips reduced-motion users, external links, and modified/non-primary
   clicks so "open in new tab" (Ctrl/Cmd/middle-click) keeps working. */
var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!prefersReducedMotion) {
  document.querySelectorAll('a[href]').forEach(function(link) {
    var href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto') || href.startsWith('tel') || link.target) return;
    if (link.origin && link.origin !== window.location.origin) return; // external link
    link.addEventListener('click', function(e) {
      // Let the browser handle new-tab / modified / non-primary clicks natively.
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      document.body.style.transition = 'opacity 0.25s ease';
      document.body.style.opacity = '0';
      setTimeout(function() { window.location.href = href; }, 260);
    });
  });
}
