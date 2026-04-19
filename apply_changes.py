#!/usr/bin/env python3
"""
Ambleside School of Durban — Batch 2 Changes
Run from the project root:  python apply_changes.py
"""
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
log = []

def read(path):
    with open(os.path.join(BASE, path), 'r', encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(os.path.join(BASE, path), 'w', encoding='utf-8') as f:
        f.write(content)

def apply(path, *pairs):
    """Apply (old, new) replacement pairs to a file."""
    try:
        c = read(path)
        orig = c
        misses = []
        for old, new in pairs:
            if old in c:
                c = c.replace(old, new, 1)
            else:
                misses.append(old[:60].replace('\n', ' '))
        write(path, c)
        status = "CHANGED" if c != orig else "NO-CHANGE"
        log.append(f"{status}: {path}")
        for m in misses:
            log.append(f"  MISS (already applied or typo): {m}...")
    except FileNotFoundError:
        log.append(f"NOT-FOUND: {path}")
    except Exception as e:
        log.append(f"ERROR {e}: {path}")

# ════════════════════════════════════════════════════════════════
# SHARED SNIPPETS
# ════════════════════════════════════════════════════════════════
FOOTER_OLD = (
    '          <li><a href="/primary-school/">Primary School (Gr 1\u20137)</a></li>\n'
    '          <li><a href="/primary-school/curriculum/">Curriculum</a></li>\n'
    '          <li><a href="/preschool/">Preschool \u2014 Acorns</a></li>\n'
    '          <li><a href="/preschool/what-we-offer/">What We Offer</a></li>\n'
    '          <li><a href="/about/charlotte-mason/">Our Philosophy</a></li>'
)
FOOTER_NEW = (
    '          <li><a href="/preschool/">Preschool (Acorns)</a></li>\n'
    '          <li><a href="/preschool/what-we-offer/">What We Offer</a></li>\n'
    '          <li><a href="/primary-school/">Primary School (Gr 1\u20137)</a></li>\n'
    '          <li><a href="/primary-school/curriculum/">Curriculum</a></li>\n'
    '          <li><a href="/about/charlotte-mason/">Our Philosophy</a></li>'
)
MOB_OLD = '<a href="/preschool/">Preschool \u2014 Acorns</a>'
MOB_NEW = '<a href="/preschool/">Preschool (Acorns)</a>'

# Nav dropdown — add Thursday Enrichment under Admissions
ADM_DROP_OLD = (
    '          <ul class="dropdown">\n'
    '            <li><a href="/admissions/how-to-apply/">How to Apply</a></li>\n'
    '            <li><a href="/admissions/fees/">Fees 2026</a></li>\n'
    '          </ul>'
)
ADM_DROP_NEW = (
    '          <ul class="dropdown">\n'
    '            <li><a href="/admissions/how-to-apply/">How to Apply</a></li>\n'
    '            <li><a href="/admissions/fees/">Fees 2026</a></li>\n'
    '            <li><a href="/thursday-enrichment/">Thursday Enrichment</a></li>\n'
    '          </ul>'
)
MOB_ADM_OLD = (
    '  <a href="/admissions/">Admissions</a>\n'
    '  <a href="/admissions/how-to-apply/" class="mobile-sub">How to Apply</a>\n'
    '  <a href="/admissions/fees/" class="mobile-sub">Fees 2026</a>'
)
MOB_ADM_NEW = (
    '  <a href="/admissions/">Admissions</a>\n'
    '  <a href="/admissions/how-to-apply/" class="mobile-sub">How to Apply</a>\n'
    '  <a href="/admissions/fees/" class="mobile-sub">Fees 2026</a>\n'
    '  <a href="/thursday-enrichment/" class="mobile-sub">Thursday Enrichment</a>'
)
FOOTER_ADM_OLD = (
    '          <li><a href="/admissions/how-to-apply/">How to Apply</a></li>\n'
    '          <li><a href="/admissions/fees/">Fees 2026</a></li>\n'
    '          <li><a href="/news/">News</a></li>'
)
FOOTER_ADM_NEW = (
    '          <li><a href="/admissions/how-to-apply/">How to Apply</a></li>\n'
    '          <li><a href="/admissions/fees/">Fees 2026</a></li>\n'
    '          <li><a href="/thursday-enrichment/">Thursday Enrichment</a></li>\n'
    '          <li><a href="/news/">News</a></li>'
)

def base_pairs():
    """Common pairs applied to every page."""
    return [
        (FOOTER_OLD, FOOTER_NEW),
        (MOB_OLD, MOB_NEW),
        (ADM_DROP_OLD, ADM_DROP_NEW),
        (MOB_ADM_OLD, MOB_ADM_NEW),
        (FOOTER_ADM_OLD, FOOTER_ADM_NEW),
    ]

# ════════════════════════════════════════════════════════════════
# 1. OUR STORY — remaining changes (lede + school name done via edit_file)
# ════════════════════════════════════════════════════════════════
apply('about/our-story/index.html',
    *base_pairs(),
    # CM quote — all three terms
    (
        'By \u201cdiscipline\u201d Mason did not mean punishment or rigidity \u2014 she meant the formation of good habits: of attention, of honesty, of perseverance. These habits, she believed, are the quiet engine of a well-lived life.',
        'By <em>\u201catmosphere\u201d</em> Mason meant the living environment in which a child learns \u2014 the tone, the relationships, and the spirit of the home and school. By <em>\u201cdiscipline\u201d</em> she did not mean punishment or rigidity, but the formation of good habits: of attention, honesty, and perseverance. And by <em>\u201clife\u201d</em> she meant that education is not a preparation for living \u2014 it is living itself, encountered through real ideas, real books, and real relationships.'
    ),
    # coherent → cohesive
    ('is coherent, warm, and deeply intentional.', 'is cohesive, warm, and deeply intentional.'),
    # Preschool naming in body
    ('Ambleside Preschool \u2014 <em>Acorns</em> for children', 'Ambleside Preschool (Acorns) for children'),
)

# ════════════════════════════════════════════════════════════════
# 2. OUR VALUES
# ════════════════════════════════════════════════════════════════
apply('about/our-values/index.html',
    *base_pairs(),
    # Character over credentials — reword
    (
        '<p>We care deeply about academic excellence \u2014 but we care more about who our students are becoming, because we believe character will ultimately have greater and longer-lasting value. Diligence, honesty, kindness, courage, and a genuine love of learning are the outcomes we measure ourselves against. Small classes make real character formation possible.</p>',
        '<p>We pursue excellence in both character and academics \u2014 because we believe the two are inseparable. Diligence, honesty, kindness, and courage are not soft alternatives to academic rigour; they are the very qualities that make genuine learning possible. Small classes allow us to hold both well, knowing every child by name and nurturing who they are becoming alongside what they know.</p>'
    ),
    # Families are partners — reword
    (
        '<p>Education is a whole-family journey. We keep our partnership with parents warm, honest, and mutual \u2014 sharing regularly, listening carefully, and treating parents as essential participants in their child\'s formation, not merely as observers.</p>',
        '<p>We believe that parents are the primary educators of their children \u2014 and we take that seriously. Our role is to come alongside you, not replace you. We actively partner with families in both the education and formation of each child, sharing openly, listening carefully, and keeping the relationship warm, honest, and genuinely mutual.</p>'
    ),
)

# ════════════════════════════════════════════════════════════════
# 3. CHARLOTTE MASON — reorder cards + school name in body
# ════════════════════════════════════════════════════════════════
apply('about/charlotte-mason/index.html',
    *base_pairs(),
    # School name in body
    (
        'At Ambleside Durban North, we believe the best education we can give',
        'At Ambleside School of Durban, we believe the best education we can give'
    ),
    # Card reorder: Atmosphere & Habit first, A Broad Curriculum second, then rest
    (
        '      <div class="card fade-up">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Living Books</h4>\n        <p style="font-size:.88rem;">We use books written by authors who genuinely love their subjects \u2014 people who write with care and passion. When a child reads such a book, they encounter a real mind engaging with real ideas, and that encounter forms lasting understanding.</p>\n      </div>\n      <div class="card fade-up d1">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Narration</h4>\n        <p style="font-size:.88rem;">After reading or listening, children narrate \u2014 they tell back, in their own words, what they have encountered. This is not a test. It is the act of making something your own. Narration builds comprehension, develops memory, trains clear thinking, and gives children a genuine voice.</p>\n      </div>\n      <div class="card fade-up d2">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Nature Study</h4>\n        <p style="font-size:.88rem;">Children spend regular time outdoors, keeping nature notebooks and learning to observe the world with care. The habit of careful attention \u2014 developed through looking closely at a bird, a plant, or a cloud \u2014 underpins all good scientific thinking and makes the world endlessly interesting.</p>\n      </div>\n      <div class="card fade-up d3">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Composer &amp; Picture Study</h4>\n        <p style="font-size:.88rem;">Each term, children spend unhurried time with one composer and one visual artist \u2014 listening carefully to music, looking closely at paintings, and learning to receive beauty thoughtfully. Over time, this develops a genuine aesthetic sensibility: the capacity to be moved and changed by what is beautiful.</p>\n      </div>\n      <div class="card fade-up">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">A Broad Curriculum</h4>\n        <p style="font-size:.88rem;">History, literature, science, languages, mathematics, art, music, handwork \u2014 all of it, taken seriously. We offer a wide and generous curriculum because children are capable of engaging with the richness of human knowledge and experience. A narrow diet does not serve them well.</p>\n      </div>\n      <div class="card fade-up d1">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Atmosphere &amp; Habit</h4>\n        <p style="font-size:.88rem;">The environment in which children learn matters deeply. A calm, ordered, warm atmosphere is the soil in which real learning takes root. Equally, the habits children form \u2014 of attention, honesty, perseverance \u2014 shape who they become far more than any single lesson. We attend to both, every day.</p>\n      </div>',
        '      <div class="card fade-up">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Atmosphere &amp; Habit</h4>\n        <p style="font-size:.88rem;">The environment in which children learn matters deeply. A calm, ordered, warm atmosphere is the soil in which real learning takes root. Equally, the habits children form \u2014 of attention, honesty, perseverance \u2014 shape who they become far more than any single lesson. We attend to both, every day.</p>\n      </div>\n      <div class="card fade-up d1">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">A Broad Curriculum</h4>\n        <p style="font-size:.88rem;">History, literature, science, languages, mathematics, art, music, handwork \u2014 all of it, taken seriously. We offer a wide and generous curriculum because children are capable of engaging with the richness of human knowledge and experience. A narrow diet does not serve them well.</p>\n      </div>\n      <div class="card fade-up d2">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Living Books</h4>\n        <p style="font-size:.88rem;">We use books written by authors who genuinely love their subjects \u2014 people who write with care and passion. When a child reads such a book, they encounter a real mind engaging with real ideas, and that encounter forms lasting understanding.</p>\n      </div>\n      <div class="card fade-up d3">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Narration</h4>\n        <p style="font-size:.88rem;">After reading or listening, children narrate \u2014 they tell back, in their own words, what they have encountered. This is not a test. It is the act of making something your own. Narration builds comprehension, develops memory, trains clear thinking, and gives children a genuine voice.</p>\n      </div>\n      <div class="card fade-up">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Nature Study</h4>\n        <p style="font-size:.88rem;">Children spend regular time outdoors, keeping nature notebooks and learning to observe the world with care. The habit of careful attention \u2014 developed through looking closely at a bird, a plant, or a cloud \u2014 underpins all good scientific thinking and makes the world endlessly interesting.</p>\n      </div>\n      <div class="card fade-up d1">\n        <h4 style="color:var(--navy);margin-bottom:.6rem;">Composer &amp; Picture Study</h4>\n        <p style="font-size:.88rem;">Each term, children spend unhurried time with one composer and one visual artist \u2014 listening carefully to music, looking closely at paintings, and learning to receive beauty thoughtfully. Over time, this develops a genuine aesthetic sensibility: the capacity to be moved and changed by what is beautiful.</p>\n      </div>'
    ),
)

# ════════════════════════════════════════════════════════════════
# 4. CONTACT
# ════════════════════════════════════════════════════════════════
apply('contact/index.html',
    *base_pairs(),
    # h1 — single line
    ('<h1>Contact<br><em>Us</em></h1>', '<h1 class="contact-h1">Contact Us</h1>'),
    # "Prefer to write?"
    ('Prefer to write? Fill in the form below', 'Prefer to drop us a message? Fill in the form below'),
    # Book a School Visit — Thursday Open Days
    (
        '<p style="font-size:.9rem;margin-bottom:1.5rem;">The best way to know whether Ambleside is right for your family is to come and experience it. We schedule visits on school days so you can see the school in action.</p>',
        '<p style="font-size:.9rem;margin-bottom:.8rem;">The best way to know whether Ambleside is right for your family is to come and experience it in action. We host <strong>Thursday Open Days</strong> every week during term, with two sessions available:</p>\n          <ul style="font-size:.88rem;color:var(--muted);margin:.6rem 0 .8rem 1rem;display:flex;flex-direction:column;gap:.3rem;list-style:disc;">\n            <li><strong>Morning:</strong> 07:30 \u2013 10:30</li>\n            <li><strong>Midday:</strong> 12:00 \u2013 13:30</li>\n          </ul>\n          <p style="font-size:.88rem;color:var(--muted);margin-bottom:1.5rem;">If Thursdays don\u2019t work for you, use the enquiry form below and we\u2019ll arrange a time that suits.</p>'
    ),
    # Schema office hours
    ('"opens":"07:30","closes":"16:00"', '"opens":"07:45","closes":"14:00"'),
)

# ════════════════════════════════════════════════════════════════
# 5. HOW TO APPLY
# ════════════════════════════════════════════════════════════════
apply('admissions/how-to-apply/index.html',
    *base_pairs(),
    # Step 0 label
    ('<div class="label label-brown">Not Ready Yet?</div>', '<div class="label label-brown">Take a Look Around First?</div>'),
    # Step 0 body
    (
        '<p>Not sure if Ambleside is right for your family? That is completely fine \u2014 and we would love to help you find out. You can send us a question using the form at the bottom of this page, or take a virtual tour via our YouTube channel to get a feel for who we are before committing to a visit. There is no obligation, and no question is too small.</p>\n          <div style="margin-top:1rem;display:flex;gap:1rem;flex-wrap:wrap;">\n            <a href="https://youtu.be/nSeaLk3kbOU" target="_blank" rel="noopener" class="btn btn-outline" style="font-size:.78rem;">Take a Virtual Tour</a>\n          </div>',
        '<p>Not sure if Ambleside is right for your family? That is completely fine \u2014 and we would love to help you find out. You can send us a question using the form below, or join us for a <strong>Thursday Open Day</strong> to experience the school before committing to a visit. There is no obligation, and no question is too small.</p>\n          <div style="margin-top:1rem;display:flex;gap:1rem;flex-wrap:wrap;">\n            <a href="https://cal.com/ambleside/visit" target="_blank" rel="noopener" class="btn btn-outline" style="font-size:.78rem;">Join a Thursday Open Day</a>\n            <a href="https://youtu.be/nSeaLk3kbOU" target="_blank" rel="noopener" class="btn btn-outline" style="font-size:.78rem;">Virtual Tour</a>\n          </div>'
    ),
    # Step 1 body — Thursday Open Days
    (
        '<p>The best way to know whether Ambleside is right for your family is to come and experience it. We warmly invite all prospective families to visit \u2014 meet our teachers, see our classrooms, ask your questions, and get a feel for the Ambleside community. We schedule visits on school days so you can see the school in action. There is no obligation whatsoever.</p>\n          <p style="margin-top:.8rem;"><a href="/contact/" style="color:var(--navy);font-weight:600;">Book your visit here \u2192</a></p>',
        '<p>We host <strong>Weekly Open Days every Thursday</strong> during term so you can see the school in action, meet our teachers, and ask every question you have. Two sessions available:</p>\n          <ul style="font-size:.88rem;color:var(--muted);margin:.6rem 0 .8rem 1rem;display:flex;flex-direction:column;gap:.3rem;list-style:disc;">\n            <li><strong>Morning:</strong> 07:30 \u2013 10:30</li>\n            <li><strong>Midday:</strong> 12:00 \u2013 13:30</li>\n          </ul>\n          <p style="font-size:.88rem;color:var(--muted);">If Thursdays don\u2019t work for you, send us an enquiry below and we\u2019ll arrange an alternative.</p>\n          <p style="margin-top:.8rem;"><a href="/contact/" style="color:var(--navy);font-weight:600;">Book a Thursday visit \u2192</a></p>'
    ),
)

# ════════════════════════════════════════════════════════════════
# 6. FEES
# ════════════════════════════════════════════════════════════════
apply('admissions/fees/index.html',
    *base_pairs(),
    (
        '<span style="font-size:.88rem;max-width:360px;text-align:right;">Small, occasional contributions may be requested for school outings, termly Food Fridays, and the annual Market Day. These are kept modest and communicated well in advance.</span>',
        '<span style="font-size:.88rem;max-width:360px;text-align:right;">Termly school outings are invoiced separately at a modest cost communicated in advance. Food Fridays are an optional, fun termly tradition \u2014 entirely at the family\u2019s discretion. Market Day is part of the school calendar and included in the school experience.</span>'
    ),
)

# ════════════════════════════════════════════════════════════════
# 7. PRESCHOOL WHAT WE OFFER — emojis → SVG icons
# ════════════════════════════════════════════════════════════════
ICON = {
    '\U0001f3ae': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="7" width="20" height="15" rx="2"/><polyline points="17 2 12 7 7 2"/></svg>',
    '\U0001f4da': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    '\U0001f3ca': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12c2 0 3-1.5 3-3s-1-3-3-3m20 6c-2 0-3-1.5-3-3s1-3 3-3m-7 6c-2 0-3-1.5-3-3s1-3 3-3-3 1.5-3 3 1 3 3 3"/><circle cx="19" cy="4" r="2"/></svg>',
    '\U0001f522': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/><line x1="10" y1="3" x2="8" y2="21"/><line x1="16" y1="3" x2="14" y2="21"/></svg>',
    '\U0001f5e3\ufe0f': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    '\U0001f3a8': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13.5" cy="6.5" r="2.5"/><path d="M17 12h2a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h2"/><path d="M9 12V7l-2 2m4-2 2 2"/></svg>',
    '\U0001f33f': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22V12"/><path d="M5 12c0-4 3.13-8 7-8 3.87 0 7 4 7 8H5z"/><path d="M9 22h6"/></svg>',
    '\u271d\ufe0f': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><line x1="12" y1="2" x2="12" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/></svg>',
}

try:
    c = read('preschool/what-we-offer/index.html')
    orig = c
    c = c.replace(FOOTER_OLD, FOOTER_NEW, 1)
    c = c.replace(MOB_OLD, MOB_NEW, 1)
    c = c.replace(ADM_DROP_OLD, ADM_DROP_NEW, 1)
    c = c.replace(MOB_ADM_OLD, MOB_ADM_NEW, 1)
    c = c.replace(FOOTER_ADM_OLD, FOOTER_ADM_NEW, 1)
    for emoji, svg in ICON.items():
        c = c.replace(f'<span style="font-size:1.3rem;">{emoji}</span>', svg, 1)
    write('preschool/what-we-offer/index.html', c)
    log.append(f"{'CHANGED' if c != orig else 'NO-CHANGE'}: preschool/what-we-offer/index.html")
except Exception as e:
    log.append(f"ERROR {e}: preschool/what-we-offer/index.html")

# ════════════════════════════════════════════════════════════════
# 8. PRESCHOOL FAQs — school hours
# ════════════════════════════════════════════════════════════════
apply('preschool/faqs/index.html',
    *base_pairs(),
    (
        'Preschool hours are <strong>Monday to Friday, 07:30 to 13:30</strong>. Aftercare is available from 13:30 to 17:30 at R1,900 per term or R70 per day.',
        'Preschool hours are <strong>Monday to Thursday, 07:45 to 14:00</strong>, and <strong>Friday, 07:45 to 13:30</strong>. Aftercare is available until 17:30 at R1,900 per term or R70 per day.'
    ),
    (
        '"text":"Preschool hours are Monday to Friday, 07:30 to 13:30. Aftercare is available from 13:30 to 17:30."',
        '"text":"Preschool hours are Monday to Thursday, 07:45 to 14:00, and Friday, 07:45 to 13:30. Aftercare is available until 17:30."'
    ),
)

# ════════════════════════════════════════════════════════════════
# 9. PRESCHOOL INDEX
# ════════════════════════════════════════════════════════════════
apply('preschool/index.html',
    *base_pairs(),
    ('<div class="label label-white">Grades 000 \u2014 R</div>', '<div class="label label-white grade-range-label">Gr 000 \u2013 R</div>'),
    ('<h1>Ambleside Preschool<br><em>\u2014 Acorns</em></h1>', '<h1>Ambleside Preschool<br><em>(Acorns)</em></h1>'),
    ('At Ambleside Preschool \u2014 Acorns,', 'At Ambleside Preschool (Acorns),'),
    ('<span>Preschool \u2014 Acorns</span>', '<span>Preschool (Acorns)</span>'),
)

# ════════════════════════════════════════════════════════════════
# 10. PRIMARY SCHOOL FAQs — school hours
# ════════════════════════════════════════════════════════════════
apply('primary-school/faqs/index.html',
    *base_pairs(),
    (
        'School hours are <strong>Monday to Friday, 07:30 to 13:30</strong>. Aftercare is available from 13:30 to 17:30 at R1,900 per term or R70 per day.',
        'School hours are <strong>Monday to Thursday, 07:45 to 14:00</strong>, and <strong>Friday, 07:45 to 13:30</strong>. Aftercare is available until 17:30 at R1,900 per term or R70 per day.'
    ),
    (
        '"text":"School hours are Monday to Friday, 07:30 to 13:30, with aftercare available until 17:30."',
        '"text":"School hours are Monday to Thursday, 07:45 to 14:00, and Friday, 07:45 to 13:30. Aftercare is available until 17:30."'
    ),
)

# ════════════════════════════════════════════════════════════════
# 11. NAV+FOOTER ONLY — remaining pages
# ════════════════════════════════════════════════════════════════
for p in [
    'about/index.html',
    'about/our-team/index.html',
    'admissions/index.html',
    'primary-school/index.html',
    'primary-school/curriculum/index.html',
    'primary-school/sport/index.html',
    'events/index.html',
    'news/index.html',
]:
    apply(p, *base_pairs())

# About index — school name in h1
apply('about/index.html',
    ('About Ambleside<br>Durban North', 'About Ambleside<br>School of Durban'),
)

# ════════════════════════════════════════════════════════════════
# 12. ADMIN CMS — fix logo, remove events collection
# ════════════════════════════════════════════════════════════════
apply('admin/config.yml',
    ('logo_url: /images/ambleside-logo.svg', 'logo_url: /images/logo-nav.jpg'),
    # Remove events CMS collection (handled by Google Calendar)
    (
        '\n  # EVENTS\n  - name: "events"\n    label: "Events"\n    label_singular: "Event"\n    folder: "_content/events"\n    create: true\n    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"\n    fields:\n      - { label: "Event Name", name: "title", widget: "string" }\n      - { label: "Event Date", name: "event_date", widget: "datetime" }\n      - { label: "End Date (optional)", name: "event_end_date", widget: "datetime", required: false }\n      - { label: "Location", name: "location", widget: "string", default: "Ambleside School, 27 Chelsea Drive, Durban North", required: false }\n      - { label: "Category", name: "category", widget: "select", options: ["School Event", "Sport", "Academic", "Cultural", "Preschool", "Junior School", "Parents", "Community"] }\n      - { label: "Featured Image", name: "image", widget: "image", required: false }\n      - { label: "Description", name: "body", widget: "markdown" }\n      - { label: "Open to Public?", name: "public", widget: "boolean", default: true }',
        '\n  # EVENTS — managed via Google Calendar (see events/index.html)\n  # No CMS collection needed here'
    ),
)

# ════════════════════════════════════════════════════════════════
# 13. THURSDAY ENRICHMENT PROGRAMME — new page
# ════════════════════════════════════════════════════════════════
os.makedirs(os.path.join(BASE, 'thursday-enrichment'), exist_ok=True)

ENRICHMENT_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Thursday Enrichment Programme | Ambleside School Durban North</title>
  <meta name="description" content="A weekly Thursday enrichment programme for homeschooled children in Grades 1\u20137 \u2014 nature study, composer study, music appreciation and peer play. Durban North. Thursdays in May.">
  <meta name="keywords" content="homeschool enrichment Durban, homeschool co-op KZN, Charlotte Mason homeschool Durban North, homeschool programme Durban, nature study homeschool KZN, Thursday enrichment programme">
  <link rel="canonical" href="https://amblesidedurban.com/thursday-enrichment/">
  <link rel="icon" type="image/png" href="/images/favicon.png">
  <link rel="shortcut icon" href="/images/favicon.ico">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://amblesidedurban.com/thursday-enrichment/">
  <meta property="og:title" content="Thursday Enrichment Programme | Ambleside School Durban North">
  <meta property="og:description" content="A weekly Thursday enrichment programme for homeschooled children in Grades 1\u20137 in Durban North. Nature study, composer study, music appreciation, and peer play.">
  <meta property="og:image" content="https://amblesidedurban.com/images/og-home.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Jost:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/global.css">
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Thursday Enrichment","item":"https://amblesidedurban.com/thursday-enrichment/"}]}
  </script>
</head>
<body>
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-logo" aria-label="Ambleside School of Durban \u2014 Home">
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
</div>

<div class="page-header">
  <div class="breadcrumb container"><a href="/">Home</a> <span>\u203a</span> <span>Thursday Enrichment</span></div>
  <div class="container">
    <div class="label label-white">Homeschool Community</div>
    <h1>Thursday Enrichment<br><em>Programme</em></h1>
    <p>A weekly morning for homeschooled children \u2014 rich learning, real community, and the joy of doing it together.</p>
  </div>
</div>

<!-- INTRO -->
<section class="section section-bg-warm-white">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr;gap:3rem;max-width:960px;">
      <style>@media(min-width:768px){.enrich-grid{grid-template-columns:1fr 1fr!important}}</style>
      <div class="enrich-grid" style="display:grid;grid-template-columns:1fr;gap:3rem;">

        <div class="fade-up">
          <div class="label label-brown">For Homeschool Families</div>
          <h2>The best parts of school,<br>without <em>leaving home.</em></h2>
          <p style="margin-top:1rem;">You\u2019ve built something remarkable. Homeschooling your children takes courage, commitment, and deep love \u2014 and if you\u2019re reading this, you probably already know that the Ambleside philosophy resonates with what you\u2019re trying to do at home.</p>
          <p style="margin-top:1rem;">The Thursday Enrichment Programme is our way of opening our doors to the homeschool community. Not to convince you to change what\u2019s working \u2014 but to offer something that\u2019s genuinely hard to replicate at home: peer community, specialist-led subjects, and the particular joy that comes from learning alongside others.</p>
          <p style="margin-top:1rem;">Come for a Thursday. Stay for the term. See what happens.</p>
        </div>

        <div class="fade-up d1">
          <div class="card card-cream" style="padding:2rem;">
            <div class="label label-brown">Programme Details</div>
            <div style="display:flex;flex-direction:column;gap:1rem;margin-top:1.2rem;">
              <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="width:36px;height:36px;background:var(--navy);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="16" height="16" fill="none" stroke="white" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                </div>
                <div><div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:.2rem;">When</div><p style="font-size:.88rem;">Every Thursday in May \u00b7 10:00 \u2013 12:30</p></div>
              </div>
              <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="width:36px;height:36px;background:var(--navy);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="16" height="16" fill="none" stroke="white" stroke-width="1.5" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                </div>
                <div><div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:.2rem;">Who</div><p style="font-size:.88rem;">Homeschooled children, Grades 1 \u2013 7</p></div>
              </div>
              <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="width:36px;height:36px;background:var(--navy);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="16" height="16" fill="none" stroke="white" stroke-width="1.5" viewBox="0 0 24 24"><path d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><circle cx="12" cy="11" r="3"/></svg>
                </div>
                <div><div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:.2rem;">Where</div><p style="font-size:.88rem;">Ambleside School \u00b7 27 Chelsea Drive, Durban North</p></div>
              </div>
              <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="width:36px;height:36px;background:var(--gold);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="16" height="16" fill="none" stroke="var(--navy)" stroke-width="1.5" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                </div>
                <div><div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:.2rem;">Cost</div><p style="font-size:.88rem;"><strong>R100</strong> first child &nbsp;\u00b7&nbsp; <strong>R80</strong> each additional child<br><span style="color:var(--muted);">All materials provided</span></p></div>
              </div>
              <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="width:36px;height:36px;background:var(--brown);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="16" height="16" fill="none" stroke="white" stroke-width="1.5" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
                </div>
                <div><div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--navy);margin-bottom:.2rem;">Please Bring</div><p style="font-size:.88rem;">A light lunch and water bottle</p></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- WHAT WE DO -->
<section class="section section-bg-cream">
  <div class="container">
    <div class="fade-up" style="text-align:center;margin-bottom:3rem;">
      <div class="label label-center">What Happens on Thursdays</div>
      <h2>Three hours of <em>living learning.</em></h2>
      <p style="max-width:560px;margin:.8rem auto 0;">Every Thursday session follows the same warm rhythm \u2014 three activities that are genuinely difficult to do well alone at home, but come alive in community.</p>
    </div>
    <div class="grid-3" style="max-width:900px;margin:0 auto;">

      <div class="card fade-up" style="border-top-color:var(--brown);">
        <div style="width:48px;height:48px;background:var(--brown);display:flex;align-items:center;justify-content:center;margin-bottom:1.2rem;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22V12"/><path d="M5 12c0-4 3.13-8 7-8 3.87 0 7 4 7 8H5z"/><path d="M9 22h6"/></svg>
        </div>
        <h4 style="color:var(--navy);margin-bottom:.6rem;">Nature Study</h4>
        <p style="font-size:.88rem;">Children head outdoors with notebooks in hand \u2014 observing, sketching, and recording what they find. Charlotte Mason believed careful attention to the natural world was the foundation of all good scientific thinking, and we take that seriously. No two Thursdays look the same.</p>
      </div>

      <div class="card fade-up d1" style="border-top-color:var(--navy);">
        <div style="width:48px;height:48px;background:var(--navy);display:flex;align-items:center;justify-content:center;margin-bottom:1.2rem;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
        </div>
        <h4 style="color:var(--navy);margin-bottom:.6rem;">Composer Study &amp; Music Appreciation</h4>
        <p style="font-size:.88rem;">We spend unhurried time with a single composer \u2014 listening carefully, talking about what we hear, and learning to receive music as something meaningful. This term we are getting to know a composer whose work rewards slow, attentive listening. No prior musical experience needed.</p>
      </div>

      <div class="card fade-up d2" style="border-top-color:var(--gold);">
        <div style="width:48px;height:48px;background:var(--gold);display:flex;align-items:center;justify-content:center;margin-bottom:1.2rem;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--navy)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <h4 style="color:var(--navy);margin-bottom:.6rem;">Play &amp; Peer Interaction</h4>
        <p style="font-size:.88rem;">One of the things homeschooling families tell us they miss most is simply \u2014 other children. Unstructured play with peers of different ages is genuinely valuable, and we protect time for it every Thursday. Children make friends here. Parents do too.</p>
      </div>

    </div>
  </div>
</section>

<!-- FOR HOMESCHOOLERS -->
<section class="section section-bg-navy" style="text-align:center;">
  <div class="container" style="max-width:720px;">
    <div class="label label-white label-center fade-up">A Word to Homeschool Families</div>
    <h2 class="title-light fade-up d1">You\u2019ve done something <em style="color:var(--gold);">remarkable.</em></h2>
    <p class="text-white mt-sm fade-up d2">Whether you\u2019ve been homeschooling for one year or seven, whether you\u2019re thriving or wondering what comes next \u2014 this programme is for you. It\u2019s a space to connect, to enrich, and to explore whether Ambleside might be a community worth knowing better. There is no pressure. Just a warm door, open on Thursdays.</p>
    <div style="margin-top:2rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;" class="fade-up d3">
      <a href="#booking" class="btn btn-gold">Book Your Place</a>
      <a href="/about/charlotte-mason/" class="btn btn-outline-white">Our Philosophy</a>
    </div>
  </div>
</section>

<!-- BOOKING -->
<section class="section section-bg-warm-white" id="booking">
  <div class="container" style="max-width:700px;">
    <div class="fade-up">
      <div class="label label-brown">Reserve Your Spot</div>
      <h2 style="margin-bottom:.6rem;">Book for May</h2>
      <p style="font-size:.9rem;margin-bottom:.5rem;">Spaces are limited and booking is essential. Fill in the form below and we\u2019ll confirm your child\u2019s place.</p>
      <div style="background:var(--cream);padding:1rem 1.2rem;border-left:3px solid var(--gold);margin-bottom:1.5rem;font-size:.84rem;color:var(--muted);">
        <strong style="color:var(--navy);">May Thursday dates:</strong> 1, 8, 15, 22, 29 May &nbsp;\u00b7&nbsp; 10:00 \u2013 12:30 each session
      </div>
      <!-- TALLY FORM — create a new Tally form for Thursday Enrichment bookings
           and replace REPLACE_WITH_TALLY_FORM_ID with your form ID -->
      <iframe data-tally-src="https://tally.so/embed/REPLACE_WITH_TALLY_FORM_ID?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="500" frameborder="0" marginheight="0" marginwidth="0" title="Thursday Enrichment Booking Form"></iframe>
      <script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector(\'script[src="\'+w+\'"]\')===null){var s=d.createElement("script");s.src=w;s.onload=v;s.onerror=v;d.body.appendChild(s);}</script>
      <p style="margin-top:1rem;font-size:.8rem;color:var(--muted);">Questions? Email us at <a href="mailto:admin@amblesidedurban.com" style="color:var(--navy);">admin@amblesidedurban.com</a> or call <a href="tel:0713902182" style="color:var(--navy);">071 390 2182</a>.</p>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="/" style="display:inline-block;margin-bottom:1rem;" aria-label="Ambleside School of Durban \u2014 Home">
          <img src="/images/logo-stacked.png" alt="Ambleside School of Durban" class="footer-logo-img" width="160" height="88" loading="lazy">
        </a>
        <p class="footer-tagline">Nourishing minds and nurturing character in Durban North, KwaZulu-Natal \u2014 a Member School of Ambleside Schools International.</p>
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
          <li><a href="/primary-school/">Primary School (Gr 1\u20137)</a></li>
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
        <span>\u00a9 2026 Ambleside School of Durban North. All rights reserved.</span>
        <span>Member of Ambleside Schools International</span>
      </div>
    </div>
  </div>
</footer>
<script src="/js/global.js"></script>
</body>
</html>'''

try:
    write('thursday-enrichment/index.html', ENRICHMENT_PAGE)
    log.append("CREATED: thursday-enrichment/index.html")
except Exception as e:
    log.append(f"ERROR {e}: thursday-enrichment/index.html")

# ════════════════════════════════════════════════════════════════
# REPORT
# ════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("AMBLESIDE BATCH 2 — CHANGE REPORT")
print("="*60)
for line in log:
    print(line)
print("="*60)
print(f"\nDone. {len([l for l in log if 'CHANGED' in l or 'CREATED' in l])} files modified/created.")
