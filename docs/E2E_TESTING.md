# E2E Testing Guide

## Overview

This project uses [Playwright](https://playwright.dev/) for end-to-end testing. Playwright provides reliable testing by using auto-waiting, retries, and cross-browser support.

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium

# For macOS Sequoia users: Install WebKit for headed mode
uv run playwright install webkit
```

### 2. Start Services

```bash
# Start all Docker services (including app)
make start

# Or start only db and mock-oauth (for local app development)
make start-local
# Then run the app locally:
uv run python manage.py runserver 0.0.0.0:8000
# Or use VSCode's "Python Debugger: Django" launch configuration
```

### 3. Run Tests

```bash
# Run all e2e tests (headless)
make test-e2e

# Run tests with visible browser
make test-e2e-headed

# Run tests with slow motion for debugging
make test-e2e-debug

# Run tests with WebKit (for macOS Sequoia)
make test-e2e-webkit

# Run only authentication tests
make test-e2e-auth
```

## Project Structure

```
tests/
├── conftest.py                 # Pytest fixtures and configuration
├── README.md                   # Detailed testing documentation
├── e2e/                        # Test cases
│   ├── test_auth_flow.py       # Login/logout tests
│   ├── test_navigation.py      # General navigation
│   └── test_form_manager.py    # Form functionality
├── pages/                      # Page Object Model
│   ├── base_page.py            # Base page class
│   ├── login_page.py           # Login interactions
│   └── form_manager_page.py    # Form manager interactions
├── fixtures/                   # Test data
├── screenshots/                # Screenshots on failure
├── videos/                     # Video recordings
└── traces/                     # Playwright traces
```

## Writing Tests

### Basic Test Structure

```python
import pytest
from playwright.sync_api import Page
from tests.e2e.pages.login_page import LoginPage

@pytest.mark.e2e
@pytest.mark.auth
def test_user_can_login(page: Page, base_url: str) -> None:
    """Test that a user can successfully log in."""
    login_page = LoginPage(page, base_url)
    login_page.navigate_to_login()
    login_page.login("testuser", "password")
    login_page.expect_logged_in()
```

### Using Page Objects

Page Objects encapsulate page interactions and make tests more maintainable:

```python
from tests.e2e.pages.form_manager_page import FormManagerPage

def test_submit_form(authenticated_page: Page, base_url: str) -> None:
    form_page = FormManagerPage(authenticated_page, base_url)
    form_page.navigate_to_forms()
    form_page.click_form("Contact Form")
    form_page.fill_form_field("Name", "Test User")
    form_page.submit_form()
    form_page.expect_success_message()
```

### Using Fixtures

```python
# Fixture for authenticated user
def test_forms_page(authenticated_page: Page, base_url: str) -> None:
    # authenticated_page already has a logged-in session
    authenticated_page.goto(f"{base_url}/forms/")
    # ... test logic
```

## Test Markers

Use pytest markers to organize and filter tests:

- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.auth` - Tests requiring authentication
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.skip` - Temporarily skip a test

Run specific markers:
```bash
# Run only auth tests
uv run pytest tests/e2e/ -m "e2e and auth"

# Skip slow tests
uv run pytest tests/e2e/ -m "e2e and not slow"
```

## Debugging

### View Traces

Playwright traces capture everything that happened during a test:

```bash
# View the trace
uv run playwright show-trace tests/traces/trace.zip
```

### Generate Test Code

Use Playwright codegen to generate test code:

```bash
# Record actions and generate code
uv run playwright codegen http://ui.csfeer:8000
```

### Debug Mode

Run tests in debug mode with headed browser and slow motion:

```bash
# See what's happening
make test-e2e-headed

# Even slower for debugging
make test-e2e-debug
```

### macOS Headed Mode (WebKit)

**Important for macOS Sequoia users:** Chromium has compatibility issues on macOS Sequoia 26.1+. Use WebKit (Safari engine) for headed mode testing:

```bash
# Install WebKit browser
uv run playwright install webkit

# Quick way: Use Makefile target (runs all E2E tests)
make test-e2e-webkit

# Run single test with visible browser (1 second delays)
uv run pytest tests/e2e/test_tribal_short_form.py::test_tribal_short_form_complete_workflow -v --headed --browser=webkit --slowmo=1000

# Run with slower motion for easier observation (1.5 second delays)
uv run pytest tests/e2e/test_tribal_short_form.py::test_tribal_short_form_complete_workflow -v --headed --browser=webkit --slowmo=1500

# Run all E2E tests in headed WebKit mode
uv run pytest tests/e2e/ -v --headed --browser=webkit --slowmo=1000
```

**Note:** CI/CD pipelines use headless Chromium and are unaffected by this issue.

### Screenshots and Videos

Failed tests automatically capture:
- Screenshots: `tests/screenshots/`
- Videos: `tests/videos/`

## Configuration

### Environment Variables

```bash
# Override base URL
BASE_URL=http://localhost:8000 make test-e2e

# Run specific test
uv run pytest tests/e2e/test_auth_flow.py::test_user_can_login -v
```

### Timeouts

Adjust timeouts in `tests/conftest.py`:

```python
page.set_default_timeout(60000)  # 60 seconds
page.set_default_navigation_timeout(60000)
```

### Test Users

Test users are defined in `devops/mocks/keycloak/users.csv` and configured in Keycloak:

| Username | Password | Roles |
|----------|----------|-------|
| admin | admin | csfeer_admin, csfeer_user |
| demo | demo | csfeer_user |
| demo-1 | demo-1 | csfeer_user |
| demo-2 | demo-2 | csfeer_user |

**Using different users in tests:**

```python
# Use admin_page fixture for admin user
def test_admin_feature(admin_page: Page, base_url: str):
    page = admin_page  # Already logged in as admin
    
# Use demo_page fixture for regular user
def test_user_feature(demo_page: Page, base_url: str):
    page = demo_page  # Already logged in as demo
    
# Or use the login_as helper
from tests.fixtures.users import login_as

def test_multiple_users(page: Page, base_url: str):
    login_as(page, base_url, "demo-1")
    # ... test as demo-1
    
    page.get_by_role("link", name="Logout").click()
    
    login_as(page, base_url, "admin")
    # ... test as admin
```

## CI/CD

Tests run automatically on:
- Pull requests to main
- Pushes to main
- Manual workflow dispatch

### GitHub Actions Workflow

File: `.github/workflows/e2e-tests.yml`

The workflow:
1. Sets up Python and dependencies
2. Starts Docker services
3. Runs migrations and OAuth setup
4. Executes e2e tests
5. Uploads artifacts (screenshots, videos, traces)

### View CI Results

After a failed CI run:
1. Go to Actions tab
2. Select the failed workflow run
3. Download `playwright-artifacts` under Artifacts
4. Extract and view screenshots/traces locally

## Best Practices

### 1. Use Stable Selectors

Prefer data attributes over CSS classes:

```html
<!-- Good -->
<button data-testid="submit-button">Submit</button>

<!-- In test -->
page.get_by_test_id("submit-button").click()
```

### 2. Wait for Elements

Playwright auto-waits, but be explicit when needed:

```python
# Wait for element to be visible
page.wait_for_selector("[data-testid='form-list']")

# Wait for URL
page.wait_for_url(f"{base_url}/success")
```

### 3. Keep Tests Independent

Each test should work in isolation:

```python
# Good - creates its own data
def test_submit_form(authenticated_page):
    # Setup
    create_test_form()
    
    # Test
    submit_form()
    
    # Cleanup (if needed)
    delete_test_form()
```

### 4. Use Page Objects

Don't repeat selectors and interactions:

```python
# Good - encapsulated in page object
form_page.submit_form()

# Bad - direct page interaction
page.click("button[type='submit']")
```

### 5. Clear Test Names

Test names should describe what they verify:

```python
# Good
def test_user_cannot_submit_form_without_required_fields()

# Bad
def test_form()
```

## Troubleshooting

### Services Not Running

```bash
# Check service status
docker compose ps

# Restart services
make restart

# Check logs
docker compose logs
```

### Import Errors

```bash
# Ensure Playwright is installed
uv run playwright install

# With system dependencies
uv run playwright install --with-deps
```

### OAuth/Authentication Issues

```bash
# Verify Keycloak is accessible
curl http://oauth.csfeer:8081

# Check /etc/hosts
cat /etc/hosts | grep csfeer

# Re-run OAuth setup
make oauth-setup
```

### Test Timeouts

If tests timeout:
1. Check Docker services are healthy: `docker compose ps`
2. Verify network connectivity to services
3. Increase timeouts in `conftest.py`
4. Check application logs: `docker compose logs`

## Resources

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model](https://playwright.dev/docs/pom)
- [Best Practices](https://playwright.dev/docs/best-practices)
