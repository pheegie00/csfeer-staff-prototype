# Footer Component

A modular footer following USWDS patterns. Supports **big**, **medium**, and **slim** variants.

## Basic Usage

```django
<c-footer type="medium" agency_name="My Agency">
    <c-footer.primary_link href="/about" text="About" />
    <c-footer.primary_link href="/contact" text="Contact" />
</c-footer>
```

## Props

| Prop                 | Default               | Description                          |
|----------------------|-----------------------|--------------------------------------|
| `type`               | `"medium"`            | `"big"`, `"medium"`, or `"slim"`     |
| `return_to_top_href` | `"#"`                 | Return to top link URL (empty hides) |
| `agency_name`        | `""`                  | Agency name in footer                |
| `agency_logo`        | `""`                  | Agency logo image path               |
| `contact_heading`    | `""`                  | Contact section heading              |
| `show_signup`        | `"false"`             | Show signup form (big footer only)   |
| `signup_heading`     | `"Sign up"`           | Signup section heading               |
| `signup_label`       | `"Your email address"`| Email input label                    |

---

## Examples

### Big Footer

```django
<c-footer 
  type="big" 
  agency_name="Agency Name"
  agency_logo="/assets/img/logo-img.png"
  contact_heading="Agency Contact Center"
  show_signup="true"
>
  <c-footer.nav_column title="Topic One">
    <c-footer.secondary_link href="/design" text="Design" />
    <c-footer.secondary_link href="/development" text="Development" />
  </c-footer.nav_column>

  <c-footer.nav_column title="Topic Two">
    <c-footer.secondary_link href="/about" text="About Us" />
    <c-footer.secondary_link href="/careers" text="Careers" />
  </c-footer.nav_column>

  <c-slot name="social_links">
    <c-footer.social_links>
      <c-footer.social_link href="#" icon="facebook" alt="Facebook" />
      <c-footer.social_link href="#" icon="twitter" alt="Twitter" />
    </c-footer.social_links>
  </c-slot>

  <c-slot name="contact_info">
    <c-footer.address>
      <c-footer.contact_item href="tel:1-800-555-1234" text="(800) 555-1234" />
      <c-footer.contact_item href="mailto:info@agency.gov" text="info@agency.gov" />
    </c-footer.address>
  </c-slot>
</c-footer>
```

### Medium Footer

```django
<c-footer type="medium" agency_name="Agency Name" contact_heading="Contact Us">
  <c-footer.primary_link href="/" text="Home" />
  <c-footer.primary_link href="/about" text="About" />
  <c-footer.primary_link href="/contact" text="Contact" />

  <c-slot name="social_links">
    <c-footer.social_links>
      <c-footer.social_link href="#" icon="facebook" alt="Facebook" />
    </c-footer.social_links>
  </c-slot>

  <c-slot name="contact_info">
    <c-footer.address>
      <c-footer.contact_item href="tel:1-800-555-1234" text="(800) 555-1234" />
    </c-footer.address>
  </c-slot>
</c-footer>
```

### Slim Footer

```django
<c-footer type="slim" agency_name="Agency Name">
  <c-footer.slim_link href="/" text="Home" />
  <c-footer.slim_link href="/about" text="About" />

  <c-slot name="contact_info">
    <c-footer.address type="slim">
      <c-footer.contact_item href="tel:1-800-555-1234" text="(800) 555-1234" type="slim" />
    </c-footer.address>
  </c-slot>
</c-footer>
```

---

## Sub-components

### Navigation

| Component                                      | Description                    |
|------------------------------------------------|--------------------------------|
| `<c-footer.nav_column title="">`               | Collapsible column (big)       |
| `<c-footer.secondary_link href="" text="">`    | Link inside nav_column         |
| `<c-footer.primary_link href="" text="">`      | Primary link (medium)          |
| `<c-footer.slim_link href="" text="">`         | Primary link (slim)            |

### Social Links

| Component                                      | Description                    |
|------------------------------------------------|--------------------------------|
| `<c-footer.social_links>`                      | Container for social icons     |
| `<c-footer.social_link href="" icon="" alt="">` | Social media link              |

### Contact

| Component                                      | Description                    |
|------------------------------------------------|--------------------------------|
| `<c-footer.address type="">`                   | Contact info wrapper           |
| `<c-footer.contact_item href="" text="" type="">` | Contact link (phone, email) |

*Note: Pass `type="slim"` to address and contact_item for slim footer styling.*

---

## Slots

| Slot           | Description         |
|----------------|---------------------|
| default        | Navigation links    |
| `social_links` | Social media icons  |
| `contact_info` | Contact information |
