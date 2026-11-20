# themagolabs.com

Static site, plain HTML, CSS and vanilla JS. No framework, no build dependencies beyond Python.

## Build

```
python -I src/build.py           # production -> dist/
python -I src/build.py preview   # self-contained preview -> preview/
```

All content lives in `src/data.py`: clients, testimonials, concept builds, packages, services, industries and FAQs.
Edit there, rebuild, deploy `dist/`.

## Before launch

1. `src/data.py` -> `form_endpoint`: paste a Formspree, Web3Forms or Basin endpoint so forms reach your inbox.
   Until then, forms hand off to WhatsApp with the visitor's details prefilled.
2. `src/data.py` -> `ga4`: paste your GA4 measurement ID. Events already fire for form leads,
   phone, email, WhatsApp and live-site clicks, and `/thank-you/` fires the conversion.
3. `src/data.py` -> `email`: switch to a themagolabs.com address once the mailbox exists.
4. Privacy and Terms pages are plain-English drafts. Have them reviewed.
5. Deploy: Vercel serves the committed `dist/` folder (see the root `vercel.json`: no build step, clean URLs,
   trailing slashes, long cache on /assets). After any edit, run the production build, commit `dist/` and push;
   Vercel redeploys from `main` automatically.
6. Verify the domain in Google Search Console and submit `/sitemap.xml`.

## Content rules

- Live client work and testimonials come from magolabs.in. Concept builds come from trades.magolabs.in and
  are always labelled "Concept" with the note that they are not client work.
- Only facts from the source pages. Numbers in the HTML are final values; animation only counts up to them.
- No em dashes anywhere.
