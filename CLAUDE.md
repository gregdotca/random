# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

"Randomizer" (demo: https://random.greg.ca) is a single-page Flask app. The user picks a number of options and a number of rolls; the app rolls that many times and reports which option won. It has no database and no tests.

## Commands

Production (the tracked config): gunicorn on container port 5000, published on host port 8088.

```bash
docker-compose up -d --build
```

Lint. The Docker builder stage runs this, so a lint failure fails the build. To run it on the host, install the same flake8 version first:

```bash
pip install flake8==3.9.1
cd services/web && flake8 --ignore=E501,W503,F401 .
```

### Dev vs. prod environment swap

Dev config lives in local-only files that aren't in the repository (they're listed in this checkout's `.git/info/exclude`, so a fresh clone won't have them): `docker-compose.DEV.yml`, `services/web/Dockerfile.DEV`, `to-dev.sh`, and `to-prod.sh`. Where they exist, the scripts swap files by renaming them:

- `./to-dev.sh` renames `docker-compose.yml` → `docker-compose.PROD.yml` and `docker-compose.DEV.yml` → `docker-compose.yml` (same for the Dockerfiles). Dev runs `python manage.py run` (Flask dev server) on port 5000 with `services/web/` bind-mounted to `/app` for live reload.
- `./to-prod.sh` reverses it.

Always run `./to-prod.sh` before committing. Otherwise the dev `docker-compose.yml` and `Dockerfile` show up as changes to the tracked files.

## Architecture

All code is in `services/web/`:

- `project/__init__.py`: the whole app. `GET /` renders the form with defaults; `POST /` parses the form (falling back to defaults on bad input), caps values at `MAX_OPTIONS`/`MAX_ROLLS`, and calls `gjcode.rand.rand(options, rolls, details)`.
- The randomizing logic is **not in this repo**. It's in the external `gjcode` package (pinned in `requirements.txt`). The app turns its plain-text output into HTML (newlines → `<BR>`, `WINNER!` wrapped in a red span) and passes it to the template as `page_body`, which renders with `|safe`.
- `manage.py`: Flask CLI entry point; gunicorn loads `manage:app`.
- `project/templates/home.html`: the only template. Styling comes from Tailwind v4 browser build and daisyUI 5 via jsDelivr CDN (theme `bumblebee`). jQuery is served locally from `project/assets/`, which is the Flask `static_folder`.
- `project/templates/custom.headers`: optional, gitignored, deployment-specific HTML (e.g. analytics) included in `<head>` via `{% include ... ignore missing %}`.

`requirements.txt` lists Flask-SQLAlchemy and psycopg2-binary, but the app doesn't use them.
