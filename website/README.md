# BeatIQ marketing site (www.beatiq.co.uk)

Static-first **Next.js 14** app: landing page and public legal documents. **No Django or API dependency** — deploy on **Vercel** by pointing the project at this directory.

## Local

```bash
cd website
npm install
npm run dev
```

With a committed `package-lock.json`, CI and Vercel can use `npm ci` instead of `npm install`.

Open [http://localhost:3000](http://localhost:3000).

## Production build

```bash
cd website
npm ci
npm run build
npm run start
```

## Vercel

1. New project → import the **BeatIQ** Git repository.
2. Set **Root Directory** to `website`.
3. Framework preset: **Next.js** (auto).
4. Optional env: `NEXT_PUBLIC_SITE_URL` = `https://www.beatiq.co.uk` (defaults to this if unset).
5. Add custom domain **www.beatiq.co.uk** in Vercel → Domains.

Public routes:

| Path | Page |
|------|------|
| `/` | Landing |
| `/privacy-policy` | Privacy Policy |
| `/terms-and-conditions` | Terms and Conditions |
| `/cookie-policy` | Cookie Policy |

SEO: `metadata` in `app/layout.tsx` and per-route `metadata`, plus `app/sitemap.ts` and `app/robots.ts`.
