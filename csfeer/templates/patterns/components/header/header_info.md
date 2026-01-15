# Header

A flexible, modular navigation header following USWDS patterns. Supports basic, extended, and megamenu variants.

## Props

| Prop          | Default   | Description                                     |
| ------------- | --------- | ----------------------------------------------- |
| `type`        | `basic`   | Header type: `basic` or `extended`              |
| `is_megamenu` | `false`   | Enable megamenu styling                         |
| `title`       |           | Logo/site title text                            |
| `logo_href`   | `/`       | Logo link URL                                   |
| `show_search` | `true`    | Show search form                                |

## Slots

| Slot              | Description                              |
| ----------------- | ---------------------------------------- |
| (default)         | Navigation items                         |
| `secondary_links` | Secondary links (extended header only)   |

## Sub-components

### `<c-header.nav-item>`

| Prop         | Default | Description                              |
| ------------ | ------- | ---------------------------------------- |
| `type`       | `link`  | Item type: `link` or `dropdown`          |
| `href`       |         | Link URL (for `type="link"`)             |
| `text`       |         | Display text                             |
| `is_current` | `false` | Mark as current page                     |
| `submenu_id` |         | ID for submenu (for `type="dropdown"`)   |

### `<c-header.nav-submenu>`

| Prop         | Default | Description                              |
| ------------ | ------- | ---------------------------------------- |
| `id`         |         | Unique ID (matches `submenu_id`)         |
| `is_megamenu`| `false` | Enable megamenu grid layout              |

### `<c-header.nav-submenu-item>`

| Prop   | Default | Description |
| ------ | ------- | ----------- |
| `href` |         | Link URL    |
| `text` |         | Link text   |

### `<c-header.megamenu-column>`

Wrapper for megamenu columns. Contains `<c-header.nav-submenu-item>` elements.

### `<c-header.secondary-link>`

| Prop   | Default | Description |
| ------ | ------- | ----------- |
| `href` |         | Link URL    |
| `text` |         | Link text   |

## Example Usage

### Basic Header

```django
<c-header title="Project Title" show_search="true">
    <c-header.nav-item type="link" href="/about" text="About" />
    <c-header.nav-item type="dropdown" text="Services" submenu_id="services-menu">
        <c-header.nav-submenu id="services-menu">
            <c-header.nav-submenu-item href="/design" text="Design" />
            <c-header.nav-submenu-item href="/development" text="Development" />
        </c-header.nav-submenu>
    </c-header.nav-item>
</c-header>
```

### Megamenu Header

```django
<c-header is_megamenu="true" title="Project Title">
    <c-header.nav-item type="dropdown" text="Services" submenu_id="mega-menu">
        <c-header.nav-submenu id="mega-menu" is_megamenu="true">
            <c-header.megamenu-column>
                <c-header.nav-submenu-item href="#" text="Web Design" />
                <c-header.nav-submenu-item href="#" text="Mobile Design" />
            </c-header.megamenu-column>
            <c-header.megamenu-column>
                <c-header.nav-submenu-item href="#" text="Frontend" />
                <c-header.nav-submenu-item href="#" text="Backend" />
            </c-header.megamenu-column>
        </c-header.nav-submenu>
    </c-header.nav-item>
</c-header>
```

### Extended Header with Secondary Links

```django
<c-header type="extended" title="Project Title">
    <c-header.nav-item type="link" href="/about" text="About" />
    <c-header.nav-item type="link" href="/contact" text="Contact" />

    <c-slot name="secondary_links">
        <c-header.secondary-link href="tel:1-800-555-1234" text="(800) 555-1234" />
        <c-header.secondary-link href="mailto:info@example.gov" text="Email Us" />
    </c-slot>
</c-header>
```
