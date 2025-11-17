# Component Library

The project uses [django-pattern-library](https://github.com/torchbox/django-pattern-library) to showcase Cotton USWDS components.

**Access the pattern library**: http://ui.csfeer:8000/pattern-library/

## Adding New Components

1. Create a directory under `csfeer/templates/patterns/components/`:
   ```bash
   mkdir -p csfeer/templates/patterns/components/my-component
   ```

2. Create the template file (`my-component.html`):
   ```html
   {% load cotton %}
   
   <div class="component-variants">
       <h1>My Component</h1>
       
       {% for variant in variants %}
       <div class="component-variant">
           <h2 class="variant-title">{{ variant.title }}</h2>
           <c-my-component type="{{ variant.type }}">
               {{ variant.content }}
           </c-my-component>
       </div>
       {% endfor %}
   </div>
   ```

3. Create the context file (`my-component.yaml`):
   ```yaml
   name: My Component
   context:
     variants:
       - title: "Variant 1"
         type: "primary"
         content: "Example content"
       - title: "Variant 2"
         type: "secondary"
         content: "Another example"
   ```

The component will automatically appear in the pattern library navigation.

## Existing Components

- **Accordion** - Borderless, bordered, and multiselectable variants
- **Alert** - Info, warning, success, error, emergency, slim, and no-icon variants
- **Summary Box** - Simple and with actions variants

## Directory Structure

```
csfeer/templates/patterns/
├── README.md                  # This file
├── base.html                  # Base template with USWDS styling
└── components/
    ├── accordion/
    │   ├── accordion.html     # Renders 3 variants
    │   └── accordion.yaml     # Context data
    ├── alert/
    │   ├── alert.html         # Renders 7 variants
    │   └── alert.yaml         # Context data
    └── summary_box/
        ├── summary_box.html   # Renders 2 variants
        └── summary_box.yaml   # Context data
```

## Technical Details

### Configuration

Pattern library is configured in `csfeer/settings.py`:

```python
# Django templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "csfeer", "templates"),
        ],
        # ... other settings
    },
]

# Pattern library configuration
PATTERN_LIBRARY = {
    "SECTIONS": (
        ("Components", ["patterns/components"]),
        ("Pages", ["patterns/pages"]),
    ),
    "TEMPLATE_SUFFIX": ".html",
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
}
```

The patterns live in `csfeer/templates/patterns/` (a subdirectory of the main templates directory). The `patterns/` prefix in `PATTERN_LIBRARY` paths allows Django to find them relative to `csfeer/templates/`.

### Key Learnings

1. **Template Location**: Pattern templates are in `csfeer/templates/patterns/` subdirectory of main templates
2. **Path Resolution**: Use `patterns/` prefix in PATTERN_LIBRARY settings so Django resolves paths correctly
3. **Cotton Component Syntax**: Cannot use Django template tags inside Cotton component opening tags
4. **Component Attributes**: Different components handle content differently (slots vs attributes)
5. **YAML Context**: Each component needs a matching `.yaml` file with context data for rendering

### Resources

- [Django Pattern Library Documentation](https://torchbox.github.io/django-pattern-library/)
- [Online Demo](https://torchbox.github.io/django-pattern-library/demo/)
- [Multiple Variants Guide](https://torchbox.github.io/django-pattern-library/guides/multiple-variants/)
- [USWDS Components](https://designsystem.digital.gov/components/)
