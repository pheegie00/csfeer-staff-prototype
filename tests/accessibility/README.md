# Accessibility Tests (dev only)

Uses [axe-playwright-python](https://github.com/abhinand5ai/axe-playwright-python) to run axe-core against live pages and check for WCAG 2.1 AA violations.

These are **not run in CI** — intended for local use before submitting a PR.

## Setup

```bash
uv sync
```

## Running

```bash
# All accessibility tests
uv run pytest tests/accessibility/ -v

# Single test
uv run pytest tests/accessibility/test_accessibility.py::test_forms_list_accessibility -v
```

## Adding tests

Navigate to the page using an existing fixture (`demo_page`, `admin_page`), then run axe:

```python
results = Axe().run(page)
assert results.violations_count == 0, results.generate_report()
```

Mark tests with both `@pytest.mark.e2e` and `@pytest.mark.accessibility`.
