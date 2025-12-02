Example usage:
<!-- The button gives all the state by default, but you can explicitly set if needed for visual purposes -->
state options: "" | hover | active | focus | disabled | aria-disabled
variant options: "" | secondary | accent-warm | accent-cool | base | outline | outline-inverse | big

<c-button 
    text="Default" 
/>

<c-button 
    text="Default"
    variant="accent-cool"
/>

<c-button 
    text="Disabled" 
    disabled="true" 
/>