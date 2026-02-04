# Initialize Error States After Review Page Implementation Plan

## Overview

When users navigate from the review page back to form sections via "Edit section" links, the form should display validation errors on the fields that need correction. This eliminates the need for users to navigate back and forth between the review page and form pages to identify which fields have errors.

## Related

- Beads Task: bd-240
- External Reference: https://jira.acf.gov/browse/FE-316
- **Area**: api

## Current State Analysis

### How Validation Currently Works

1. **Form Edit Pages** ([form_manager/views/form_edit.py:144](form_manager/views/form_edit.py#L144)):
   - Forms are created as unbound forms with `initial` data
   - No validation occurs during GET requests
   - POST requests save drafts without validation

2. **Review Page** ([form_manager/views/form_review.py:49-51](form_manager/views/form_review.py#L49-L51)):
   - Full form validation happens here
   - Calls `form.is_valid(use_default_if_excluded=True)` to validate all fields
   - Errors displayed inline with field values

3. **Error Display Templates**:
   - **Review template** ([form_manager/templates/form_manager/forms/field_review.html:3-9](form_manager/templates/form_manager/forms/field_review.html#L3-L9)): Shows errors with `text-error` styling
   - **Edit template** ([form_manager/templates/form_manager/forms/field.html:1-12](form_manager/templates/form_manager/forms/field.html#L1-L12)): Does NOT display errors

4. **USWDS Components Available**:
   - `<c-form-group error="...">` - Adds error styling to form groups
   - `<c-error-message error="...">` - Renders error messages with proper ARIA attributes

### Previous Implementation Attempt

Commit `20fe02e` attempted to solve this with a query parameter approach:
- Added `from_review=1` query parameter to edit section links
- View logic to detect parameter and create bound form with validation
- **But failed because**:
  1. `field.html` template was never updated to display errors
  2. Query parameter approach required propagating `&from_review=1` through all navigation URLs

**Better Approach**: This plan uses Django session storage instead of query parameters, providing cleaner URLs and automatic state persistence.

## Desired End State

Once a user has visited the review page for a form entry:

1. A session variable is set indicating they've seen the review page
2. All subsequent visits to form edit pages show validation errors
3. Fields with errors display error messages inline below the field
4. Error state persists naturally across all page navigation (no query parameters needed)
5. No general error alert is shown at the top of the page
6. Session variable is cleared when form is successfully submitted

### Verification

**Manual Testing**:
1. Fill out a form with intentionally invalid data (e.g., leave required fields blank)
2. Navigate to the review page
3. Observe errors displayed on the review page
4. Click "Edit section" for a section with errors
5. Verify:
   - Fields with errors show red error messages below them
   - Error messages match those shown on review page
   - No `from_review` query parameter in URL
6. Navigate to next/prev pages
7. Verify errors persist across all pages without query parameters
8. Save a draft and verify errors refresh to reflect new data

## What We're NOT Doing

- NOT adding a general error banner/alert at the top of edit pages
- NOT changing the validation logic or when validation occurs
- NOT changing the review page's error display
- NOT using query parameters to track state

## Implementation Approach

This is a focused enhancement that:
1. Uses Django session storage to track when a user has visited the review page
2. Reuses the existing validation mechanism from the review page
3. Updates the field template to display errors using existing USWDS components
4. Maintains clean URLs without query parameters
5. Maintains backward compatibility (users who haven't visited review page see no errors)

## Phase 1: Update Field Template to Display Errors

### Overview
Modify the field template to render validation errors inline below each field using USWDS components.

### Changes Required:

#### 1. Field Template
**File**: `form_manager/templates/form_manager/forms/field.html`
**Changes**: Add error handling to the template

**Current**:
```django
<c-form-group>
   {% if field.label and field.field.widget.input_type != "checkbox" %}
    <c-label
        id="{{ field.id_for_label }}"
        label="{{ field.field.title }}"
        required="{{ field.field.required }}"
    />
    {% endif %}

    {{ field.as_widget|safe }}

</c-form-group>
```

**Updated**:
```django
<c-form-group error="{% if field.errors %}{{ field.errors.0 }}{% endif %}">
   {% if field.label and field.field.widget.input_type != "checkbox" %}
    <c-label
        id="{{ field.id_for_label }}"
        label="{{ field.field.title }}"
        required="{{ field.field.required }}"
        error="{% if field.errors %}{{ field.errors.0 }}{% endif %}"
    />
    {% endif %}

    <c-error-message
        id="{{ field.id_for_label }}"
        error="{% if field.errors %}{{ field.errors.0 }}{% endif %}"
    />

    {{ field.as_widget|safe }}

</c-form-group>
```

**Explanation**:
- Pass `error` attribute to `c-form-group` to apply `usa-form-group--error` styling
- Pass `error` attribute to `c-label` for proper label styling in error state
- Add `c-error-message` component to render the error text with proper ARIA attributes
- Use `field.errors.0` to get the first error message (Django form field pattern)

### Success Criteria:

#### Automated Verification:
- [x] Templates parse without syntax errors: `python manage.py check --deploy`
- [x] No template rendering errors in tests: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/ -k template`

#### Manual Verification:
- [ ] When viewing a form page without session flag, no errors are shown (existing behavior preserved)
- [ ] When viewing a form page after visiting review, error messages appear below each invalid field
- [ ] Error messages have proper ARIA attributes for screen readers
- [ ] Error styling matches USWDS design patterns (red text, error icon)

---

## Phase 2: Set Session Variable on Review Page Visit

### Overview
Update the `form_review` view to set a session variable when the user views the review page, indicating they should see validation errors on subsequent form edits.

### Changes Required:

#### 1. Form Review View
**File**: `form_manager/views/form_review.py`
**Changes**: Set session variable when review page is visited

**Location**: Around line 51 (after form validation)

**Add after validation** (after line 51):
```python
# Set session flag to indicate user has seen the review page
# This will cause form_edit to show validation errors
request.session[f"show_errors_{entry.pk}"] = True
```

**Explanation**:
- Use a per-form-entry session key: `show_errors_{entry.pk}`
- Set to `True` when user visits review page
- This persists across all subsequent page loads for this form entry
- No query parameters needed - state is stored server-side in session

### Success Criteria:

#### Automated Verification:
- [ ] Python syntax is correct: `cd /Users/ryanbagwell/projects/csfeer && python -m py_compile form_manager/views/form_review.py`
- [ ] Type checking passes: `cd /Users/ryanbagwell/projects/csfeer && mypy form_manager/views/form_review.py`
- [ ] Existing tests pass: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/form_manager/`

#### Manual Verification:
- [ ] Visiting review page sets the session variable (can verify with Django debug toolbar)
- [ ] Session variable is specific to the form entry
- [ ] Multiple form entries can have independent session states

---

## Phase 3: Check Session Variable in Form Edit View

### Overview
Update the `form_edit` view to check for the session variable and trigger validation when present.

### Changes Required:

#### 1. Form Edit View
**File**: `form_manager/views/form_edit.py`
**Changes**: Check session variable and validate form accordingly

**Location**: Lines 106-144 (around where form is instantiated)

**Add after line 107** (after current_page_number):
```python
# Check if user has visited the review page for this entry
show_errors = request.session.get(f"show_errors_{entry.pk}", False)
```

**Replace line 144** (form instantiation):
```python
# Old:
form = django_form_class(initial=entry.data or {})

# New:
# If user has visited the review page, create a bound form with validation
# to show error states. Otherwise, create an unbound form.
if show_errors and entry.data:
    form = django_form_class(entry.data)
    form.is_valid(use_default_if_excluded=True)
else:
    form = django_form_class(initial=entry.data or {})
```

**Explanation**:
- Check session for `show_errors_{entry.pk}` flag
- When flag is `True` and entry has data, create a bound form (data instead of initial)
- Call `is_valid(use_default_if_excluded=True)` to trigger validation and populate field errors
- Otherwise, use existing behavior (unbound form with initial data)
- No URL manipulation needed - state persists via session

### Success Criteria:

#### Automated Verification:
- [ ] Python syntax is correct: `cd /Users/ryanbagwell/projects/csfeer && python -m py_compile form_manager/views/form_edit.py`
- [ ] Type checking passes: `cd /Users/ryanbagwell/projects/csfeer && mypy form_manager/views/form_edit.py`
- [ ] Existing tests pass: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/form_manager/`

#### Manual Verification:
- [ ] Navigating to form edit page without visiting review first shows no errors
- [ ] After visiting review page, all form edit pages show errors
- [ ] Bound form correctly populates with existing data
- [ ] Field errors are accessible in the template context
- [ ] Errors persist across page navigation without query parameters

---

## Phase 4: Clear Session Variable on Form Submission

### Overview
Update the `form_finalize` view to clear the session variable when the form is successfully submitted.

### Changes Required:

#### 1. Form Finalize View
**File**: `form_manager/views/form_finalize.py`
**Changes**: Clear session variable after successful submission

**Location**: Around line 53 (after success message)

**Add after success message** (after line 53):
```python
# Clear the show_errors flag since form is now submitted
request.session.pop(f"show_errors_{entry.pk}", None)
```

**Explanation**:
- Remove the session flag for this form entry after successful submission
- Uses `pop()` with default `None` to avoid KeyError if flag doesn't exist
- This ensures clean state if user needs to edit a submitted form later
- Session naturally times out if user doesn't submit

### Success Criteria:

#### Automated Verification:
- [ ] Python syntax is correct: `cd /Users/ryanbagwell/projects/csfeer && python -m py_compile form_manager/views/form_finalize.py`
- [ ] Type checking passes: `cd /Users/ryanbagwell/projects/csfeer && mypy form_manager/views/form_finalize.py`
- [ ] Existing tests pass: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/form_manager/`

#### Manual Verification:
- [ ] After form submission, session variable is cleared
- [ ] If user somehow returns to edit pages after submission, errors don't show (unless they visit review again)
- [ ] Session cleanup doesn't cause errors if variable doesn't exist

---

## Testing Strategy

### Unit Tests

No new unit tests required - this feature enhances the UI without changing business logic. Existing tests should continue to pass.

### Integration Tests

Consider adding a test to verify the full flow:

**File**: `tests/form_manager/test_error_states.py` (new file)

```python
import pytest
from django.urls import reverse
from form_manager.models import FormEntry

@pytest.mark.django_db
def test_error_states_shown_after_review_page_visit(client, form_entry_with_invalid_data):
    """Test that visiting review page enables error display on form edit pages."""
    entry = form_entry_with_invalid_data

    # First, visit form edit page before review - should not show errors
    url = reverse("form_edit", kwargs={"pk": entry.pk})
    response = client.get(f"{url}?step=0&page=0")
    assert response.status_code == 200
    assert not response.context["current_page"].form.is_bound

    # Visit review page to set session variable
    review_url = reverse("form_review", kwargs={"pk": entry.pk})
    response = client.get(review_url)
    assert response.status_code == 200
    assert client.session[f"show_errors_{entry.pk}"] is True

    # Now revisit form edit page - should show errors
    response = client.get(f"{url}?step=0&page=0")
    assert response.status_code == 200
    assert response.context["current_page"].form.is_bound
    assert response.context["current_page"].form.errors

    # Navigate to another page - errors should persist
    response = client.get(f"{url}?step=0&page=1")
    assert response.status_code == 200
    assert response.context["current_page"].form.is_bound
```

### Manual Testing Steps

1. **Setup**: Create a new form entry and leave required fields blank
2. **Navigate through form**: Fill out some pages, leaving some required fields blank
3. **Before review visit**: Navigate to a form edit page and verify NO errors are shown
4. **Navigate to review**: Complete form navigation to reach review page
5. **Verify review errors**: Confirm errors are shown on review page
6. **Click Edit section**: Click "Edit section" for a section with errors
7. **Verify edit page errors**: Confirm:
   - Error messages appear below invalid fields
   - Error styling matches USWDS patterns
   - URL is clean (no `from_review` parameter)
8. **Test persistence**: Click "Next" or "Back" buttons
9. **Verify continued errors**: Confirm:
   - Errors remain visible on other pages with invalid fields
   - URLs remain clean without query parameters
10. **Test draft save**: Make changes and save draft
11. **Verify error refresh**: Errors should update to reflect new data
12. **Test form submission**: Submit the form successfully
13. **Verify cleanup**: If somehow returning to form edit, errors should not show (session cleared)

### Edge Cases to Test

1. **Empty form data**: Verify behavior when `entry.data` is empty or None
2. **Conditional fields**: Test with fields excluded via `FieldFilterField`
3. **Multi-page forms**: Verify errors show correctly across multiple pages in a step
4. **Valid data**: Test that no errors appear when all data is valid
5. **Mixed valid/invalid**: Pages with both valid and invalid fields
6. **Session timeout**: Verify graceful handling if session expires between review and edit
7. **Multiple form entries**: Verify session variables don't conflict between different form entries
8. **Direct URL access**: Test accessing form edit page directly without visiting review first

## Performance Considerations

**Impact**: Minimal - validation already occurs on review page. We're simply moving the same validation to form edit pages when appropriate.

**Session Storage**: Session variables are lightweight (boolean flag per form entry). Django's default session backend handles this efficiently.

**Optimization**: The `is_valid()` call is only made when the session flag is set, so users who haven't visited the review page experience no performance impact.

## Migration Notes

No database migrations required. This is a UI-only enhancement.

## References

- Original issue: bd-240 / FE-316
- Previous implementation commit: `20fe02e9d3544e29671bde7b9817e98f66d8f986`
- Revert commit: `e2f1420acd8055ed1ebb5c6e0cbc6de7e532bcd9`
- Form validation: `form_manager/schema/forms/base.py:57-81`
- USWDS error components: `django_cotton_uswds/templates/cotton/`
