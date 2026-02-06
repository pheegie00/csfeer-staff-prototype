# Pagination

A navigation component for multi-page content, following USWDS patterns. Supports bounded and unbounded pagination.

## Props

| Prop            | Default      | Description                                |
| --------------- | ------------ | ------------------------------------------ |
| `aria_label`    | `Pagination` | ARIA label for the pagination navigation   |
| `extra_classes` |              | Additional CSS classes for the pagination  |

## Slots

| Slot      | Description        |
| --------- | ------------------ |
| (default) | Pagination items   |

## Sub-components

### `<c-pagination.item>`

| Prop            | Default | Description                                                    |
| --------------- | ------- | -------------------------------------------------------------- |
| `type`          | `page`  | Item type: `page`, `previous`, `next`, or `overflow`           |
| `page_number`   |         | Page number to display (for `type="page"`)                     |
| `href`          | `#`     | Link URL                                                       |
| `is_current`    | `false` | Mark as current page (for `type="page"`)                       |
| `aria_label`    |         | ARIA label for the item                                        |
| `extra_classes` |         | Additional CSS classes for the item                            |

**Slot**: Text for previous/next buttons (e.g., "Previous", "Next").

## Example Usage

### Default Pagination (Bounded)

```django
<c-pagination aria_label="Pagination">
    <c-pagination.item
        type="previous"
        href="/page/9"
        aria_label="Previous page"
    >Previous</c-pagination.item>

    <c-pagination.item
        type="page"
        page_number="1"
        href="/page/1"
        aria_label="Page 1"
    />

    <c-pagination.item type="overflow" />

    <c-pagination.item
        type="page"
        page_number="9"
        href="/page/9"
        aria_label="Page 9"
    />

    <c-pagination.item
        type="page"
        page_number="10"
        href="/page/10"
        is_current="true"
        aria_label="Page 10"
    />

    <c-pagination.item
        type="page"
        page_number="11"
        href="/page/11"
        aria_label="Page 11"
    />

    <c-pagination.item type="overflow" />

    <c-pagination.item
        type="page"
        page_number="24"
        href="/page/24"
        aria_label="Last page, page 24"
    />

    <c-pagination.item
        type="next"
        href="/page/11"
        aria_label="Next page"
    >Next</c-pagination.item>
</c-pagination>
```

### Unbounded Pagination

```django
<c-pagination>
    <c-pagination.item
        type="previous"
        href="/page/9"
        aria_label="Previous page"
    >Previous</c-pagination.item>

    <c-pagination.item type="page" page_number="1" href="/page/1" aria_label="Page 1" />
    <c-pagination.item type="overflow" />
    <c-pagination.item type="page" page_number="9" href="/page/9" aria_label="Page 9" />
    <c-pagination.item type="page" page_number="10" href="/page/10" is_current="true" aria_label="Page 10" />
    <c-pagination.item type="page" page_number="11" href="/page/11" aria_label="Page 11" />
    <c-pagination.item type="page" page_number="12" href="/page/12" aria_label="Page 12" />
    <c-pagination.item type="overflow" />

    <c-pagination.item
        type="next"
        href="/page/11"
        aria_label="Next page"
    >Next</c-pagination.item>
</c-pagination>
```

## Usage Notes

- **Bounded pagination**: Shows first and last page numbers with overflow indicators
- **Unbounded pagination**: No last page shown, continues with overflow at the end
- Use `type="overflow"` for ellipsis (...) indicators between page ranges
- Always provide descriptive `aria_label` attributes for accessibility
- The current page should have `is_current="true"` and will receive `aria-current="page"`
- Previous/Next buttons use icons from the USWDS sprite (`navigate_before`, `navigate_next`)
