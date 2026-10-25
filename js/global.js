/* Ambleside — global.js */

/* ── CONTACT BAR (phones) + contact rows in the mobile menu ──
   One place for the school's phone, WhatsApp and visit booking, so every page
   gets them without editing 25 hand-copied navs. The WhatsApp message differs
   from the Meta ad's ("I saw your ad on Facebook") so the school can tell a
   website chat from an ad chat. */
var CONTACT = {
  tel: 'tel:+27713902182',
  telLabel: '071 390 2182',
  whatsapp: 'https://wa.me/27713902182?text=' +
    encodeURIComponent('Hi, I found Ambleside on your website and would like to know more.'),
  visit: 'https://cal.com/ambleside/visit'
};
var CONTACT_ICONS = {
  call: '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
  wa: '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
  visit: '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'
};

function contactLink(kind, cls) {
  var items = {
    call:  { href: CONTACT.tel,      text: 'Call',         label: 'Call the school on ' + CONTACT.telLabel, ext: false },
    wa:    { href: CONTACT.whatsapp, text: 'WhatsApp',     label: 'WhatsApp the school',                    ext: true },
    visit: { href: CONTACT.visit,    text: 'Book a visit', label: 'Book a school visit',                    ext: true }
  };
  var it = items[kind];
  var a = document.createElement('a');
  a.href = it.href;
  a.className = cls + ' ' + cls + '--' + kind;
  a.setAttribute('aria-label', it.label);
  if (it.ext) { a.target = '_blank'; a.rel = 'noopener'; }
  a.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" ' +
    'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' +
    CONTACT_ICONS[kind] + '</svg><span>' + it.text + '</span>';
  return a;
}

function injectContactBar() {
  if (window.location.pathname.indexOf('/admin') === 0) return;

  var bar = document.createElement('nav');
  bar.className = 'contact-bar';
  bar.setAttribute('aria-label', 'Contact the school');
  ['call', 'wa', 'visit'].forEach(function(k) { bar.appendChild(contactLink(k, 'contact-bar__link')); });
  document.body.appendChild(bar);
  document.body.classList.add('has-contact-bar');

  var menu = document.querySelector('.nav-mobile');
  if (menu) {
    var rows = document.createElement('div');
    rows.className = 'mobile-contact';
    ['call', 'wa', 'visit'].forEach(function(k) { rows.appendChild(contactLink(k, 'mobile-contact__link')); });
    menu.insertBefore(rows, menu.firstChild);
  }
}

document.addEventListener('DOMContentLoaded', () => {

  /* Runs first so the menu's focus trap and close-on-click include the new links */
  injectContactBar();

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
