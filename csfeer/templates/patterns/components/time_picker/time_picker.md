# Time Picker

A time picker input component that allows users to select times from a dropdown or type directly into the input field. Uses the c-form, c-label, and c-error-message components. Follows USWDS time picker patterns.

## Props

| Prop            | Default | Description                                      |
| --------------- | ------- | ------------------------------------------------ |
| `disabled`      |         | Set to `"true"` to disable the input            |
| `required`      |         | Set to `"true"` to mark the field as required   |
| `extra_classes` |         | Additional CSS classes to apply to the wrapper  |

All other input attributes (such as `id`, `name`, `aria-describedby`, `value`, etc.) are passed through the `{{ attrs }}` mechanism.

## Example Usage

### Basic Time Picker

```django
<c-form>
    <c-label
        id="appointment-time"
        label="Appointment time"
    />

    <c-time_picker
        id="appointment-time"
        name="appointment-time"
    />
</c-form>
```

### Time Picker with Hint

```django
<c-form>
    <c-label
        id="appointment-time-hint"
        label="Appointment time"
        hint="Select a time from the dropdown. Type into the input to filter options."
    />

    <c-time_picker
        id="appointment-time-hint"
        name="appointment-time-hint"
    />
</c-form>
```

### Required Time Picker

```django
<c-form>
    <c-label
        id="appointment-time-required"
        label="Appointment time"
        hint="This field is required"
        required="true"
    />

    <c-time_picker
        id="appointment-time-required"
        name="appointment-time-required"
        required="true"
    />
</c-form>
```

### Time Picker with Error

```django
<c-form>
    <c-label
        id="appointment-time-error"
        label="Appointment time"
        hint="Select a time from the dropdown"
        error="Please select a valid time"
    />

    <c-error-message
        id="appointment-time-error"
        error="Please select a valid time"
    />

    <c-time_picker
        id="appointment-time-error"
        name="appointment-time-error"
    />
</c-form>
```

### Disabled Time Picker

```django
<c-form>
    <c-label
        id="appointment-time-disabled"
        label="Appointment time"
        hint="This time picker is disabled"
    />

    <c-time_picker
        id="appointment-time-disabled"
        name="appointment-time-disabled"
        disabled="true"
    />
</c-form>
```

## Usage Notes

- The time picker must be wrapped in a c-form component to maintain proper form structure
- Use c-label component for labels, hints, and required markers
- Use c-error-message component to display error messages
- The `disabled` and `required` props are handled via c-vars and should be set to `"true"` (as strings) when needed
- All other HTML attributes can be passed directly to the input element via `{{ attrs }}`
- The time picker uses JavaScript to provide an interactive dropdown with time options
- Users can either select a time from the dropdown or type directly into the input
