# Side Navigation

A hierarchical, vertical navigation component following USWDS patterns. Supports up to three levels of navigation depth.

## Props

| Prop            | Default            | Description                              |
| --------------- | ------------------ | ---------------------------------------- |
| `aria_label`    | `Side navigation`  | ARIA label for the navigation element    |
| `extra_classes` |                    | Additional CSS classes for the sidenav   |

## Slots

| Slot      | Description       |
| --------- | ----------------- |
| (default) | Navigation items  |

## Sub-components

### `<c-side_nav.item>`

| Prop            | Default | Description                                     |
| --------------- | ------- | ----------------------------------------------- |
| `text`          |         | Link text                                       |
| `href`          |         | Link URL                                        |
| `is_current`    | `false` | Mark as current page                            |
| `extra_classes` |         | Additional CSS classes for the item             |

**Slot**: Can contain child `<c-side_nav.item>` elements to create nested navigation (sublists).

## Example Usage

### Basic Side Navigation

```django
<c-side_nav>
    <c-side_nav.item text="Current page" href="#" is_current="true" />
    <c-side_nav.item text="Parent link" href="#" />
    <c-side_nav.item text="Parent link" href="#" />
</c-side_nav>
```

### Side Navigation with Children

```django
<c-side_nav aria_label="Main navigation">
    <c-side_nav.item text="Parent link" href="#" />
    <c-side_nav.item text="Current page" href="#" is_current="true">
        <c-side_nav.item text="Child link" href="#" />
        <c-side_nav.item text="Child link" href="#" />
        <c-side_nav.item text="Child link (current)" href="#" is_current="true" />
    </c-side_nav.item>
    <c-side_nav.item text="Parent link" href="#" />
</c-side_nav>
```

### Side Navigation with Grandchildren

```django
<c-side_nav>
    <c-side_nav.item text="Parent link" href="#" />
    <c-side_nav.item text="Current page" href="#" is_current="true">
        <c-side_nav.item text="Child link" href="#" />
        <c-side_nav.item text="Child link" href="#">
            <c-side_nav.item text="Grandchild link" href="#" />
            <c-side_nav.item text="Grandchild link (current)" href="#" is_current="true" />
            <c-side_nav.item text="Grandchild link" href="#" />
        </c-side_nav.item>
        <c-side_nav.item text="Child link" href="#" />
    </c-side_nav.item>
    <c-side_nav.item text="Parent link" href="#" />
</c-side_nav>
```

## Usage Notes

- The `is_current` prop adds the `usa-current` class to indicate the current page
- Nested items automatically create sublists with the `usa-sidenav__sublist` class
- USWDS supports up to three levels of nesting (parent, child, grandchild)
- Only the active navigation path should be expanded to show children
