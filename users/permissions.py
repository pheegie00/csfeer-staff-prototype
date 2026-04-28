# This is a map of group name -> specific permissions that will be available
ORG_PERMISSION_GROUPS = {
    "Recipient Form Viewer": ["form_view"],
    "Recipient Form Editor": ["form_view", "form_start", "form_edit"],
    "Recipient Form Approver": ["form_view", "form_start", "form_edit", "form_submit"],
    "Recipient Authorized Official": [
        "form_view",
        "form_start",
        "form_edit",
        "form_submit",
        "form_tribal_plan_can_sign_authorized_official",
    ],
}
