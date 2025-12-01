Example usage:

Must use inside of <c-form-group>

input_type options: single | multiple | specific | wildcard | error

<c-form-group>
    <c-file-input
        input_type="single"
        label="This is a label"
        hint="This is a hint and file types"
        disabled="false"
        accept=".pdf"
        multiple="false"
        error_message=""
    />
</c-form-group>