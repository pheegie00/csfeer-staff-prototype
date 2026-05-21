"""Help section content registry + audience derivation (Phase 4 Step 9).

Articles are plain Python dataclasses, audience-tagged so each user
only sees the help that applies to them. Adding a new article is a
single tuple entry in ARTICLES below.

Style rules for all article bodies (and any user-facing string in
this module):
  - No em dashes. Use hyphens, parentheses, or commas instead.
  - Plain text with single blank lines as paragraph breaks. No
    markdown rendering at template time, so don't rely on bold or
    bullets unless you wrap them in HTML.

Audience tokens:
  all                    every authenticated user
  federal_staff          any user in the Federal Staff group
  reviewer               UserProgramAssignment.role = reviewer
  program_admin          UserProgramAssignment.role = admin
  auditor                UserProgramAssignment.role = auditor
  platform_admin         is_superuser
  recipient              any user with an org membership
  recipient_viewer       Recipient Form Viewer group
  recipient_editor       Recipient Form Editor group
  recipient_approver     Recipient Form Approver group
  recipient_ao           Recipient Authorized Official group

An article shown to many audiences should list each one explicitly
(or use the catch-all "all"). Audience filtering takes the union, so
listing both "reviewer" and "program_admin" shows the article to
either role.
"""

from dataclasses import dataclass, field

from staff_review.permissions import FEDERAL_STAFF_GROUP


# ---- Audience tokens --------------------------------------------------

AUD_ALL = "all"
AUD_FEDERAL_STAFF = "federal_staff"
AUD_REVIEWER = "reviewer"
AUD_PROGRAM_ADMIN = "program_admin"
AUD_AUDITOR = "auditor"
AUD_PLATFORM_ADMIN = "platform_admin"
AUD_RECIPIENT = "recipient"
AUD_RECIPIENT_VIEWER = "recipient_viewer"
AUD_RECIPIENT_EDITOR = "recipient_editor"
AUD_RECIPIENT_APPROVER = "recipient_approver"
AUD_RECIPIENT_AO = "recipient_ao"


def audiences_for_user(user) -> set[str]:
    """Compute which audience tokens apply to a given user.

    A user may belong to multiple audiences. The {"all"} token is
    always included for authenticated users so cross-cutting articles
    surface to everyone.
    """
    if not user.is_authenticated:
        return set()

    auds: set[str] = {AUD_ALL}

    if user.is_superuser:
        auds.add(AUD_PLATFORM_ADMIN)

    # Staff side
    if user.groups.filter(name=FEDERAL_STAFF_GROUP).exists():
        auds.add(AUD_FEDERAL_STAFF)
        roles = set(user.program_assignments.values_list("role", flat=True))
        if "reviewer" in roles:
            auds.add(AUD_REVIEWER)
        if "admin" in roles:
            auds.add(AUD_PROGRAM_ADMIN)
        if "auditor" in roles:
            auds.add(AUD_AUDITOR)

    # Recipient side (membership in any org -> recipient; check group
    # membership at the UserOrganizationMembership level since recipient
    # groups attach there, not on user.groups).
    if user.org_memberships.exists():
        auds.add(AUD_RECIPIENT)
    membership_groups = set(
        user.org_memberships.values_list("groups__name", flat=True)
    )
    if "Recipient Form Viewer" in membership_groups:
        auds.add(AUD_RECIPIENT_VIEWER)
    if "Recipient Form Editor" in membership_groups:
        auds.add(AUD_RECIPIENT_EDITOR)
    if "Recipient Form Approver" in membership_groups:
        auds.add(AUD_RECIPIENT_APPROVER)
    if "Recipient Authorized Official" in membership_groups:
        auds.add(AUD_RECIPIENT_AO)

    return auds


# ---- Article registry -------------------------------------------------

CATEGORY_QUICKSTART = "Quick start"
CATEGORY_SUBMISSIONS = "Submissions"
CATEGORY_FORM_BUILDER = "Form Builder"
CATEGORY_REPORTING = "Reporting and audit"
CATEGORY_RECIPIENT = "Recipient workflow"
CATEGORY_PLATFORM = "Platform"
CATEGORY_ABOUT = "About"


@dataclass(frozen=True)
class Article:
    id: str
    slug: str
    title: str
    summary: str
    body: str
    audiences: tuple[str, ...]
    category: str
    keywords: tuple[str, ...] = field(default_factory=tuple)


ARTICLES: tuple[Article, ...] = (
    # ============================================================
    # Quick start (role-specific)
    # ============================================================
    Article(
        id="qs-reviewer",
        slug="getting-started-reviewer",
        title="Getting started as a Federal Reviewer",
        summary="Your day-to-day workflow for triaging and resolving submissions.",
        body=(
            "Welcome. As a Federal Reviewer, your primary view is the "
            "Submissions inbox at /staff/. Each card represents one "
            "FormEntry from a recipient organization, grouped by status: "
            "Submitted, In Progress (after a return), Returned, Accepted, "
            "and Closed.\n\n"
            "Open any submission to see the full form data on the left and "
            "the review rail on the right. From the rail you can record an "
            "edit-on-behalf rationale, send the form back to the recipient "
            "for revision, or record an Accept / Close determination once "
            "the package is final.\n\n"
            "Your inbox is automatically scoped to the programs you cover. "
            "If you have program assignments for CSBG only, you will not "
            "see TANF submissions in your inbox even though they exist in "
            "the system. Ask your program lead if you need wider access."
        ),
        audiences=(AUD_REVIEWER, AUD_FEDERAL_STAFF),
        category=CATEGORY_QUICKSTART,
        keywords=("getting started", "reviewer", "inbox", "first time"),
    ),
    Article(
        id="qs-program-admin",
        slug="getting-started-program-admin",
        title="Getting started as a Program Admin",
        summary="Managing form templates, windows, and scoping for your program.",
        body=(
            "As a Program Admin you can do everything a reviewer can, "
            "plus manage the lifecycle of form templates from the Form "
            "templates nav item.\n\n"
            "The Form templates page lists every template attached to "
            "your assigned programs. Click any row to manage that "
            "template: edit the submission window for the current fiscal "
            "year, adjust which organization types are in scope, or "
            "publish a new version when the schema needs to change.\n\n"
            "Publishing a new version deprecates the previous version and "
            "automatically closes any in-progress drafts so recipients "
            "always work against the current schema. See the 'How to "
            "publish a new version' article for the full flow."
        ),
        audiences=(AUD_PROGRAM_ADMIN,),
        category=CATEGORY_QUICKSTART,
        keywords=("getting started", "program admin", "form templates"),
    ),
    Article(
        id="qs-auditor",
        slug="getting-started-auditor",
        title="Getting started as an Auditor",
        summary="Read-only access plus reporting tools across your programs.",
        body=(
            "As an Auditor you have read-only access to every submission "
            "under your assigned programs. You cannot return, accept, or "
            "edit submissions, but you can view their full history and "
            "export data for reporting.\n\n"
            "Your main tools are the Exports nav item (CSV downloads of "
            "resolved submissions filtered by fiscal year and form type) "
            "and the Audit log nav item (chronological view of every "
            "system event for compliance review).\n\n"
            "If you need to take an action on a submission, ask the "
            "program reviewer or admin assigned to that program."
        ),
        audiences=(AUD_AUDITOR,),
        category=CATEGORY_QUICKSTART,
        keywords=("getting started", "auditor", "read-only", "reports"),
    ),
    Article(
        id="qs-platform-admin",
        slug="getting-started-platform-admin",
        title="Getting started as a Platform Admin",
        summary="Cross-program access, View-as testing, and feature flag control.",
        body=(
            "Platform Admins are superusers. You bypass every program "
            "scoping rule, so the inbox shows submissions from every "
            "program in the system.\n\n"
            "Three tools are unique to your role. First, the View-as "
            "toggle on your avatar lets you impersonate any seeded demo "
            "persona with one click, useful for testing what each role "
            "sees. Second, the Features nav item lets you turn features "
            "on or off across the entire app (used to hide work in "
            "progress before a customer demo). Third, you can manage "
            "shared forms like SF-424 that span multiple programs.\n\n"
            "Use your superuser powers thoughtfully. Every action is "
            "audit-logged with your real identity, even when viewing as "
            "another persona."
        ),
        audiences=(AUD_PLATFORM_ADMIN,),
        category=CATEGORY_QUICKSTART,
        keywords=("getting started", "platform admin", "superuser", "view as"),
    ),
    Article(
        id="qs-recipient",
        slug="getting-started-recipient",
        title="Getting started as a recipient",
        summary="Filling out and submitting forms for your organization.",
        body=(
            "Your home screen lists the forms your organization is "
            "eligible to submit, plus any drafts you have started. "
            "Eligibility is determined by your organization type and "
            "the form's current submission window.\n\n"
            "Click 'Start New Form' on any open form to begin a draft. "
            "Drafts auto-save as you type. Once complete, your "
            "Authorized Official needs to sign before the form can be "
            "submitted (for forms that require AO sign-off, such as the "
            "CSBG Tribal Plan).\n\n"
            "After submission, federal staff review your form. They may "
            "accept it, close it, or return it to you with specific items "
            "to address. Returned forms appear in your list with the "
            "items inline; resolve each item, then resubmit."
        ),
        audiences=(AUD_RECIPIENT,),
        category=CATEGORY_QUICKSTART,
        keywords=("getting started", "recipient", "first time", "draft"),
    ),

    # ============================================================
    # Submissions (staff)
    # ============================================================
    Article(
        id="sub-inbox",
        slug="understanding-the-inbox",
        title="Understanding the Submissions inbox",
        summary="How cards, columns, and filters work on the staff inbox.",
        body=(
            "The inbox groups submissions into five status columns. "
            "Submitted are new packages awaiting review. In Progress are "
            "drafts a recipient is actively editing (often after a "
            "return). Returned are packages a reviewer sent back. "
            "Accepted and Closed are final states.\n\n"
            "Each card shows the organization name, submission date, "
            "form type, and the current owner. Click any card to open "
            "the full review screen. Counts at the top of each column "
            "update live as you take actions.\n\n"
            "The inbox is filtered to your assigned programs. To see a "
            "submission from another program, ask the relevant program "
            "reviewer for context or ask a Platform Admin to widen your "
            "assignments."
        ),
        audiences=(AUD_FEDERAL_STAFF,),
        category=CATEGORY_SUBMISSIONS,
        keywords=("inbox", "kanban", "cards", "status", "columns"),
    ),
    Article(
        id="sub-return",
        slug="returning-a-submission",
        title="How to return a submission for revision",
        summary="Compose review items, send back to the recipient.",
        body=(
            "Open the submission you want to return. In the review rail "
            "on the right, click 'Return for revision'. The return "
            "builder lets you add one or more discrete review items, each "
            "with a section reference, a field reference, and your "
            "comment.\n\n"
            "Once you send the return, the submission moves to the "
            "Returned status. The recipient is notified, sees each review "
            "item inline on their form, and must acknowledge each item "
            "before they can resubmit. Returns are one-per-submission: "
            "you cannot send a second return on the same package.\n\n"
            "Use returns for substantive content issues that the "
            "recipient must address. For typos or formatting you can "
            "fix yourself, use Edit on behalf instead."
        ),
        audiences=(AUD_REVIEWER, AUD_PROGRAM_ADMIN),
        category=CATEGORY_SUBMISSIONS,
        keywords=("return", "revision", "review items", "send back"),
    ),
    Article(
        id="sub-determination",
        slug="recording-a-determination",
        title="How to record a determination",
        summary="Accept or Close a submission to resolve it.",
        body=(
            "Determination is the final step on a submission. Once you "
            "are confident the package is complete and correct, click "
            "'Record determination' in the review rail. Choose Accepted "
            "(meets all requirements) or Closed (does not meet "
            "requirements and will not be re-reviewed this cycle).\n\n"
            "Both outcomes lock the submission. The recipient can no "
            "longer edit it, and the FormEntry status moves to Accepted "
            "or Closed. Add a notes field to explain your reasoning for "
            "the audit trail; this is required for Closed determinations.\n\n"
            "Determinations are reversible only by reopening through the "
            "audit interface, which is a Platform Admin action. Take "
            "your time and use Return for revision if you are not yet "
            "ready to make a final call."
        ),
        audiences=(AUD_REVIEWER, AUD_PROGRAM_ADMIN),
        category=CATEGORY_SUBMISSIONS,
        keywords=("determination", "accept", "close", "resolve", "final"),
    ),
    Article(
        id="sub-edit-on-behalf",
        slug="editing-on-behalf",
        title="How to edit on behalf of an organization",
        summary="Direct corrections without sending the form back.",
        body=(
            "Edit on behalf is for small staff-side corrections you can "
            "make without burdening the recipient (typos, formatting, "
            "data entry corrections from a separate phone call).\n\n"
            "Open the submission, click 'Edit on behalf' in the review "
            "rail. You must provide a rationale before you can save: "
            "what you changed and why. This rationale is recorded as a "
            "permanent audit row tied to your user account.\n\n"
            "Use Return for revision instead when the change is "
            "substantive enough that the recipient should see it, "
            "acknowledge it, and re-sign. Anything that affects "
            "compliance attestation should go through return, not edit."
        ),
        audiences=(AUD_REVIEWER, AUD_PROGRAM_ADMIN),
        category=CATEGORY_SUBMISSIONS,
        keywords=("edit", "on behalf", "rationale", "corrections"),
    ),

    # ============================================================
    # Form Builder (admin)
    # ============================================================
    Article(
        id="fb-what",
        slug="what-is-the-form-builder",
        title="What is the Form Builder",
        summary="The admin layer for managing form templates per program.",
        body=(
            "Form Builder is the multi-tenant admin layer for form "
            "templates. Each program admin sees only their own program's "
            "form templates; shared forms like SF-424 are managed by "
            "Platform Admins and shown read-only to everyone else.\n\n"
            "For each template you can edit the submission window for "
            "each fiscal year (when recipients can start drafts), adjust "
            "the organization type scoping (which org types can fill out "
            "the form), and publish a new version when the schema changes.\n\n"
            "Note that the underlying form schema (which fields exist, "
            "their validation rules) is defined in code and shipped via "
            "deployment, not edited in the UI. Form Builder controls "
            "lifecycle metadata only."
        ),
        audiences=(AUD_PROGRAM_ADMIN, AUD_PLATFORM_ADMIN),
        category=CATEGORY_FORM_BUILDER,
        keywords=("form builder", "templates", "what is"),
    ),
    Article(
        id="fb-window",
        slug="setting-submission-window",
        title="How to set a submission window",
        summary="Define when recipients can start drafts for a fiscal year.",
        body=(
            "Open a form template in the Form Builder. Find the "
            "'Submission window' card. Each fiscal year has at most one "
            "window with an opens-at date and a closes-at date.\n\n"
            "Three derived states: Upcoming (opens-at is in the future, "
            "no new drafts can be started but the form is visible), Open "
            "(now is between opens-at and closes-at, recipients can "
            "start drafts), Past Due (closes-at is in the past, no new "
            "drafts but existing drafts remain editable).\n\n"
            "Click 'Edit window' to set or update the dates. You can "
            "shorten an open window or extend a closed one; existing "
            "drafts are unaffected."
        ),
        audiences=(AUD_PROGRAM_ADMIN, AUD_PLATFORM_ADMIN),
        category=CATEGORY_FORM_BUILDER,
        keywords=("submission window", "opens", "closes", "fiscal year", "FY"),
    ),
    Article(
        id="fb-scope",
        slug="adjusting-org-scoping",
        title="How to adjust organization scoping",
        summary="Choose which org types can see and fill out a form.",
        body=(
            "Open a form template. Find the 'Org scoping' card. The "
            "scope is expressed as a list of organization types (Tribe, "
            "State, Territory, CBO, etc.); any organization matching one "
            "of those types is eligible to see and start the form.\n\n"
            "Click 'Edit scope', check the org types that should be in "
            "scope, save. The 'in scope' count below updates to reflect "
            "the new rule. Recipients whose org type no longer matches "
            "lose access to NEW drafts; their existing in-progress "
            "drafts remain editable.\n\n"
            "For one-off exceptions (an organization that should see a "
            "form even though their org type is not in the rule), use "
            "the explicit-org override. This is a Platform Admin "
            "responsibility."
        ),
        audiences=(AUD_PROGRAM_ADMIN, AUD_PLATFORM_ADMIN),
        category=CATEGORY_FORM_BUILDER,
        keywords=("scope", "scoping", "org type", "eligibility"),
    ),
    Article(
        id="fb-publish",
        slug="publishing-a-new-version",
        title="How to publish a new version",
        summary="Deprecate the current version and auto-close in-progress drafts.",
        body=(
            "Publishing creates a new FormDefinition row with a bumped "
            "variant (semver: minor bump for backward-compatible "
            "changes, major bump for breaking schema changes), marks the "
            "previous version inactive, and (per CORE-24) automatically "
            "closes every in-progress draft of the previous version with "
            "a determination of Closed and a note explaining the auto-close.\n\n"
            "Resolved submissions on the previous version (Accepted or "
            "Closed) are NOT modified. The new version inherits the org "
            "scoping and the current fiscal year's submission window "
            "from the source version by default; you can override both "
            "in the publish form.\n\n"
            "Open the form template, click 'Publish new version'. The "
            "form shows you how many in-progress drafts will be "
            "auto-closed before you confirm."
        ),
        audiences=(AUD_PROGRAM_ADMIN, AUD_PLATFORM_ADMIN),
        category=CATEGORY_FORM_BUILDER,
        keywords=("publish", "new version", "semver", "deprecate", "auto-close"),
    ),

    # ============================================================
    # Reporting and audit
    # ============================================================
    Article(
        id="rep-csv",
        slug="exporting-csv-data",
        title="How to export data as CSV",
        summary="Download resolved submissions filtered by form and fiscal year.",
        body=(
            "The Exports page lists every (form template, fiscal year) "
            "combination that has at least one resolved submission. Pick "
            "the combination you want, click 'Export CSV', and your "
            "browser downloads a flat file with one row per submission "
            "and one column per form field.\n\n"
            "Each export is logged as a SystemEvent so the action shows "
            "up in the audit log. Only resolved (Accepted or Closed) "
            "submissions are exported; in-progress and returned "
            "submissions are excluded to keep reports stable."
        ),
        audiences=(AUD_REVIEWER, AUD_PROGRAM_ADMIN, AUD_AUDITOR),
        category=CATEGORY_REPORTING,
        keywords=("export", "csv", "download", "report"),
    ),
    Article(
        id="rep-audit",
        slug="understanding-the-audit-log",
        title="Understanding the audit log",
        summary="Tamper-evident log of every action across the system.",
        body=(
            "The Audit log nav item shows a chronological view of every "
            "logged action: logins, logouts, edits on behalf, returns, "
            "determinations, CSV exports, form publish events, and "
            "account changes. Each row is append-only at both the "
            "application layer (save() raises on existing rows) and the "
            "DB layer (in production, the audit tables have UPDATE / "
            "DELETE grants revoked).\n\n"
            "Filter by user, action type, or date range. Each row "
            "includes the actor's IP address and user agent for forensic "
            "review. This satisfies the bulk of the FISMA / NIST 800-53 "
            "audit requirements per CORE-47."
        ),
        audiences=(AUD_AUDITOR, AUD_PLATFORM_ADMIN),
        category=CATEGORY_REPORTING,
        keywords=("audit log", "compliance", "FISMA", "NIST", "tamper-evident"),
    ),

    # ============================================================
    # Recipient workflow
    # ============================================================
    Article(
        id="rec-start",
        slug="starting-a-new-draft",
        title="How to start a new form draft",
        summary="From the form list to your first save.",
        body=(
            "On your forms list, available forms appear at the top with "
            "a 'Start New Form' button. Click it to create a new draft. "
            "You will be taken to the form edit page where you can fill "
            "out each section.\n\n"
            "Drafts auto-save as you type. You can leave and return; "
            "your draft appears under 'Your Form Entries' below the "
            "available forms list, with status 'in_progress'.\n\n"
            "If a form shows 'Opens Jul 1' or 'Closed' as a badge, the "
            "Start button is disabled. That fiscal year's submission "
            "window is not currently open; either wait for the window "
            "to open or contact your program lead."
        ),
        audiences=(AUD_RECIPIENT,),
        category=CATEGORY_RECIPIENT,
        keywords=("start", "new form", "draft", "first"),
    ),
    Article(
        id="rec-window",
        slug="why-form-shows-opens-or-closed",
        title="Why is a form showing 'Opens' or 'Closed'",
        summary="Understanding submission windows on the recipient view.",
        body=(
            "Each form template has a submission window per fiscal year. "
            "The window controls when new drafts can be started.\n\n"
            "If you see 'Opens Jul 1, 2026' on a form, that fiscal "
            "year's window has not yet opened. The form is visible so "
            "you can prepare, but Start is disabled. The form will "
            "become startable on the date shown.\n\n"
            "If you see 'Closed Dec 31, 2025', the window has passed. "
            "New drafts cannot be started. However, any DRAFT you "
            "already started before the close date remains editable and "
            "can still be submitted. Look for your in-progress draft in "
            "the 'Your Form Entries' table below."
        ),
        audiences=(AUD_RECIPIENT,),
        category=CATEGORY_RECIPIENT,
        keywords=("opens", "closed", "window", "deadline", "past due"),
    ),

    # ============================================================
    # Platform
    # ============================================================
    Article(
        id="plat-viewas",
        slug="using-view-as-toggle",
        title="How to use the View-as toggle",
        summary="One-click impersonation of seeded demo personas.",
        body=(
            "Click your avatar in the top right to open the View-as "
            "panel. Pick any seeded demo persona to switch the session. "
            "No log-out / log-in cycle needed. The session remembers "
            "your demo-admin status so you can keep switching after the "
            "first hop (root to Maya to Dana stays toggleable).\n\n"
            "Impersonation is allow-listed: you can only switch to "
            "seeded demo emails, not to arbitrary production accounts. "
            "Each switch fires the login audit signal with the new "
            "user's identity.\n\n"
            "Disable the View-as feature globally from the Features "
            "page if you want it hidden during a customer demo."
        ),
        audiences=(AUD_PLATFORM_ADMIN,),
        category=CATEGORY_PLATFORM,
        keywords=("view as", "impersonation", "switch user", "personas"),
    ),
    Article(
        id="plat-flags",
        slug="using-feature-flags",
        title="How to use feature flags",
        summary="Turn features on or off across the entire app.",
        body=(
            "The Features nav item opens the feature flag admin. Every "
            "registered flag appears with its current state, description, "
            "and a turn-on / turn-off button.\n\n"
            "Toggling a flag off hides the corresponding nav item AND "
            "blocks the underlying URL with a friendly 'feature "
            "disabled' page so users know why their bookmark stopped "
            "working. The change is global and takes effect immediately.\n\n"
            "Use cases: hide work-in-progress nav items before a "
            "customer demo, disable a flow that has a known issue, "
            "compare the experience with and without recipient "
            "enforcement. Re-enable any flag at any time to restore "
            "normal behavior."
        ),
        audiences=(AUD_PLATFORM_ADMIN,),
        category=CATEGORY_PLATFORM,
        keywords=("feature flag", "toggle", "disable", "demo"),
    ),

    # ============================================================
    # About
    # ============================================================
    Article(
        id="about-core",
        slug="about-core",
        title="About CORE",
        summary="What CORE is and how it fits into ACF reporting.",
        body=(
            "CORE (Community Outcomes Reporting Engine) is the "
            "next-generation grant reporting platform for the "
            "Administration for Children and Families (ACF). It "
            "consolidates form intake, review, and reporting for "
            "multiple ACF programs starting with CSBG (Community "
            "Services Block Grant) and scaling to LIHEAP, TANF, HMRF, "
            "CED, and others.\n\n"
            "CORE is built around a multi-tenant architecture: each ACF "
            "office (OCS, OFA) has multiple programs, each program has "
            "multiple form templates, and each form template has its "
            "own submission window and organization-type scoping per "
            "fiscal year.\n\n"
            "The federal staff side (this app) handles review and "
            "reporting. The recipient side handles form filling and "
            "submission. Both sides share the same underlying data "
            "model so an action on one side is immediately visible to "
            "the other."
        ),
        audiences=(AUD_ALL,),
        category=CATEGORY_ABOUT,
        keywords=("about", "core", "what is core", "platform"),
    ),
)


def articles_for(audiences: set[str]) -> list[Article]:
    """Filter the registry to articles whose audiences intersect with the user's."""
    return [a for a in ARTICLES if set(a.audiences) & audiences]


def article_by_slug(slug: str) -> Article | None:
    for a in ARTICLES:
        if a.slug == slug:
            return a
    return None
