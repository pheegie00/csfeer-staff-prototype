# Claude Code Guidelines

See [AGENTS.md](AGENTS.md) for the full project rules. This file adds Claude Code-specific guidance.

## Code Style

- **Max line length: 100 characters.** Ruff enforces E501 at 100 chars via pre-commit. Wrap
  docstrings, comments, and code before column 100. Put the closing `"""` on its own line when
  needed to avoid pushing a sentence over the limit.
- **No inline (function-body) imports.** All imports must be at the top of the file. Do not place
  `import` or `from X import Y` statements inside functions or methods.

## Configuration / Env Vars

Adding a new environment variable is a three-step process:

1. **Declare it on `AppConfig`** (or a nested config) in [csfeer/config.py](csfeer/config.py)
   with a typed default, e.g. `lock_duration_minutes: int = 15`. Pydantic-settings reads
   `.env` and process env vars; nested fields use the `__` delimiter
   (`DB_CONFIG__PGHOST=...`).
2. **Expose it as a Django setting** in [csfeer/settings.py](csfeer/settings.py) with the
   uppercase Django name, e.g. `LOCK_DURATION_MINUTES = settings.lock_duration_minutes`.
3. **Consume it via `django.conf.settings`** in app code, e.g.
   `from django.conf import settings; settings.LOCK_DURATION_MINUTES`.

Do **not** call `get_app_config()` from app code — it instantiates `AppConfig` and
re-parses `.env` on every call. Routing through `django.conf.settings` is lazy, idiomatic,
and lets tests use `@override_settings(...)` instead of monkeypatching the config.

## Running Tests (macOS native)

Docker is the default runner (`make test-unit`), but when running tests natively on macOS:

```bash
set -a && source .env && set +a
DYLD_LIBRARY_PATH=/opt/homebrew/lib uv run pytest tests/unit -v
```

`DYLD_LIBRARY_PATH` is required for WeasyPrint to find system libraries. Docker must be running
(`docker compose up -d`) for the PostgreSQL database.

## Git & PR Conventions

- **Never commit directly to `main`.**
- Branch naming: `talebbits/<ticket>-<description>` (e.g. `talebbits/FE-493-fix-lock-ttl`)
- **User commits manually** — do not create commits unless explicitly asked.
- Do NOT add "🤖 Generated with Claude Code" to commits or PR bodies.
- PR bodies must include a Jira link at the bottom: `Jira: https://jira.acf.gov/browse/FE-XXX`
- Do NOT include a "Test plan" section in PRs.
- Commit message format: `<type>(<scope>): [FE-<issue>] <description>`
  - Types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `perf`
- **Commit message length** (enforced by [.gitlint](.gitlint)):
  - Title: max **72 chars** (`title-max-length`)
  - Body: max **72 chars per line** (`body-max-line-length`) — wrap manually
  - Title regex: `^(feat|fix|chore|docs|style|refactor|test|perf|ci|build)(\(scope\))?: (\[FE-\d+\] )?<lowercase description, no trailing period>`
