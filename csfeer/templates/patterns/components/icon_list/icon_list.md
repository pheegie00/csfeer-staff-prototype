# Icon List

A list component that pairs icons with content, following USWDS patterns. Supports simple text content or rich content with titles and descriptions.

## Props

| Prop            | Default | Description                                              |
| --------------- | ------- | -------------------------------------------------------- |
| `variant`       |         | Style variant: `primary` for primary color icons         |
| `size`          |         | Icon size: `lg` for large icons                          |
| `extra_classes` |         | Additional CSS classes for the list                      |

## Slots

| Slot      | Description       |
| --------- | ----------------- |
| (default) | Icon list items   |

## Sub-components

### `<c-icon_list.item>`

| Prop            | Default | Description                                              |
| --------------- | ------- | -------------------------------------------------------- |
| `icon`          |         | Icon name from USWDS icon sprite                         |
| `icon_color`    |         | Text color class for icon (e.g., `text-green`, `text-red`) |
| `title`         |         | Optional title for rich content                          |
| `title_tag`     | `h4`    | HTML tag for title                                       |
| `content`       |         | Text content for the item                                |
| `extra_classes` |         | Additional CSS classes for the item                      |

**Slot**: Can contain HTML content for complex formatting.

## Example Usage

### Default Icon List

```django
<c-icon_list>
    <c-icon_list.item
        icon="check_circle"
        icon_color="text-green"
        content="Wash your hands for 20 seconds with soap"
    />
    <c-icon_list.item
        icon="check_circle"
        icon_color="text-green"
        content="Stay six feet away from others"
    />
    <c-icon_list.item
        icon="cancel"
        icon_color="text-red"
        content="Avoid large gatherings"
    />
</c-icon_list>
```

### Primary Variant (Simple Content)

```django
<c-icon_list variant="primary">
    <c-icon_list.item icon="thumb_up_alt" content="No processing lines" />
    <c-icon_list.item icon="thumb_up_alt" content="Available at major U.S. airports" />
    <c-icon_list.item icon="thumb_up_alt" content="Reduced wait times" />
</c-icon_list>
```

### Icon List with Rich Content

```django
<c-icon_list>
    <c-icon_list.item
        icon="check_circle"
        icon_color="text-ink"
        title="Donate cash when possible."
        content="Financial contributions to recognized disaster relief organizations are the fastest, most flexible and most effective method of donating."
    />
    <c-icon_list.item
        icon="check_circle"
        icon_color="text-ink"
        title="Confirm what donations are needed."
        content="Unneeded and unsolicited goods burden local organizations' ability to meet survivors' confirmed needs."
    />
</c-icon_list>
```

### Large Icons with Rich Content

```django
<c-icon_list size="lg">
    <c-icon_list.item
        icon="attach_money"
        icon_color="text-green"
        title="Let the sun shine."
    >
        <p>On sunny days, open your curtains to allow the sun to naturally warm the rooms of your home without using electricity. Natural sunlight can also lift your mood to help brighten your day.</p>
    </c-icon_list.item>
    <c-icon_list.item
        icon="attach_money"
        icon_color="text-green"
        title="Adjust your schedule."
    >
        <p>Instead of running high-energy-use appliances during mid-afternoon or early evening hours, operate them early in the morning or late at night.</p>
    </c-icon_list.item>
</c-icon_list>
```

### With HTML Content

```django
<c-icon_list size="lg">
    <c-icon_list.item icon="help" icon_color="text-blue">
        <span class="text-bold">Timing.</span> Is now the right time to start a business?
    </c-icon_list.item>
    <c-icon_list.item icon="help" icon_color="text-blue">
        <span class="text-bold">Funding.</span> Do I have enough money to launch a business?
    </c-icon_list.item>
</c-icon_list>
```

## Usage Notes

- Icons reference the USWDS icon sprite at `/assets/img/sprite.svg`
- Common icon names: `check_circle`, `cancel`, `thumb_up_alt`, `help`, `attach_money`
- Color classes: `text-green`, `text-red`, `text-blue`, `text-ink`, `text-primary`
- Use `variant="primary"` for primary-colored icons
- Use `size="lg"` for larger icons (useful with rich content)
- Content can be plain text (via `content` prop) or HTML (via slot)
