# Rendile Travels — where we are

_Last updated: 2026-06-22_

A static, no-framework marketing site for a women's luxury East Africa travel brand.
**Source of truth = this folder** (`~/Documents/oaks/rendile-travels/`). Not yet published.

## Run / build
- **Preview:** `sh tools/sync-preview.sh`, then open http://localhost:4321/
  (the server is sandboxed and can't read `~/Documents`, so it serves the copy at
  `~/.rendile-preview`; ask Claude to `preview_start` if it isn't running).
  Quick alternative: `python3 -m http.server 8000` from this folder.
- **Deploy zip:** `sh tools/build-deploy.sh` → `rendile-travels-site.zip` (drag into Cloudflare Pages).

## Backup & recovery (off-machine — set up 2026-06-22)
- **GitHub (private):** https://github.com/wanjirukanyi/rendile-travels — the off-machine source of record.
  **Save your work after editing:** `git add -A && git commit -m "…" && git push`.
- **One-command backup:** `sh tools/autosave.sh` — commits + pushes, but only if something changed.
- **Auto-backup on session end (optional):** add a `SessionEnd` hook to `.claude/settings.local.json`
  calling `tools/autosave.sh` (Claude is blocked from self-installing it — paste it by hand):
  `"hooks": {"SessionEnd": [{"hooks": [{"type": "command", "command": "sh /Users/maureenkanyi/Documents/oaks/rendile-travels/tools/autosave.sh", "timeout": 30}]}]}`
- **iCloud:** dated full-source zips in `~/Library/Mobile Documents/.../Rendile Travels Backups/`.
- **Recover on a new machine:** `git clone https://github.com/wanjirukanyi/rendile-travels.git`
  (or unzip the iCloud backup). Then `sh tools/sync-preview.sh` + preview as above.
- The deploy zip is git-ignored (rebuild it); the parent Odoo `.env` is NOT in this repo (root is this folder).

## Pages (all built, wired, verified live)
- **Home:** index.html
- **Destinations (rich):** kenya, tanzania, uganda, rwanda
- **Kenya itineraries (6):** classic-kenya-safari, great-migration, savanna-to-sea,
  women-only-kenya, mummy-and-me-safari, lamu-yoga-festival
- **Zanzibar trip:** zanzibar-womens-retreat
- **SEO articles (7):** maasai-mara, amboseli, lake-nakuru, samburu, lamu-coast, nairobi, best-time-kenya
- **Other:** contact, custom-safaris

## Done recently (this session)
- Built the Tanzania / Uganda / Rwanda rich destination pages with verified imagery.
- Swapped the Tanzania card/hero portrait for a more flattering one (same photographer).
- Wired the 3 homepage Signature Trips to internal pages; built the missing Zanzibar page.
- Gave **every** internal page its own hero, distinct from its homepage card and its own highlights.
- Made the setup durable (persistent preview copy, scripts in `tools/`, one-command deploy build).

## Next steps (pick up here)
1. Upgrade the other 5 Kenya itineraries to the **full** `classic-kenya-safari.html` template
   (day photos, Camps & Lodges, rates table, what's-included). Only classic-kenya-safari has it.
2. Build sub-pages for Tanzania/Uganda/Rwanda: per-highlight SEO articles + itinerary-detail pages.
   Until then their highlight/season cards are non-clickable and journey cards go to `contact.html?trip=…`.
3. Point the homepage **"Explore all trips"** button somewhere real (currently `mailto:`), or build a trips index.
4. Wire the **contact form** to a backend (Formspree / Netlify Forms) — it's a front-end demo today.
5. Replace placeholder contact details: `hello@rendiletravels.com`, `+254 700 000 000`, `wa.me/254700000000`.
6. **Publish:** Cloudflare Pages (Direct Upload of the zip), then move `rendiletravels.com` DNS from GoDaddy.
7. (Optional) Refresh `README.md` — it still describes the old single-page / Unsplash-placeholder version.

## Gotchas
- The preview must serve from a non-Documents, non-`/tmp` folder (macOS TCC blocks the sandboxed
  server from `~/Documents`; `/tmp` gets auto-wiped). `~/.rendile-preview` satisfies both. Re-sync with
  `tools/sync-preview.sh` after edits.
- Imagery is self-hosted & verified (Wikimedia Commons + Pexels), credited in each page's footer.
  **Never pick image IDs blind** — download and actually look before using.
- `tools/`, `README.md`, `STATUS.md`, and `assets/Layer 1 (2).png` are excluded from the deploy zip.
