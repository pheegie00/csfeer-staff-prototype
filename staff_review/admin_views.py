"""Superuser-only admin pages for staff_review.

Phase 4 Step 10: FeatureFlagAdminView lets a demo presenter toggle
features on/off right before a walkthrough.
"""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from staff_review.feature_flags import (
    REGISTERED_FLAGS,
    FeatureFlag,
    categories_in_order,
    get_flag_definition,
)


class _SuperuserOnlyMixin:
    """Restrict admin pages to actual superusers (NOT impersonators).

    Note: deliberately stricter than the View-as eligibility check
    elsewhere. Toggling feature flags affects every user in the
    system, so we want the real superuser to do it (not a persona
    they switched into).
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("staff_review:inbox"))
        if not request.user.is_superuser:
            raise PermissionDenied("Feature flag admin is restricted to platform superusers.")
        return super().dispatch(request, *args, **kwargs)


class FeatureFlagAdminView(_SuperuserOnlyMixin, TemplateView):
    """List all registered flags with current enabled state + a toggle UI."""

    template_name = "staff_review/feature_flags_admin.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Hydrate rows in registry order so the UI stays predictable
        # even after key renames. Auto-create missing rows.
        existing = {f.key: f for f in FeatureFlag.objects.all()}
        rows = []
        for defn in REGISTERED_FLAGS:
            flag = existing.get(defn.key)
            if flag is None:
                flag = FeatureFlag.objects.create(
                    key=defn.key, is_enabled=defn.default_enabled,
                )
            rows.append({
                "key": defn.key,
                "label": defn.label,
                "description": defn.description,
                "category": defn.category,
                "is_enabled": flag.is_enabled,
                "updated_at": flag.updated_at,
                "updated_by": flag.updated_by,
            })

        # Group by category for the UI.
        grouped: dict[str, list] = {c: [] for c in categories_in_order()}
        for r in rows:
            grouped[r["category"]].append(r)

        ctx["grouped_flags"] = grouped
        ctx["total_on"] = sum(1 for r in rows if r["is_enabled"])
        ctx["total_off"] = sum(1 for r in rows if not r["is_enabled"])
        return ctx


class FeatureFlagToggleView(_SuperuserOnlyMixin, View):
    """POST /staff/features/toggle/  -- flip one flag's is_enabled bit."""

    http_method_names = ["post"]

    def post(self, request):
        key = (request.POST.get("key") or "").strip()
        defn = get_flag_definition(key)
        if defn is None:
            messages.error(request, f"Unknown feature flag: {key!r}")
            return redirect(reverse("staff_review:feature_flags_admin"))

        flag, _ = FeatureFlag.objects.get_or_create(
            key=key, defaults={"is_enabled": defn.default_enabled},
        )
        flag.is_enabled = not flag.is_enabled
        flag.updated_by = request.user
        flag.save()

        state = "enabled" if flag.is_enabled else "disabled"
        messages.success(request, f"{defn.label} is now {state}.")
        return redirect(reverse("staff_review:feature_flags_admin"))
