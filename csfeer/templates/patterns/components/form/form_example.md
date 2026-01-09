Example usage:


    <c-form action="/submit">

        <fieldset class="usa-fieldset">

            <legend class="usa-legend usa-legend--large">Your Information</legend>

            <c-form-group>
                <c-label 
                    id="first-name" 
                    label="First Name" 
                    required="true"
                />

                <c-text-input
                    id="first-name-input"
                    name="first-name"
                    type="text"
                    required="true"
                    type="text"
                />
            </c-form-group>

            <c-form-group>
                <c-label 
                    id="last-name" 
                    label="Last Name" 
                    required="true"
                />

                <c-text-input
                    id="last-name-input"
                    name="last-name"
                    type="text"
                    required="true"
                    type="text"
                />
            </c-form-group>

            <c-button>Submit</c-button>


        </fieldset>

    </c-form>