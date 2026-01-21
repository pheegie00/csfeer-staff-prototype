# Process List

A process list displays a series of steps or stages in a process, helping users understand what to expect.

## Props

### `<c-process_list>`

The main wrapper component. No props required.

### `<c-process_list.item>`

| Prop              | Default | Description                                                      |
| ----------------- | ------- | ---------------------------------------------------------------- |
| `heading`         |         | The heading text for the step                                    |
| `heading_tag`     | `h4`    | HTML tag for heading (`h4`, `p`, etc.)                           |
| `heading_classes` |         | Additional CSS classes for the heading (e.g., `font-sans-xl`)    |
| `extra_classes`   |         | Additional CSS classes for the list item (e.g., `padding-bottom-4`) |

## Example Usage

### Default Process List

```django
<c-process_list>
    <c-process_list.item heading="Start a process">
        <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</p>
        <ul>
            <li>First sub-item</li>
            <li>Second sub-item</li>
        </ul>
    </c-process_list.item>
    <c-process_list.item heading="Proceed to the second step">
        <p>More description text here.</p>
    </c-process_list.item>
    <c-process_list.item heading="Complete the step-by-step process">
        <p>Final step description.</p>
    </c-process_list.item>
</c-process_list>
```

### Custom Sizing (No Body Text)

```django
<c-process_list>
    <c-process_list.item 
        heading="Start a process." 
        heading_tag="p" 
        extra_classes="padding-bottom-4"
    />
    <c-process_list.item 
        heading="Proceed to the second step." 
        heading_tag="p" 
        extra_classes="padding-bottom-4"
    />
    <c-process_list.item 
        heading="Complete the step-by-step process." 
        heading_tag="p"
    />
</c-process_list>
```

### Custom Sizing (With Body Text)

```django
<c-process_list>
    <c-process_list.item 
        heading="Start a process."
        heading_classes="font-sans-xl line-height-sans-1"
        extra_classes="padding-bottom-4"
    >
        <p class="font-sans-lg margin-top-1 text-light">
            Nullam sit amet enim. Suspendisse id velit vitae ligula volutpat condimentum.
        </p>
    </c-process_list.item>
    <c-process_list.item 
        heading="Proceed to the second step."
        heading_classes="font-sans-xl line-height-sans-1"
        extra_classes="padding-bottom-4"
    >
        <p class="font-sans-lg margin-top-1 text-light">
            Suspendisse id velit vitae ligula volutpat condimentum. Aliquam erat volutpat.
        </p>
    </c-process_list.item>
    <c-process_list.item 
        heading="Complete the step-by-step process."
        heading_classes="font-sans-xl line-height-sans-1"
    >
        <p class="font-sans-lg margin-top-1 text-light">
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        </p>
    </c-process_list.item>
</c-process_list>
```
