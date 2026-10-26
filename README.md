# webdesignvijayawada

Website for **Web Design in Vijayawada**: a plain HTML, CSS and JavaScript site with no build step.

## Run it locally

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 5500
```

Then visit http://localhost:5500.

## Files

- `index.html` – all page content
- `styles.css` – design, colours and layout
- `script.js` – intro animation, menu, filters, contact form (opens WhatsApp)
- `motion.js` – scroll animations (GSAP, ScrollTrigger and Lenis, loaded from jsDelivr)
- `assets/` – logo, hero image and project screenshots (`assets/work/README.md` explains how to add more)

After changing `styles.css`, `script.js` or `motion.js`, bump the `?v=` number on its tag in
`index.html` so visitors' browsers load the new version.
