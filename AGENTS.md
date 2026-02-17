# Project Golden Rules

## About This File

This file contains rules that are injected into every AI coding session. Keep it focused on your "golden rules" - what should ALWAYS be done and what should NEVER be done.

> ⚠️ **Remember**: The longer this file, the less likely AI will follow everything. Be selective and prioritize.

---

## 🚫 NEVER Do (Hard Rules)

### Security

- Never put API keys, secrets, or credentials in code or version control
- Never use wildcard imports in production code
- Never disable security features without explicit approval
- Never commit sensitive data even in comments

### Code Quality

- Never use global variables
- Never leave debug/print statements in committed code
- Never catch exceptions and ignore them silently
- Never commit code with TODO comments that reference security issues

### Process

- Never commit directly to main/master branch
- Never force push to shared branches
- Never delete tests to make the build pass
- Never skip running the test suite

---

## ✅ ALWAYS Do (Mandatory Practices)

### Before Coding

- Always read existing code in the area you're modifying
- Always check for existing utilities before writing new ones
- Always understand the existing patterns in the codebase

### During Coding

- Always use the project's established patterns and conventions
- Always handle errors explicitly (no silent failures)
- Always use meaningful variable and function names
- Always write self-documenting code (comments for "why", not "what")

### After Coding

- Always run the full test suite before claiming success
- Always verify your changes work as expected
- Always clean up temporary files and debug code
- Always update documentation if behavior changes

---

## 📋 Project-Specific Conventions

### Language/Framework Rules
<!-- Python 3.12+, Django 6, Pydantic -->
- Avoid using `# type: ignore` if you must, leave comment as to why
- Prefer `Type | None` over `Optional[Type]`
- Prefer Django ORM querysets over raw SQL
- Use `model_dump()` over `.dict()` for Pydantic models
- Prefer strict validation in Pydantic models
- Use specific exception types, not bare `Exception`
- Log errors before re-raising
- Follow existing `form_manager/schema/` patterns for new form types
- Use django-cotton components for USWDS markup, don't write raw USWDS HTML

### File Organization
<!-- Django project structure -->
- Django project config goes in `csfeer/` (settings, urls, auth backend)
- Django ORM models go in `form_manager/models/`
- View functions and CBVs go in `form_manager/views/`
- Pydantic form schemas, field definitions, and layout go in `form_manager/schema/`
- Django Ninja API endpoints go in `form_manager/api/`
- Form and widget templates go in `form_manager/templates/`
- USWDS component templates go in `django_cotton_uswds/templates/cotton/`
- SCSS and JS source go in `frontend/src/` (webpack builds to `frontend/built/`)
- Tests mirror source structure in `tests/` (e.g., `tests/unit/form_manager/`)
- Infrastructure and deployment go in `devops/` (Terraform, Helm, Docker)

### Naming Conventions

- Modules: `snake_case.py` (e.g., `form_edit.py`, `form_review.py`)
- Classes: `PascalCase` (e.g., `FormEntry`, `BaseFormSchema`)
- Functions/variables: `snake_case` (e.g., `get_next_step_and_page`, `save_form_entry`)
- Constants: `SCREAMING_SNAKE_CASE` (e.g., `ALL_FORM_NAME_CHOICES`)
- Test files: `test_*.py` (e.g., `test_form_error_states.py`)
- Commit messages: `FE-{ISSUE} - Description (#PR)` (e.g., `FE-521 - Fix review page back button (#168)`)

### Testing Requirements

- Use pytest with **function-based** test organization (not class-based)
- Use fixtures from `tests/conftest.py` and `tests/unit/form_manager/conftest.py`
- Use `freezegun` for time-dependent tests
- E2E tests use Playwright with Page Object Model (`tests/e2e/pages/`)
- Mark tests: `@pytest.mark.e2e`, `@pytest.mark.unit`, `@pytest.mark.auth`
- Use `authenticated_page` / `admin_page` fixtures for E2E auth
- Prefer deterministic waits (`expect().to_be_visible()`) over `wait_for_timeout()`

---

## 🔧 Environment & Tools

### Python Environment

This project uses `uv` for dependency management. **No manual venv activation needed** - use `uv run` or Makefile targets.

```bash
# uv handles the venv automatically
uv run python manage.py runserver 0.0.0.0:8000
uv run pytest
```

### Build Commands

```bash
# Dependencies
uv sync                    # Install dependencies
uv add <package>           # Add a dependency
uv add --dev <package>     # Add a dev dependency

# Development (local app + Docker infrastructure)
make start-local           # Start db + mock-oauth only (run app locally)
make start                 # Start ALL services in Docker (db, oauth, app)
make stop                  # Stop services
make migrate               # Run Django migrations (locally)
npm run build              # Build frontend assets (SCSS + JS)

# Running commands in Docker app container
docker exec -it csfeer-app-1 bash -c "<command>"  # Run in container
make test-unit-with-docker # Run unit tests inside container

# Testing
make test-unit             # Run unit tests (locally)
make test-e2e              # Run E2E tests (headless, starts app container)
make test-e2e-headed       # E2E with visible browser

# Quality
uv run pre-commit run --all-files  # Run all hooks
pyright                    # Type checking
ruff check .               # Linting
ruff format .              # Formatting

# Utilities
make create-erds           # Generate ER diagrams
```

### Key Files to Know

```
# Configuration
- pyproject.toml          - Dependencies, tool config (black, ruff, pyright, pytest)
- example.env             - Required environment variables
- csfeer/settings.py      - Django settings
- csfeer/config.py        - Pydantic settings (env var loading)
- compose.yml             - Local development services (db, mock-oauth)
- Makefile                - Common dev commands

# Entry Points
- manage.py               - Django management entry point
- csfeer/urls.py          - Root URL routing
- csfeer/backends.py      - OIDC authentication backend

# Core Domain
- form_manager/schema/    - Form definitions, field types, layout components
- form_manager/views/     - Form lifecycle (edit, review, finalize)
- form_manager/models/    - Django ORM models (FormEntry, FormDefinition, etc.)
- form_manager/api/       - Django Ninja REST API

# Testing
- tests/conftest.py       - Shared test fixtures and Playwright config
- tests/e2e/pages/        - Page Object Model for E2E tests
```

---

## ⚡ Quick Reference

### When You Get Stuck

1. Re-read this file
2. Check existing implementations for patterns
3. Ask for clarification rather than guessing
4. If unsure, implement the simplest solution first

### When Making Changes

1. Small, focused changes
2. One logical change per commit
3. Test before and after
4. Verify nothing else broke

### When Tests Fail

1. Don't disable or delete the test
2. Understand why it's failing
3. Fix the code, not the test (unless test is wrong)
4. Run full suite after fix

---

## Workflows & Tool Preferences

### Available Commands

| Command | Purpose |
|---|---|
| `/create_plan` | Create implementation plan (researches codebase first) |
| `/implement_plan` | Execute a plan phase-by-phase with verification |
| `/iterate_plan` | Update existing plan based on feedback |
| `/validate_plan` | Verify implementation matches plan |
| `/create_adr` | Document architectural decision |
| `/create_handoff` | Save session state for next session |
| `/resume_handoff` | Continue from a previous handoff |
| `/describe_pr` | Generate PR description (embeds plan) |
| `/commit` | Create git commits with approval |
| `/research_codebase` | Document codebase to `thoughts/shared/research/` |
| `/create_worktree` | Create parallel worktree for isolation |
| `/beads_workflow` | Beads task tracking quick reference |
| `/cleanup` | Clean up working documents after PR merge |
| `/local_review` | Set up worktree for reviewing a colleague's branch |

### Branch Workflow

**Main branch is protected.** All work on feature branches.

```bash
# 1. Create feature branch
git checkout -b feature/<task-id>-short-description
# Examples:
git checkout -b feature/FE-123-add-date-picker
git checkout -b fix/FE-456-review-page-bug

# 2. Always verify you're on the correct branch before committing
git branch --show-current  # Should NOT be 'main'
```

Branch naming: `feature/<task-id>-description` for features, `fix/<task-id>-description` for bugs.

### PR Workflow

1. Create feature branch (or use `/create_worktree`)
2. Make changes and commit using `/commit`
3. Run tests: `make test-unit`
4. Run `/describe_pr` to generate description (embeds plan in PR)
5. Push and create PR:
   ```bash
   git push -u origin feature/<branch-name>
   gh pr create --base main --body-file thoughts/shared/prs/<task-id>_description.md
   ```
6. PRs require review before merge to main
7. After merge: Run `/cleanup <task-id>` to delete plan files

### Task Tracking with Beads

This project uses `bd` (beads) for task tracking. At session start:

1. Check for ready work: `bd ready`
2. Pick a task or create one: `bd create "Task title" -t task -p 2`
3. Update status when starting: `bd update <id> --status in_progress`
4. Close when done: `bd close <id> --reason "Completed in PR #X"`
5. Sync changes: `bd sync`

### Parallel Development

For complex features, use git worktrees via `/create_worktree`:
- Each worktree is isolated with its own venv
- Worktrees share the beads database
- Use `BEADS_NO_DAEMON=1` in worktrees

### Agent & Skill Preferences

**Prefer project-specific tools over generic ones:**

| Task | Prefer | Avoid |
|---|---|---|
| Find files/components | `codebase-locator` agent | Generic `Explore` agent |
| Deep implementation analysis | `codebase-analyzer` agent | Generic `Explore` agent |
| Find examples to model after | `codebase-pattern-finder` agent | Generic `Explore` agent |
| Find existing research/notes | `thoughts-locator` agent | Duplicating work |
| Document findings | `/research_codebase` skill | Ad-hoc notes |
| Create plans | `/create_plan` (saves to `thoughts/shared/plans/`) | `EnterPlanMode` (ephemeral) |
| Git commits | `/commit` skill | Raw git commands |
| PR descriptions | `/describe_pr` skill | Manual PR body |
| Implementation | `/implement_plan` (when plan exists) | Ad-hoc coding |

### Document Retention Policy

| Document Type       | Location                    | Retention                               |
| ------------------- | --------------------------- | --------------------------------------- |
| **ADRs**            | `thoughts/shared/adrs/`     | **Forever** - architectural decisions   |
| **Plans**           | `thoughts/shared/plans/`    | Delete after PR merges (embedded in PR) |
| **Handoffs**        | `thoughts/shared/handoffs/` | Delete after task closes                |
| **PR Descriptions** | `thoughts/shared/prs/`      | Never commit (local working files)      |
| **Research**        | `thoughts/shared/research/` | Keep if reusable, delete if one-off     |

### Session Completion (Landing the Plane)

Work is NOT complete until `git push` succeeds. Never stop before pushing.

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Push to remote** - This is MANDATORY:

   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```

4. **Clean up** - Clear stashes, prune remote branches
5. **Verify** - All changes committed AND pushed
6. **Hand off** - Use `/create_handoff` if work remains

**CRITICAL:**
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

*Last updated: 2/17/2026*
*Version: 2.0*
