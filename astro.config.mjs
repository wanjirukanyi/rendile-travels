import { defineConfig } from 'astro/config';

// Rendile Travels — static marketing site.
// `build.format: 'file'` emits pages as `kenya.html` at the site root (not
// `kenya/index.html`), so every existing relative link (assets/, *.html) and
// live URL keeps working exactly as it did in the old hand-written static site.
export default defineConfig({
  site: 'https://rendiletravels.com',
  build: {
    format: 'file',
  },
});
