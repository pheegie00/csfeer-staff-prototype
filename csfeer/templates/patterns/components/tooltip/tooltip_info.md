# Tooltip

A tooltip that displays additional information when hovering over or focusing on an element. Follows USWDS patterns.

## Props

| Prop           | Default | Description                                      |
| -------------- | ------- | ------------------------------------------------ |
| `tooltip_text` |         | Text displayed in the tooltip                    |
| `text`         |         | Button text                                      |
| `position`     | `top`   | Tooltip position: `top`, `right`, `bottom`, `left` |
| `data_classes` |         | Utility classes for tooltip styling              |

## Example Usage

### Standard Tooltip

```django
<c-tooltip
    tooltip_text="Helpful information"
    text="Hover me"
    position="top"
/>
```

### Tooltip Positions

```django
<c-tooltip tooltip_text="Top" text="Show on top" position="top" />
<c-tooltip tooltip_text="Right" text="Show on right" position="right" />
<c-tooltip tooltip_text="Bottom" text="Show on bottom" position="bottom" />
<c-tooltip tooltip_text="Left" text="Show on left" position="left" />
```

### Tooltip with Utility Classes

```django
<c-tooltip
    tooltip_text="Custom width tooltip"
    text="Show tooltip"
    position="top"
    data_classes="width-full tablet:width-auto"
/>
```
