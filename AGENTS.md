# AGENTS.md

## Project

Mario's one-page portfolio site. Django 5 (one app, `portfolio`), server-rendered
templates, plain JavaScript (no framework, no build step), PostgreSQL 16, served by
gunicorn + whitenoise, run with Docker Compose. Python 3.11.

Content (focus areas, projects, posts, timeline) lives in the database and is edited in
`/admin`. `portfolio/data.py` is starter content only: `load_initial_data` copies it into
an **empty** database on container start, so editing it does not change a running site.

## Commands

- Run: `docker compose up --build`, then <http://localhost:8000/> and `/admin/`.
- Code is copied into the image, not mounted: rebuild (`--build`) after every change before
  checking it in the browser.
- Django commands against the running stack: `docker compose exec web python manage.py <cmd>`
- Migrations: create them in a local venv (`python manage.py makemigrations`; the warning
  about not reaching the database is expected) so the files land in the repo. Creating
  them inside the container loses them.
- `python manage.py runserver` outside Docker does not work (no reachable database).
- There are no tests and no linter configured yet.

## Where things live

- Settings: `mario_portfolio/settings.py`, all from environment variables (see README)
- Models / admin / view: `portfolio/models.py`, `portfolio/admin.py`, `portfolio/views.py`
- Template: `portfolio/templates/portfolio/index.html`. The hero, the infrastructure
  panel and the footer are hard-coded here, not in the database.
- Styles: `portfolio/static/portfolio/css/style.css` (dark theme only; the light theme
  rules exist but nothing turns them on)
- Interactivity: `portfolio/static/portfolio/js/app.js` (tabs and focus-area filter)
- Container start-up: `scripts/run.sh` (migrate, seed, optional superuser, collectstatic,
  gunicorn)

## Rules

- Never commit secrets (`.env`, `SECRET_KEY`, database passwords).
- Model changes need a migration, committed with the change.
- Check UI changes in the running site, not only by reading the code.
- The settings defaults (`DEBUG=1`, a public secret key, `ALLOWED_HOSTS=*`) are for local
  development; don't treat the current setup as production-ready.
- Ask before deleting files, changing Docker/deploy setup, pushing to `main`, or running
  `docker compose down -v` (it deletes the database).
- Keep `README.md` and this file accurate when you change how things work.
- Conventional Commits (`feat:`, `fix:`, `docs:`…); the body explains why.
