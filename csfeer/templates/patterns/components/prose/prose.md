# Prose

A container that applies USWDS typography styling to nested content. Use for long-form text content like articles, documentation, and body copy.

## Props

| Prop           | Default | Description                              |
| -------------- | ------- | ---------------------------------------- |
| `extra_classes`|         | Additional CSS classes (e.g., `measure-3`) |

## Slots

| Slot      | Description                                           |
| --------- | ----------------------------------------------------- |
| (default) | Content to style (headings, paragraphs, lists, tables) |

## Example Usage

### Basic Prose

```django
<c-prose>
    <h1>Page heading</h1>
    <p class="usa-intro">Introduction paragraph with larger text.</p>
    <h2>Section heading</h2>
    <p>Body text with proper typography styling applied automatically.</p>
</c-prose>
```

### Prose with Lists

```django
<c-prose>
    <h2>Features</h2>
    <ul>
        <li>Unordered list item</li>
        <li>Unordered list item</li>
        <li>Nested list
            <ul>
                <li>Nested item</li>
                <li>Nested item</li>
            </ul>
        </li>
    </ul>
    <ol>
        <li>Ordered list item</li>
        <li>Ordered list item</li>
    </ol>
</c-prose>
```

### Prose with Measure Constraint

```django
<c-prose extra_classes="measure-4">
    <h2>Constrained line length</h2>
    <p>This prose block uses the measure-4 utility class to constrain the line length for better readability.</p>
</c-prose>
```

### Prose with Table

```django
<c-prose>
    <table>
        <caption>Document list</caption>
        <thead>
            <tr>
                <th scope="col">Title</th>
                <th scope="col">Year</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th scope="row">Declaration of Independence</th>
                <td>1776</td>
            </tr>
            <tr>
                <th scope="row">Bill of Rights</th>
                <td>1791</td>
            </tr>
        </tbody>
    </table>
</c-prose>
```
