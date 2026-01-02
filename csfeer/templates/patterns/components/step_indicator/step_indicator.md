Example usage:

<c-step-indicator
    indicator_type="centered"
    current_step="3"
    total_steps="5"
    name="Supporting Documents"
>
    <c-step-indicator.step-item 
        segment_state="completed" 
        name="Personal information" 
    />
    <c-step-indicator.step-item 
        segment_state="completed" 
        name="Household status" 
    />
    <c-step-indicator.step-item 
        segment_state="current" 
        name="Supporting documents" 
    />
    <c-step-indicator.step-item 
        segment_state="incomplete" 
        name="Signature" 
    />
    <c-step-indicator.step-item 
        segment_state="incomplete" 
        name="Review and submit" 
    />
</c-step-indicator>