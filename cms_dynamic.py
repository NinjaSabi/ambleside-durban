#!/usr/bin/env python3
"""
Ambleside — CMS Dynamic Integration
Wires News, Our Team, and Testimonials to Decap CMS content
Run from project root: python cms_dynamic.py
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"WROTE: {path}")

# ── SHARED JS ────────────────────────────────────────────────────
SHARED_JS = """
  const REPO = 'NinjaSabi/ambleside-durban';
  const BRANCH = 'main';
  const RAW = `https://raw.githubusercontent.com/${REPO}/${BRANCH}`;
  const API = `https://api.github.com/repos/${REPO}/contents`;

  async function listDir(path) {
    const key = 'ams_' + path;
    const c = sessionStorage.getItem(key);
    if (c) return JSON.parse(c);
    try {
      const r = await fetch(`${API}/${path}`);
      if (!r.ok) return [];
      const d = await r.json();
      sessionStorage.setItem(key, JSON.stringify(d));
      return Array.isArray(d) ? d : [];
    } catch { return []; }
  }

  async function fetchRaw(path) {
    try {
      const r = await fetch(`${RAW}/${path}`);
      return r.ok ? r.text() : null;
    } catch { return null; }
  }

  function parseFM(text) {
    if (!text) return { meta: {}, body: '' };
    const m = text.match(/^---\\r?\\n([\\s\\S]*?)\\r?\\n---\\r?\\n?([\\s\\S]*)$/);
    if (!m) return { meta: {}, body: text };
    const meta = {};
    m[1].split(/\\r?\\n/).forEach(line => {
      const i = line.indexOf(':');
      if (i > -1) {
        const k = line.slice(0, i).trim();
        const v = line.slice(i + 1).trim().replace(/^["']|["']$/g, '');
        if (k) meta[k] = v;
      }
    });
    return { meta, body: m[2].trim() };
  }

  function fmtDate(str) {
    if (!str) return '';
    try {
      return new Date(str).toLocaleDateString('en-ZA', {day:'numeric',month:'long',year:'numeric'});
    } catch { return str; }
  }

  function fadeIn(container) {
    container.querySelectorAll('.fade-up').forEach((el, i) => {
      setTimeout(() => el.classList.add('visible'), i * 80);
    });
  }
"""

# ── SHARED NAV (already updated from Batch 2) ───────────────────
NAV = """<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-logo" aria-label="Ambleside School of Durban — Home">
      <img src="/images/logo-nav.jpg" alt="Ambleside School of Durban" class="nav-logo-img" width="180" height="42" loading="eager" fetchpriority="high">
      <span class="nav-est">Est. 2020</span>
    </a>
    <div class="nav-right">
      <ul class="nav-links">
        <li class="has-dropdown"><a href="/about/">About Us</a>
          <ul class="dropdown">
            <li><a href="/about/our-story/">Our Story</a></li>
            <li><a href="/about/our-values/">Our Values</a></li>
            <li><a href="/about/charlotte-mason/">Our Philosophy</a></li>
            <li><a href="/about/our-team/">Our Team</a></li>
          </ul>
        </li>
        <li class="has-dropdown"><a href="/preschool/">Preschool</a>
          <ul class="dropdown">
            <li><a href="/preschool/what-we-offer/">What We Offer</a></li>
            <li><a href="/preschool/faqs/">FAQs</a></li>
          </ul>
        </li>
        <li class="has-dropdown"><a href="/primary-school/">Primary School</a>
          <ul class="dropdown">
            <li><a href="/primary-school/curriculum/">Curriculum</a></li>
            <li><a href="/primary-school/sport/">Sport &amp; Activities</a></li>
            <li><a href="/primary-school/faqs/">FAQs</a></li>
          </ul>
        </li>
        <li class="has-dropdown"><a href="/admissions/">Admissions</a>
          <ul class="dropdown">
            <li><a href="/admissions/how-to-apply/">How to Apply</a></li>
            <li><a href="/admissions/fees/">Fees 2026</a></li>
            <li><a href="/thursday-enrichment/">Thursday Enrichment</a></li>
          </ul>
        </li>
        <li><a href="/news/">News</a></li>
        <li><a href="/events/">Events</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
      <a href="/admissions/how-to-apply/" class="nav-cta">Apply Now</a>
      <button class="nav-burger" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>
<div class="nav-mobile" role="dialog" aria-label="Mobile navigation">
  <a href="/about/">About Us</a>
  <a href="/about/our-story/" class="mobile-sub">Our Story</a>
  <a href="/about/our-values/" class="mobile-sub">Our Values</a>
  <a href="/about/charlotte-mason/" class="mobile-sub">Our Philosophy</a>
  <a href="/about/our-team/" class="mobile-sub">Our Team</a>
  <a href="/preschool/">Preschool (Acorns)</a>
  <a href="/preschool/what-we-offer/" class="mobile-sub">What We Offer</a>
  <a href="/primary-school/">Primary School</a>
  <a href="/primary-school/curriculum/" class="mobile-sub">Curriculum</a>
  <a href="/primary-school/sport/" class="mobile-sub">Sport &amp; Activities</a>
  <a href="/admissions/">Admissions</a>
  <a href="/admissions/how-to-apply/" class="mobile-sub">How to Apply</a>
  <a href="/admissions/fees/" class="mobile-sub">Fees 2026</a>
  <a href="/thursday-enrichment/" class="mobile-sub">Thursday Enrichment</a>
  <a href="/news/">News</a>
  <a href="/events/">Events</a>
  <a href="/contact/">Contact</a>
  <a href="/admissions/how-to-apply/" class="mobile-cta">Apply Now</a>
</div>"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="/" style="display:inline-block;margin-bottom:1rem;" aria-label="Ambleside School of Durban — Home">
          <img src="/images/logo-stacked.png" alt="Ambleside School of Durban" class="footer-logo-img" width="160" height="88" loading="lazy">
        </a>
        <p class="footer-tagline">Nourishing minds and nurturing character in Durban North, KwaZulu-Natal — a Member School of Ambleside Schools International.</p>
        <img src="/images/footer-asi-white.png" alt="A Member School of Ambleside Schools International" class="footer-asi-badge" width="280" loading="lazy">
        <div class="footer-social" style="margin-top:1.5rem;">
          <a href="https://instagram.com/amblesidedurban" target="_blank" rel="noopener" class="footer-social-btn" aria-label="Instagram">IG</a>
          <a href="https://facebook.com/amblesideschoolofdurban" target="_blank" rel="noopener" class="footer-social-btn" aria-label="Facebook">FB</a>
          <a href="https://youtu.be/ua5DWLBSjXU" target="_blank" rel="noopener" class="footer-social-btn" aria-label="YouTube">YT</a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Our Schools</h4>
        <ul>
          <li><a href="/preschool/">Preschool (Acorns)</a></li>
          <li><a href="/preschool/what-we-offer/">What We Offer</a></li>
          <li><a href="/primary-school/">Primary School (Gr 1–7)</a></li>
          <li><a href="/primary-school/curriculum/">Curriculum</a></li>
          <li><a href="/about/charlotte-mason/">Our Philosophy</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Admissions</h4>
        <ul>
          <li><a href="/admissions/how-to-apply/">How to Apply</a></li>
          <li><a href="/admissions/fees/">Fees 2026</a></li>
          <li><a href="/thursday-enrichment/">Thursday Enrichment</a></li>
          <li><a href="/news/">News</a></li>
          <li><a href="/events/">Events</a></li>
          <li><a href="/school-life/testimonials/">Testimonials</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact Us</h4>
        <address class="footer-address">
          27 Chelsea Drive<br>Durban North, KZN<br><br>
          <a href="tel:0713902182">071 390 2182</a><br>
          <a href="mailto:admin@amblesidedurban.com">admin@amblesidedurban.com</a>
        </address>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <div class="footer-bottom-inner">
        <span>© 2026 Ambleside School of Durban North. All rights reserved.</span>
        <span>Member of Ambleside Schools International</span>
      </div>
    </div>
  </div>
</footer>"""

HEAD = lambda title, desc, canon: f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canon}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://amblesidedurban.com/images/og-home.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="/images/favicon.png">
  <link rel="shortcut icon" href="/images/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Jost:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/global.css">"""

# ════════════════════════════════════════════════════════════════
# 1. NEWS INDEX
# ════════════════════════════════════════════════════════════════
NEWS_INDEX = HEAD(
    "News & Updates — Ambleside Durban North",
    "Latest news and announcements from Ambleside School of Durban — keeping our community informed and connected.",
    "https://amblesidedurban.com/news/"
) + """
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"News","item":"https://amblesidedurban.com/news/"}]}
  </script>
</head>
<body>
""" + NAV + """
<div class="page-header">
  <div class="breadcrumb container"><a href="/">Home</a> <span>›</span> <span>News</span></div>
  <div class="container">
    <div class="label label-white">School News</div>
    <h1>News &amp;<br><em>Updates</em></h1>
    <p>Stories, announcements, and happenings from life at Ambleside.</p>
  </div>
</div>

<section class="section section-bg-warm-white">
  <div class="container">
    <div style="max-width:960px;">
      <style>
        @media(min-width:640px){.news-grid{grid-template-columns:1fr 1fr!important}}
        @media(min-width:960px){.news-grid{grid-template-columns:1fr 1fr 1fr!important}}
        .skel{background:linear-gradient(90deg,var(--cream) 25%,var(--border) 50%,var(--cream) 75%);background-size:200% 100%;animation:shimmer 1.4s infinite;}
        @keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
      </style>

      <!-- Loading skeletons -->
      <div id="news-loading" class="news-grid" style="display:grid;grid-template-columns:1fr;gap:1.5rem;">
        <div class="skel" style="height:280px;"></div>
        <div class="skel" style="height:280px;"></div>
        <div class="skel" style="height:280px;"></div>
      </div>

      <!-- Dynamic content -->
      <div id="news-grid" class="news-grid" style="display:none;grid-template-columns:1fr;gap:1.5rem;"></div>

      <!-- Empty state -->
      <div id="news-empty" style="display:none;padding:3rem 2rem;background:var(--cream);border:1px solid var(--border);text-align:center;">
        <p style="font-family:var(--font-serif);font-size:1.1rem;color:var(--navy);margin-bottom:.6rem;">No news posts yet.</p>
        <p style="font-size:.88rem;color:var(--muted);">Check back soon, or follow us on <a href="https://instagram.com/amblesidedurban" target="_blank" rel="noopener" style="color:var(--navy);">Instagram</a> for updates.</p>
      </div>

      <p style="font-size:.82rem;color:var(--muted);margin-top:2rem;">
        Follow us on <a href="https://instagram.com/amblesidedurban" target="_blank" rel="noopener" style="color:var(--navy);">Instagram</a> and <a href="https://facebook.com/amblesideschoolofdurban" target="_blank" rel="noopener" style="color:var(--navy);">Facebook</a> for regular updates.
      </p>
    </div>
  </div>
</section>

""" + FOOTER + """
<script src="/js/global.js"></script>
<script>
""" + SHARED_JS + """
  (async function() {
    const grid = document.getElementById('news-grid');
    const loading = document.getElementById('news-loading');
    const empty = document.getElementById('news-empty');

    const files = await listDir('_content/news');
    const mdFiles = files
      .filter(f => f.name.endsWith('.md'))
      .sort((a, b) => b.name.localeCompare(a.name))
      .slice(0, 12);

    if (!mdFiles.length) {
      loading.style.display = 'none';
      empty.style.display = 'block';
      return;
    }

    const posts = await Promise.all(mdFiles.map(async (f, i) => {
      const text = await fetchRaw(f.path);
      const { meta } = parseFM(text);
      const slug = f.name.replace('.md', '');
      return { slug, ...meta, _index: i };
    }));

    const delays = ['', ' d1', ' d2'];
    grid.innerHTML = posts.map((p, i) => {
      const imgHtml = p.image
        ? `<img src="${p.image}" alt="${p.title || ''}" style="width:100%;height:100%;object-fit:cover;" loading="lazy">`
        : '';
      return `
        <a href="/news/article/?slug=${p.slug}" class="news-card fade-up${delays[i % 3]}">
          <div class="news-card-image img-placeholder-16-9">${imgHtml}</div>
          <div class="news-card-body">
            <div class="news-card-meta">${fmtDate(p.date)}${p.category ? ' · ' + p.category : ''}</div>
            <div class="news-card-title">${p.title || 'Untitled'}</div>
            <div class="news-card-summary">${p.summary || ''}</div>
          </div>
        </a>`;
    }).join('');

    loading.style.display = 'none';
    grid.style.display = 'grid';
    fadeIn(grid);
  })();
</script>
</body>
</html>"""

write('news/index.html', NEWS_INDEX)

# ════════════════════════════════════════════════════════════════
# 2. NEWS ARTICLE VIEWER
# ════════════════════════════════════════════════════════════════
NEWS_ARTICLE = HEAD(
    "News — Ambleside School of Durban",
    "News and updates from Ambleside School of Durban, Durban North.",
    "https://amblesidedurban.com/news/article/"
) + """
</head>
<body>
""" + NAV + """
<div id="article-header" class="page-header">
  <div class="breadcrumb container"><a href="/">Home</a> <span>›</span> <a href="/news/">News</a> <span>›</span> <span id="breadcrumb-title">Article</span></div>
  <div class="container">
    <div class="label label-white" id="article-category">News</div>
    <h1 id="article-title" style="color:white;">Loading...</h1>
    <p id="article-meta" style="color:rgba(255,255,255,.6);font-size:.88rem;"></p>
  </div>
</div>

<section class="section section-bg-warm-white">
  <div class="container" style="max-width:740px;">
    <div id="article-image" style="margin-bottom:2.5rem;display:none;">
      <img id="article-img" src="" alt="" style="width:100%;height:auto;" loading="eager">
    </div>
    <div id="article-body" style="line-height:1.9;color:var(--text);font-size:1rem;">
      <div style="background:linear-gradient(90deg,var(--cream) 25%,var(--border) 50%,var(--cream) 75%);background-size:200% 100%;animation:shimmer 1.4s infinite;height:400px;"></div>
    </div>
    <div style="margin-top:3rem;padding-top:2rem;border-top:1px solid var(--border);">
      <a href="/news/" class="btn btn-outline">&larr; Back to News</a>
    </div>
  </div>
</section>

<style>
  @keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
  #article-body h2{font-family:var(--font-serif);font-size:1.5rem;color:var(--navy);margin:2rem 0 .8rem;}
  #article-body h3{font-family:var(--font-serif);font-size:1.2rem;color:var(--navy);margin:1.5rem 0 .6rem;}
  #article-body p{margin-bottom:1.2rem;color:var(--muted);}
  #article-body img{max-width:100%;height:auto;margin:1.5rem 0;}
  #article-body ul,#article-body ol{margin:1rem 0 1rem 1.5rem;color:var(--muted);}
  #article-body li{margin-bottom:.4rem;}
  #article-body strong{color:var(--text);font-weight:600;}
  #article-body a{color:var(--navy);text-decoration:underline;}
  #article-body blockquote{border-left:3px solid var(--gold);padding-left:1.5rem;margin:1.5rem 0;font-style:italic;color:var(--muted);}
</style>

""" + FOOTER + """
<script src="/js/global.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@9/marked.min.js"></script>
<script>
""" + SHARED_JS + """
  (async function() {
    const params = new URLSearchParams(window.location.search);
    const slug = params.get('slug');
    if (!slug) { window.location.href = '/news/'; return; }

    const text = await fetchRaw(`_content/news/${slug}.md`);
    if (!text) {
      document.getElementById('article-title').textContent = 'Article not found';
      document.getElementById('article-body').innerHTML = '<p>This article could not be loaded.</p>';
      return;
    }

    const { meta, body } = parseFM(text);

    document.title = (meta.title || 'News') + ' — Ambleside School of Durban';
    document.getElementById('article-title').textContent = meta.title || 'Untitled';
    document.getElementById('breadcrumb-title').textContent = meta.title || 'Article';
    document.getElementById('article-category').textContent = meta.category || 'News';

    const metaParts = [];
    if (meta.date) metaParts.push(fmtDate(meta.date));
    if (meta.author) metaParts.push('By ' + meta.author);
    document.getElementById('article-meta').textContent = metaParts.join(' · ');

    if (meta.image) {
      document.getElementById('article-img').src = meta.image;
      document.getElementById('article-img').alt = meta.title || '';
      document.getElementById('article-image').style.display = 'block';
    }

    document.getElementById('article-body').innerHTML = marked.parse(body || '');
  })();
</script>
</body>
</html>"""

write('news/article/index.html', NEWS_ARTICLE)

# ════════════════════════════════════════════════════════════════
# 3. OUR TEAM — dynamic
# ════════════════════════════════════════════════════════════════
TEAM_PAGE = HEAD(
    "Our Team — Ambleside Durban North",
    "Meet the teachers and staff at Ambleside School of Durban — people who love children, love learning, and are committed to knowing every child personally.",
    "https://amblesidedurban.com/about/our-team/"
) + """
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"About Us","item":"https://amblesidedurban.com/about/"},{"@type":"ListItem","position":2,"name":"Our Team","item":"https://amblesidedurban.com/about/our-team/"}]}
  </script>
  <style>
    .skel{background:linear-gradient(90deg,var(--cream) 25%,var(--border) 50%,var(--cream) 75%);background-size:200% 100%;animation:shimmer 1.4s infinite;}
    @keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
    @media(min-width:560px){.team-grid{grid-template-columns:1fr 1fr!important}}
    @media(min-width:900px){.team-grid{grid-template-columns:repeat(3,1fr)!important}}
  </style>
</head>
<body>
""" + NAV + """
<div class="page-header">
  <div class="breadcrumb container"><a href="/">Home</a> <span>›</span> <a href="/about/">About Us</a> <span>›</span> <span>Our Team</span></div>
  <div class="container">
    <div class="label label-white">Our People</div>
    <h1>Our Team</h1>
    <p>Education happens through relationship. Meet the people who make Ambleside what it is every single day.</p>
  </div>
</div>

<section class="section section-bg-warm-white">
  <div class="container">
    <p class="fade-up" style="max-width:640px;margin-bottom:3.5rem;">Our teachers are people who love children, love learning, and have a deep commitment to giving each child the very best we can offer. At a small school, every relationship matters — and that is exactly how we want it.</p>

    <div style="max-width:1100px;">
      <!-- Loading -->
      <div id="team-loading" class="team-grid" style="display:grid;grid-template-columns:1fr;gap:2rem;">
        <div class="skel" style="height:320px;"></div>
        <div class="skel" style="height:320px;"></div>
        <div class="skel" style="height:320px;"></div>
      </div>
      <!-- Dynamic grid -->
      <div id="team-grid" class="team-grid" style="display:none;grid-template-columns:1fr;gap:2rem;"></div>
      <!-- Empty -->
      <div id="team-empty" style="display:none;padding:2rem;background:var(--cream);">
        <p style="color:var(--muted);">Team profiles coming soon.</p>
      </div>
    </div>

    <div style="margin-top:3rem;display:flex;gap:1rem;flex-wrap:wrap;" class="fade-up">
      <a href="/contact/" class="btn btn-primary">Book a School Visit</a>
      <a href="/about/our-story/" class="btn btn-outline">Our Story</a>
    </div>
  </div>
</section>

""" + FOOTER + """
<script src="/js/global.js"></script>
<script>
""" + SHARED_JS + """
  (async function() {
    const grid = document.getElementById('team-grid');
    const loading = document.getElementById('team-loading');
    const empty = document.getElementById('team-empty');

    const files = await listDir('_content/team');
    const mdFiles = files.filter(f => f.name.endsWith('.md'));

    if (!mdFiles.length) {
      loading.style.display = 'none';
      empty.style.display = 'block';
      return;
    }

    const members = await Promise.all(mdFiles.map(async f => {
      const text = await fetchRaw(f.path);
      const { meta, body } = parseFM(text);
      return { ...meta, bio: body };
    }));

    members.sort((a, b) => (parseInt(a.order) || 99) - (parseInt(b.order) || 99));

    const delays = ['', ' d1', ' d2'];
    grid.innerHTML = members.map((m, i) => {
      const imgHtml = m.image
        ? `<img src="${m.image}" alt="${m.title || ''}" loading="lazy">`
        : '';
      const bioHtml = m.bio
        ? `<p style="font-size:.85rem;line-height:1.8;text-align:left;">${m.bio.replace(/^["']|["']$/g,'')}</p>`
        : `<p style="font-size:.85rem;line-height:1.8;text-align:left;color:var(--muted);font-style:italic;">Bio coming soon.</p>`;
      return `
        <div class="card fade-up${delays[i % 3]}" style="text-align:center;padding:2.5rem 2rem;">
          <div class="team-photo-wrap">${imgHtml}</div>
          <h4 style="margin-bottom:.25rem;color:var(--navy);">${m.title || ''}</h4>
          <div style="font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem;">${m.role || ''}</div>
          ${bioHtml}
        </div>`;
    }).join('');

    loading.style.display = 'none';
    grid.style.display = 'grid';
    fadeIn(grid);
  })();
</script>
</body>
</html>"""

write('about/our-team/index.html', TEAM_PAGE)

# ════════════════════════════════════════════════════════════════
# 4. TESTIMONIALS — dynamic
# ════════════════════════════════════════════════════════════════
TEST_PAGE = HEAD(
    "Testimonials — What Families Say About Ambleside Durban North",
    "What parents say about Ambleside School of Durban — testimonials from families who have chosen a Charlotte Mason education for their children in Durban North, KZN.",
    "https://amblesidedurban.com/school-life/testimonials/"
) + """
  <style>
    .skel{background:linear-gradient(90deg,var(--cream) 25%,var(--border) 50%,var(--cream) 75%);background-size:200% 100%;animation:shimmer 1.4s infinite;}
    @keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
    @media(min-width:640px){.test-grid{grid-template-columns:1fr 1fr!important}}
  </style>
</head>
<body>
""" + NAV + """
<div class="page-header">
  <div class="breadcrumb container"><a href="/">Home</a> <span>›</span> <a href="/school-life/">School Life</a> <span>›</span> <span>Testimonials</span></div>
  <div class="container">
    <div class="label label-white">School Life</div>
    <h1>What Our Families<br><em>Are Saying</em></h1>
    <p>The best endorsement of Ambleside is the families who have chosen it.</p>
  </div>
</div>

<section class="section section-bg-warm-white">
  <div class="container">
    <div style="max-width:960px;">
      <!-- Loading -->
      <div id="test-loading" class="test-grid" style="display:grid;grid-template-columns:1fr;gap:1.5rem;">
        <div class="skel" style="height:180px;"></div>
        <div class="skel" style="height:180px;"></div>
        <div class="skel" style="height:180px;"></div>
        <div class="skel" style="height:180px;"></div>
      </div>
      <!-- Dynamic grid -->
      <div id="test-grid" class="test-grid" style="display:none;grid-template-columns:1fr;gap:1.5rem;"></div>
      <!-- Empty -->
      <div id="test-empty" style="display:none;padding:2rem;background:var(--cream);">
        <p style="color:var(--muted);">Testimonials coming soon.</p>
      </div>
    </div>
    <div style="margin-top:3rem;display:flex;gap:1rem;flex-wrap:wrap;" class="fade-up">
      <a href="/contact/" class="btn btn-primary">Book a School Visit</a>
      <a href="/admissions/how-to-apply/" class="btn btn-outline">Apply Now</a>
    </div>
  </div>
</section>

""" + FOOTER + """
<script src="/js/global.js"></script>
<script>
""" + SHARED_JS + """
  (async function() {
    const grid = document.getElementById('test-grid');
    const loading = document.getElementById('test-loading');
    const empty = document.getElementById('test-empty');

    const files = await listDir('_content/testimonials');
    const mdFiles = files.filter(f => f.name.endsWith('.md'));

    if (!mdFiles.length) {
      loading.style.display = 'none';
      empty.style.display = 'block';
      return;
    }

    const items = await Promise.all(mdFiles.map(async f => {
      const text = await fetchRaw(f.path);
      const { meta } = parseFM(text);
      return meta;
    }));

    items.sort((a, b) => (parseInt(a.order) || 99) - (parseInt(b.order) || 99));

    const delays = ['', ' d1', ' d2', ' d3'];
    grid.innerHTML = items.map((t, i) => `
      <div class="card fade-up${delays[i % 4]}" style="position:relative;">
        <div style="font-family:var(--font-serif);font-size:5rem;line-height:.7;color:rgba(0,56,101,.06);position:absolute;top:1rem;left:1.2rem;">"</div>
        <p style="font-family:var(--font-serif);font-style:italic;font-size:.95rem;line-height:1.8;color:var(--text);margin-bottom:1.2rem;position:relative;z-index:1;">"${t.quote || ''}"</p>
        <div style="font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--brown);">${t.author || ''}</div>
      </div>`).join('');

    loading.style.display = 'none';
    grid.style.display = 'grid';
    fadeIn(grid);
  })();
</script>
</body>
</html>"""

write('school-life/testimonials/index.html', TEST_PAGE)

# ════════════════════════════════════════════════════════════════
# 5. SEED FILES — Team members
# ════════════════════════════════════════════════════════════════
TEAM_SEEDS = [
    ("kim", 1, "Kim", "Head of School", "Leadership", "/images/team-kim.jpg",
     '"Children\'s innate love of learning is protected and grown at Ambleside — deepening their character and setting them up for success and excellence in godliness and in life."'),
    ("naomi", 2, "Naomi", "Director of Philosophy", "Leadership", "/images/team-naomi.jpg", ""),
    ("liza", 3, "Liza", "Yellowwoods Teacher · Gr 3–4", "Junior School", "/images/team-liza.jpg",
     '"I love how the method at Ambleside views children as whole persons — not empty vessels to be filled with answers for tomorrow\'s test, but filled with curiosity and delight, able to find joy even through struggle. The aim of an Ambleside education is growth."'),
    ("jo", 4, "Jo", "Music Teacher", "Junior School", "/images/team-jo.jpg",
     '"It is an absolute delight to teach the Kodály method of music to all the children at our school. It dovetails beautifully with their music appreciation and composer studies."'),
    ("faith", 5, "Faith", "Acorns Preschool Teacher", "Preschool — Acorns", "/images/team-faith.jpg",
     '"I love the Ambleside curriculum because it is calm, Christ-centred, and helps children learn by retelling stories — building a genuine love of learning from the very beginning."'),
    ("terri-anne", 6, "Terri-Anne", "Administrator", "Administration", "/images/team-terri-anne.jpg", ""),
]

for slug, order, name, role, dept, img, bio in TEAM_SEEDS:
    content = f"""---
title: {name}
role: {role}
department: {dept}
image: {img}
order: {order}
---
{bio}"""
    write(f"_content/team/{slug}.md", content)

# ════════════════════════════════════════════════════════════════
# 6. SEED FILES — Testimonials
# ════════════════════════════════════════════════════════════════
TESTIMONIAL_SEEDS = [
    (1, "Each morning he's up, dressed, and ready to go. He loves school — and for a parent, there is no greater gift than a child who is genuinely excited to learn.", "Parent — Grade 000 Student", True),
    (2, "Ambleside taught me the value of learning — not for the sake of a grade, but for the privilege of growing in understanding. I carry that with me every day.", "Parent — Grade 7 Graduate", True),
    (3, "The teachers here actually know my daughter. They know what makes her laugh, what she's capable of, what she's working through. That kind of knowledge is extraordinary.", "Parent — Primary School", True),
    (4, "We looked at many schools before choosing Ambleside. What struck us immediately was the warmth — not just of the teachers, but of the children toward each other. That comes from the top.", "Parent — Preschool & Primary School", False),
    (5, "My son came home after his first week at Ambleside and said, 'Mum, I actually like school now.' That sentence made every difficult decision worth it.", "Parent — Grade 4 Student", False),
    (6, "The breadth of the curriculum surprised us. Our daughter is studying history, literature, science, music, Afrikaans, isiZulu, art, and maths — all with genuine depth. This is not a narrow education.", "Parent — Grade 6 Student", False),
]

for order, quote, author, featured in TESTIMONIAL_SEEDS:
    content = f"""---
quote: "{quote}"
author: "{author}"
featured: {"true" if featured else "false"}
order: {order}
---"""
    slug = f"testimonial-{order:02d}"
    write(f"_content/testimonials/{slug}.md", content)

print("\n" + "="*60)
print("CMS DYNAMIC INTEGRATION — COMPLETE")
print("="*60)
print("Pages updated: news, news/article, about/our-team, school-life/testimonials")
print("Seed files created: 6 team members, 6 testimonials")
print("\nNext steps:")
print("1. git add -A && git commit -m 'CMS dynamic: news, team, testimonials'")
print("2. git push origin main")
print("3. Wait 60s for Netlify to deploy")
print("4. Test /news/ — should show empty state (no CMS posts yet)")
print("5. Test /about/our-team/ — should show all 6 team members")
print("6. Test /school-life/testimonials/ — should show all 6 testimonials")
