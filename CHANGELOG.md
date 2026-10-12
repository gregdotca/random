# Changelog

## 2026-10-11

- Raise the contrast of the red `WINNER!` label in the full results. It was styled inline as plain `red`, which is about 4.0:1 on the light background and 4.1:1 on the dark one, under the 4.5:1 that WCAG asks for normal-size text. daisyUI's own error colours are worse (2.9:1 and 2.7:1), so the label now has its own red for each mode: `oklch(50% .2 27)` in light mode (6.7:1) and `oklch(72% .17 22)` in dark mode (6.1:1). The Python code outputs a `winner` class instead of an inline style, and the colours are in a plain CSS rule, which Tailwind always keeps (unlike utility classes, which are only built if a template uses them).
  - `services/web/project/__init__.py:55`: output `<span class='winner'>` instead of the inline style.
  - `services/web/project/styles/app.css`: add the `.winner` rule and its dark-mode colour.
  - `CLAUDE.md`: describe the `winner` class.
- Update Python from 3.9 to 3.14, Flask from 2.3.0 to 3.1.3, Werkzeug from 2.3.0 to 3.1.9, gunicorn from 20.1.0 to 26.2.0, and flake8 from 3.9.1 to 7.4.1, and remove Flask-SQLAlchemy and psycopg2-binary. Python 3.9 reached end of life in October 2025, so it no longer gets security fixes. gunicorn 20.1.0 has a request-smuggling vulnerability (CVE-2024-1135, fixed in 22.0.0). Flask-SQLAlchemy and psycopg2-binary were never imported, and psycopg2-binary 2.8.6 has no wheels for Python 3.14, so it would have broken the build. gunicorn 26 also adds a control socket for its `gunicornc` tool, which this app doesn't use; gunicorn would try to create it in `/home/app/.gunicorn`, which the `app` user can't write to, so it's turned off with `--no-control-socket`.
  - `services/web/requirements.txt`: new Flask, Werkzeug, and gunicorn versions; remove the unused packages.
  - `services/web/Dockerfile:6,35,52`: `python:3.14.7-slim` for both stages, and flake8 7.4.1.
  - `docker-compose.yml:10`: add `--no-control-socket` to the gunicorn command.
  - `CLAUDE.md`: note the control socket setting and the new flake8 version, and drop the note about the unused packages.
- Add `<!doctype html>`, `lang="en"`, and a viewport meta tag to the page, and remove three classes that did nothing. Without a doctype the browser rendered the page in quirks mode, which Tailwind's base styles don't expect; without `lang` screen readers had to guess the language; and without a viewport tag phones showed a zoomed-out desktop layout. `form` and `loading-circle` aren't daisyUI classes and `justify-left` isn't a Tailwind class (it's `justify-start`), so none of them was in the built CSS. File changed: `services/web/project/templates/home.html:1-5,15-16,33`.
- Add an `ACR.md` file with the project's [AI Code Rating](https://aicoderating.com/spec/0.1/), B1b (Maintainer: Experienced · AI Share: 1–25% · Oversight: Reviewed), so readers can see how much of the code AI wrote and how carefully it was checked, and add its badge to `README.md`.
- Add automatic dark mode that follows the visitor's system colour scheme, with no toggle or JavaScript. The page only had daisyUI's light `bumblebee` theme, set with `data-theme="bumblebee"` on `<html>`, so it stayed light for visitors who prefer dark. daisyUI's `business` theme is now built in as `--prefersdark`, which puts its colours inside `@media (prefers-color-scheme: dark)`; the page background, text, form, and button all switch with it. The `data-theme` attribute is removed, because daisyUI only applies the dark theme to a root without one. A `color-scheme` meta tag tells the browser about both modes before the CSS loads, which avoids a white flash. In dark mode the Randomize button uses a navy blue instead of `business`'s orange accent (`business`'s primary darkened from `oklch(41.703% .099 251.473)` to `oklch(34% .085 251.473)`, which raises the button text's contrast from 6.0:1 to 8.3:1), and the form and its fields keep `bumblebee`'s rounder corners instead of `business`'s near-square ones. Light mode keeps its black accent button and looks the same as before.
  - `services/web/project/styles/app.css`: add `business --prefersdark` to the daisyUI themes, and set a darker `--color-primary` and `bumblebee`'s `--radius-*` values for dark mode.
  - `services/web/project/templates/home.html`: remove `data-theme="bumblebee"`, add the `color-scheme` meta tag, and add `dark:btn-primary` to the Randomize button.
  - `CLAUDE.md`: add a dark mode note.
- Build Tailwind 4.3.3 and daisyUI 5.7.46 CSS at Docker build time instead of loading them from jsDelivr. The page used the in-browser Tailwind compiler, a floating `daisyui@5` tag, and a separate themes file pinned to `5.0.0`, so every visitor downloaded and ran a third-party compiler, and upstream releases could change the styling without any change here. The build now produces a single minified `app.css` (about 30 KB) with only the classes the template uses and the `bumblebee` theme.
  - `services/web/Dockerfile`: the builder stage downloads the Tailwind standalone CLI (checksum-verified, amd64 and arm64) and builds the CSS; the final stage copies in `app.css`.
  - `services/web/project/styles/app.css`: new Tailwind input file.
  - `services/web/project/styles/daisyui-5.7.46.mjs`: vendored daisyUI plugin.
  - `services/web/project/templates/home.html`: load `app.css` locally instead of the three CDN files.
  - `.gitignore`: ignore the generated `project/assets/app.css`.
  - `CLAUDE.md`: describe the CSS build.
- Add `CLAUDE.md` with run and lint commands, the dev/prod file swap, and an overview of the app, so Claude Code can work in the repo without rediscovering them.
- Update the copyright notices in `LICENSE` and `README.md` to `Copyright (c) 2024-2026 Greg Chetcuti <greg@chetcuti.com>`. The project started in January 2024, and the notices only said 2025 and had no contact address.
- Fix the install URL in `README.md` from `https://` to `http://`. Gunicorn serves plain HTTP on port 8088, so the `https://` URL failed to connect.
- Add this changelog.
