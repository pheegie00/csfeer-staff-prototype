# django-cotton-uswds

Small collection of USWDS-styled django-cotton components (summary box, alert)
packaged as a Django app so they can be reused across projects.

Quick start

1. Install this package (locally, or add to your project path).
2. Add `django_cotton_uswds` to `INSTALLED_APPS` in your Django settings.
3. Option A — use tags locally: in templates, `{% load cotton %}` and then use
   `<c-summary-box>...</c-summary-box>` or `<c-alert>...</c-alert>`.
4. Option B — make tags available globally by adding the builtin alias to
   your template engine builtins (so you don't need `{% load cotton %}` everywhere):

```py
# in settings.py
TEMPLATES[0]['OPTIONS'].setdefault('builtins', []).append(
    'django_cotton_uswds.templatetags.cotton_aliases'
)
```

Notes

- This package simply provides templates and a convenience shim. It depends on
  `django-cotton` and your project should already be set up to use it.
