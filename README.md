# webdesignvijayawada

Website for **Web Design in Vijayawada**: plain HTML, CSS and JavaScript. No framework.
Live at https://learning-boop.github.io/webdesignvijayawada/

## Run it locally

```bash
python -m http.server 5500
```

Then visit http://localhost:5500.

## Pages

| Page | File |
|---|---|
| Home | `index.html` (hand-written) |
| About, Services, Portfolio, Blog, Careers, Contact, Privacy, Terms | `<page>/index.html` |
| 57 service pages | `services/<slug>/index.html` |
| 17 case studies | `work/<slug>/index.html` |
| 6 blog articles | `blog/<slug>/index.html` |
| Not found | `404.html` |

All pages except the home page are **generated** by `_build/build.py` from `_build/content.json`
(text originally taken from creatorstouchglobal.com). Don't edit the generated pages by hand —
change the content or templates, then rebuild:

```bash
python _build/build.py
```

The build also:

- copies the shared header and footer into `index.html` (between the `<!-- site:header -->` and
  `<!-- site:footer -->` markers), so every page has the same menu and footer
- updates the `?v=` numbers on the CSS/JS links so visitors always get the latest files
- writes `sitemap.xml` and `robots.txt`

When the site moves to its own domain, change `BASE` at the top of `_build/build.py` and rebuild.
GitHub Pages doesn't publish folders that start with `_`, so `_build/` stays private to the repo.

## Files

- `styles.css` – design, colours and layout for every page
- `script.js` – logo intro (home), menu, project filters, contact form (opens WhatsApp)
- `motion.js` – scroll animations (GSAP, ScrollTrigger and Lenis, loaded from jsDelivr)
- `assets/` – logo, hero image and project screenshots (`assets/work/README.md` explains how to add more)

## cPanel copy (websitedesigninvijayawada.com)

After `python _build/build.py`, run `python _build/make_cpanel.py`. It writes
`_cpanel/websitedesigninvijayawada-cpanel.zip`: the same site with every address
switched to https://websitedesigninvijayawada.com/ plus an `.htaccess` (https, no-www,
404 page, compression, caching). Upload the zip to `public_html` in cPanel File
Manager and choose Extract. `_cpanel/` is not committed to git.
