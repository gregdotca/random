# Changelog

## 2026-10-11

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
