# Tag

A simple label component used to draw attention to new, important, or categorized content. Follows USWDS tag patterns.

## Props

| Prop            | Default | Description                                      |
| --------------- | ------- | ------------------------------------------------ |
| `variant`       |         | Tag size variant: leave empty for default or use `big` for larger size |
| `extra_classes` |         | Additional CSS classes to apply to the tag      |

All other attributes (such as `id`, `data-*`, `aria-*`, etc.) are passed through the `{{ attrs }}` mechanism.

## Example Usage

### Default Tag

```django
<c-tag>
    Info
</c-tag>
```

### Big Tag

```django
<c-tag variant="big">
    Big
</c-tag>
```

### Tag with Additional Attributes

```django
<c-tag id="status-tag" data-status="active">
    Active
</c-tag>
```

### Tag with Extra Classes

```django
<c-tag extra_classes="margin-2">
    Custom
</c-tag>
```

## Usage Notes

- Tag content is passed as the slot content (text between the opening and closing tags)
- The `variant` prop accepts `"big"` for a larger tag size
- Use tags to highlight important information or status indicators
- All HTML attributes can be passed directly to the tag element via `{{ attrs }}`
