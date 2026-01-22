# Site Alert

A site alert communicates urgent sitewide information. It wraps the `c-alert` component inside a `<section>` element.

## Props

| Prop         | Default       | Description                                              |
| ------------ | ------------- | -------------------------------------------------------- |
| `type`       | `info`        | Alert type: `info` or `emergency`                        |
| `heading`    |               | Optional heading text (adds `--no-heading` class if empty)|
| `aria_label` | `Site alert`  | Accessible label for the section                         |
| `slim`       |               | Enable slim variant when set                             |
| `no_icon`    |               | Hide the icon when set                                   |

## Example Usage

### Standard Informational Site Alert

```django
<c-site_alert type="info" heading="Short alert message">
    Additional context and followup information including
    <a class="usa-link" href="#">a link</a>.
</c-site_alert>
```

### Standard Emergency Site Alert

```django
<c-site_alert type="emergency" heading="Emergency alert message">
    Additional context and followup information including
    <a class="usa-link" href="#">a link</a>.
</c-site_alert>
```

### Site Alert with No Header

```django
<c-site_alert type="emergency">
    <strong>Short alert message.</strong> Additional context and followup
    information including <a class="usa-link" href="#">a link</a>.
</c-site_alert>
```

### Site Alert with List

```django
<c-site_alert type="emergency" heading="Emergency alert message">
    <c-list>
        <li>The primary emergency message and <a class="usa-link" href="#">a link</a> for supporting context.</li>
        <li>Another message, <a class="usa-link" href="#">and another link</a>.</li>
        <li>A final emergency message.</li>
    </c-list>
</c-site_alert>
```

### Slim Site Alert

```django
<c-site_alert type="emergency" slim="true">
    <strong>Short alert message.</strong> Additional context and followup
    information including <a class="usa-link" href="#">a link</a>.
</c-site_alert>
```

### Site Alert with No Icon

```django
<c-site_alert type="emergency" no_icon="true">
    <strong>Short alert message.</strong> Additional context and followup
    information including <a class="usa-link" href="#">a link</a>.
</c-site_alert>
```
