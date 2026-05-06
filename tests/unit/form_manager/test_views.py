import uuid
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from form_manager.models import FormDefinition, FormEntry
from form_manager.schema.layout import PageBlock, StepBlock, AlertBoxBlock
from form_manager.schema.navigation import build_form_edit_url
from form_manager.views.form_edit import _build_post_save_redirect
from users.signals import create_permission_groups
from users.permissions import RECIPIENT_AUTHORIZED_OFFICIAL

if TYPE_CHECKING:
    from django.test.client import Client
    from users.models import CoreUser


@pytest.mark.django_db
def test_can_start_new_form(django_db_setup, seed_data, authenticated_client_with_user):
    """Ensure the load_initial_forms command loads successfully."""

    client, user = authenticated_client_with_user

    form = FormDefinition.objects.all().first()

    assert form

    url = reverse("form_start", args=[form.pk])

    response = client.get(url)

    assert response.status_code == 302

    assert FormEntry.objects.count() == 1

    obj = FormEntry.objects.first()

    assert obj

    assert response.headers.get("Location", "") == reverse("form_edit", args=[obj.pk])


@pytest.mark.django_db
def test_can_render_and_edit_form(django_db_setup, form_entry: "FormEntry", authenticated_client):
    """Ensure the load_initial_forms command loads successfully."""

    url = build_form_edit_url(form_entry.pk, step_number=0, page_number=0)

    response = authenticated_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_form_edit_redirects_to_canonical_first_page_when_query_params_missing(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    url = reverse("form_edit", args=[form_entry.pk])

    response = authenticated_client.get(url)

    assert response.status_code == 302
    assert response.headers.get("Location") == build_form_edit_url(
        form_entry.pk, step_number=0, page_number=0
    )


@pytest.mark.django_db
def test_can_correctly_filter_fields(
    django_db_setup, form_entry: "FormEntry", authenticated_client_with_user
):
    """Ensure the load_initial_forms command loads successfully and test Next button behavior."""

    url = build_form_edit_url(form_entry.pk, step_number=0, page_number=0)

    client, user = authenticated_client_with_user

    # Make a GET request to the form's first page
    response = client.get(url)

    # It should be a 200 response
    assert response.status_code == 200

    # Now post some data for the first page (without page-action=save-exit, simulating Next button)
    response = client.post(
        url,
        data={
            "first_name": "Steven",
            "last_name": "Jones",
        },
        query_params={
            "step": 1,
            "page": 0,
        },
    )

    # It should be a 200 response (stays on form edit page, not redirected)
    assert response.status_code == 200

    # The data should have been saved
    form_entry.refresh_from_db()
    assert form_entry.data.get("first_name") == "Steven"
    assert form_entry.data.get("last_name") == "Jones"

    # Make a post request to choose the applicable fields
    response = client.post(
        url,
        data={
            "applicable_topics": ["item1_cost", "item2_cost"],
        },
        query_params={
            "step": 1,
            "page": 1,
        },
    )

    # It should be a 200 response
    assert response.status_code == 200

    # there should be a field for item 1 and item 2 in the response
    assert "item1_cost" in response.content.decode("utf-8")
    assert "item2_cost" in response.content.decode("utf-8")

    # but the item 3 field should not be in the response
    assert "item3_cost" not in response.content.decode("utf-8")


@pytest.mark.django_db
def test_back_button_not_shown_on_first_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that the back button and Save & Exit button are not displayed on
    the first page (step=0, page=0). This regression test ensures that
    current_step_number and current_page_number are correctly passed to
    the page template context.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Request the first page explicitly
    response = authenticated_client.get(url, {"step": 0, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    # Verify the back button link is not in the response
    assert "← Back" not in content

    # Verify that current_step_number and current_page_number are in the context
    assert response.context["current_step_number"] == 0
    assert response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_back_button_shown_on_second_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that the back button and Save & Exit button are displayed when not on the first page.
    This verifies both buttons appear for step > 0 or page > 0.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Request the second page
    response = authenticated_client.get(url, {"step": 1, "page": 0})

    assert response.status_code == 200

    content = response.content.decode("utf-8")

    # Verify the back button link IS in the response
    assert "← Back" in content

    # Verify the "Save & Exit" button IS in the response
    assert "Save &amp; Exit" in content or "Save & Exit" in content
    assert 'value="save-exit"' in content

    # Verify that current_step_number and current_page_number are in the context
    assert response.context["current_step_number"] == 1
    assert response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_review_back_button_accounts_for_excluded_fields(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    When fields are excluded and entire pages are removed from the UI,
    the review page back button should point to the last *visible* page,
    not the last page in the unfiltered UI definition.
    """
    edit_url = reverse("form_edit", args=[form_entry.pk])

    # Post data with NO topics selected — this excludes all cost fields
    # (item1_cost, item2_cost, item3_cost), causing the "Specific costs"
    # PageBlock to be removed entirely from the UI.
    authenticated_client.post(
        edit_url,
        data={"applicable_topics": []},
        query_params={"step": 1, "page": 0},
    )

    # Navigate to the review page
    review_url = reverse("form_review", args=[form_entry.pk])
    response = authenticated_client.get(review_url)

    assert response.status_code == 200

    prev_url = response.context["prev_url"]

    # With the "Specific costs" page removed, step 1 has only 1 page (the
    # PermanentPageBlock at index 0). So the back button should point to
    # step=1, page=0 — NOT step=1, page=1 which would cause a 500.
    expected_url = build_form_edit_url(form_entry.pk, step_number=1, page_number=0)
    assert prev_url == expected_url


@pytest.mark.django_db
def test_invalid_query_params_fall_back_to_first_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    url = reverse("form_edit", args=[form_entry.pk])

    response = authenticated_client.get(url, {"step": "not-a-number", "page": "also-bad"})

    assert response.status_code == 200
    assert response.context["current_step_number"] == 0
    assert response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_out_of_range_page_query_params_clamp_to_last_visible_page(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    url = reverse("form_edit", args=[form_entry.pk])

    authenticated_client.post(
        url,
        data={"applicable_topics": []},
        query_params={"step": 1, "page": 0},
    )

    response = authenticated_client.get(url, {"step": 1, "page": 99})

    assert response.status_code == 200
    assert response.context["current_step_number"] == 1
    assert response.context["current_page_number"] == 0


@pytest.mark.django_db
def test_save_and_exit_redirects_to_form_list(
    django_db_setup, form_entry: "FormEntry", authenticated_client
):
    """
    Test that clicking 'Save & Exit' saves the form data and redirects to the form list.
    """
    url = reverse("form_edit", args=[form_entry.pk])

    # Post data with page-action=save-exit
    response = authenticated_client.post(
        url,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "page-action": "save-exit",
        },
        query_params={
            "step": 0,
            "page": 0,
        },
    )

    # Should redirect to form_list
    assert response.status_code == 302
    assert response.headers.get("Location") == reverse("form_list")


@pytest.mark.django_db
def test_side_nav_redirect_accepts_valid_same_entry_url(
    django_db_setup, form_entry: "FormEntry", authenticated_client_with_user
):
    target = reverse("form_edit", args=[form_entry.pk]) + "?step=0&page=0"
    url = reverse("form_edit", args=[form_entry.pk])

    client, user = authenticated_client_with_user

    response = client.post(
        url,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "redirect_to": target,
        },
        query_params={"step": 1, "page": 0},
    )

    assert response.status_code == 302
    assert response.headers["Location"] == target


@pytest.mark.django_db
def test_side_nav_redirect_rejects_external_urls(
    django_db_setup, form_entry: "FormEntry", authenticated_client_with_user
):
    url = reverse("form_edit", args=[form_entry.pk])

    client, user = authenticated_client_with_user

    response = client.post(
        url,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "redirect_to": "//attacker.example/phish",
        },
        query_params={"step": 0, "page": 0},
    )

    assert response.status_code == 200
    assert response.context["current_step_number"] == 0
    assert response.context["current_page_number"] == 0

    # Data should be saved
    form_entry.refresh_from_db()
    assert form_entry.data.get("first_name") == "John"
    assert form_entry.data.get("last_name") == "Doe"


@pytest.mark.django_db
def test_build_post_save_redirect_to_valid_step():
    """Side-nav click on a step that still has pages after save goes directly there."""
    entry_pk = str(uuid.uuid4())
    components = [
        StepBlock(title="S1", children=[PageBlock(title="P1")]),
        StepBlock(title="S2", children=[PageBlock(title="P2")]),
    ]
    target_url = build_form_edit_url(entry_pk, step_number=1, page_number=0)
    result = _build_post_save_redirect(target_url, entry_pk=entry_pk, components=components)
    assert result == build_form_edit_url(entry_pk, step_number=1, page_number=0)


@pytest.mark.django_db
def test_build_post_save_redirect_to_empty_step_goes_forward():
    """Side-nav click on a step that became empty after save skips forward to the next valid step."""
    entry_pk = str(uuid.uuid4())
    components = [
        StepBlock(title="S1", children=[PageBlock(title="P1")]),
        StepBlock(title="S2 empty", children=[]),
        StepBlock(title="S3", children=[PageBlock(title="P3")]),
    ]
    target_url = build_form_edit_url(entry_pk, step_number=1, page_number=0)
    result = _build_post_save_redirect(target_url, entry_pk=entry_pk, components=components)
    assert result == build_form_edit_url(entry_pk, step_number=2, page_number=0)


@pytest.mark.django_db
def test_build_post_save_redirect_to_empty_step_no_forward_steps_goes_to_review():
    """Side-nav click on a step that became empty with no further steps redirects to review."""
    entry_pk = str(uuid.uuid4())
    components = [
        StepBlock(title="S1", children=[PageBlock(title="P1")]),
        StepBlock(title="S2 empty", children=[]),
    ]
    target_url = build_form_edit_url(entry_pk, step_number=1, page_number=0)
    result = _build_post_save_redirect(target_url, entry_pk=entry_pk, components=components)
    assert result == reverse("form_review", kwargs={"pk": entry_pk})


# ---------------------------------------------------------------------------
# submit_permissions gate
# ---------------------------------------------------------------------------

AO_PERMISSION = "form_manager.form_tribal_plan_can_sign_authorized_official"


def _ensure_custom_permissions_exist():
    for model in apps.get_models():
        ct = ContentType.objects.get_for_model(model)
        for codename, name in model._meta.permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={"name": name},
            )


@pytest.fixture
def permission_groups(db):
    _ensure_custom_permissions_exist()
    with patch("users.signals.create_permission_groups"):
        create_permission_groups(
            app_config=None,
            verbosity=0,
            interactive=False,
            using="default",
            plan=[],
        )


@pytest.fixture
def ao_schema(use_test_schema):
    """Patch the test schema so step 0 page 0 requires the AO permission."""
    from pydantic import ConfigDict, Field
    from pydantic_extra_types.semantic_version import SemanticVersion

    from form_manager.constants import AllFormNames, CSBGAnnualReportForms, FormFamilies
    from form_manager.schema.fields import acf_fields
    from form_manager.schema.forms.base import BaseFields, BaseFormSchema, UIDefinition
    from form_manager.schema.layout import FieldBlock, PageBlock, SectionBlock, StepBlock
    from tests.unit.form_manager.fixtures.use_test_schema import TestSchemaForm

    class AOSchema(BaseFormSchema):
        family: FormFamilies = Field(FormFamilies.CSBG_ANNUAL_REPORT, frozen=True)
        name: AllFormNames = Field(CSBGAnnualReportForms.TRIBAL_ANNUAL_REPORT_3_0, frozen=True)
        variant: SemanticVersion = Field(SemanticVersion(3, 0, 4), frozen=True)
        form_fields: TestSchemaForm  # type: ignore
        ui: UIDefinition = Field(
            frozen=True,
            default=[
                StepBlock(
                    title="Restricted Step",
                    children=[
                        PageBlock(
                            title="AO-only page",
                            submit_permissions=[AO_PERMISSION],
                            children=[
                                SectionBlock(children=[FieldBlock(field_name="first_name")]),
                                AlertBoxBlock(
                                    alert_type="warning",
                                    heading="Only an authorized official can complete this section",
                                    message=(
                                        "Your changes will not be saved. Contact your organization's "
                                        "Authorized Official to complete and sign this page."
                                    ),
                                    render_when=lambda ctx: not ctx.get("page_permissions_met"),
                                ),
                            ],
                        )
                    ],
                ),
                StepBlock(
                    title="Open Step",
                    children=[
                        PageBlock(
                            title="Regular page",
                            children=[SectionBlock(children=[FieldBlock(field_name="last_name")])],
                        )
                    ],
                ),
            ],
        )
        model_config = ConfigDict(use_enum_values=True)

    with patch("form_manager.schema.forms.utils.import_string", return_value=AOSchema):
        yield AOSchema


@pytest.fixture
def ao_form_entry(seed_data, ao_schema, create_user):
    from organizations.models import OrganizationProfile

    user = create_user
    org = OrganizationProfile.objects.filter(userorganizationmembership__user=user).first()
    form_def = FormDefinition.objects.first()
    return FormEntry.objects.create(
        form_definition=form_def, organization=org, created_by=user, version_number="1"
    )


@pytest.fixture
def non_ao_client(permission_groups, ao_form_entry, django_user_model, client):
    """An authenticated client whose user has edit rights but NOT the AO permission."""
    from faker import Faker
    from organizations.models import UserOrganizationMembership

    fake = Faker()
    user = django_user_model.objects.create_user(email=fake.email(), password="pw", is_active=True)
    membership = UserOrganizationMembership.objects.create(
        user=user, organization=ao_form_entry.organization
    )
    editor_group = Group.objects.get(name="Recipient Form Editor")
    membership.groups.add(editor_group)
    client.force_login(user)
    return client, user


@pytest.mark.django_db
def test_ao_page_allows_ao_user_post(
    django_db_setup, ao_form_entry, authenticated_client_with_user, permission_groups
):
    """A user WITH the AO permission can POST past an AO-restricted page."""
    client, user = authenticated_client_with_user

    from organizations.models import UserOrganizationMembership

    membership = UserOrganizationMembership.objects.get(
        user=user, organization=ao_form_entry.organization
    )
    ao_group = Group.objects.get(name=RECIPIENT_AUTHORIZED_OFFICIAL)
    membership.groups.add(ao_group)

    url = reverse("form_edit", args=[ao_form_entry.pk])

    response = client.post(
        url,
        data={"first_name": "Allowed"},
        query_params={"step": 1, "page": 0},
    )

    assert response.status_code in (200, 302)

    ao_form_entry.refresh_from_db()
    assert ao_form_entry.data.get("first_name") == "Allowed"


@pytest.mark.django_db
def test_unrestricted_page_allows_any_user_post(django_db_setup, form_entry, authenticated_client):
    """Pages without submit_permissions are not affected by the gate."""
    url = reverse("form_edit", args=[form_entry.pk])

    response = authenticated_client.post(
        url,
        data={"first_name": "Open"},
        query_params={"step": 1, "page": 0},
    )

    assert response.status_code in (200, 302)

    form_entry.refresh_from_db()
    assert form_entry.data.get("first_name") == "Open"


@pytest.mark.django_db
def test_ao_page_shows_permission_notice_for_non_ao_user(
    django_db_setup, ao_form_entry, non_ao_client
):
    """GET on an AO-restricted page shows a warning notice for non-AO users."""
    client, _ = non_ao_client
    url = reverse("form_edit", args=[ao_form_entry.pk])

    response = client.get(url, {"step": 0, "page": 0})

    assert response.status_code == 200
    assert "Only an authorized official can complete this section" in response.content.decode(
        "utf-8"
    )
