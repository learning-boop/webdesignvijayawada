"""Build the inner pages of the site from _build/content.json.

Run from the repository root:  python _build/build.py

It writes about/, services/, portfolio/, work/, blog/, careers/, contact/, privacy-policy/,
terms-and-conditions/, 404.html, sitemap.xml and robots.txt, and refreshes the shared header,
footer and asset versions inside index.html (between the <!-- site:... --> markers).
GitHub Pages ignores folders that start with "_", so this folder is never published.
"""

import datetime
import hashlib
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://learning-boop.github.io/webdesignvijayawada/'  # change when you move to your own domain
FOUNDED = 2008
YEARS = datetime.date.today().year - FOUNDED
PHONE, PHONE_HREF = '+91 98859 33339', 'tel:+919885933339'
EMAIL = 'info@creatorstouchglobal.com'
WHATSAPP = 'https://wa.me/919885933339'
SITE = 'Web Design in Vijayawada'

C = json.load(open(os.path.join(ROOT, '_build', 'content.json'), encoding='utf-8'))
e = html.escape


def asset_version():
    h = hashlib.md5()
    for f in ('styles.css', 'script.js', 'motion.js'):
        h.update(open(os.path.join(ROOT, f), 'rb').read())
    return h.hexdigest()[:8]


V = asset_version()

ICONS = {
    'code': '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 4l-3 16" />',
    'pen': '<path d="M4 20l4-1 11-11-3-3L5 16z" /><path d="M14 7l3 3" />',
    'megaphone': '<path d="M3 11l15-6v14L3 13z" /><path d="M7 13v5h3" />',
    'phone': '<rect x="7" y="3" width="10" height="18" rx="2" /><path d="M11 18h2" />',
    'doc': '<path d="M6 3h9l4 4v14H6z" /><path d="M14 3v5h5M9 13h7M9 17h5" />',
    'spark': '<path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z" />',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2" /><path d="M3 7l9 6 9-6" />',
    'pin': '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z" /><circle cx="12" cy="10" r="2.5" />',
    'call': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2" />',
    'chat': '<path d="M4 20l1.3-3.9A8 8 0 1 1 8 19l-4 1z" />',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6" />',
}


def icon(name, cls=''):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


ARROW = icon('arrow', 'btn-arrow')
NAV = [('Work', 'portfolio/'), ('Services', 'services/'), ('About', 'about/'), ('Blog', 'blog/'),
       ('Careers', 'careers/'), ('Contact', 'contact/')]
WA_LOGO = (
    '<svg viewBox="0 0 32 32" aria-hidden="true" style="stroke: none"><circle cx="16" cy="16" r="14" fill="#25d366" />'
    '<path fill="#fff" d="M21.6 18.3c-.3-.2-1.8-.9-2-1s-.5-.2-.7.2-.8 1-.9 1.2-.3.2-.6.1a7.6 7.6 0 0 1-3.8-3.3c-.3-.5.3-.5.8-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.1-.3-.2-.6-.3z" /></svg>'
)


# ---------------------------------------------------------------- shared pieces

def brand_mark(p):
    return (f'<span class="brand-mark" aria-hidden="true">'
            f'<img class="hand hand-blue" src="{p}assets/hand-blue.png" alt="" />'
            f'<img class="hand hand-pink" src="{p}assets/hand-pink.png" alt="" />'
            f'<img class="dot" src="{p}assets/dot-green.png" alt="" /></span>')


def header(p, active=None):
    home = p or './'
    cur = ' aria-current="page"'
    links = '\n'.join(f'        <a href="{p}{href}"{cur if href == active else ""}>{label}</a>' for label, href in NAV)
    return f'''    <header class="nav" id="nav">
      <a href="{home}" class="brand" aria-label="{SITE} — home">
        {brand_mark(p)}
        <span>Web Design <b>Vijayawada</b></span>
      </a>

      <nav class="nav-links" aria-label="Main">
{links}
      </nav>

      <div class="nav-end">
        <a class="btn btn-wa" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
          {WA_LOGO}
          <span>WhatsApp</span>
        </a>
        <a class="btn btn-navy nav-audit" href="{p}contact/">
          Free website audit
          {ARROW}
        </a>
        <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mobileMenu" aria-label="Open menu">
          <span></span><span></span>
        </button>
      </div>

      <div class="mobile-menu" id="mobileMenu" hidden>
{links}
        <a class="btn btn-navy" href="{p}contact/">Free website audit</a>
      </div>
    </header>'''


def footer(p):
    cats = '\n'.join(f'          <a href="{p}services/#{c["anchor"]}">{e(c["name"])}</a>' for c in C['service_categories'])
    company = '\n'.join(f'          <a href="{p}{href}">{label}</a>' for label, href in
                        [('Home', ''), ('Portfolio', 'portfolio/'), ('About us', 'about/'), ('Blog', 'blog/'),
                         ('Careers', 'careers/'), ('Contact', 'contact/')])
    return f'''    <footer class="footer">
      <div class="footer-grid">
        <div class="footer-about">
          <a href="{p or './'}" class="brand">
            {brand_mark(p)}
            <span>Web Design <b>Vijayawada</b></span>
          </a>
          <p>Websites, branding, SEO and automation for businesses in Vijayawada and around the world — {2000}+ brands since {FOUNDED}.</p>
          <a class="btn btn-navy" href="{p}contact/">Start your website {ARROW}</a>
        </div>
        <nav class="footer-col" aria-label="Company">
          <h2>Company</h2>
{company.replace('href="' + p + '"', 'href="' + (p or './') + '"')}
        </nav>
        <nav class="footer-col" aria-label="Services">
          <h2>Services</h2>
{cats}
        </nav>
        <div class="footer-col">
          <h2>Get in touch</h2>
          <a href="{PHONE_HREF}">{PHONE}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a>
          <span>Vijayawada, Andhra Pradesh</span>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="year">{datetime.date.today().year}</span> {SITE}. All rights reserved.</span>
        <span class="footer-legal"><a href="{p}privacy-policy/">Privacy policy</a><a href="{p}terms-and-conditions/">Terms &amp; conditions</a></span>
      </div>
    </footer>'''


def scripts(p):
    return f'''    <a class="float-chat" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">
      <span class="float-chat-dot">{icon('chat')}</span>
      Chat on WhatsApp
    </a>

    <script src="{p}script.js?v={V}" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
    <script src="{p}motion.js?v={V}" defer></script>'''


def head(p, path, title, desc, jsonld):
    url = BASE + path
    ld = ''.join(f'\n    <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in jsonld)
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}" />
    <meta name="theme-color" content="#ffffff" />
    <link rel="icon" type="image/png" href="{p}assets/favicon.png" />
    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="{SITE}" />
    <meta property="og:title" content="{e(title)}" />
    <meta property="og:description" content="{e(desc)}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{BASE}assets/logo.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{p}styles.css?v={V}" />
    <script>
      // Scroll animations are on unless the visitor prefers reduced motion.
      if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {{
        document.documentElement.classList.add('motion')
        setTimeout(() => window.__motionReady || document.documentElement.classList.remove('motion'), 6000)
      }}
    </script>{ld}
  </head>'''


PAGES = []  # (path, priority) for the sitemap


def write(path, title, desc, body, active=None, crumbs=None, jsonld=None, prefix=None):
    """path is the page's folder (e.g. 'services/x/') or a root file name like '404.html'."""
    p = '../' * path.count('/') if prefix is None else prefix
    jsonld = list(jsonld or [])
    if crumbs:
        items = [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + h} for i, (n, h) in enumerate([('Home', '')] + crumbs)]
        jsonld.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items})
    doc = f'''{head(p, path, title, desc, jsonld)}
  <body class="inner">
    <a class="skip" href="#main">Skip to content</a>

{header(p, active)}

    <main id="main">
{body(p)}
    </main>

{footer(p)}

{scripts(p)}
  </body>
</html>
'''
    out = os.path.join(ROOT, path, 'index.html') if path.endswith('/') else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8', newline='\n').write(doc)
    if path.endswith('/'):
        PAGES.append(path)


def crumbs_html(p, crumbs):
    parts = [f'<a href="{p or "./"}">Home</a>']
    for i, (name, href) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        parts.append(f'<span aria-current="page">{e(name)}</span>' if last else f'<a href="{p}{href}">{e(name)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">/</i>'.join(parts) + '</nav>'


def photo(p, name, alt, cls='photo', eager=False):
    """A stock photo from assets/photos (see assets/photos/CREDITS.md)."""
    loading = '' if eager else ' loading="lazy"'
    return f'<img class="{cls}" src="{p}assets/photos/{name}.webp" alt="{e(alt)}" width="1400" height="933"{loading} />'


def page_hero(p, crumbs, eyebrow, title, lead, buttons='', image=None):
    """image is (photo name, alt text); with it the hero becomes two columns."""
    art = (f'<figure class="page-hero-photo">{photo(p, *image, eager=True)}</figure>' if image else
           f'<div class="page-hero-art" aria-hidden="true">{brand_mark(p).replace("brand-mark", "page-hero-mark")}</div>')
    return f'''      <section class="page-hero{' has-photo' if image else ''}">
        {art}
        <div class="page-hero-inner">
          {crumbs_html(p, crumbs)}
          <p class="eyebrow">{e(eyebrow)}</p>
          <h1>{title}</h1>
          <p class="lead">{e(lead)}</p>
          {f'<div class="hero-cta">{buttons}</div>' if buttons else ''}
        </div>
      </section>'''


def btns(p, primary=('Get a free consultation', 'contact/'), secondary=('See our work', 'portfolio/')):
    out = f'<a class="btn btn-navy btn-lg" href="{p}{primary[1]}">{primary[0]} {ARROW}</a>'
    if secondary:
        out += f'<a class="btn btn-outline btn-lg" href="{p}{secondary[1]}">{secondary[0]}</a>'
    return out


def cta_band(p, title='Ready to grow your business?', text='Free consultation, honest advice, no obligation. Tell us about your business and we’ll tell you exactly how we can help.'):
    return f'''      <section class="section">
        <div class="cta-band reveal">
          <div class="cta-glow" aria-hidden="true"></div>
          <div>
            <p class="eyebrow">Let’s talk</p>
            <h2>{title}</h2>
            <p>{e(text)}</p>
          </div>
          <div class="hero-cta">
            <a class="btn btn-navy btn-lg" href="{p}contact/">Get a free consultation {ARROW}</a>
            <a class="btn btn-outline btn-lg" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a>
          </div>
        </div>
      </section>'''


def stats(items):
    return '<dl class="stat-row reveal">' + ''.join(f'<div><dd>{e(v)}</dd><dt>{e(k)}</dt></div>' for v, k in items) + '</dl>'


def shot(p, w, big=False):
    """Browser frame with a real screenshot, or a drawn placeholder page in the project's colour."""
    domain = re.sub(r'^https?://(www\.)?', '', w['live']).strip('/')
    if w['shot']:
        page = f'<img class="shot-page" src="{p}assets/work/{w["shot"]}" alt="{e(w["name"])} website" loading="lazy" />'
    else:
        page = f'''<div class="shot-page mock-page" aria-hidden="true">
                  <div class="mp-nav"><b>{e(w["name"])}</b><span></span><span></span><span></span></div>
                  <div class="mp-hero"><b>{e(w["tagline"])}</b><s></s><s class="short"></s><div class="mock-row"><u></u><u class="ghost"></u></div></div>
                  <div class="mp-tiles"><em></em><em></em><em></em></div>
                  <div class="mp-split"><em></em><div><s></s><s></s><s class="short"></s></div></div>
                  <div class="mp-tiles"><em></em><em></em><em></em></div>
                  <div class="mp-band"></div>
                  <div class="mp-foot"><s></s><s class="short"></s></div>
                </div>'''
    return f'''<div class="shot{' shot-lg' if big else ''}">
              <div class="mock-bar" aria-hidden="true"><i></i><i></i><i></i><span>{e(domain)}</span></div>
              <div class="shot-view">
                {page}
              </div>
            </div>'''


def work_card(p, slug, n=None):
    w = C['work'][slug]
    num = f'<span class="work-n">{n:02d}</span>' if n else ''
    return f'''          <a class="work-card reveal" data-cat="{e(w["filter"])}" href="{p}work/{slug}/" style="--c: {w["color"]}">
            {shot(p, w)}
            <div class="work-meta">
              {num}
              <div><h3>{e(w["name"])}</h3><p>{e(w["category"])}</p></div>
              <span class="arrow" aria-hidden="true">↗</span>
            </div>
          </a>'''


ORG = {'@context': 'https://schema.org', '@type': 'ProfessionalService', 'name': SITE, 'url': BASE,
       'telephone': PHONE, 'email': EMAIL, 'foundingDate': str(FOUNDED),
       'address': {'@type': 'PostalAddress', 'addressLocality': 'Vijayawada', 'addressRegion': 'Andhra Pradesh', 'addressCountry': 'IN'}}

PROCESS = [('Discovery', 'A free call to understand your customers, competitors and what success looks like for you.'),
           ('Strategy', 'A written plan with scope, dated milestones and a fixed quote — agreed before work starts.'),
           ('Execution', 'Design, content and build by our own team, with reviews at every stage.'),
           ('Growth', 'After launch we track enquiries and rankings, then keep improving what works.')]


CAT_ALT = {
    'web': 'Website code on a laptop screen',
    'branding': 'Colour swatches, pencils and brand sketches on a designer’s desk',
    'marketing': 'A marketing team planning a campaign around laptops',
    'apps': 'A hand holding a phone showing an app dashboard',
    'content': 'A laptop and an open notebook on a writing desk',
    'automation': 'A friendly robot working at a laptop',
}
BLOG_PHOTO = {
    'why-your-business-needs-a-brand-not-just-a-logo': ('blog-brand', 'Branded business cards and stationery'),
    '5-signs-your-website-is-costing-you-customers': ('blog-website', 'Someone browsing a business website on a laptop'),
    'whatsapp-automation-the-secret-weapon-for-local-businesses': ('blog-whatsapp', 'A person replying to messages on a smartphone'),
    'seo-vs-paid-ads-whats-right-for-your-business': ('blog-seo', 'Google search open on a laptop next to a coffee'),
    'how-to-measure-if-your-digital-marketing-is-working': ('blog-analytics', 'A laptop showing marketing charts on a sunny desk'),
    'the-real-cost-of-a-badly-designed-website': ('blog-design', 'A designer sketching website wireframes on paper'),
}


def process_steps():
    return '<ol class="steps steps-4">' + ''.join(
        f'<li class="reveal" style="--d: {i * 80}ms"><span class="step-n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (t, d) in enumerate(PROCESS)) + '</ol>'


# ---------------------------------------------------------------- pages

def about():
    principles = [
        ('Clarity over complexity', 'We explain everything in plain language. No jargon, no hidden fees, no surprises. You always know what we are doing and why.', 'var(--blue)'),
        ('Results, not just deliverables', 'A logo is not the goal. More customers are. We measure success by what changes in your business, not by what we hand over.', 'var(--pink)'),
        ('Made for India', 'We understand the Indian customer, the Indian market, and the Indian business owner. Everything we build is grounded in that reality.', 'var(--green)'),
        ('Long-term thinking', 'We do not chase quick wins. We build systems, brands, and assets that compound over time and keep working for you.', '#f2a900'),
    ]
    story = [
        (str(FOUNDED), 'Founded in Vijayawada as a graphic design studio serving local businesses.'),
        ('2012', 'Expanded into digital — websites, social media, and early SEO for Indian SMEs.'),
        ('2017', 'Launched performance marketing practice. First international client (UAE).'),
        ('2020', 'Went fully remote. Doubled team size. Added WhatsApp automation and e-commerce builds.'),
        ('2024', 'Opened presence in the UK. Serving clients across India, UAE, and Europe.'),
        ('2026', '2000+ projects. Building the definitive digital studio for Indian small business.'),
    ]

    def body(p):
        tiles = ''.join(f'<article class="tile reveal" style="--c: {c}; --d: {i * 80}ms"><span class="tile-n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></article>'
                        for i, (t, d, c) in enumerate(principles))
        tl = ''.join(f'<li class="reveal"><b>{y}</b><p>{e(t)}</p></li>' for y, t in story)
        return f'''{page_hero(p, [('About us', 'about/')], 'Who we are', 'About <em>us</em>',
                  'We are a digital studio founded in Vijayawada, built for the small business owner who is serious about growth.',
                  btns(p), image=('about-team', 'Our team collaborating around a conference table'))}

      <section class="section">
        {stats([(f'{YEARS}+', 'Years in business'), ('2000+', 'Projects delivered'), ('12+', 'Industries served'), ('5', 'Countries served')])}
      </section>

      <section class="section split-section">
        <figure class="split-photo reveal">{photo(p, 'about-work', 'Two colleagues reviewing a website together on a laptop')}</figure>
        <div class="prose reveal">
          <p class="eyebrow">Our mission</p>
          <h2>Great design shouldn’t be <span class="thin">a luxury</span></h2>
          <p>Most digital agencies are built for big brands with big budgets. We built our studio for everyone else — the shop owner in Bengaluru, the clinic in Pune, the clothing label in Surat trying to reach customers online.</p>
          <p>We believe great design and smart marketing should not be a luxury. Our mission is to close the gap between what Indian small businesses look like and what they deserve to look like — so they can compete, grow, and thrive.</p>
        </div>
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">How we work</p>
          <h2>Principles we <span class="thin">never compromise on</span></h2>
        </div>
        <div class="grid-4">{tiles}</div>
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">Our story</p>
          <h2>From a design studio to <span class="thin">a full digital partner</span></h2>
        </div>
        <ol class="timeline">{tl}</ol>
        <figure class="big-quote reveal">
          <blockquote>“We started as designers who cared about craft. We grew into a full-service studio that cares about outcomes. The craft never left.”</blockquote>
          <figcaption>— The founders</figcaption>
        </figure>
      </section>

{cta_band(p, 'Work <span class="thin">with us</span>', 'Free consultation, honest advice, no obligation. Tell us about your business and we’ll tell you exactly how we can help.')}'''

    write('about/', f'About us — {SITE}', 'A Vijayawada digital studio since 2008, built for small business owners who are serious about growth.',
          body, active='about/', crumbs=[('About us', 'about/')], jsonld=[ORG])


def services_index():
    def body(p):
        blocks = []
        for i, c in enumerate(C['service_categories']):
            chips = ''.join(f'<a class="svc-link" href="{p}services/{s}/">{e(C["services"][s]["title"])}<span aria-hidden="true">→</span></a>' for s in c['services'])
            blocks.append(f'''        <section class="svc-cat reveal" id="{c["anchor"]}" style="--c: {['var(--blue)', 'var(--pink)', 'var(--green)', '#8b6cf0', '#f2a900', '#1fa8c9'][i]}">
          <div class="svc-cat-head">
            <figure class="svc-cat-photo">{photo(p, 'cat-' + c['anchor'], CAT_ALT[c['anchor']])}<span class="tile-icon">{icon(c["icon"])}</span></figure>
            <h2>{e(c["name"])}</h2>
            <p>{e(c["blurb"])}</p>
            <span class="svc-count">{len(c["services"])} services</span>
          </div>
          <div class="svc-links">{chips}</div>
        </section>''')
        jump = ''.join(f'<a class="filter" href="#{c["anchor"]}">{e(c["name"])}</a>' for c in C['service_categories'])
        return f'''{page_hero(p, [('Services', 'services/')], 'What we do', 'Our <em>services</em>',
                  'Everything your business needs to grow online — strategy, design, development, marketing and automation, all under one roof.',
                  btns(p))}

      <section class="section">
        <nav class="filters jump reveal" aria-label="Service categories">{jump}</nav>
        <div class="svc-cats">
{chr(10).join(blocks)}
        </div>
      </section>

      <section class="section">
        {stats([(f'{YEARS}+', 'Years of experience'), ('2000+', 'Projects delivered'), ('5', 'Countries served'), ('95+', 'Avg. performance score')])}
      </section>

{cta_band(p, 'Ready to <span class="thin">start?</span>', 'Tell us what you need. We’ll put together a plan built around your business and your budget.')}'''

    write('services/', f'Services — {SITE}', 'Website design, e-commerce, branding, SEO, ads, mobile apps, content writing and WhatsApp automation from a Vijayawada studio.',
          body, active='services/', crumbs=[('Services', 'services/')], jsonld=[ORG])


def service_page(slug):
    s = C['services'][slug]
    cat = next(c for c in C['service_categories'] if slug in c['services'])
    others = [x for x in cat['services'] if x != slug][:6]

    def body(p):
        items = ''.join(f'<li class="reveal" style="--d: {(i % 3) * 80}ms"><span>{i + 1:02d}</span><p>{e(t)}</p></li>' for i, t in enumerate(s['deliverables']))
        work = ''.join(work_card(p, w) for w in s['related_work'])
        rel = ''.join(f'<a class="svc-link" href="{p}services/{x}/">{e(C["services"][x]["title"])}<span aria-hidden="true">→</span></a>' for x in others)
        return f'''{page_hero(p, [('Services', 'services/'), (s['title'], f'services/{slug}/')], s['category'], e(s['title']) + ' <span class="thin">in Vijayawada</span>',
                  s['tagline'], btns(p), image=('cat-' + cat['anchor'], CAT_ALT[cat['anchor']]))}

      <section class="section split-section">
        <div class="prose reveal">
          <p class="prose-lead">{e(s['intro'])}</p>
        </div>
        <aside class="why-card reveal">
          <p class="eyebrow">Why us</p>
          <h2>{YEARS} years, 2000+ brands, <span class="thin">one in-house team.</span></h2>
          <p>{e(s['why'])}</p>
          <dl class="mini-stats"><div><dd>2000+</dd><dt>Brands served</dt></div><div><dd>{YEARS}+</dd><dt>Years</dt></div><div><dd>5</dd><dt>Countries</dt></div><div><dd>100%</dd><dt>In-house team</dt></div></dl>
        </aside>
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">What you get</p>
          <h2>Our {e(s['title'])} <span class="thin">services</span></h2>
        </div>
        <ol class="deliverables">{items}</ol>
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">Related work</p>
          <h2>Projects like yours — <span class="thin">delivered</span></h2>
        </div>
        <div class="pf-grid">
{work}
        </div>
        <p class="center-link reveal"><a class="btn btn-outline" href="{p}portfolio/">View all projects {ARROW}</a></p>
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">How it works</p>
          <h2>Our <span class="thin">process</span></h2>
        </div>
        {process_steps()}
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">Related services</p>
          <h2>More {e(cat['name'])} <span class="thin">services</span></h2>
        </div>
        <div class="svc-links svc-links-center reveal">{rel}<a class="svc-link svc-link-all" href="{p}services/">View all services<span aria-hidden="true">→</span></a></div>
      </section>

{cta_band(p, 'Ready to get <span class="thin">started?</span>', f'Share a few details about your business and we’ll come back with a {s["title"].lower()} plan and a fixed quote that fits your budget.')}'''

    ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': s['title'], 'serviceType': s['title'], 'description': s['intro'],
          'provider': {'@type': 'ProfessionalService', 'name': SITE, 'url': BASE}, 'areaServed': 'Vijayawada'}
    write(f'services/{slug}/', f'{s["title"]} in Vijayawada — {SITE}', s['intro'][:155], body, active='services/',
          crumbs=[('Services', 'services/'), (s['title'], f'services/{slug}/')], jsonld=[ld])


def portfolio():
    filters = ['All'] + list(dict.fromkeys(C['work'][s]['filter'] for s in C['work_order']))

    def body(p):
        chips = ''.join(f'<button class="filter{" is-active" if f == "All" else ""}" data-filter="{"all" if f == "All" else e(f)}" aria-pressed="{"true" if f == "All" else "false"}">{e(f)}</button>' for f in filters)
        cards = '\n'.join(work_card(p, s, i + 1) for i, s in enumerate(C['work_order']))
        return f'''{page_hero(p, [('Portfolio', 'portfolio/')], f'{len(C["work_order"])} featured projects', 'Our <em>portfolio</em>',
                  'Every project here started with a real business problem and ended with measurable results — websites, brands, e-commerce stores and digital campaigns, built by our in-house team.')}

      <section class="section">
        <div class="filters reveal" role="group" aria-label="Filter projects">{chips}</div>
        <div class="pf-grid">
{cards}
        </div>
      </section>

{cta_band(p, 'Your project could be <span class="thin">next.</span>', 'Free consultation, honest strategy, no obligation. Tell us about your business.')}'''

    write('portfolio/', f'Portfolio — {SITE}', 'Websites, brands and platforms we have built for hospitals, clinics, schools, NGOs and movements in India and the UK.',
          body, active='portfolio/', crumbs=[('Portfolio', 'portfolio/')], jsonld=[ORG])


def case_study(i, slug):
    w = C['work'][slug]
    nxt = C['work_order'][(i + 1) % len(C['work_order'])]

    def body(p):
        st = ''.join(f'<div><dd>{e(a)}</dd><dt>{e(b)}</dt></div>' for a, b in w['stats'])
        did = ''.join(f'<li class="reveal" style="--d: {(j % 2) * 80}ms"><span class="step-n">{j + 1:02d}</span><h3>{e(d["title"])}</h3><p>{e(d["text"])}</p></li>' for j, d in enumerate(w['did']))
        tags = ''.join(f'<li>{e(t)}</li>' for t in w['services'])
        live = f'<a class="btn btn-navy btn-lg" href="{e(w["live"])}" target="_blank" rel="noopener noreferrer">Visit live site {ARROW}</a>' if w['live'] else ''
        nw = C['work'][nxt]
        return f'''{page_hero(p, [('Portfolio', 'portfolio/'), (w['name'], f'work/{slug}/')], f'{w["category"]} · {w["year"]}', e(w['name']),
                  w['tagline'], live + f'<a class="btn btn-outline btn-lg" href="{p}contact/">Start a similar project</a>')}

      <section class="section">
        <div class="case-shot reveal" style="--c: {w['color']}">
          {shot(p, w, big=True)}
        </div>
        <dl class="stat-row reveal">{st}</dl>
      </section>

      <section class="section case-grid">
        <div class="reveal"><p class="eyebrow">Overview</p><p class="prose-lead">{e(w['overview'])}</p></div>
        <div class="reveal"><p class="eyebrow">The challenge</p><p class="prose-lead">{e(w['challenge'])}</p></div>
      </section>

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">What we did</p>
          <h2>How we <span class="thin">solved it</span></h2>
        </div>
        <ol class="steps steps-2">{did}</ol>
      </section>

      <section class="section">
        <div class="outcome reveal" style="--c: {w['color']}">
          <p class="eyebrow">The outcome</p>
          <p>{e(w['outcome'])}</p>
          <ul class="tags">{tags}</ul>
        </div>
      </section>

      <section class="section">
        <a class="next-case reveal" href="{p}work/{nxt}/" style="--c: {nw['color']}">
          <span>Next case study</span>
          <b>{e(nw['name'])}</b>
          <span class="arrow" aria-hidden="true">→</span>
        </a>
      </section>

{cta_band(p, 'Want results like these <span class="thin">for your business?</span>')}'''

    write(f'work/{slug}/', f'{w["name"]} — case study — {SITE}', f'{w["name"]}: {w["tagline"]} {w["overview"]}'[:155], body, active='portfolio/',
          crumbs=[('Portfolio', 'portfolio/'), (w['name'], f'work/{slug}/')])


def blog_index():
    def body(p):
        cards = ''.join(f'''<a class="post-card reveal" href="{p}blog/{s}/" style="--d: {(i % 3) * 80}ms">
            <figure class="post-cover">{photo(p, *BLOG_PHOTO[s])}</figure>
            <span class="post-meta"><b>{e(b["category"])}</b> {e(b["date"])} · {e(b["read"])}</span>
            <h2>{e(b["title"])}</h2>
            <p>{e(b["excerpt"])}</p>
            <span class="post-more">Read article {ARROW}</span>
          </a>''' for i, (s, b) in enumerate((s, C['blog'][s]) for s in C['blog_order']))
        return f'''{page_hero(p, [('Blog', 'blog/')], 'Insights', 'The <em>blog</em>',
                  'Practical ideas that help your business grow — no jargon, no fluff.')}

      <section class="section">
        <div class="post-grid">{cards}</div>
      </section>

{cta_band(p)}'''

    write('blog/', f'Blog — {SITE}', 'Practical ideas on websites, branding, SEO, ads and automation for growing businesses.',
          body, active='blog/', crumbs=[('Blog', 'blog/')])


def blog_post(i, slug):
    b = C['blog'][slug]
    nxt = C['blog_order'][(i + 1) % len(C['blog_order'])]

    def body(p):
        paras = ''.join(f'<p>{e(t)}</p>' for t in b['body'])
        return f'''{page_hero(p, [('Blog', 'blog/'), (b['title'], f'blog/{slug}/')], f'{b["category"]} · {b["date"]} · {b["read"]}', e(b['title']), b['excerpt'], image=BLOG_PHOTO[slug])}

      <section class="section">
        <article class="article reveal">
          {paras}
          <footer class="article-by">{brand_mark(p)}<span><b>{SITE} team</b>Vijayawada, India</span></footer>
        </article>
        <a class="next-case reveal" href="{p}blog/{nxt}/">
          <span>Next article</span>
          <b>{e(C['blog'][nxt]['title'])}</b>
          <span class="arrow" aria-hidden="true">→</span>
        </a>
      </section>

{cta_band(p, 'Want results like these <span class="thin">for your business?</span>')}'''

    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': b['title'], 'description': b['excerpt'],
          'author': {'@type': 'Organization', 'name': SITE}, 'publisher': {'@type': 'Organization', 'name': SITE}}
    write(f'blog/{slug}/', f'{b["title"]} — {SITE}', b['excerpt'][:155], body, active='blog/',
          crumbs=[('Blog', 'blog/'), (b['title'], f'blog/{slug}/')], jsonld=[ld])


def careers():
    jobs = [
        ('Full-Stack Developer', 'Build performant websites and web apps using Next.js, React, and Node.js. You care about clean code, fast load times, and accessibility. 2+ years experience.'),
        ('Performance / Digital Marketer', 'Run Google Ads, Meta Ads, and paid campaigns that deliver measurable ROI. Plan and execute digital marketing strategies across SEO, social media, and email. Data-driven, detail-oriented, and experienced with Indian market budgets.'),
    ]

    def body(p):
        cards = ''.join(f'''<article class="job reveal">
            <ul class="tags"><li>Full-time</li><li>Remote / Vijayawada</li></ul>
            <h3>{t}</h3>
            <p>{d}</p>
            <a class="btn btn-navy" href="mailto:{EMAIL}?subject={e('Application — ' + t)}">Apply via email {ARROW}</a>
          </article>''' for t, d in jobs)
        return f'''{page_hero(p, [('Careers', 'careers/')], 'Careers', 'Build what <em>matters.</em>',
                  'We’re a small team helping Indian businesses look credible, grow digitally, and compete globally. If you care about craft and impact, you’ll fit right in.',
                  image=('careers-office', 'Our team in a planning meeting at the Creators Touch office'))}

      <section class="section">
        <div class="section-head reveal">
          <p class="eyebrow">Open positions</p>
          <h2>Current <span class="thin">openings</span></h2>
        </div>
        <div class="grid-2">{cards}</div>
      </section>

      <section class="section">
        <div class="apply reveal">
          <div>
            <p class="eyebrow">How to apply</p>
            <h2>No cover letters. <span class="thin">No algorithms.</span></h2>
            <p>Send us an email with your portfolio or resume, a short note about which role interests you and why, and any links to work you’re proud of. That’s it.</p>
          </div>
          <div class="apply-side">
            <p>Don’t see a role that fits? We’re always open to meeting talented people.</p>
            <a class="btn btn-outline btn-lg" href="mailto:{EMAIL}?subject={e('General enquiry — Careers')}">Say hello {ARROW}</a>
          </div>
        </div>
      </section>'''

    write('careers/', f'Careers — {SITE}', 'Join a small Vijayawada team building websites and campaigns for growing businesses. Full-stack developer and digital marketer roles open.',
          body, active='careers/', crumbs=[('Careers', 'careers/')])


def contact(form_html):
    def body(p):
        cards = [
            ('call', 'Call or WhatsApp', f'<a href="{PHONE_HREF}">{PHONE}</a>', 'var(--blue)'),
            ('mail', 'Email us', f'<a href="mailto:{EMAIL}">{EMAIL}</a>', 'var(--pink)'),
            ('chat', 'Chat now', f'<a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Message us on WhatsApp</a>', '#1fa855'),
            ('pin', 'Find us', '<span>Vijayawada, Andhra Pradesh</span>', '#f2a900'),
        ]
        cc = ''.join(f'<div class="contact-card reveal" style="--c: {c}; --d: {i * 80}ms"><span class="tile-icon">{icon(ic)}</span><h3>{t}</h3>{v}</div>' for i, (ic, t, v, c) in enumerate(cards))
        return f'''{page_hero(p, [('Contact', 'contact/')], 'Start a project', 'Tell us where you want your <em>business</em> to go.',
                  'You don’t need to know the marketing terminology. Tell us about your business and what you want to improve. We’ll help you figure out the next step.')}

      <section class="section">
        <div class="grid-4">{cc}</div>
      </section>

      <section class="section" id="contact">
        <div class="cta reveal">
          <div class="cta-glow" aria-hidden="true"></div>
          <div class="cta-copy">
            <p class="eyebrow">Book a free consultation</p>
            <h2>Let’s plan your <span class="thin">next step</span></h2>
            <p>Fill in the form and we’ll reply on WhatsApp within one business day with a plan tailored to your business.</p>
            <dl class="mini-stats"><div><dd>2000+</dd><dt>Brands served</dt></div><div><dd>{YEARS}+</dd><dt>Years experience</dt></div><div><dd>&lt;24h</dd><dt>Response time</dt></div></dl>
          </div>
          {form_html}
        </div>
      </section>

      <section class="section">
        <div class="office reveal">
          <figure class="office-photo">{photo(p, 'vijayawada', 'The Krishna river at Vijayawada')}</figure>
          <div>
            <p class="eyebrow">Our office</p>
            <h2>Vijayawada, <span class="thin">Andhra Pradesh</span></h2>
            <p>We work with businesses across India and internationally, but our home base is in the heart of Vijayawada. Drop in for a coffee and a conversation about your business.</p>
          </div>
          <a class="btn btn-outline btn-lg" href="https://www.google.com/maps/search/?api=1&query=Vijayawada%2C+Andhra+Pradesh" target="_blank" rel="noopener noreferrer">Open in Google Maps {ARROW}</a>
        </div>
      </section>'''

    write('contact/', f'Contact — {SITE}', 'Call, WhatsApp or email us, or book a free consultation for your website, branding or marketing.',
          body, active='contact/', crumbs=[('Contact', 'contact/')], jsonld=[ORG])


def legal(key, path, label):
    d = C[key]

    def body(p):
        out = []
        for kind, text in d['blocks']:
            if kind == 'h2':
                out.append(f'<h2>{e(text)}</h2>')
            elif ' • ' in text or text.startswith('• '):
                head_, *items = [x.strip() for x in text.split('•')]
                if head_:
                    out.append(f'<p>{e(head_)}</p>')
                out.append('<ul>' + ''.join(f'<li>{e(x)}</li>' for x in items if x) + '</ul>')
            else:
                out.append(f'<p>{e(text)}</p>')
        return f'''{page_hero(p, [(label, path)], d['updated'], e(d['title']), d['lead'])}

      <section class="section">
        <article class="article legal reveal">
          {''.join(out)}
        </article>
      </section>

{cta_band(p, 'Have <span class="thin">questions?</span>', 'If anything here is unclear, reach out and we’ll explain it in plain language.')}'''

    write(path, f'{d["title"]} — {SITE}', d['lead'][:155], body, crumbs=[(label, path)])


def not_found():
    def body(p):
        return f'''      <section class="page-hero page-404">
        <div class="page-hero-art" aria-hidden="true">{brand_mark(p).replace('brand-mark', 'page-hero-mark')}</div>
        <div class="page-hero-inner">
          <p class="eyebrow">Error 404</p>
          <h1>This page <em>wandered off.</em></h1>
          <p class="lead">The link may be old or mistyped. Let’s get you back on track.</p>
          <div class="hero-cta">{btns(p, ('Go to the home page', ''), ('Contact us', 'contact/'))}</div>
        </div>
      </section>'''
    # GitHub Pages serves 404.html for a missing URL at any depth, so its links must be absolute
    write('404.html', f'Page not found — {SITE}', 'This page could not be found.', body, prefix='/' + BASE.split('/', 3)[3])


# ---------------------------------------------------------------- home page sync + run

def sync_home():
    path = os.path.join(ROOT, 'index.html')
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'(<!-- site:header -->\n).*?(\n\s*<!-- /site:header -->)', lambda m: m.group(1) + header('') + m.group(2), s, flags=re.S)
    s = re.sub(r'(<!-- site:footer -->\n).*?(\n\s*<!-- /site:footer -->)', lambda m: m.group(1) + footer('') + m.group(2), s, flags=re.S)
    s = re.sub(r'(styles\.css|script\.js|motion\.js)\?v=[\w]+', lambda m: f'{m.group(1)}?v={V}', s)
    s = s.replace('https://www.webdesigninvijayawada.com/', BASE)
    open(path, 'w', encoding='utf-8', newline='\n').write(s)
    form = re.search(r'<form class="form" id="enquiry".*?</form>', s, flags=re.S).group(0)
    return form


def sitemap():
    urls = [''] + PAGES
    xml = ''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in urls)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xml}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')


if __name__ == '__main__':
    form = sync_home()
    about()
    services_index()
    for slug in C['services']:
        service_page(slug)
    portfolio()
    for i, slug in enumerate(C['work_order']):
        case_study(i, slug)
    blog_index()
    for i, slug in enumerate(C['blog_order']):
        blog_post(i, slug)
    careers()
    contact(form)
    legal('privacy', 'privacy-policy/', 'Privacy policy')
    legal('terms', 'terms-and-conditions/', 'Terms & conditions')
    not_found()
    sitemap()
    print(f'Built {len(PAGES)} pages + 404, sitemap.xml, robots.txt (assets v={V})')
