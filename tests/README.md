# E2E Tests with Playwright

This directory contains end-to-end tests for the csfeer application using Playwright.

## Setup

1. Install dependencies:
```bash
uv sync
uv run playwright install chromium
```

2. Ensure Docker services are running:
```bash
make start
```

3. Verify `/etc/hosts` has the required entries:
```
127.0.0.1       oauth.csfeer
127.0.0.1       ui.csfeer
```

## Running Tests

### Run all e2e tests in Docker (headless, recommended):
```bash
make test-e2e
# Override test path:
make test-e2e TEST=tests/e2e/test_auth_flow.py::test_user_can_login
```

### Run tests natively in headed mode (see browser):
```bash
make native-test-e2e-headed
# or
uv run pytest tests/e2e/ -v -m e2e --headed
```

### Run tests natively in debug mode (slow motion):
```bash
make native-test-e2e-debug
# or
uv run pytest tests/e2e/ -v -m e2e --headed --slowmo 1000
```

### Run only authentication tests:
```bash
make native-test-e2e-auth
# or
uv run pytest tests/e2e/ -v -m "e2e and auth"
```

### Run a specific test:
```bash
uv run pytest tests/e2e/test_auth_flow.py::test_user_can_login -v
```

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── e2e/                     # E2E test cases
│   ├── test_auth_flow.py    # Authentication tests
│   ├── test_navigation.py   # Navigation tests
│   └── test_form_manager.py # Form manager tests
├── pages/                   # Page Object Model classes
│   ├── base_page.py         # Base page class
│   ├── login_page.py        # Login page interactions
│   └── form_manager_page.py # Form manager interactions
├── fixtures/                # Test data and fixtures
├── screenshots/             # Screenshots on failure
├── videos/                  # Video recordings
└── traces/                  # Playwright traces
```

## Page Object Model

Tests use the Page Object Model pattern to encapsulate page interactions:

- **BasePage**: Common functionality for all pages
- **LoginPage**: Login/logout and authentication flows
- **FormManagerPage**: Form listing, viewing, and submission

## Test Markers

- `@pytest.mark.e2e`: Marks test as end-to-end test
- `@pytest.mark.auth`: Marks test as requiring authentication
- `@pytest.mark.slow`: Marks test as slow-running
- `@pytest.mark.skip`: Temporarily skip test

## Debugging

### View test artifacts:
- **Screenshots**: `tests/screenshots/`
- **Videos**: `tests/videos/`
- **Traces**: `tests/traces/`

### View trace in Playwright Inspector:
```bash
uv run playwright show-trace tests/traces/trace.zip
```

### Use Playwright codegen to generate selectors:
```bash
uv run playwright codegen http://ui.csfeer:8000
```

## Configuration

### Base URL
Default: `http://ui.csfeer:8000`

Override with environment variable:
```bash
BASE_URL=http://localhost:8000 uv run pytest tests/e2e/
```

### Browser Options
Configure in `tests/conftest.py`:
- Viewport size: 1920x1080
- Timezone: America/New_York
- Locale: en-US

### Test Users
Authentication tests use Keycloak test users from `devops/mocks/keycloak/users.csv`:

- **admin**: `admin` / `admin` (roles: csfeer_admin, csfeer_user)
- **demo**: `demo` / `demo` (roles: csfeer_user)
- **demo-1**: `demo-1` / `demo-1` (roles: csfeer_user)
- **demo-2**: `demo-2` / `demo-2` (roles: csfeer_user)

Use fixtures: `admin_page`, `demo_page`, or helper function `login_as()`.

## CI/CD Integration

To run in CI:
1. Start Docker services
2. Wait for services to be healthy
3. Run tests: `make test-e2e`
4. Collect artifacts (screenshots, videos, traces)

## Best Practices

1. **Use data-testid attributes** in HTML for stable selectors
2. **Avoid hardcoded waits** - use Playwright's auto-waiting
3. **Keep tests independent** - each test should work in isolation
4. **Use Page Objects** - encapsulate page interactions
5. **Add descriptive test names** - clearly state what is being tested
6. **Take screenshots on failure** - automatically captured
7. **Use fixtures for common setup** - reduce code duplication

## Troubleshooting

### Services not accessible
Ensure Docker services are running:
```bash
docker compose ps
make start
```

### OAuth login fails
Check Keycloak is running and accessible:
```bash
curl http://oauth.csfeer:8081
```

### Tests timeout
Increase timeout in `tests/conftest.py`:
```python
page.set_default_timeout(60000)  # 60 seconds
```

### Import errors
Ensure Playwright is installed:
```bash
uv run playwright install --with-deps
```
