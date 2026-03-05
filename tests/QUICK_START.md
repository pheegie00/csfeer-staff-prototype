# E2E Tests - Quick Start

## Setup (One-time)

```bash
# 1. Install dependencies
uv sync
# Note: `uv run playwright install chromium` is only needed for native/headed runs.
# Docker-based runs (make test-e2e) use the bundled Chromium in the e2e image.

# 2. Start Docker services
make start

# 3. Verify /etc/hosts (should already be set)
cat /etc/hosts | grep csfeer
# Should show:
# 127.0.0.1  oauth.csfeer
# 127.0.0.1  ui.csfeer
```

## Run Tests

```bash
# Run all tests in Docker (headless) — recommended
make test-e2e

# Run a specific test in Docker
make test-e2e TEST=tests/e2e/test_auth_flow.py::test_user_can_login

# Run natively with visible browser
make native-test-e2e-headed

# Run natively with slow motion for debugging
make native-test-e2e-debug

# Run specific test file natively
uv run pytest tests/e2e/test_auth_flow.py -v

# Run specific test natively
uv run pytest tests/e2e/test_auth_flow.py::test_user_can_login -v
```

## Test Users

All users have their username as password:

| User | Roles | Usage |
|------|-------|-------|
| `admin` / `admin` | Admin + User | Use `admin_page` fixture |
| `demo` / `demo` | User | Use `demo_page` fixture or `authenticated_page` |
| `demo-1` / `demo-1` | User | Use `login_as()` helper |
| `demo-2` / `demo-2` | User | Use `login_as()` helper |

## Common Test Patterns

### Using authenticated fixtures:
```python
@pytest.mark.e2e
@pytest.mark.auth
def test_something(demo_page: Page, base_url: str):
    page = demo_page  # Already logged in as demo user
    page.goto(f"{base_url}/forms/")
    # ... your test
```

### Using admin fixture:
```python
@pytest.mark.e2e
@pytest.mark.auth
def test_admin_feature(admin_page: Page, base_url: str):
    page = admin_page  # Already logged in as admin
    page.goto(f"{base_url}/admin/")
    # ... your test
```

### Using Page Objects:
```python
from tests.e2e.pages.form_manager_page import FormManagerPage

@pytest.mark.e2e
@pytest.mark.auth
def test_form_submission(demo_page: Page, base_url: str):
    form_page = FormManagerPage(demo_page, base_url)
    form_page.navigate_to_forms()
    form_page.click_form("My Form")
    form_page.fill_form_field("Name", "Test")
    form_page.submit_form()
    form_page.expect_success_message()
```

## Debugging

### View what happened:
```bash
# Check screenshots
ls tests/screenshots/

# View trace (interactive)
uv run playwright show-trace tests/traces/trace.zip

# Generate test code
uv run playwright codegen http://ui.csfeer:8000
```

### Common Issues:

**"Services not accessible"**
```bash
docker compose ps  # Check services are running
make start        # Start if needed
```

**"OAuth login fails"**
```bash
curl http://oauth.csfeer:8081  # Check Keycloak is up
make oauth-setup               # Re-run setup if needed
```

**"Import errors"**
```bash
uv sync  # Reinstall dependencies
```

## Writing New Tests

1. Choose the right fixture:
   - `page` - Fresh browser page (not logged in)
   - `authenticated_page` - Logged in as demo user
   - `demo_page` - Logged in as demo user  
   - `admin_page` - Logged in as admin user

2. Add markers:
   ```python
   @pytest.mark.e2e        # Always for e2e tests
   @pytest.mark.auth       # If test requires login
   @pytest.mark.slow       # If test takes >10s
   ```

3. Use Page Objects when possible:
   ```python
   from tests.e2e.pages.your_page import YourPage
   
   page_obj = YourPage(page, base_url)
   page_obj.do_something()
   ```

4. Run your test:
   ```bash
   uv run pytest tests/e2e/test_your_file.py::test_your_test -v --headed
   ```

## Need Help?

- Full docs: `tests/README.md`
- Detailed guide: `docs/E2E_TESTING.md`
- Playwright docs: https://playwright.dev/python/docs/intro
