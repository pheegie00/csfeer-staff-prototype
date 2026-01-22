# Date Range Picker

A date range picker helps users select a start and end date. Uses the `<c-label>` and `<c-date-picker>` sub-components internally.

## Props

| Prop               | Default | Description                                      |
| ------------------ | ------- | ------------------------------------------------ |
| `start_date_id`    |         | ID for the start date input                      |
| `start_date_name`  |         | Name attribute for the start date input          |
| `start_date_label` |         | Label text for the start date field              |
| `start_date_hint`  |         | Hint text for the start date (e.g., "mm/dd/yyyy")|
| `end_date_id`      |         | ID for the end date input                        |
| `end_date_name`    |         | Name attribute for the end date input            |
| `end_date_label`   |         | Label text for the end date field                |
| `end_date_hint`    |         | Hint text for the end date (e.g., "mm/dd/yyyy")  |
| `required`         |         | Makes both date fields required when set         |
| `disabled`         |         | Disables both date fields when set               |

## Example Usage

### Default Date Range Picker

```django
<c-date-range-picker
    start_date_id="event-date-start"
    start_date_name="event-date-start"
    start_date_label="Event start date"
    start_date_hint="mm/dd/yyyy"
    end_date_id="event-date-end"
    end_date_name="event-date-end"
    end_date_label="Event end date"
    end_date_hint="mm/dd/yyyy"
/>
```

### Disabled Date Range Picker

```django
<c-date-range-picker
    start_date_id="disabled-date-start"
    start_date_name="disabled-date-start"
    start_date_label="Start date"
    start_date_hint="mm/dd/yyyy"
    end_date_id="disabled-date-end"
    end_date_name="disabled-date-end"
    end_date_label="End date"
    end_date_hint="mm/dd/yyyy"
    disabled="true"
/>
