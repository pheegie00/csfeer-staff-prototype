# Range Slider

A form input component for selecting a numeric value from a range using a slider, following USWDS patterns. Uses the c-form, c-label, and c-error-message components for consistent styling.

## Props

| Prop            | Default | Description                                          |
| --------------- | ------- | ---------------------------------------------------- |
| `label`         |         | Label text for the slider                            |
| `hint`          |         | Optional hint text displayed below the label         |
| `error`         |         | Error message to display                             |
| `required`      |         | Set to `"true"` to mark the field as required        |
| `disabled`      |         | Set to `"true"` to disable the input                 |
| `readonly`      |         | Set to `"true"` to make the input readonly           |
| `extra_classes` |         | Additional CSS classes for the form                  |

**Note:** All other input attributes (`id`, `name`, `min`, `max`, `step`, `value`, etc.) are passed through the `{{ attrs }}` mechanism. Simply add them as attributes to the component.

## Example Usage

### Basic Range Slider

```django
<c-range_slider
    label="Volume"
    id="volume"
    name="volume"
    min="0"
    max="100"
    step="1"
    value="50"
/>
```

### Range Slider with Hint

```django
<c-range_slider
    label="Temperature (°F)"
    hint="Select your preferred temperature"
    id="temperature"
    name="temperature"
    min="60"
    max="80"
    value="72"
/>
```

### Range Slider with Custom Steps

```django
<c-range_slider
    label="Volume level"
    hint="Adjusts in increments of 10"
    id="volume"
    name="volume"
    min="0"
    max="100"
    step="10"
    value="50"
/>
```

### Required Range Slider

```django
<c-range_slider
    label="Priority level"
    required="true"
    id="priority"
    name="priority"
    min="1"
    max="5"
    value="3"
/>
```

### Range Slider with Error

```django
<c-range_slider
    label="Age"
    error="This field is required"
    id="age"
    name="age"
    min="0"
    max="120"
/>
```

### Disabled Range Slider

```django
<c-range_slider
    label="Disabled range slider"
    hint="This slider is disabled"
    disabled="true"
    id="range-disabled"
    name="disabled"
    min="0"
    max="100"
    value="60"
/>
```

### Readonly Range Slider

```django
<c-range_slider
    label="Readonly range slider"
    hint="This slider is readonly"
    readonly="true"
    id="range-readonly"
    name="readonly"
    min="0"
    max="100"
    value="75"
/>
```

## Usage Notes

- Always provide a descriptive `label` for accessibility
- Use `hint` text to provide additional guidance on acceptable values
- The `disabled`, `readonly`, and `required` attributes are handled directly by the component via c-vars
- All other HTML input attributes (`id`, `name`, `min`, `max`, `step`, `value`, etc.) are passed directly to the input via `{{ attrs }}`
- The component uses the `c-form`, `c-label`, and `c-error-message` components internally for consistent styling
- Error messages are properly associated with the input via `aria-describedby`
- The component automatically wraps content in a `<form class="usa-form">` element
