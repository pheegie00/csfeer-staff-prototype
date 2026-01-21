# Memorable Date

A memorable date component allows users to enter a date they know well, such as a birthday, using three separate fields for month, day, and year.

## Props

| Prop          | Default                         | Description                                |
| ------------- | ------------------------------- | ------------------------------------------ |
| `id`          |                                 | Base ID for the component fields           |
| `name`        |                                 | Base name for form submission              |
| `legend`      |                                 | Fieldset legend text                       |
| `hint`        | `For example: January 19 2000`  | Hint text shown below the legend           |
| `month_value` |                                 | Pre-selected month value (1-12)            |
| `day_value`   |                                 | Pre-filled day value                       |
| `year_value`  |                                 | Pre-filled year value                      |
| `required`    |                                 | Makes all fields required when set         |
| `disabled`    |                                 | Disables all fields when set               |
| `error`       |                                 | Shows error state on form groups           |

## Example Usage

### Default Memorable Date

```django
<c-memorable_date
    id="date_of_birth"
    name="date_of_birth"
    legend="Date of Birth"
    hint="For example: January 19 2000"
/>
```

### Pre-filled Memorable Date

```django
<c-memorable_date
    id="event_date"
    name="event_date"
    legend="Event Date"
    hint="For example: April 15 2025"
    month_value="4"
    day_value="15"
    year_value="2025"
/>
```

### Required Memorable Date

```django
<c-memorable_date
    id="required_date"
    name="required_date"
    legend="Start Date"
    hint="For example: January 1 2026"
    required="true"
/>
```

### Disabled Memorable Date

```django
<c-memorable_date
    id="disabled_date"
    name="disabled_date"
    legend="End Date"
    hint="For example: December 31 2026"
    month_value="12"
    day_value="31"
    year_value="2026"
    disabled="true"
/>
```

### Error State Memorable Date

```django
<c-memorable_date
    id="error_date"
    name="error_date"
    legend="Expiration Date"
    hint="For example: June 30 2024"
    error="true"
/>
```
