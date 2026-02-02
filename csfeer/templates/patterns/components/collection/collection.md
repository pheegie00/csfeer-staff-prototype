# Collection

A flexible collection component following USWDS patterns for displaying lists of content with various metadata, images, or calendar displays.

## Props

| Prop            | Default | Description                                    |
| --------------- | ------- | ---------------------------------------------- |
| `condensed`     | `false` | Enable condensed layout (headings only style)  |
| `extra_classes` |         | Additional CSS classes for the collection      |

## Slots

| Slot      | Description       |
| --------- | ----------------- |
| (default) | Collection items  |

## Sub-components

### `<c-collection.item>`

| Prop              | Default | Description                                    |
| ----------------- | ------- | ---------------------------------------------- |
| `heading`         |         | Item heading text                              |
| `heading_tag`     | `h4`    | HTML tag for heading                           |
| `heading_classes` |         | Additional CSS classes for heading             |
| `link_url`        |         | URL for the heading link                       |
| `description`     |         | Item description text                          |
| `img_src`         |         | Image source URL (for media thumbnail variant) |
| `img_alt`         |         | Image alt text                                 |
| `calendar_date`   |         | ISO datetime for calendar display              |
| `calendar_month`  |         | Month abbreviation (e.g., "SEP")               |
| `calendar_day`    |         | Day number for calendar display                |
| `extra_classes`   |         | Additional CSS classes for the item            |

### `<c-collection.meta>`

Wrapper for metadata information (authors, dates, sources).

| Prop            | Default            | Description                              |
| --------------- | ------------------ | ---------------------------------------- |
| `aria_label`    | `More information` | ARIA label for the meta list             |
| `extra_classes` |                    | Additional CSS classes for the meta list |

### `<c-collection.meta_item>`

Individual metadata item (author, date, or tag).

| Prop            | Default | Description                              |
| --------------- | ------- | ---------------------------------------- |
| `extra_classes` |         | Additional CSS classes for the meta item |
| `is_tag`        | `false` | Style as a tag badge                     |
| `tag_new`       | `false` | Add "new" styling to tag                 |

## Example Usage

### Default Collection

```django
<c-collection>
    <c-collection.item
        heading="Gears of Government President's Award winners"
        link_url="https://example.gov/article"
        description="Today, the Administration announces the winners of the Gears of Government President's Award."
    >
        <c-collection.meta>
            <c-collection.meta_item>By Sondra Ainsworth</c-collection.meta_item>
            <c-collection.meta_item>
                <time datetime="2020-09-30T12:00:00+01:00">September 30, 2020</time>
            </c-collection.meta_item>
        </c-collection.meta>
        <c-collection.meta aria_label="Topics">
            <c-collection.meta_item is_tag tag_new>New</c-collection.meta_item>
            <c-collection.meta_item is_tag>PMA</c-collection.meta_item>
            <c-collection.meta_item is_tag>OMB</c-collection.meta_item>
        </c-collection.meta>
    </c-collection.item>
</c-collection>
```

### Collection with Media Thumbnail

```django
<c-collection>
    <c-collection.item
        heading="Women-owned small business dashboard"
        link_url="https://example.gov/article"
        description="In honor of National Women's Small Business Month..."
        img_src="https://example.gov/img/wosb.jpg"
        img_alt="Woman Owned Small Business"
    >
        <c-collection.meta>
            <c-collection.meta_item>By Constance Lu</c-collection.meta_item>
            <c-collection.meta_item>
                <time datetime="2020-09-30T12:00:00+01:00">September 30, 2020</time>
            </c-collection.meta_item>
        </c-collection.meta>
        <c-collection.meta aria_label="Topics">
            <c-collection.meta_item is_tag>SBA</c-collection.meta_item>
        </c-collection.meta>
    </c-collection.item>
</c-collection>
```

### Collection with Calendar Date

```django
<c-collection>
    <c-collection.item
        heading="September 2020 updates show progress"
        link_url="https://example.gov/article"
        description="Progress updates for both Cross-Agency Priority (CAP) Goals..."
        calendar_date="2020-09-17T12:00:00+01:00"
        calendar_month="SEP"
        calendar_day="17"
    />
</c-collection>
```

### Condensed Collection (Headings Only)

```django
<c-collection condensed>
    <c-collection.item
        heading="The eight principles of mobile-friendliness"
        link_url="https://digital.gov/guides/mobile-principles/"
    >
        <c-collection.meta>
            <c-collection.meta_item extra_classes="position-relative">
                <c-icon name="public" extra_classes="position-relative bottom-neg-2px" />
                Digital.gov
            </c-collection.meta_item>
        </c-collection.meta>
    </c-collection.item>

    <c-collection.item
        heading="The USWDS maturity model"
        link_url="https://designsystem.digital.gov/maturity-model/"
    >
        <c-collection.meta>
            <c-collection.meta_item extra_classes="position-relative">
                <c-icon name="public" extra_classes="position-relative bottom-neg-2px" />
                U.S. Web Design System
            </c-collection.meta_item>
        </c-collection.meta>
    </c-collection.item>
</c-collection>
```
