# CSFeer

A Django application for managing forms and workflows.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker-Based Development](#docker-based-development)
- [Local Development (Outside Docker)](#local-development-outside-docker)
- [Development Workflow](#development-workflow)
- [Database Management](#database-management)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Reference](#reference)

## Prerequisites

- Docker and Docker Compose
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- Python 3.11+

### macOS Setup

If you are on macOS, you need to install system dependencies for WeasyPrint:

```bash
brew install pango
```

## Quick Start

Choose your development approach based on your needs:

- **[Docker-Based Development](#docker-based-development)**: Quick setup, production-like environment
- **[Local Development](#local-development-outside-docker)**: Faster iteration, better debugging (Recommended)

### Initial Setup (Required for Both Approaches)

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

3. **Install pre-commit hooks** (recommended)

   ```bash
   uv run pre-commit install
   ```

## Docker-Based Development

Best for quick setup and production-like environment. All services run in containers.

### Starting Services

```bash
# Build and start all services (app, database, mock OAuth)
make start

# View logs
docker compose logs -f app

# Stop services
make stop
```

### Frontend Changes in Docker

When running in Docker, volume mounts handle file synchronization automatically:

```bash
# 1. Edit SCSS files in frontend/src/scss/
# 2. Build frontend assets
npm run build

# 3. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
# Changes appear immediately!
```

## Local Development (Outside Docker)

**Recommended** for faster iteration and debugging. Run Django locally while using Docker only for database and OAuth services.

### Initial Setup (One-Time)

1. **Create static symlink**

   This symlink allows Django to serve frontend assets without running `collectstatic`:

   ```bash
   # Remove existing directory if present and create symlink
   rm -rf csfeer/static/frontend
   ln -s ../../frontend/built csfeer/static/frontend
   ```

   **How it works:**
   - `frontend/built/` contains webpack output
   - `csfeer/static/frontend` symlinks to `frontend/built/`
   - Django's runserver automatically serves from the symlinked directory
   - No need to run `collectstatic` during development!

2. **Start supporting services**

   ```bash
   # Start only database and mock OAuth services
   make start-local
   ```

3. **Run migrations**

   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser** (optional)

   ```bash
   uv run python manage.py createsuperuser
   ```

### Daily Development Workflow

1. **Start supporting services** (if not already running)

   ```bash
   make start-local
   ```

2. **Start the Django development server**

   ```bash
   # Option 1: Command line
   uv run python manage.py runserver 0.0.0.0:8000

   # Option 2: VSCode debugger (Recommended)
   # Press F5 or use "Python Debugger: Django" launch configuration
   ```

3. **Making frontend changes**

   ```bash
   # 1. Edit SCSS files in frontend/src/scss/
   # 2. Build frontend assets
   npm run build

   # 3. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
   # Changes appear immediately - no collectstatic needed!
   ```

### Production Deployment

For production, `collectstatic` copies the files (following symlinks):

```bash
npm run build
uv run python manage.py collectstatic --noinput
```

## Development Workflow

### Running Django Commands

**For Local Development:**

Use `uv` to run Django commands (installs dependencies from `pyproject.toml` automatically):

```bash
# Run system checks
uv run python manage.py check

# Create/apply migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create a superuser
uv run python manage.py createsuperuser

# Collect static files (production only - not needed in local dev)
uv run python manage.py collectstatic --noinput
```

**For Docker Development:**

Execute commands inside the running container:

```bash
# Run any Django command
docker compose exec app python manage.py <command>

# Examples:
docker compose exec app python manage.py migrate
docker compose exec app python manage.py createsuperuser
```

**Note:** Database commands require PostgreSQL to be running (via `make start` or `make start-local`).

### Viewing Logs

**Docker logs:**

```bash
# Application logs
docker compose logs -f app

# Database logs
docker compose logs -f db

# All services
docker compose logs -f
```

**Local development logs:**

Check the terminal where you ran `uv run python manage.py runserver` or the VSCode debug console.

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
- [USWDS Guidelines](docs/USWDS_GUIDELINES.md) - Component and styling best practices
