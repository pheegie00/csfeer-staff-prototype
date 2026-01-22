# Identifier

A federal agency identifier that communicates a site's parent agency and displays required agency links following USWDS patterns.

## Props

| Prop                  | Default                                              | Description                        |
| --------------------- | ---------------------------------------------------- | ---------------------------------- |
| `domain`              |                                                      | Agency domain (e.g., "agency.gov") |
| `disclaimer`          |                                                      | Agency disclaimer HTML content     |
| `masthead_aria_label` | `Agency identifier`                                  | ARIA label for masthead section    |
| `identity_aria_label` | `Agency description`                                 | ARIA label for identity section    |
| `links_aria_label`    | `Important links`                                    | ARIA label for required links      |
| `usagov_aria_label`   | `U.S. government information and services`           | ARIA label for USA.gov section     |
| `usagov_text`         | `Looking for U.S. government information and services?` | USA.gov section text            |
| `usagov_link_text`    | `Visit USA.gov`                                      | USA.gov link text                  |
| `usagov_link_href`    | `https://www.usa.gov/`                               | USA.gov link URL                   |

## Slots

| Slot      | Description                                    |
| --------- | ---------------------------------------------- |
| (default) | Required links (`<c-identifier.link>`)         |
| `logos`   | Agency logos (`<c-identifier.logo>`)           |

## Sub-components

### `<c-identifier.logo>`

| Prop   | Default | Description                          |
| ------ | ------- | ------------------------------------ |
| `href` |         | Logo link URL                        |
| `icon` |         | USWDS icon name (e.g., "flag")       |
| `alt`  |         | Image alt text                       |

### `<c-identifier.link>`

| Prop   | Default | Description |
| ------ | ------- | ----------- |
| `href` |         | Link URL    |
| `text` |         | Link text   |

## Example Usage

### Default Identifier

```django
<c-identifier
    domain="agency.gov"
    disclaimer='<span aria-hidden="true">An </span>official website of the <a href="#">Parent Agency</a>'
>
    <c-slot name="logos">
        <c-identifier.logo href="#" icon="flag" alt="Parent agency logo" />
    </c-slot>

    <c-identifier.link href="#" text="About Parent Agency" />
    <c-identifier.link href="#" text="Accessibility statement" />
    <c-identifier.link href="#" text="FOIA requests" />
    <c-identifier.link href="#" text="No FEAR Act data" />
    <c-identifier.link href="#" text="Office of the Inspector General" />
    <c-identifier.link href="#" text="Performance reports" />
    <c-identifier.link href="#" text="Privacy policy" />
</c-identifier>
```

### Multiple Logos

```django
<c-identifier
    domain="agency.gov"
    disclaimer='<span aria-hidden="true">An </span>official website of <a href="#">Agency One</a> and <a href="#">Agency Two</a>'
>
    <c-slot name="logos">
        <c-identifier.logo href="#" icon="flag" alt="Agency One logo" />
        <c-identifier.logo href="#" icon="flag" alt="Agency Two logo" />
    </c-slot>

    <c-identifier.link href="#" text="About the agencies" />
    <c-identifier.link href="#" text="Accessibility statement" />
</c-identifier>
```

### No Logos

```django
<c-identifier
    domain="agency.gov"
    disclaimer='<span aria-hidden="true">An </span>official website of the <a href="#">Parent Agency</a>'
>
    <c-identifier.link href="#" text="About Parent Agency" />
    <c-identifier.link href="#" text="Accessibility statement" />
    <c-identifier.link href="#" text="FOIA requests" />
</c-identifier>
```

### Taxpayer Disclaimer

```django
<c-identifier
    domain="agency.gov"
    disclaimer='<span aria-hidden="true">An </span>official website of the <a href="#">Parent Agency</a>. Produced and published at taxpayer expense.'
>
    <c-slot name="logos">
        <c-identifier.logo href="#" icon="flag" alt="Parent agency logo" />
    </c-slot>

    <c-identifier.link href="#" text="About Parent Agency" />
    <c-identifier.link href="#" text="Accessibility statement" />
</c-identifier>
```
