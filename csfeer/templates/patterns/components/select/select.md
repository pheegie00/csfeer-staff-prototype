### Usage:

<c-select :options="[{'display': 'Option 1', 'value': 'option1'}, {'display': 'Option 2', 'value': 'option2'}, {'display': 'Option 3', 'value': 'option3'}]"
    id="select_1"
    name="Select One"
    disabled=""
    required=""
/>

<!-- With Default Options -->
<c-select :options="[{'display': 'Option 1', 'value': 'option1'}, {'display': 'Option 2', 'value': 'option2'}, {'display': 'Option 3', 'value': 'option3'}]"
    id="select_1"
    name="Select One"
    default_option="Default Option"
    default_value="default1"
    disabled=""
    required=""
/>
