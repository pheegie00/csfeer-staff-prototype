# Link

A flexible link component that supports multiple USWDS link variants.

## Props

| Prop          | Default | Description                                                    |
| ------------- | ------- | -------------------------------------------------------------- |
| `href`        |         | Link URL                                                       |
| `text`        |         | Link text                                                      |
| `variant`     |         | Link style: `default`, `nav`, `summary-box`, `footer-primary`  |
| `is_current`  |         | Set to `true` to add `usa-current` class                       |
| `is_inverse`  |         | Set to `true` for inverse (light on dark) styling              |
| `is_external` |         | Set to `true` for external link with icon                      |
| `target`      |         | Link target attribute (e.g., `_blank`)                         |
| `rel`         |         | Link rel attribute (e.g., `noopener`)                          |
| `attrs`       |         | Additional HTML attributes                                     |

## Variants

| Variant          | Class                      | Use Case                       |
| ---------------- | -------------------------- | ------------------------------ |
| (none)           | (no class)                 | Plain unstyled link            |
| `default`        | `usa-link`                 | Standard USWDS text links      |
| `nav`            | `usa-nav__link`            | Header navigation links        |
| `summary-box`    | `usa-summary-box__link`    | Links within summary boxes     |
| `footer-primary` | `usa-footer__primary-link` | Footer primary navigation      |

## Example Usage

### Plain Link (no styling)

```django
<c-link href="/about" text="About Us" />
```

### Styled USWDS Link

```django
<c-link href="/about" text="About Us" variant="default" />
```

### Navigation Link

```django
<c-link href="/home" variant="nav" is_current="true" text="Home" />
```

### Summary Box Link

```django
<c-link href="#" variant="summary-box" text="Find shelter" />
```

### Footer Link

```django
<c-link href="/contact" variant="footer-primary" text="Contact" />
```

### External Link

```django
<c-link href="https://example.com" text="External site" is_external="true" target="_blank" rel="noopener" />
```

### Inverse Link

```django
<c-link href="/privacy" text="Privacy Policy" is_inverse="true" />
```