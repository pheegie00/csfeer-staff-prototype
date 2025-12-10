# django-cotton-uswds

Small collection of USWDS-styled django-cotton components (summary box, alert, checkbox, card)
packaged as a Django app so they can be reused across projects.

Quick start

1. Install this package (locally, or add to your project path).
2. Add `django_cotton_uswds` to `INSTALLED_APPS` in your Django settings.
3. Option A — use tags locally: in templates, `{% load cotton %}` and then use
   `<c-summary-box>...</c-summary-box>`, `<c-alert>...</c-alert>`, `<c-checkbox>...</c-checkbox>`, or `<c-card>...</c-card>`.
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

### Card

USWDS-styled card components for displaying content in a modular, collection-friendly format.

#### Components

- `c-card-group`: Wraps multiple cards in a list.
- `c-card`: The main card element.
- `c-card-header`: The card header section.
- `c-card-media`: The card media section.
- `c-card-body`: The card body section.
- `c-card-footer`: The card footer section.

#### Usage

```html
<c-card-group>
    <c-card layout="standardDefault" grid_layout="tablet:grid-col-6">
        <c-card-header>
            <h2 class="usa-card__heading">Card Title</h2>
        </c-card-header>
        <c-card-body>
            <p>Card content goes here.</p>
        </c-card-body>
        <c-card-footer>
            <a href="#" class="usa-button">Action</a>
        </c-card-footer>
    </c-card>
</c-card-group>
```

#### Attributes

##### Card Group
- `extra_classes`: Additional CSS classes.

##### Card
- `layout`: Card layout variant (`standardDefault`, `flagDefault`, `flagMediaRight`).
- `header_first`: If true, displays header before media.
- `grid_layout`: CSS classes for grid layout (e.g., `tablet:grid-col-6`).
- `container_class`: Additional classes for the card container.
- `extra_classes`: Additional CSS classes.

##### Card Header
- `exdent`: If true, extends header over card border.
- `extra_classes`: Additional CSS classes.

##### Card Media
- `exdent`: If true, extends media over card border.
- `inset`: If true, indents media.
- `image_class`: Additional classes for the image container.
- `extra_classes`: Additional CSS classes.

##### Card Body
- `exdent`: If true, extends body over card border.
- `extra_classes`: Additional CSS classes.

##### Card Footer
- `exdent`: If true, extends footer over card border.
- `extra_classes`: Additional CSS classes.

Notes

- This package simply provides templates and a convenience shim. It depends on
  `django-cotton` and your project should already be set up to use it.
