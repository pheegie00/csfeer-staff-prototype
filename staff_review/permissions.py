"""Permission scoping for staff_review.

Implements CORE-132 (Federal Staff permissions), CORE-29 (cross-region
access), CORE-192 (org-scoped content visibility at login).

Federal Staff are a separate Django auth Group whose membership grants
the 5 staff permissions defined on FormEntry's Meta.permissions:
    staff_view_any_submission        -- queue + detail visibility
    staff_edit_on_behalf             -- rationale flow (CORE-167)
    staff_return_submission          -- return flow (CORE-168, 169)
    staff_determine_submission       -- determination (CORE-44, 45)
    staff_archive_submission         -- archive (CORE-132 last clause)

Per CORE-29, Federal Staff see submissions from ANY region (no
geographic filter at the queryset level). Per CORE-192, recipients
see only their org's content -- recipient-side scoping is handled by
the existing form_manager views, not by this app.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

FEDERAL_STAFF_GROUP = "Federal Staff"
FEDERAL_STAFF_PERMISSIONS = [
    "form_manager.staff_view_any_submission",
    "form_manager.staff_edit_on_behalf",
    "form_manager.staff_return_submission",
    "form_manager.staff_determine_submission",
    "form_manager.staff_archive_submission",
]


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Block non-Federal-Staff users at the view layer.

    - Unauthenticated users: redirect to LOGIN_URL (per LoginRequiredMixin default).
    - Authenticated users without the staff group: 403 Permission Denied.
    """

    permission_denied_message = (
        "This area is restricted to Federal Staff. If you believe you "
        "should have access, contact your OCS / OFA program lead."
    )

    def test_func(self):
        u = self.request.user
        # Unauthenticated -> let LoginRequiredMixin handle (redirect to login).
        # We return True here so UserPassesTestMixin doesn't fire; the
        # LoginRequiredMixin.dispatch already short-circuits unauthenticated
        # requests before we get here. Defensive: also return True so the
        # control flow is explicit.
        if not u.is_authenticated:
            return True
        if u.is_superuser:
            return True
        if u.groups.filter(name=FEDERAL_STAFF_GROUP).exists():
            return True
        return u.has_perm("form_manager.staff_view_any_submission")

    def handle_no_permission(self):
        """Differentiate auth-required (redirect) vs group-required (403)."""
        if not self.request.user.is_authenticated:
            # Defer to LoginRequiredMixin -> redirect to settings.LOGIN_URL
            return super().handle_no_permission()
        # Authenticated but failed test -> 403
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied(self.permission_denied_message)


def staff_queryset_filter(queryset, user):
    """Filter a FormEntry queryset to what `user` can see.

    Visibility rules:
      - Anonymous: empty
      - Superuser: everything (admin bypass)
      - User with explicit cross-program permission
        ('form_manager.staff_view_any_submission' OUTSIDE the group):
        everything
      - Federal Staff group member with one or more
        UserProgramAssignment rows: limited to FormEntries whose
        form_definition.program is in the user's assigned programs
        (STAFF-MP-04). This enables OCS staff to see only CSBG,
        OFA staff to see only TANF/HMRF/etc.
      - Federal Staff group member with NO program assignments:
        cross-program access -- the legacy "Federal Staff sees all"
        behavior from CORE-29. Keeps backward compatibility for
        single-program installs.
    """
    if not user.is_authenticated:
        return queryset.none()
    if user.is_superuser:
        return queryset
    # Explicit override permission (granted to e.g. ACF leadership)
    if user.has_perm("form_manager.staff_view_any_submission") and not user.groups.filter(name=FEDERAL_STAFF_GROUP).exists():
        return queryset

    if user.groups.filter(name=FEDERAL_STAFF_GROUP).exists():
        # STAFF-MP-04: program-scoped if user has assignments;
        # falls back to CORE-29 cross-program if no assignments are configured.
        assigned_program_ids = list(
            user.program_assignments.values_list("program_id", flat=True)
        )
        if assigned_program_ids:
            return queryset.filter(form_definition__program_id__in=assigned_program_ids)
        return queryset  # legacy cross-program access
    return queryset.none()
