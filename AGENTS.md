# AGENTS.md

## Project

Mario's one-page portfolio site. Django 5 (one app, `portfolio`), server-rendered
templates, plain JavaScript (no framework, no build step), PostgreSQL 16, Python 3.13.
Development: `docker-compose.yml` (code mounted, `runserver`). Production:
`docker-compose.deploy.yml` (gunicorn + whitenoise behind nginx with Let's Encrypt,
settings from `.env`), the same layout as the `gesis_surf_backend` repo.

Content (focus areas, projects, posts, timeline) lives in the database and is edited in
`/admin`. `portfolio/data.py` is starter content only: `load_initial_data` copies it into
an **empty** database on container start, so editing it does not change a running site.

## Commands

- Run: `docker compose up --build`, then <http://localhost:8000/> and `/admin/`. Code is
  mounted and reloads; rebuild only after changing `requirements*.txt` or the `Dockerfile`.
- Django commands: `docker compose run --rm app python manage.py <cmd>` (or `exec app` on
  the running stack). `makemigrations` run this way writes into the repo.
- Tests: `docker compose run --rm app python manage.py test` (separate test database).
  Lint: `docker compose run --rm app flake8`. CI runs both (`.github/workflows/checks.yml`)
  and, on pushes to `main`, builds the image to `ghcr.io` and deploys it over SSH with
  `scripts/deploy.sh`. A push to `main` is a production deploy.
- `python manage.py runserver` outside Docker does not work (no reachable database).
- Terraform (Hetzner server): `docker compose run --rm terraform <plan|validate|fmt>`;
  needs `HCLOUD_TOKEN` in the environment.
- Deploy steps are in the README; never run deploy commands against a server, or
  `terraform apply`/`destroy`, unless asked.

## Where things live

- Settings: `mario_portfolio/settings.py`, all from environment variables (see README)
- Models / admin / view: `portfolio/models.py`, `portfolio/admin.py`, `portfolio/views.py`
- Template: `portfolio/templates/portfolio/index.html`. Hero and footer come from the
  `Profile` and `ProfileLink` models (admin); only the infrastructure panel is hard-coded.
  Link logos are SVGs in `portfolio/templates/portfolio/icons/<kind>.svg` (credits in
  README). The photo is `portfolio/static/portfolio/img/mario-ramirez.jpg`.
- Content changes that must reach production go in data migrations (see
  `0003_initial_profile`, `0004_replace_seed_timeline`); `data.py` only seeds empty
  databases.
- Styles: `portfolio/static/portfolio/css/style.css`, a dark "cassette futurism" look
  (1970s–80s sci-fi hardware). Fonts are self-hosted in `portfolio/static/portfolio/fonts/`:
  Michroma only for small capital section headings, Jost for names and titles, Source
  Sans 3 for body text, IBM Plex Mono for labels, DSEG14 for the LED readouts. Never load
  fonts or assets from third-party domains (GDPR); keep text contrast at WCAG AA (4.5:1).
- Skills: `.agents/skills/` (real files) with symlinks in `.claude/skills/`, tracked in
  `skills-lock.json`. Use `web-design-guidelines` to review UI changes. Add skills one at a
  time with `npx skills add <repo> --skill <name> -a claude-code -a github-copilot`, and
  read their files before committing.
- Interactivity: `portfolio/static/portfolio/js/app.js` (tabs and focus-area filter)
- Production start-up: `scripts/run.sh` (migrate, seed, `ensure_superuser`, gunicorn).
  Static files are collected at image build time into `/vol/static` (`Dockerfile`) and
  served by whitenoise.
- Proxy / certificates: `docker/proxy/` (nginx templates for HTTP-only and HTTPS;
  `www.DOMAIN` redirects to `DOMAIN`) and `docker/certbot/` (one certificate for both).
- Hosting: Hetzner Cloud server created by Terraform in `infra/` (local, git-ignored
  state; first-boot setup in `infra/cloud-init.yaml`), domain `geomario.com` with DNS at
  GoDaddy (README "Deploy"). On the server the app runs from
  `/home/deploy/geomario_personal` as the `deploy` user (no sudo), whose crontab renews
  the certificate daily.

## Rules

- Never commit secrets (`.env`, `SECRET_KEY`, database passwords).
- Model changes need a migration, committed with the change.
- Check UI changes in the running site, not only by reading the code.
- The settings defaults (`DEBUG=1`, a public secret key, `ALLOWED_HOSTS=*`) are for local
  development only; with `DJANGO_DEBUG=0` settings refuse to load without real values.
  Don't weaken that check.
- Ask before deleting files, changing Docker/deploy setup, pushing to `main`, or running
  `docker compose down -v` (it deletes the database).
- Keep `README.md` and this file accurate when you change how things work.
- Conventional Commits (`feat:`, `fix:`, `docs:`…); the body explains why.
