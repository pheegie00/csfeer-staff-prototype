# In-Page Navigation

A JavaScript-powered navigation component that automatically generates a table of contents from page headings, following USWDS patterns. The component uses Intersection Observer to highlight the current section as users scroll.

## Props

| Prop                    | Default           | Description                                                    |
| ----------------------- | ----------------- | -------------------------------------------------------------- |
| `title_text`            | `On this page`    | Text for the navigation title                                  |
| `title_heading_level`   | `h4`              | Heading level for the navigation title (h1-h6)                 |
| `scroll_offset`         | `0`               | Offset from top when scrolling to sections (in pixels)         |
| `root_margin`           | `0px 0px 0px 0px` | Root margin for Intersection Observer                          |
| `threshold`             | `1`               | Visibility threshold for Intersection Observer (0-1)           |
| `content_id`            | `main-content`    | ID attribute for the main content element                      |
| `extra_classes`         |                   | Additional CSS classes for the container                       |

## Slots

| Slot      | Description                                                     |
| --------- | --------------------------------------------------------------- |
| (default) | Main content with headings (h1, h2, h3) that will be tracked   |

## How It Works

The in-page navigation component:
1. Automatically scans the content for h2 and h3 headings
2. Generates a table of contents navigation sidebar
3. Uses Intersection Observer to track which section is currently visible
4. Highlights the current section in the navigation
5. Provides smooth scrolling to sections when clicked

## Example Usage

### Basic In-Page Navigation

```django
<c-in_page_nav>
    <h1>Page Title</h1>

    <h2>Introduction</h2>
    <p>Introduction content goes here...</p>

    <h2>Getting Started</h2>
    <p>Getting started content...</p>

    <h3>Installation</h3>
    <p>Installation instructions...</p>

    <h3>Configuration</h3>
    <p>Configuration details...</p>

    <h2>Examples</h2>
    <p>Example content...</p>
</c-in_page_nav>
```

### Custom Title and Heading Level

```django
<c-in_page_nav
    title_text="Page contents"
    title_heading_level="h3"
>
    <h1>Documentation</h1>

    <h2>Overview</h2>
    <p>Overview content...</p>

    <h2>API Reference</h2>
    <p>API documentation...</p>

    <h3>Methods</h3>
    <p>Method descriptions...</p>

    <h3>Properties</h3>
    <p>Property descriptions...</p>
</c-in_page_nav>
```

### With Custom Scroll Offset

```django
<c-in_page_nav
    title_text="Table of contents"
    scroll_offset="100"
>
    <h1>User Guide</h1>

    <h2>Chapter 1</h2>
    <p>Chapter content...</p>

    <h2>Chapter 2</h2>
    <p>Chapter content...</p>
</c-in_page_nav>
```

## Usage Notes

- The component automatically generates navigation from h2 and h3 headings in your content
- Headings must have text content to appear in the navigation
- The `scroll_offset` prop is useful when you have a fixed header
- The component requires the USWDS JavaScript to be loaded and initialized
- The navigation will be empty if no h2 headings are found in the content
- Use semantic heading levels (don't skip from h2 to h4)
