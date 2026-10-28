# Mario — portfolio (Django)

A one-page portfolio site. Django renders the page from content stored in PostgreSQL, and
you edit that content in the Django admin. The page's tabs and filter chips use a small
plain-JavaScript file; there is no frontend framework and no build step.

**Stack:** Python 3.11, Django 5, PostgreSQL 16, gunicorn, whitenoise, Docker Compose.

## Run it

Docker is the supported way to run the site:

```bash
docker compose up --build
```

Then open <http://localhost:8000/> (the site) and <http://localhost:8000/admin/> (the admin).

On every start, the container:

1. applies database migrations,
2. loads the starter content from `portfolio/data.py`, but only if the database is empty,
3. creates an admin user, if the three `DJANGO_SUPERUSER_*` variables below are set,
4. collects static files and starts gunicorn on port 8000.

The code is copied into the image, not mounted, so **after changing any file, run
`docker compose up --build` again** to see the change.

### Admin user

Either set `DJANGO_SUPERUSER_USER`, `DJANGO_SUPERUSER_EMAIL` and `DJANGO_SUPERUSER_PASSWORD`
(in a `.env` file next to `docker-compose.yml`) before the first start, or create one by
hand while the stack is running:

```bash
docker compose exec web python manage.py createsuperuser
```

### Running without Docker

Not supported yet: the settings expect PostgreSQL at host `db`, and the Compose database
doesn't publish its port to your machine. A local virtualenv is still useful for commands
that don't need the database, such as creating migrations:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations   # warns that it can't reach the database; that's fine
```

## Editing content

Most content is edited in the admin, under **Portfolio**:

| Admin section | What it controls on the page |
| --- | --- |
| Focus areas | The filter chips above the projects |
| Projects | Project cards: name, focus area (tag), description, stack (a JSON list such as `["Python", "Django"]`) |
| Posts | Tiles in the Writing tab. **Span** sets the tile shape: square, wide (2×1), tall (1×2) or feature (2×2) |
| Timeline entries | The "Path" section |

Each list has an **Order** column you can edit in place; lower numbers come first.

Not in the admin yet; edit `portfolio/templates/portfolio/index.html` for these: the hero
(name, role, intro, location, email), the "Current research infrastructure" panel and the
footer.

`portfolio/data.py` is only starter content. It is loaded once, into an empty database, so
editing it later changes nothing on a running site.

## Configuration

All settings come from environment variables. `docker-compose.yml` passes them through and
falls back to development defaults; put real values in a `.env` file (it's git-ignored).

| Variable | Default | Notes |
| --- | --- | --- |
| `DJANGO_DEBUG` | `1` | Set to `0` in production |
| `DJANGO_SECRET_KEY` | `dev-secret-key-change-me` | Must be a long random value in production |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated host names |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | `postgres` | Used by both the app and the database container |
| `DB_HOST`, `DB_PORT` | `db`, `5432` | |
| `DJANGO_SUPERUSER_USER`, `_EMAIL`, `_PASSWORD` | empty | All three needed to create the admin user on start |
| `PORT`, `GUNICORN_WORKERS` | `8000`, `2` | |

> [!WARNING]
> The defaults are for local development only and are not safe to deploy: debug mode is on,
> the secret key is public and any host name is accepted.

## Where things live

- `mario_portfolio/settings.py`: settings (environment-driven)
- `portfolio/models.py`, `portfolio/admin.py`: the content models and their admin pages
- `portfolio/views.py`: the single page view
- `portfolio/templates/portfolio/index.html`: the page template
- `portfolio/static/portfolio/css/style.css`: all styles (dark theme)
- `portfolio/static/portfolio/js/app.js`: Projects/Writing tabs and focus-area filter
- `portfolio/data.py` + `portfolio/management/commands/load_initial_data.py`: starter content
- `scripts/run.sh`: what the container runs on start

## Working with AI agents

Project rules for coding assistants (Claude Code, GitHub Copilot and others) are in
[`AGENTS.md`](AGENTS.md). `CLAUDE.md` only imports it, so there is one file to maintain.
