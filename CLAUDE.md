# Claude Code Guidelines

See [AGENTS.md](AGENTS.md) for the full project rules. This file adds Claude Code-specific guidance.

## Code Style

- **Max line length: 100 characters.** Ruff enforces E501 at 100 chars via pre-commit. Wrap
  docstrings, comments, and code before column 100. Put the closing `"""` on its own line when
  needed to avoid pushing a sentence over the limit.
- **No inline (function-body) imports.** All imports must be at the top of the file. Do not place
  `import` or `from X import Y` statements inside functions or methods.

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
