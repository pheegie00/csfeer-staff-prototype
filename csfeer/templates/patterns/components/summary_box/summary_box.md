# Summary Box

A summary box draws attention to important content on a page.

## Props

| Prop            | Default | Description                                  |
| --------------- | ------- | -------------------------------------------- |
| `heading`       |         | The heading text for the summary box         |
| `heading_level` | `h4`    | The HTML heading element (h1-h6)             |
| `id`            |         | Custom ID for aria-labelledby (auto-generated from heading if not provided) |

## Slots

| Slot      | Description                                      |
| --------- | ------------------------------------------------ |
| (default) | The body content of the summary box              |

## Sub-components

### `<c-summary_box.link>`

A styled link for use within a summary box.

| Prop   | Default | Description           |
| ------ | ------- | --------------------- |
| `href` |         | The URL for the link  |

## Example Usage

### Summary Box with List

```django
<c-summary_box heading="Key information">
    <ul class="usa-list">
        <li>
            If you are under a winter storm warning,
            <c-summary_box.link href="#">find shelter</c-summary_box.link>
            right away.
        </li>
        <li>
            Sign up for
            <c-summary_box.link href="#">your community's warning system</c-summary_box.link>.
        </li>
    </ul>
</c-summary_box>
```

### With Custom Heading Level

```django
<c-summary_box heading="Section Summary" heading_level="h2">
    <ul class="usa-list">
        <li>
            If you are under a winter storm warning,
            <c-summary_box.link href="#">find shelter</c-summary_box.link>
            right away.
        </li>
    </ul>
</c-summary_box>
```