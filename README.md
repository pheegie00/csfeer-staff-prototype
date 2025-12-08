# CSFeer

A Django application for managing forms and workflows.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Workflow](#development-workflow)
- [Database Management](#database-management)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Reference](#reference)

## Prerequisites

- Docker and Docker Compose
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Python 3.11+

## Quick Start

1. **Configure hosts file**

   For OpenID redirection to work correctly, add these entries to your `/etc/hosts` file:

   ```
   127.0.0.1       oauth.csfeer
   127.0.0.1       ui.csfeer
   ```

2. **Environment configuration**

   Copy the example environment file and configure as needed:

   ```bash
   cp example.env .env
   ```

3. **Choose your development approach**

### Option A: Run Everything in Docker

Best for quick setup and production-like environment:

```bash
# Build and start all services (app, database, mock OAuth)
make start

# View logs
docker compose logs -f app

# Stop services
make stop
```

### Option B: Local Development (Recommended)

Run the app locally for faster iteration and debugging:

```bash
# Start only database and mock OAuth services
make start-local

# Run migrations
uv run python manage.py migrate

# Create a superuser (optional)
uv run python manage.py createsuperuser

# Start the development server
uv run python manage.py runserver 0.0.0.0:8000

# Or use VSCode's debugger:
# Press F5 or use "Python Debugger: Django" launch configuration
```

4. **Install pre-commit hooks** (recommended)

```bash
uv run pre-commit install
```

## Development Workflow

### Running Django Commands

Use `uv` to run Django commands (installs dependencies from `pyproject.toml` automatically):

```bash
# Run system checks
uv run python manage.py check

# Create/apply migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Collect static files
uv run python manage.py collectstatic --noinput

# Create a superuser
uv run python manage.py createsuperuser
```

**Note:** Database commands require PostgreSQL to be running (via `make start` or `make start-local`).

### Viewing Logs

```bash
# Docker logs
docker compose logs -f app
docker compose logs -f db

# Or view all services
docker compose logs -f
```

### Stopping Services

```bash
# Stop all services
make stop

# Or using docker compose directly
docker compose down
```

## Database Management

### Running Migrations

```bash
# Apply pending migrations
uv run python manage.py migrate

# Create new migrations after model changes
uv run python manage.py makemigrations form_manager
```

### Generating ERD Diagrams

Generate entity relationship diagrams for your database schema:

```bash
# First-time setup: Install graphviz system dependency
brew install graphviz

# Then sync Python dependencies (includes django-extensions and pydotplus)
uv sync

# Generate ERD diagrams
make create-erds
```

Diagrams are saved to `docs/app/erds/` by default.

### Resetting the Database

```bash
# Remove database volume and restart
make reset-db
make start-local
uv run python manage.py migrate
```

### Resetting Everything

```bash
# Remove all Docker volumes and restart fresh
make reset-all
make start
```

## Code Quality

### Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to automatically run code quality checks before each commit. The hooks include:

- **Black**: Python code formatter
- **isort**: Import statement organizer
- **Pyright**: Static type checker
- **ER Diagram Generator**: Auto-generates database diagrams when models change

**Installation:**

```bash
# Install pre-commit hooks (one-time setup)
uv run pre-commit install

# Now hooks will run automatically on git commit
```

**Manual execution:**

```bash
# Run all hooks on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run black --all-files
uv run pre-commit run isort --all-files
uv run pre-commit run pyright --all-files

# Update hook versions
uv run pre-commit autoupdate
```

**Skipping hooks** (not recommended):

```bash
git commit --no-verify
```

## Component Library

See [csfeer/templates/patterns/README.md](csfeer/templates/patterns/README.md) for component library documentation.

## Testing

See [docs/E2E_TESTING.md](docs/E2E_TESTING.md) for detailed testing documentation.

```bash
# Run unit tests
make test-unit

# Run E2E tests (headless)
make test-e2e

# Run with visible browser
make test-e2e-headed

# Run with debugging
make test-e2e-debug
```

## Reference

### Available Make Targets

#### Development
- `make start` - Start all services in Docker (app, db, mock-oauth)
- `make start-local` - Start only db and mock-oauth (for local app development)
- `make stop` - Stop all services
- `make restart` - Restart all services

#### Database
- `make reset-all` - Remove all volumes and restart fresh
- `make reset-db` - Remove only the database volume
- `make create-erds` - Generate entity relationship diagrams

#### Testing
- `make test-e2e` - Run E2E tests (headless)
- `make test-e2e-headed` - Run E2E tests with visible browser
- `make test-e2e-debug` - Run E2E tests with slow motion debugging
- `make test-e2e-auth` - Run only authentication E2E tests

#### Other
- `make oauth-setup` - Run OAuth setup script

### Additional Documentation

- [E2E Testing Guide](docs/E2E_TESTING.md) - Comprehensive testing documentation
- [ER Diagrams](docs/app/erds/) - Database schema diagrams
