# This is a map of group name -> specific permissions that will be available

RECIPIENT_FORM_VIEWER = "Recipient Form Viewer"
RECIPIENT_FORM_EDITOR = "Recipient Form Editor"
RECIPIENT_FORM_APPROVER = "Recipient Form Approver"
RECIPIENT_AUTHORIZED_OFFICIAL = "Recipient Authorized Official"

FORM_VIEW = "form_view"
FORM_EDIT = "form_edit"
FORM_START = "form_start"
FORM_SUBMIT = "form_submit"
FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL = "form_tribal_plan_can_sign_authorized_official"


ORG_PERMISSION_GROUPS = {
    RECIPIENT_FORM_VIEWER: [FORM_VIEW],
    RECIPIENT_FORM_EDITOR: [FORM_VIEW, FORM_START, FORM_EDIT],
    RECIPIENT_FORM_APPROVER: [FORM_VIEW, FORM_START, FORM_EDIT, FORM_SUBMIT],
    RECIPIENT_AUTHORIZED_OFFICIAL: [
        FORM_VIEW,
        FORM_START,
        FORM_EDIT,
        FORM_SUBMIT,
        FORM_TRIBAL_PLAN_CAN_SIGN_AUTHORIZED_OFFICIAL,
    ],
}
