# Table

A flexible data table component following USWDS patterns. Supports bordered, borderless, striped, compact, scrollable, stacked, and sticky header variants.

## Props

| Prop            | Default | Description                                          |
| --------------- | ------- | ---------------------------------------------------- |
| `caption`       |         | Table caption text                                   |
| `striped`       |         | Add horizontal stripes to rows                       |
| `borderless`    |         | Remove table borders                                 |
| `compact`       |         | Reduce row padding for denser display                |
| `scrollable`    |         | Wrap table in scrollable container                   |
| `stacked`       |         | Stack cells on mobile screens                        |
| `stacked_header`|         | Stack cells with visible headers on mobile           |
| `sticky_header` |         | Keep header row fixed when scrolling                 |

## Slots

| Slot      | Description                                      |
| --------- | ------------------------------------------------ |
| (default) | Table content (`<thead>`, `<tbody>`, `<tfoot>`)  |

## Example Usage

### Bordered Table

```django
<c-table caption="Document list">
    <thead>
        <tr>
            <th scope="col">Document title</th>
            <th scope="col">Description</th>
            <th scope="col">Year</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Declaration of Independence</th>
            <td>Statement adopted by the Continental Congress.</td>
            <td>1776</td>
        </tr>
        <tr>
            <th scope="row">Bill of Rights</th>
            <td>The first ten amendments of the U.S. Constitution.</td>
            <td>1791</td>
        </tr>
    </tbody>
</c-table>
```

### Striped Table

```django
<c-table caption="Striped table" striped="true">
    <thead>
        <tr>
            <th scope="col">Name</th>
            <th scope="col">Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Item 1</th>
            <td>Value 1</td>
        </tr>
        <tr>
            <th scope="row">Item 2</th>
            <td>Value 2</td>
        </tr>
    </tbody>
</c-table>
```

### Scrollable Table

```django
<c-table caption="Scrollable table" scrollable="true">
    <thead>
        <tr>
            <th scope="col">Column 1</th>
            <th scope="col">Column 2</th>
            <th scope="col">Column 3</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Row 1</th>
            <td>Data</td>
            <td>Data</td>
        </tr>
    </tbody>
</c-table>
```

### Sticky Header Table

```django
<c-table caption="Sticky header table" scrollable="true" sticky_header="true">
    <thead>
        <tr>
            <th scope="col">Name</th>
            <th scope="col">Description</th>
            <th scope="col">Year</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Item 1</th>
            <td>Description text</td>
            <td>2020</td>
        </tr>
        <tr>
            <th scope="row">Item 2</th>
            <td>Description text</td>
            <td>2021</td>
        </tr>
    </tbody>
</c-table>
```

### Compact Borderless Table

```django
<c-table caption="Compact borderless table" compact="true" borderless="true">
    <thead>
        <tr>
            <th scope="col">Name</th>
            <th scope="col">Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Item</th>
            <td>Value</td>
        </tr>
    </tbody>
</c-table>
```
