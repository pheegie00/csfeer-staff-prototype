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

Commit `20fe02e` added:
- `from_review=1` query parameter to edit section links
- View logic to detect parameter and create bound form with validation
- **But failed because** `field.html` template was never updated to display errors

## Desired End State

When a user clicks "Edit section" from the review page:

1. They are taken to the first page of that section with `from_review=1` in the URL
2. The form is bound with existing data and validated
3. Fields with errors display error messages inline below the field
4. The `from_review=1` parameter persists as they navigate between pages
5. No general error alert is shown at the top of the page

### Verification

**Manual Testing**:
1. Fill out a form with intentionally invalid data (e.g., leave required fields blank)
2. Navigate to the review page
3. Observe errors displayed on the review page
4. Click "Edit section" for a section with errors
5. Verify:
   - URL includes `from_review=1` parameter
   - Fields with errors show red error messages below them
   - Error messages match those shown on review page
   - Navigating to next/prev page maintains `from_review=1` parameter
   - Errors persist across page navigation within the form

## What We're NOT Doing

- NOT adding a general error banner/alert at the top of edit pages
- NOT changing the validation logic or when validation occurs
- NOT changing the review page's error display
- NOT persisting `from_review` after a successful form save (draft saved clears the parameter)

## Implementation Approach

This is a focused enhancement that:
1. Reuses the existing validation mechanism from the review page
2. Updates the field template to display errors using existing USWDS components
3. Ensures `from_review` persists through navigation URLs
4. Maintains backward compatibility (forms without `from_review` work unchanged)

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
- [ ] Templates parse without syntax errors: `python manage.py check --deploy`
- [ ] No template rendering errors in tests: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/ -k template`

#### Manual Verification:
- [ ] When viewing a form page without `from_review=1`, no errors are shown (existing behavior preserved)
- [ ] When viewing a form page with `from_review=1` and invalid fields, error messages appear below each invalid field
- [ ] Error messages have proper ARIA attributes for screen readers
- [ ] Error styling matches USWDS design patterns (red text, error icon)

---

## Phase 2: Add View Logic to Detect `from_review` and Validate

### Overview
Update the `form_edit` view to detect the `from_review` query parameter, create a bound form, and trigger validation when present.

### Changes Required:

#### 1. Form Edit View
**File**: `form_manager/views/form_edit.py`
**Changes**: Add logic to handle `from_review` parameter

**Location**: Lines 106-144 (around where form is instantiated)

**Add after line 107** (after current_page_number):
```python
from_review = request.GET.get("from_review", False)
```

**Replace lines 144** (form instantiation):
```python
# Old:
form = django_form_class(initial=entry.data or {})

# New:
# If user came from review page, create a bound form with validation
# to show error states. Otherwise, create an unbound form.
if from_review and entry.data:
    form = django_form_class(entry.data)
    form.is_valid(use_default_if_excluded=True)
else:
    form = django_form_class(initial=entry.data or {})
```

**Explanation**:
- Extract `from_review` from query parameters
- When `from_review=1` and entry has data, create a bound form (data instead of initial)
- Call `is_valid(use_default_if_excluded=True)` to trigger validation and populate field errors
- Otherwise, use existing behavior (unbound form with initial data)

### Success Criteria:

#### Automated Verification:
- [ ] Python syntax is correct: `cd /Users/ryanbagwell/projects/csfeer && python -m py_compile form_manager/views/form_edit.py`
- [ ] Type checking passes: `cd /Users/ryanbagwell/projects/csfeer && mypy form_manager/views/form_edit.py`
- [ ] Existing tests pass: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/form_manager/`

#### Manual Verification:
- [ ] Navigating to form edit page without `from_review` works as before (no validation)
- [ ] Navigating to form edit page with `from_review=1` triggers validation
- [ ] Bound form correctly populates with existing data
- [ ] Field errors are accessible in the template context

---

## Phase 3: Persist `from_review` Through Navigation

### Overview
Update URL generation for next/previous page links to include `from_review` parameter when present.

### Changes Required:

#### 1. Form Edit View - Next Page URL
**File**: `form_manager/views/form_edit.py`
**Changes**: Add `from_review` to next_page_url

**Location**: Lines 158-169

**Replace**:
```python
# Old:
if next_step_number is None:
    next_page_url = reverse("form_review", kwargs={"pk": entry.pk})
else:
    next_page_url = (
        reverse(
            "form_edit",
            kwargs={
                "pk": entry.pk,
            },
        )
        + f"?step={next_step_number}&page={next_page_number}"
    )

# New:
if next_step_number is None:
    next_page_url = reverse("form_review", kwargs={"pk": entry.pk})
else:
    next_page_url = (
        reverse(
            "form_edit",
            kwargs={
                "pk": entry.pk,
            },
        )
        + f"?step={next_step_number}&page={next_page_number}"
    )
    if from_review:
        next_page_url += "&from_review=1"
```

#### 2. Form Edit View - Previous Page URL
**File**: `form_manager/views/form_edit.py`
**Changes**: Add `from_review` to prev_page_url

**Location**: Lines 171-179

**Replace**:
```python
# Old:
prev_page_url = (
    reverse(
        "form_edit",
        kwargs={
            "pk": entry.pk,
        },
    )
    + f"?step={previous_step_number}&page={previous_page_number}"
)

# New:
prev_page_url = (
    reverse(
        "form_edit",
        kwargs={
            "pk": entry.pk,
        },
    )
    + f"?step={previous_step_number}&page={previous_page_number}"
)
if from_review:
    prev_page_url += "&from_review=1"
```

**Explanation**:
- When `from_review` is present in the current request, append `&from_review=1` to navigation URLs
- This ensures error states persist as users navigate between form pages
- Review page link doesn't need the parameter (review page always validates)

### Success Criteria:

#### Automated Verification:
- [ ] Python syntax is correct: `cd /Users/ryanbagwell/projects/csfeer && python -m py_compile form_manager/views/form_edit.py`
- [ ] Type checking passes: `cd /Users/ryanbagwell/projects/csfeer && mypy form_manager/views/form_edit.py`
- [ ] Existing tests pass: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/form_manager/`

#### Manual Verification:
- [ ] Starting from review page with `from_review=1`, clicking "Next" includes parameter in URL
- [ ] Starting from review page with `from_review=1`, clicking "Back" includes parameter in URL
- [ ] Errors remain visible when navigating between pages
- [ ] "Continue to Review" button works correctly (no parameter needed for review page)

---

## Phase 4: Add `from_review` to Review Page Edit Links

### Overview
Update the review page template to include `from_review=1` in the "Edit section" links.

### Changes Required:

#### 1. Review and Submit Template
**File**: `form_manager/templates/form_manager/review_and_submit.html`
**Changes**: Add query parameter to edit section links

**Location**: Line 54

**Replace**:
```django
<!-- Old: -->
<c-link href="{% url "form_edit" entry.pk %}?step={{ forloop.counter0}}&page=0">
    <c-icon icon="edit" class="usa-icon margin-right-1"/>Edit section
</c-link>

<!-- New: -->
<c-link href="{% url "form_edit" entry.pk %}?step={{ forloop.counter0}}&page=0&from_review=1">
    <c-icon icon="edit" class="usa-icon margin-right-1"/>Edit section
</c-link>
```

**Explanation**:
- Append `&from_review=1` to the edit section URL
- This triggers validation when user lands on the form page from review

### Success Criteria:

#### Automated Verification:
- [ ] Templates parse without errors: `python manage.py check --deploy`
- [ ] No template rendering errors: `cd /Users/ryanbagwell/projects/csfeer && pytest tests/ -k review`

#### Manual Verification:
- [ ] "Edit section" links include `from_review=1` parameter
- [ ] Clicking "Edit section" takes user to form page with errors displayed
- [ ] URL in browser includes `from_review=1` parameter

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
def test_error_states_shown_from_review_page(client, form_entry_with_invalid_data):
    """Test that clicking Edit from review page shows errors."""
    entry = form_entry_with_invalid_data

    # Navigate to form edit with from_review parameter
    url = reverse("form_edit", kwargs={"pk": entry.pk})
    response = client.get(f"{url}?step=0&page=0&from_review=1")

    assert response.status_code == 200
    # Check that form is bound and has errors
    assert response.context["current_page"].form.is_bound
    assert response.context["current_page"].form.errors

    # Check that navigation URLs include from_review
    assert "from_review=1" in response.context["next_url"]
```

### Manual Testing Steps

1. **Setup**: Create a new form entry and leave required fields blank
2. **Navigate to review**: Complete form navigation to reach review page
3. **Verify review errors**: Confirm errors are shown on review page
4. **Click Edit section**: Click "Edit section" for a section with errors
5. **Verify edit page errors**: Confirm:
   - URL includes `from_review=1`
   - Error messages appear below invalid fields
   - Error styling matches USWDS patterns
6. **Test persistence**: Click "Next" or "Back" buttons
7. **Verify continued errors**: Confirm:
   - URL still includes `from_review=1`
   - Errors remain visible on other pages with invalid fields
8. **Test draft save**: Make changes and save draft
9. **Verify error refresh**: Return to review page and click edit again - errors should reflect updated data

### Edge Cases to Test

1. **Empty form data**: Verify behavior when `entry.data` is empty or None
2. **Conditional fields**: Test with fields excluded via `FieldFilterField`
3. **Multi-page forms**: Verify errors show correctly across multiple pages in a step
4. **Valid data**: Test that no errors appear when all data is valid
5. **Mixed valid/invalid**: Pages with both valid and invalid fields

## Performance Considerations

**Impact**: Minimal - validation already occurs on review page. We're simply moving the same validation to an earlier point when coming from review.

**Optimization**: The `is_valid()` call is only made when `from_review=1`, so normal form navigation remains unaffected.

## Migration Notes

No database migrations required. This is a UI-only enhancement.

## References

- Original issue: bd-240 / FE-316
- Previous implementation commit: `20fe02e9d3544e29671bde7b9817e98f66d8f986`
- Revert commit: `e2f1420acd8055ed1ebb5c6e0cbc6de7e532bcd9`
- Form validation: `form_manager/schema/forms/base.py:57-81`
- USWDS error components: `django_cotton_uswds/templates/cotton/`
