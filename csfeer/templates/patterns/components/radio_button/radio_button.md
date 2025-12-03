Example usage:

* Use inside of <c-fieldset></c-fieldset>

radio_type options: "" | "tile"

<c-fieldset legend="Radio Btn Group Name" required="true">
    <c-radio-button
        id="random_id"
        label="This is a label"
        label_description="Sub-text description for label"
        radio_type=""
        name="radio_btn_grp_1"
        value="Option 1"
        checked="false"
    />
</c-fieldset>