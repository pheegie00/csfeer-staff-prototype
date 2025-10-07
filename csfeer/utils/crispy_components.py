from crispy_forms.layout import Button  # type: ignore


class USWDSSubmit(Button):
    """
    Base USWDS button submit component.
    Add classes like `usa-button--primary`, `usa-button--secondary`, or
    `usa-button--outline` for specific design cases
    """

    input_type = "submit"
    template = "uswds/layout/basebutton.html"
    field_classes = "margin-top-2"


class PrimarySubmit(USWDSSubmit):
    """Primary submit button with usa-button--primary styling"""

    field_classes = "usa-button--primary margin-top-2"


class SecondarySubmit(USWDSSubmit):
    """Secondary submit button with usa-button--secondary styling"""

    field_classes = "usa-button--secondary margin-top-2"


class OutlineSubmit(USWDSSubmit):
    """Outline submit button with usa-button--outline styling"""

    field_classes = "usa-button--outline margin-top-2"
