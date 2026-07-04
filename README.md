# Rendile Travels — website

Luxury East African journeys, designed for women. An [Astro](https://astro.build)
static site: pages share one layout, and Astro compiles everything to plain static
HTML (no server, no client framework) for fast, host-anywhere deployment.

> **Migrated from hand-written HTML → Astro.** The 73 original `.html` files are kept
> in `_legacy-html/` as a reference/rollback safety net (not part of the build). Once
> you're happy with the Astro site, that folder can be deleted.

## Project structure
- `src/layouts/BaseLayout.astro` — the **shared chrome**: `<head>`/meta, announcement
  bar, header + nav, footer, and the `script.js` include. **Edit the nav or footer here
  once and every page updates.**
- `src/pages/*.astro` — one file per page (`kenya.astro` → `/kenya.html`). Each holds
  only that page's unique body and passes its SEO/meta (title, description, OG, canonical,
  keywords, JSON-LD) and footer image-credit to `BaseLayout` as props.
- `public/` — served verbatim at the site root: `styles.css`, `script.js`, `assets/`
  (images/video/logos), `CNAME`.
- `astro.config.mjs` — uses `build.format: 'file'` so output is `kenya.html` at the root,
  preserving every existing relative link and live URL.

## Develop & build
```bash
cd rendile-travels
npm install          # first time only
npm run dev          # live-reload dev server (http://localhost:4321)
npm run build        # compile src/ -> dist/ (the deployable static site)
npm run preview      # serve the built dist/ exactly as it'll ship
```
Requires Node (installed via Homebrew: `brew install node`).

## Publishing (Cloudflare)
The site deploys as a Cloudflare assets-only Worker serving `dist/` (see `wrangler.jsonc`):
```bash
npm run build
npx wrangler deploy
```
Cloudflare Pages can also build it natively — set **build command** `npm run build` and
**output directory** `dist`. To use **rendiletravels.com**, point its DNS at Cloudflare.

## Local tooling (`tools/`, not deployed)
- `fetch_commons.py` / `finalize_commons.py` — stage & download verified Wikimedia Commons
  imagery (search → visually verify → download → `sips` resize).
- `build-deploy.sh` / `sync-preview.sh` — **legacy** helpers from the static-HTML era;
  superseded by `npm run build` + `npx wrangler deploy` above.

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
