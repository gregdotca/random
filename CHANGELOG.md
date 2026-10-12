# Changelog

## 2026-10-11

- Add `CLAUDE.md` with run and lint commands, the dev/prod file swap, and an overview of the app, so Claude Code can work in the repo without rediscovering them.
- Update the copyright notices in `LICENSE` and `README.md` to `Copyright (c) 2024-2026 Greg Chetcuti <greg@chetcuti.com>`. The project started in January 2024, and the notices only said 2025 and had no contact address.
- Fix the install URL in `README.md` from `https://` to `http://`. Gunicorn serves plain HTTP on port 8088, so the `https://` URL failed to connect.
- Add this changelog.
