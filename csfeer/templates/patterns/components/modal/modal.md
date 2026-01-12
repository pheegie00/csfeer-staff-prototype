Example Usage:

<c-modal
    id="modal1"
    href="#example-href"
    button_text="Open Modal"
    body_id="main-body-1"
    heading_id="main-heading-1"
>
    <c-modal.modal-header heading_id="main-heading-1">
        <h2>Are you sure you want to continue?</h2>
    </c-modal.modal-header>
    <c-modal.modal-body>
        <p id="main-body-1">
            You have unsaved changes that will be lost.
        </p>
    </c-modal.modal-body>
    <c-modal.modal-footer>
        <c-button-group>   
            <c-button-group.button-group-item>
                <c-modal.modal-close-button 
                    text="Continue without saving"
                />
            </c-button-group.button-group-item>
            <c-button-group.button-group-item>
                <c-modal.modal-close-button 
                    text="Go back"
                    type="unstyled"
                    extra_classes="padding-105 text-center"
                />
            </c-button-group.button-group-item>
        </c-button-group>
    </c-modal.modal-footer>
</c-modal>