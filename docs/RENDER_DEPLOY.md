# BeatIQ Django backend — production deployment on Render

This repository is **BeatIQ only** (Django API under `config/`, `apps/`, `manage.py`). It is **not** BioAegix; use a separate Render service, GitHub repo, database, and environment variables for BeatIQ.

---

## 1. Repository scope

| Path | Purpose |
|------|--------|
| `manage.py` | CLI entry (defaults to `config.settings.development`) |
| `config/` | URLs, WSGI/ASGI, Celery, settings |
| `apps/` | Domain apps (accounts, catalog, …) |

**Demo / seed data** (`seed_demo_account`, `seed_catalog`, `beatiq_createsuperuser`) are **management commands only**. Nothing runs them on app startup or in migrations.

---

## 2. Render services

1. **PostgreSQL** — create a Render Postgres instance (note internal `DATABASE_URL`).
2. **Web Service** — connect the same Git repo, root directory `/` (repo root).

Link the Postgres **environment group** to the web service so `DATABASE_URL` is injected automatically.

---

## 3. Environment variables (BeatIQ production)

Set at minimum:

| Variable | Example / notes |
|----------|-----------------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `SECRET_KEY` | Long random string (50+ chars); **never** commit to git |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `beatiq-api.onrender.com,your-custom-domain.com` (no spaces) |
| `DATABASE_URL` | Injected by Render when DB is linked (`dj-database-url`, `conn_max_age=600`, `ssl_require=True`) |
| `PUBLIC_API_BASE_URL` | `https://beatiq-api.onrender.com` (no `/api/v1` suffix) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated `https://` origins for **browser** clients (optional if you only use native Android; see below) |
| `CSRF_TRUSTED_ORIGINS` | Optional; if unset and `RENDER_EXTERNAL_URL` is `https://…`, production derives one entry |

**Render sets** `RENDER=true` and `RENDER_EXTERNAL_URL` on web services — production uses them for host/CSRF defaults.

**Email (optional):** `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`.

**Celery:** set `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` to a **Render Redis** URL if you run a worker service; otherwise async tasks need another broker.

---

## 3b. Login returns HTTP 500 (`no such table: accounts_user`)

That error means Django is using **SQLite** on the server (empty file, no migrations) instead of **PostgreSQL**. Typical causes:

1. **`DATABASE_URL` is not set** on the web service — link your Render PostgreSQL to the web service so Render injects `DATABASE_URL`.
2. **`DJANGO_SETTINGS_MODULE`** is not `config.settings.production` — wrong module may still point at dev-like DB config.
3. **Release / migrate never ran** — ensure `preDeployCommand` (or a manual Shell) runs `python manage.py migrate` against the same database.

After fixing env vars, redeploy. Production settings now **refuse SQLite** unless you explicitly set `BEATIQ_ALLOW_SQLITE_PRODUCTION=1` (local experiments only).

---

## 4. Build / release / start commands

**Build command** (install + static files):

```bash
bash scripts/render_build.sh
```

Equivalent one-liner:

```bash
pip install -r requirements.txt && DJANGO_SETTINGS_MODULE=config.settings.production python manage.py collectstatic --noinput
```

**Release command** (migrations; Render runs this after build when configured):

```bash
bash scripts/render_release.sh
```

Equivalent:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py migrate --noinput
```

**Start command:**

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
```

`$PORT` is required on Render.

---

## 5. Migrations

- Migrations are **versioned** under each app’s `migrations/` package.
- Run them only via **release** or manual `migrate` — never auto-run seed commands in production.
- On Render, **`preDeployCommand`** in `render.yaml` runs `scripts/render_release.sh` (`migrate --noinput`) **after** a successful build and **before** traffic is routed to the new release, so schema is applied before Gunicorn serves the new deploy.

---

## 6. Secrets and `.env`

- **`.env` is gitignored** (see `.gitignore`). Do not commit secrets.
- Copy **`.env.example`** to `.env` locally only; use the Render dashboard for production secrets.

---

## 7. Android app — API base URL

Django mounts the API at **`/api/v1/`** (see `config/urls.py`).

If your Render hostname is:

`https://beatiq-api.onrender.com`

then set the Android `beatiq.api.base.url` in **`BeatIQ-App`** `local.properties` to **either**:

```properties
beatiq.api.base.url=https://beatiq-api.onrender.com/api/v1/
```

or (no trailing slash — the app normalizes it):

```properties
beatiq.api.base.url=https://beatiq-api.onrender.com/api/v1
```

**Exact pattern:** `https://<your-render-service>.onrender.com/api/v1` plus optional trailing `/`.

Native **OkHttp** calls do not rely on **CORS**; CORS env vars matter for browsers / Swagger / future web clients. You may still set `CORS_ALLOWED_ORIGINS` to your public site or admin origin if needed.

---

## 8. Health check

Configure Render health check path: **`/health/`**

---

## 9. Optional: `render.yaml`

A minimal **`render.yaml`** is in the repo root for Blueprint deploys. Create and **link** a Render PostgreSQL database in the dashboard, then set `DATABASE_URL`, `ALLOWED_HOSTS`, `PUBLIC_API_BASE_URL`, and (optionally) `CORS_ALLOWED_ORIGINS` (`sync: false` placeholders). Replace auto-generated `SECRET_KEY` with a long manual value if you prefer.

Make scripts executable locally if needed:

```bash
chmod +x scripts/render_build.sh scripts/render_release.sh
```
