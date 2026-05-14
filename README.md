# BeatIQ — Django API

Backend for the BeatIQ product (`/api/v1/`). **Not** BioAegix — use dedicated hosting and env vars for BeatIQ only.

## Local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit; never commit .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Default settings: `config.settings.development` (SQLite when `USE_SQLITE=true`).

## Public marketing site (Vercel)

The **Next.js** site for **www.beatiq.co.uk** (landing + legal pages) lives in **`website/`**. It has **no backend dependency**. See **[website/README.md](website/README.md)** for local build and **Vercel** setup (repo-root `vercel.json` + static `out/`).

## Production on Render

See **[docs/RENDER_DEPLOY.md](docs/RENDER_DEPLOY.md)** for environment variables, build/release/start commands, and the **exact Android API base URL** pattern.

Optional Blueprint: **`render.yaml`** (review and set secrets / `DATABASE_URL` in the dashboard).
