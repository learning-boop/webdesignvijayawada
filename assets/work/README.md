# Project screenshots

Put client website screenshots in this folder. Each project card shows its screenshot inside a
browser frame, and hovering the card slowly scrolls through the whole page.

## What to capture

- **Full-page** screenshots (the whole page top to bottom, not just the first screen).
  In Chrome: open DevTools → Ctrl+Shift+P → "Capture full size screenshot".
- Width **1440px**. Any height is fine; 4000–7000px works best for the hover scroll.
- Save as **.webp** or **.jpg**, ideally under 400 KB each (compress at squoosh.app).
- Name them simply, e.g. `jago-andhra.webp`, `aayush-hospitals.webp`.

## Adding one to the site

In `index.html`, find the project's card. Inside `<div class="shot-view">` replace the
placeholder `<div class="shot-page mock-page"> … </div>` with:

```html
<img class="shot-page" src="assets/work/jago-andhra.webp" alt="Jago Andhra website" loading="lazy" />
```

To add a new project, copy a whole `<a class="work-card" …> … </a>` block and change the name,
link, category (`data-cat`: `health`, `aesthetics` or `brand`), colour (`--c`) and number.
Then update the "02 / 06" total if you also want the right number before the page loads.
