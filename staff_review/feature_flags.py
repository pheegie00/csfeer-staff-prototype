"""Feature flag registry + model for demo-time on/off toggling.

Phase 4 Step 10. Built so a demo presenter can flip features on or off
right before a customer walkthrough without a code deploy. Default
state is "everything on"; toggling a flag off hides the corresponding
nav item AND blocks the underlying URLs (with a friendly disabled page
instead of a 404 so we can explain what's happening).

Adding a new feature flag:
  1. Add a constant + entry in REGISTERED_FLAGS below.
  2. Wrap the relevant nav link with `{% if flags.YOUR_KEY %}`.
  3. Wrap the relevant view's dispatch with FeatureRequiredMixin
     (or call ensure_feature_enabled() at the top).
  4. Run the seed_feature_flags management command (or just hit
     /staff/features/ once; missing flags auto-create on view).

Conventions:
  - Keys are short slug-like strings, snake_case.
  - is_enabled defaults to True so nothing breaks when a new flag
    is added without an explicit migration step.
  - Categories group flags in the admin UI for readability.
"""

from dataclasses import dataclass
from typing import Iterable

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import render

from organizations.models import BaseModel

User = get_user_model()


# ---- Registry ---------------------------------------------------------

@dataclass(frozen=True)
class FlagDefinition:
    key: str
    label: str
    description: str
    category: str
    default_enabled: bool = True


REGISTERED_FLAGS: tuple[FlagDefinition, ...] = (
    # Help section
    FlagDefinition(
        key="help_section",
        label="Help section",
        description=(
            "Top-nav Help link, quick start guides, knowledge base "
            "articles, and chatbot. Disable to hide the entire Help "
            "experience from all users."
        ),
        category="Help",
    ),
    FlagDefinition(
        key="help_chatbot",
        label="Help chatbot",
        description=(
            "Knowledge base assistant on the Help index page. Requires "
            "the Help section flag to also be on. Disable if you want "
            "to show only browse-able articles without the chat widget."
        ),
        category="Help",
    ),

    # Form Builder
    FlagDefinition(
        key="form_builder",
        label="Form Builder",
        description=(
            "Per-program form template management at /staff/form-builder/. "
            "Includes publish flow, window editing, and scope editing. "
            "Disable to hide the Form templates nav item."
        ),
        category="Staff workflow",
    ),
    FlagDefinition(
        key="form_builder_chip_filters",
        label="Form Builder program filters",
        description=(
            "Clickable program chips on the Form Builder list. When off, "
            "chips become static labels and the list always shows all "
            "your programs' forms."
        ),
        category="Staff workflow",
    ),

    # Exports + Audit
    FlagDefinition(
        key="csv_exports",
        label="CSV exports",
        description=(
            "CSV download of resolved submissions at /staff/exports/. "
            "Disable to hide the Exports nav item."
        ),
        category="Staff workflow",
    ),
    FlagDefinition(
        key="audit_log_viewer",
        label="Audit log viewer",
        description=(
            "FISMA / NIST 800-53 compliance log at /staff/audit-log/. "
            "Disable to hide the Audit log nav item."
        ),
        category="Staff workflow",
    ),

    # Demo affordances
    FlagDefinition(
        key="view_as_toggle",
        label="View-as persona switcher",
        description=(
            "Click your avatar to switch between seeded demo personas. "
            "Always restricted to superusers, but you can hide it "
            "entirely if it would distract during a customer demo."
        ),
        category="Demo affordances",
    ),

    # Recipient enforcement
    FlagDefinition(
        key="recipient_window_enforcement",
        label="Recipient window + scope enforcement",
        description=(
            "On the recipient form list, hide out-of-scope forms and "
            "block start when the submission window is upcoming or "
            "closed. Disable to make every active form startable for "
            "any org (useful when demoing the form-fill flow without "
            "the gatekeeping)."
        ),
        category="Recipient experience",
    ),

    # Formspec runtime (Phase 7 / STAFF-MP-13)
    FlagDefinition(
        key="formspec_runtime",
        label="Formspec runtime",
        description=(
            "Master switch for the Formspec integration: View spec button + "
            "lint badge on Form Builder Detail, JSON-spec-driven recipient "
            "rendering (replaces the hardcoded Tribal Plan template), and "
            "server-side response validation on FormEntry submit. Disable "
            "to fall back to the pre-Formspec behavior everywhere."
        ),
        category="Form runtime",
    ),
)


_FLAGS_BY_KEY = {f.key: f for f in REGISTERED_FLAGS}


def get_flag_definition(key: str) -> FlagDefinition | None:
    return _FLAGS_BY_KEY.get(key)


def categories_in_order() -> list[str]:
    """Distinct categories preserving registration order."""
    seen: list[str] = []
    for f in REGISTERED_FLAGS:
        if f.category not in seen:
            seen.append(f.category)
    return seen


# ---- Model ------------------------------------------------------------

class FeatureFlag(BaseModel):
    """A single feature flag's enabled state, persisted across deploys."""

    key = models.SlugField(
        max_length=64, unique=True,
        help_text="Stable identifier referenced in code. See REGISTERED_FLAGS.",
    )
    is_enabled = models.BooleanField(
        default=True,
        help_text="When False, the feature is hidden from nav and blocked at the URL.",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="feature_flag_updates",
    )

    class Meta(BaseModel.Meta):
        ordering = ["key"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.key}={'on' if self.is_enabled else 'off'}"

    @property
    def definition(self) -> FlagDefinition | None:
        """The static registry entry for this flag (for label/description/category)."""
        return get_flag_definition(self.key)


# ---- Runtime helpers --------------------------------------------------

def _ensure_seeded() -> None:
    """Idempotently create FeatureFlag rows for any registered flag missing one.

    Called by `flags_enabled_map()` so the registry always reflects the
    current code, even immediately after adding a new flag without a
    migration step.
    """
    existing = set(FeatureFlag.objects.values_list("key", flat=True))
    missing = [f for f in REGISTERED_FLAGS if f.key not in existing]
    if missing:
        FeatureFlag.objects.bulk_create([
            FeatureFlag(key=f.key, is_enabled=f.default_enabled) for f in missing
        ])


def flags_enabled_map() -> dict[str, bool]:
    """Return {key: is_enabled} for every registered flag.

    Use this in the context processor so templates can do
    `{% if flags.help_section %}`. Returns the registry default when
    no row exists yet (so the first hit on a brand-new flag still
    behaves correctly even before _ensure_seeded runs).
    """
    try:
        _ensure_seeded()
        live = dict(FeatureFlag.objects.values_list("key", "is_enabled"))
    except Exception:
        # DB not migrated yet (e.g. during the very first migrate run).
        # Fall back to registry defaults so app boot doesn't crash.
        live = {}
    return {f.key: live.get(f.key, f.default_enabled) for f in REGISTERED_FLAGS}


def is_enabled(key: str) -> bool:
    return flags_enabled_map().get(key, True)


def ensure_feature_enabled(request, key: str):
    """Raise PermissionDenied (rendered as a friendly disabled page) if off.

    Use in view code that should be unreachable when a feature is off:

        def get(self, request, ...):
            ensure_feature_enabled(request, "form_builder")
            ...
    """
    if not is_enabled(key):
        raise FeatureDisabled(key)


class FeatureDisabled(Exception):
    """Raised when a request hits a view whose feature flag is off."""

    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Feature '{key}' is currently disabled.")


class FeatureRequiredMixin:
    """View mixin form of ensure_feature_enabled.

    Usage:
        class MyView(FeatureRequiredMixin, ListView):
            feature_key = "form_builder"
            ...
    """

    feature_key: str = ""

    def dispatch(self, request, *args, **kwargs):
        if self.feature_key and not is_enabled(self.feature_key):
            return _render_disabled_page(request, self.feature_key)
        return super().dispatch(request, *args, **kwargs)


def _render_disabled_page(request, key: str):
    """Friendly 'this feature is off' page so users know why a link 404s."""
    definition = get_flag_definition(key)
    return render(
        request,
        "staff_review/feature_disabled.html",
        {
            "flag_key": key,
            "flag_label": definition.label if definition else key,
            "flag_description": definition.description if definition else "",
        },
        status=503,  # Service Unavailable: feature exists but is temporarily off
    )
