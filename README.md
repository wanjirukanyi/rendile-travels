# Rendile Travels — website

Luxury East African journeys, designed for women. A fast, self-contained marketing
site (no build step, no framework) — just open it or drop it on any host.

## Files
- `index.html` — the whole single-page site (hero, pillars, destinations, ways to
  travel, signature journeys, the Rendile Way, story, reviews, FAQ, inquiry form,
  newsletter, footer).
- `styles.css` — all styling and responsive layout.
- `script.js` — sticky header, mobile menu, scroll reveals, testimonial slider,
  and front-end form handling.

## Preview locally
Open `index.html` in a browser, or serve the folder:
```bash
cd rendile-travels
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Publishing
This is plain HTML/CSS/JS, so it works anywhere:
- **Netlify / Vercel / Cloudflare Pages** — drag-and-drop the folder, or connect a repo.
- **GitHub Pages** — push the folder and enable Pages.
- **Your existing GoDaddy hosting** — upload the three files via the file manager.

To use the domain **rendiletravels.com**, point its DNS at whichever host you choose.

### Building the deploy zip
Always build the upload artifact with the script — it bakes in the exclusions so internal
files never ship:
```bash
sh tools/build-deploy.sh   # → rendile-travels-site.zip (drag into Cloudflare Pages)
```
Excluded from the zip: `tools/` (helper scripts), `README.md`, `STATUS.md`,
`assets/Layer 1 (2).png` (hi-res logo source), `*.DS_Store`, and the zip itself.

## Local tooling (`tools/`, not deployed)
- `build-deploy.sh` — builds the deploy zip (above).
- `sync-preview.sh` — rsyncs the site into `~/.rendile-preview`, the persistent copy the
  sandboxed preview server reads (it cannot read `~/Documents`). Run after edits, then refresh
  `http://localhost:4321/`.
- `fetch_commons.py` / `finalize_commons.py` — stage & download verified Wikimedia Commons
  imagery (search → visually verify → download → `sips` resize).

## Making it real (next steps)
1. **Inquiry form** — currently shows a thank-you on the page but does not send
   anywhere. Wire it to a service in `script.js` (look for the `POST` comment):
   - Easiest: a [Formspree](https://formspree.io) endpoint (`<form action="https://formspree.io/f/XXXX" method="POST">`), or Netlify Forms (`add netlify` attribute to the `<form>`).
   - Or POST to your own backend / CRM (HubSpot, Zoho, etc.).
2. **Email & WhatsApp** — replace the placeholders `hello@rendiletravels.com` and
   `+254 700 000 000` (and the `wa.me/254700000000` link) with your real details.
3. **Photography** — the images are tasteful Unsplash placeholders loaded from their
   CDN. Swap in your own trip photography for authenticity (and to own the rights).
   Replace the `background-image`/`--img` URLs in `index.html`.
4. **Real prices & journeys** — update the three signature journeys and the FAQ price
   guidance once your packages are set.
5. **Analytics / SEO** — add Google Analytics or Plausible, a favicon, and an
   Open Graph image (`og:image`) before launch.

## Brand assets (logo)
Logo files live in `assets/`:
- `assets/logo-mark.png` — transparent emblem only → shown in the top-nav (web-sized 512px,
  generated from the hi-res source `Layer 1 (2).png`, which is kept on disk but NOT deployed).
- `assets/logo-orange.png` — orange background → favicon and social share image.
- `assets/logo-dark.png` — charcoal background, white wordmark → footer.
- `assets/logo-cream.png` — cream background → spare, for light placements.
- `assets/logo.png` — transparent full lockup → spare.

If a file is missing the site degrades gracefully (the emblem hides; the footer falls back to a
text wordmark).

## Hero video
The hero plays a crossfading East-Africa montage streamed from Mixkit's free CDN
(savanna sunset → giraffe & zebra → African drumming → gorilla → turquoise bay). Clips are
listed in the `clips` array in `script.js`; the page photo is the poster (instant paint +
fallback). Video is skipped on phones, when the browser's data-saver is on, or when the OS
prefers reduced motion — the poster shows instead.

- **To swap clips:** edit the URLs in the `clips` array in `script.js`.
- **To self-host** (more robust, heavier upload) instead of streaming: drop compressed, short,
  muted `.mp4` files into `assets/videos/` and point the array at them.
- Free libraries had no clean Mount Kilimanjaro or Maasai-dance clip — the savanna/acacia and
  drumming clips stand in. Swap in licensed/own footage for those exact scenes.

## Brand notes
- Name nods to the **Rendille** people of northern Kenya.
- **Layout/structure** copied from the earlier Kimi build; **colours come from the brand logo.**
- Type: Cormorant Garamond (headings) + Inter (body) + Montserrat (labels/buttons), via Google Fonts.
- Palette (from the logo): brand orange `#DD5A28` (primary), beaded turquoise `#3E9B9C`,
  amber sun `#E7A23C`, beaded rust `#B3381C`, charcoal `#221C18`, cream `#F4EEE3`; 8–14px rounded corners.
