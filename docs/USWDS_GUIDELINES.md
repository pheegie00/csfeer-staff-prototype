# USWDS Component & Styling Guidelines

## Overview

This project uses the U.S. Web Design System (USWDS) for all UI components and styling. Follow these guidelines to maintain consistency and avoid unnecessary custom CSS.

## Key Principles

### 1. Always Use USWDS Components First

Before creating any custom HTML/CSS, check if USWDS provides a suitable component:

**Primary Reference:** [USWDS Components](https://designsystem.digital.gov/components/overview/)

Common components available:
- Accordion
- Alert
- Button
- Form controls (inputs, selects, checkboxes, etc.)
- Tables
- Cards
- Step indicators
- And many more...

### 2. Use USWDS Utility Classes

USWDS provides comprehensive utility classes for:
- **Typography:** `.font-heading-xl`, `.font-body-md`, `.text-bold`, etc.
- **Spacing:** `.margin-top-2`, `.padding-4`, etc.
- **Colors:** `.text-primary`, `.bg-base-lighter`, etc.
- **Layout:** `.display-flex`, `.grid-row`, `.grid-col-12`, etc.

**Reference:** [USWDS Utilities](https://designsystem.digital.gov/utilities/)

### 3. Reference the Project Pattern Library

Check our internal pattern library for project-specific components before building new ones:

**Local Pattern Library:** http://ui.csfeer:8000/pattern-library/pattern/patterns/components/header/header.html

This shows components already built and integrated into the project.

### 4. Avoid Custom CSS Unless Absolutely Necessary

Only create custom styles when:
- USWDS doesn't provide the needed functionality
- Project-specific business logic requires it
- You've exhausted USWDS components and utilities

**Custom CSS Location:** `frontend/src/scss/_uswds-theme-custom-styles.scss`

## Workflow

1. **Check USWDS Components** - Is there an existing component?
2. **Check USWDS Utilities** - Can utility classes achieve the styling?
3. **Check Pattern Library** - Do we have a custom component already?
4. **Consider Alternatives** - Can we combine existing components?
5. **Only Then** - Create custom CSS if truly needed

## Examples

### Good: Using USWDS Defaults

```html
<p>
  <strong>{{ field_label }}</strong><br />
  {{ field_value }}
</p>
```

The default `<p>` tag provides proper typography (Public Sans, 16px, 400 weight, 150% line-height).

### Bad: Unnecessary Custom CSS

```html
<span class="custom-text-style">{{ field_value }}</span>
```

```scss
.custom-text-style {
  font-family: "Public Sans";
  font-size: 16px;
  font-weight: 400;
  line-height: 150%;
}
```

This is redundant when USWDS already provides these defaults.

### Good: Using USWDS Utilities

```html
<div class="display-flex flex-justify-between margin-top-4">
  <button class="usa-button">Continue</button>
  <button class="usa-button usa-button--outline">Back</button>
</div>
```

### Good: Using USWDS Components

```html
<c-accordion type="multiselectable">
  <c-accordion-item heading="Section 1" control-id="section1">
    <!-- content -->
  </c-accordion-item>
</c-accordion>
```

## Build Process

After making changes to SCSS files:

```bash
npm run build
```

**Note:** We use symlinks for static files, so `collectstatic` is NOT needed during development.

## Resources

- [USWDS Components](https://designsystem.digital.gov/components/overview/)
- [USWDS Utilities](https://designsystem.digital.gov/utilities/)
- [USWDS Design Tokens](https://designsystem.digital.gov/design-tokens/)
- [Project Pattern Library](http://ui.csfeer:8000/pattern-library/)

## Questions?

When in doubt, ask: "Does USWDS already solve this?" The answer is usually yes.
