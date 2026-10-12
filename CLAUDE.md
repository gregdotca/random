# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

"Randomizer" (demo: https://random.greg.ca) is a single-page Flask app. The user picks a number of options and a number of rolls; the app rolls that many times and reports which option won. It has no database and no tests.

## Commands

Production (the tracked config): gunicorn on container port 5000, published on host port 8088. The gunicorn command has `--no-control-socket` because the app doesn't use gunicorn's `gunicornc` control tool, and the `app` user can't create its default socket in `/home/app/.gunicorn`.

```bash
docker-compose up -d --build
```

Lint. The Docker builder stage runs this, so a lint failure fails the build. To run it on the host, install the same flake8 version first:

```bash
pip install flake8==7.4.1
cd services/web && flake8 --ignore=E501,W503,F401 .
```

### Dev vs. prod environment swap

Dev config lives in local-only files that aren't in the repository (they're listed in this checkout's `.git/info/exclude`, so a fresh clone won't have them): `docker-compose.DEV.yml`, `services/web/Dockerfile.DEV`, `to-dev.sh`, and `to-prod.sh`. Where they exist, the scripts swap files by renaming them:

- `./to-dev.sh` renames `docker-compose.yml` → `docker-compose.PROD.yml` and `docker-compose.DEV.yml` → `docker-compose.yml` (same for the Dockerfiles). Dev runs `python manage.py run` (Flask dev server) on port 5000 with `services/web/` bind-mounted to `/app` for live reload. Alongside it, `tailwindcss --watch=always` rebuilds `project/assets/app.css` into the mounted directory (`--watch=always` because the container's stdin is closed), so on the host that file is owned by root.
- `./to-prod.sh` reverses it.

Always run `./to-prod.sh` before committing. Otherwise the dev `docker-compose.yml` and `Dockerfile` show up as changes to the tracked files.

## Architecture

All code is in `services/web/`:

- `project/__init__.py`: the whole app. `GET /` renders the form with defaults; `POST /` parses the form (falling back to defaults on bad input), caps values at `MAX_OPTIONS`/`MAX_ROLLS`, and calls `gjcode.rand.rand(options, rolls, details)`.
- The randomizing logic is **not in this repo**. It's in the external `gjcode` package (pinned in `requirements.txt`). The app turns its plain-text output into HTML (newlines → `<BR>`, `WINNER!` wrapped in `<span class='winner'>`, styled by a plain CSS rule at the end of `project/styles/app.css` with a separate red for each mode) and passes it to the template as `page_body`, which renders with `|safe`.
- `manage.py`: Flask CLI entry point; gunicorn loads `manage:app`.
- `project/templates/home.html`: the only template. Static files are served from `project/assets/` at `/assets/...` (Flask's `static_folder`; use `url_for('static', ...)`). jQuery and the favicon are vendored there.
- **CSS build:** Tailwind 4 and daisyUI 5 are built at Docker build time, not loaded from a CDN. The Tailwind standalone CLI (version and per-architecture SHA-256s pinned as `ARG`s in the Dockerfile builder stage) compiles `project/styles/app.css` into `project/assets/app.css` (gitignored), and the final stage copies the built file in. `source(none)` plus `@source "../templates"` means it scans only `project/templates/`, so a class used only from Python or JS (such as in the `page_body` HTML) won't be in the build unless it also appears in a template. daisyUI is the vendored plugin `project/styles/daisyui-<version>.mjs`. To upgrade either one, update the Dockerfile `ARG`s (and `Dockerfile.DEV`), or replace the `.mjs` file and its reference in `app.css`.
- **Dark mode:** automatic only, with no toggle, JavaScript, or `data-theme` attribute. `bumblebee --default, business --prefersdark` in `project/styles/app.css` puts `business` inside `@media (prefers-color-scheme: dark)` on `:root:not([data-theme])`, so adding `data-theme` to `<html>` would lock the page to one theme. A `color-scheme` meta tag in `home.html` tells the browser about both modes before the CSS loads. Use daisyUI theme colours (`base-content`, `base-200`, and so on), not hard-coded colour classes (`text-gray-*`, `bg-white`), so both modes keep working. Tailwind's `dark:` variant uses the same media query, so per-mode tweaks go there (the Randomize button is `btn-accent dark:btn-primary`). Dark-mode overrides of theme variables live in an unlayered rule at the end of `project/styles/app.css`: a darker `--color-primary` for the button, and `bumblebee`'s `--radius-*` corner sizes so both modes match. Being unlayered, it beats daisyUI's layered theme.
- `project/templates/custom.headers`: optional, gitignored, deployment-specific HTML (e.g. analytics) included in `<head>` via `{% include ... ignore missing %}`.
