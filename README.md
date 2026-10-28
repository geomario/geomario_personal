# Mario — portfolio (Django)

A one-page portfolio site. Django renders the page from content stored in PostgreSQL, and
you edit that content in the Django admin. The page's tabs and filter chips use a small
plain-JavaScript file; there is no frontend framework and no build step.

**Stack:** Python 3.13, Django 5, PostgreSQL 16, gunicorn, whitenoise, nginx + Let's
Encrypt (production), Docker Compose.

| File | Use |
| --- | --- |
| `docker-compose.yml` | Local development: code mounted, Django's dev server, debug on |
| `docker-compose.deploy.yml` | Production: gunicorn behind an nginx proxy with HTTPS, settings from `.env` |

## Develop

```bash
docker compose up --build
```

Then open <http://localhost:8000/> (the site) and <http://localhost:8000/admin/> (the admin).

The code is mounted into the container and Django's dev server reloads on changes, so you
only need `--build` again after changing `requirements*.txt` or the `Dockerfile`.

On start, the dev container applies migrations, loads the starter content from
`portfolio/data.py` (only into an empty database) and creates an admin user if the three
`DJANGO_SUPERUSER_*` variables are set. To create one by hand instead:

```bash
docker compose exec app python manage.py createsuperuser
```

Other commands:

```bash
docker compose run --rm app python manage.py test             # tests (separate test database)
docker compose run --rm app flake8                            # lint
docker compose run --rm app python manage.py makemigrations   # written into the repo
```

GitHub Actions runs the tests, flake8 and a check of the deploy config on every push and
pull request to `main` (`.github/workflows/checks.yml`).

## Deploy

Production runs on one server with Docker Compose: **app** (gunicorn), **db** (Postgres),
**proxy** (nginx, ports 80 and 443) and **certbot** (Let's Encrypt certificates, run by
hand). The same layout as `gesis_surf_backend`.

The proxy picks its configuration when it starts: with no certificate for `DOMAIN` yet, it
only answers Let's Encrypt's challenge and redirects to HTTPS; once a certificate exists, it
serves the site over HTTPS (with HSTS) and forwards requests to the app. `www.DOMAIN` is
covered by the same certificate and always redirects to `https://DOMAIN`.

### 1. Server (Hetzner Cloud, with Terraform)

Terraform in [`infra/`](infra/) creates the server, its firewall and your SSH key in
Hetzner Cloud. It runs in Docker, so there's nothing to install:

| Resource | Details |
| --- | --- |
| Server | `cpx02` (1 vCPU, 1 GB RAM, 20 GB), Nuremberg, Ubuntu 24.04, backups on. Terraform refuses to delete it (`prevent_destroy`) |
| Firewall | Inbound 22 (SSH), 80, 443 and ping. Hetzner's firewall, because ports published by Docker bypass `ufw` on the server |
| SSH key | Your `~/.ssh/id_ed25519.pub`. Password logins are turned off |
| First boot | [`infra/cloud-init.yaml`](infra/cloud-init.yaml): Docker Engine + Compose, a 2 GB swap file, and a `deploy` user for GitHub Actions |

SSH is open to all addresses because GitHub Actions will deploy over it; only key logins
work. To limit it to your own IP for now, set `ssh_source_ips` in `infra/variables.tf`.

**API token.** In the Hetzner Console, open the project, go to **Security → API tokens**,
generate a **Read & Write** token and store it in the macOS Keychain (it asks for the
token, so it never lands in your shell history):

```bash
security add-generic-password -a "$USER" -s hcloud-token -w
```

**Create the server.** In each terminal you use for Terraform:

```bash
export HCLOUD_TOKEN=$(security find-generic-password -a "$USER" -s hcloud-token -w)
docker compose run --rm terraform plan     # shows what will be created; read it
docker compose run --rm terraform apply    # creates it after you type "yes"
docker compose run --rm terraform output   # the server's IP and the ssh command
```

Terraform's state (its record of what it created) is `infra/terraform.tfstate`, kept on
your machine and out of git. Don't delete it: without it, Terraform no longer knows the
server exists.

Wait a few minutes for the first-boot setup, then check it finished:

```bash
ssh root@<server-ip> cloud-init status --wait     # should end with "status: done"
ssh root@<server-ip> docker compose version

### 2. DNS (GoDaddy)

The domain's nameservers must be GoDaddy's, or records added at GoDaddy are ignored. Check
with `dig +short NS <domain>`. If they point elsewhere (for example an old DigitalOcean
setup), in GoDaddy go to the domain's **DNS → Nameservers → Change** and pick GoDaddy's
default nameservers. That change can take up to 48 hours to spread.

Then, in **DNS → DNS Records**:

| Type | Name | Value |
| --- | --- | --- |
| A | `@` | the server's IPv4 address (replace GoDaddy's "Parked" value) |
| CNAME | `www` | `@` (GoDaddy usually creates this one already) |

Only these are needed; skip AAAA (IPv6) records for now. Wait until both
`dig +short <domain>` and `dig +short www.<domain>` print the server's IP before the next
step: Let's Encrypt limits repeated failed attempts.

### 3. First deploy

On the server:

```bash
git clone <this repo> && cd mario_portfolio_django_2
cp .env.sample .env        # fill in every value; DOMAIN is the bare domain, e.g. geomario.com
docker compose -f docker-compose.deploy.yml up -d --build
docker compose -f docker-compose.deploy.yml run --rm certbot /opt/certify-init.sh
docker compose -f docker-compose.deploy.yml restart proxy    # switches to HTTPS
```

The first proxy start generates Diffie-Hellman parameters, which can take a minute.

### Update to a new version

```bash
git pull
docker compose -f docker-compose.deploy.yml up -d --build
```

Migrations run automatically when the app container starts.

### Renew the certificate

Let's Encrypt certificates last 90 days. Run this regularly (for example weekly, from
cron); it only renews when a certificate is close to expiring:

```bash
docker compose -f docker-compose.deploy.yml run --rm certbot certbot renew && \
docker compose -f docker-compose.deploy.yml exec proxy nginx -s reload
```

### Check the configuration

```bash
docker compose -f docker-compose.deploy.yml exec app python manage.py check --deploy
```

Two warnings are expected, because nginx handles both: `security.W004` (HSTS) and
`security.W008` (redirect to HTTPS).

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

Settings come from environment variables. In development, `docker-compose.yml` sets them
directly. In production, `docker-compose.deploy.yml` reads `.env` (copy `.env.sample`; it's
git-ignored) and refuses to start if a required value is missing.

| Variable | Set in production | Notes |
| --- | --- | --- |
| `DOMAIN` | `.env` | The site's domain. Also sets `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` |
| `ACME_DEFAULT_EMAIL` | `.env` | Let's Encrypt expiry notices |
| `DJANGO_SECRET_KEY` | `.env` | Random, 50+ characters. The app won't start without it when debug is off |
| `DB_PASSWORD` | `.env` | `DB_NAME` and `DB_USER` default to `portfolio` |
| `DJANGO_SUPERUSER_USER`, `_EMAIL`, `_PASSWORD` | `.env`, optional | Admin user created on start if all three are set |
| `DJANGO_DEBUG` | `0` (compose file) | `1` in development |
| `DJANGO_BEHIND_HTTPS_PROXY` | `1` (compose file) | Trust nginx's `X-Forwarded-Proto` header. Only safe behind a proxy that always sets it |
| `DJANGO_HSTS_SECONDS` | `0` (compose file) | Django's HSTS; off because nginx already sends the header |
| `PORT`, `GUNICORN_WORKERS` | defaults `8000`, `2` | |

With `DJANGO_DEBUG=0`, settings refuse to load unless `DJANGO_SECRET_KEY` and
`DJANGO_ALLOWED_HOSTS` have real values, and session and CSRF cookies are sent over HTTPS
only.

## Where things live

- `mario_portfolio/settings.py`: settings (environment-driven)
- `portfolio/models.py`, `portfolio/admin.py`: the content models and their admin pages
- `portfolio/views.py`: the single page view
- `portfolio/templates/portfolio/index.html`: the page template
- `portfolio/static/portfolio/css/style.css`: all styles (dark theme)
- `portfolio/static/portfolio/js/app.js`: Projects/Writing tabs and focus-area filter
- `portfolio/data.py` + `portfolio/management/commands/load_initial_data.py`: starter content
- `portfolio/management/commands/ensure_superuser.py`: creates the admin user on start
- `portfolio/tests.py`: tests
- `scripts/run.sh`: what the production app container runs on start
- `docker/proxy/`: nginx image and its HTTP / HTTPS config templates
- `docker/certbot/`: certbot image and the first-certificate script
- `infra/`: Terraform for the Hetzner server (run through `docker/terraform.sh`)

## Working with AI agents

Project rules for coding assistants (Claude Code, GitHub Copilot and others) are in
[`AGENTS.md`](AGENTS.md). `CLAUDE.md` only imports it, so there is one file to maintain.
