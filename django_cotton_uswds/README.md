# django-cotton-uswds

Small collection of USWDS-styled django-cotton components (summary box, alert, checkbox)
packaged as a Django app so they can be reused across projects.

Quick start

1. Install this package (locally, or add to your project path).
2. Add `django_cotton_uswds` to `INSTALLED_APPS` in your Django settings.
3. Option A — use tags locally: in templates, `{% load cotton %}` and then use
   `<c-summary-box>...</c-summary-box>`, `<c-alert>...</c-alert>`, or `<c-checkbox>...</c-checkbox>`.
4. Option B — make tags available globally by adding the builtin alias to
   your template engine builtins (so you don't need `{% load cotton %}` everywhere):

```py
# in settings.py
TEMPLATES[0]['OPTIONS'].setdefault('builtins', []).append(
    'django_cotton_uswds.templatetags.cotton_aliases'
)
```

## Components

### Checkbox

A USWDS-styled checkbox component.

#### Usage

```html
<c-checkbox id="my-checkbox" name="my_checkbox" label="Check this box" />
```

#### Attributes

- `id`: The ID for the checkbox input and label.
- `name`: The name attribute for the checkbox input.
- `label`: The text for the label.
- `tile`: If true, applies the tile variant styling.
- `label_description`: Optional additional description text below the label.
- `indeterminate`: If true, adds `data-indeterminate` attribute.
- `checked`: If true, the checkbox is checked.
- `value`: The value attribute for the checkbox.
- `disabled`: If true, the checkbox is disabled.
- `required`: If true, the checkbox is required.
- `extra_classes`: Additional CSS classes for the wrapper div.

Notes

- This package simply provides templates and a convenience shim. It depends on
  `django-cotton` and your project should already be set up to use it.
