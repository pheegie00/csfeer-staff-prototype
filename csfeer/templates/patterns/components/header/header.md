# Header Component

The header component provides a flexible, modular navigation header following USWDS patterns. It supports basic, extended, and megamenu variants.

## Basic Usage

```django
{% load cotton %}

<c-header title="My Project" logo_href="/" show_search="true">
    <c-header.nav_item type="link" href="/about" text="About" />
    <c-header.nav_item type="link" href="/contact" text="Contact" />
</c-header>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | string | `"basic"` | Header type: `"basic"` or `"extended"` |
| `is_megamenu` | string | `"false"` | Enable megamenu styling (`"true"` or `"false"`) |
| `title` | string | `""` | Logo/site title text |
| `logo_href` | string | `"/"` | Logo link URL |
| `show_search` | string | `"true"` | Show search form (`"true"` or `"false"`) |

---

## Examples

### Basic Header with Dropdowns

```django
{% load cotton %}

<c-header type="basic" title="Project Title" show_search="true">
    {# Dropdown with submenu #}
    <c-header.nav_item 
        type="dropdown" 
        text="Services" 
        submenu_id="services-menu"
        is_current="true"
    >
        <c-header.nav_submenu id="services-menu">
            <c-header.nav_submenu_item href="/services/design" text="Design" />
            <c-header.nav_submenu_item href="/services/development" text="Development" />
            <c-header.nav_submenu_item href="/services/consulting" text="Consulting" />
        </c-header.nav_submenu>
    </c-header.nav_item>

    {# Simple link #}
    <c-header.nav_item type="link" href="/about" text="About Us" />
</c-header>
```

### Basic Header with Megamenu

```django
{% load cotton %}

<c-header type="basic" is_megamenu="true" title="Project Title" show_search="true">
    <c-header.nav_item 
        type="dropdown" 
        text="Services" 
        submenu_id="mega-services-menu"
        is_current="true"
    >
        <c-header.nav_submenu id="mega-services-menu" is_megamenu="true">
            {# Column 1 #}
            <c-header.megamenu_column>
                <c-header.nav_submenu_item href="#" text="Web Design" />
                <c-header.nav_submenu_item href="#" text="Mobile Design" />
                <c-header.nav_submenu_item href="#" text="UX Research" />
            </c-header.megamenu_column>

            {# Column 2 #}
            <c-header.megamenu_column>
                <c-header.nav_submenu_item href="#" text="Frontend Development" />
                <c-header.nav_submenu_item href="#" text="Backend Development" />
                <c-header.nav_submenu_item href="#" text="DevOps" />
            </c-header.megamenu_column>

            {# Column 3 #}
            <c-header.megamenu_column>
                <c-header.nav_submenu_item href="#" text="Strategy" />
                <c-header.nav_submenu_item href="#" text="Training" />
                <c-header.nav_submenu_item href="#" text="Support" />
            </c-header.megamenu_column>
        </c-header.nav_submenu>
    </c-header.nav_item>

    <c-header.nav_item type="link" href="/contact" text="Contact" />
</c-header>
```

### Extended Header with Secondary Links

```django
{% load cotton %}

<c-header type="extended" title="Project Title" show_search="true">
    {# Primary navigation #}
    <c-header.nav_item 
        type="dropdown" 
        text="Programs" 
        submenu_id="programs-menu"
        is_current="true"
    >
        <c-header.nav_submenu id="programs-menu">
            <c-header.nav_submenu_item href="/programs/grants" text="Grants" />
            <c-header.nav_submenu_item href="/programs/loans" text="Loans" />
            <c-header.nav_submenu_item href="/programs/assistance" text="Assistance" />
        </c-header.nav_submenu>
    </c-header.nav_item>

    <c-header.nav_item type="link" href="/resources" text="Resources" />
    <c-header.nav_item type="link" href="/contact" text="Contact" />

    {# Secondary links (extended header only) #}
    <c-slot name="secondary_links">
        <c-header.secondary_link href="tel:1-800-555-1234" text="(800) 555-1234" />
        <c-header.secondary_link href="mailto:info@example.gov" text="Email Us" />
    </c-slot>
</c-header>
```

### Header without Search

```django
{% load cotton %}

<c-header type="basic" title="Simple Site" show_search="false">
    <c-header.nav_item type="link" href="/" text="Home" is_current="true" />
    <c-header.nav_item type="link" href="/about" text="About" />
    <c-header.nav_item type="link" href="/contact" text="Contact" />
</c-header>
```

---

## Sub-components

### `<c-header.nav_item>`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | string | `"link"` | Item type: `"link"` or `"dropdown"` |
| `href` | string | `""` | Link URL (for `type="link"`) |
| `text` | string | `""` | Display text |
| `is_current` | string | `"false"` | Mark as current page |
| `submenu_id` | string | `""` | ID for submenu (for `type="dropdown"`) |

### `<c-header.nav_submenu>`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | string | `""` | Unique ID (matches `submenu_id` on parent) |
| `is_megamenu` | string | `"false"` | Enable megamenu grid layout |

### `<c-header.nav_submenu_item>`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | string | `""` | Link URL |
| `text` | string | `""` | Display text |

### `<c-header.megamenu_column>`

Wrapper for megamenu column. Contains `<c-header.nav_submenu_item>` elements.

### `<c-header.secondary_link>`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | string | `""` | Link URL |
| `text` | string | `""` | Display text |

*Note: Secondary links only appear in extended headers.*

### `<c-header.search>`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | string | `"small"` | Search size: `"small"` or `"big"` |
| `input_id` | string | `"search-field"` | Input element ID |
| `label` | string | `"Search"` | Screen reader label |
