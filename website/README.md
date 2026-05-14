# BeatIQ marketing site (www.beatiq.co.uk)

Next.js 14 **App Router** site (`app/page.tsx` is the homepage). **No Django or API dependency.**

Production output is a **static export** (`next.config.mjs` → `output: "export"`) into `website/out/`, which Vercel can serve as plain HTML.

## Local

```bash
cd website
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Production build

```bash
cd website
npm ci
npm run build
```

After `npm run build`, the static site is in **`website/out/`** (includes `index.html` for `/`).

## Vercel (fixes 404 when the Git repo is the full BeatIQ monorepo)

The repo root contains Django **and** this Next app under **`website/`**. Vercel must either build from `website/` **or** use the root **`vercel.json`**.

### Option A — Recommended (repo root on Vercel)

1. Import the **BeatIQ** Git repository.
2. In **Settings → General → Root Directory**, leave it **empty** (repository root).
3. Do **not** override Build / Output in the dashboard unless you know what you are changing — the committed **`vercel.json`** at the repo root runs:
   - `cd website && npm ci`
   - `cd website && npm run build`
   - publishes **`website/out`**
4. Optional env: `NEXT_PUBLIC_SITE_URL` = `https://www.beatiq.co.uk`
5. Add the custom domain **www.beatiq.co.uk**.

If you previously set **Root Directory** to `website`, clear it for Option A, or use Option B.

### Option B — Vercel Root Directory = `website`

1. Set **Root Directory** to **`website`**.
2. Remove or ignore the **repo root** `vercel.json` (or delete its custom commands in the Vercel UI so defaults apply).
3. Framework: **Next.js**. With `output: "export"`, set **Output Directory** to **`out`** (Vercel often detects this automatically).

### If you still see `NOT_FOUND`

Confirm the deployed files include **`index.html`** at the configured output root. The static export places it at `website/out/index.html` (Option A) or `out/index.html` (Option B).

## Public routes

| Path | Page |
|------|------|
| `/` | Landing |
| `/privacy-policy/` | Privacy Policy |
| `/terms-and-conditions/` | Terms and Conditions |
| `/cookie-policy/` | Cookie Policy |

SEO: `metadata` in `app/layout.tsx` and per-route `metadata`, plus `app/sitemap.ts` and `app/robots.ts`.
