# Multi-Program Architecture: Scaling CORE Beyond CSBG

## Why this doc exists

CORE was originally scoped to CSBG (Community Services Block Grant), administered by
the Office of Community Services (OCS). The platform vision is to host **all
ACF grant program reporting**, not just CSBG. This document captures what's
already abstracted vs. CSBG-coupled, identifies what would cause massive
rework if we ignored it, and proposes the minimum-viable changes to keep the
architecture program-agnostic.

## Target program portfolio

Per stakeholder input, the following ACF grant programs are candidates for
hosting in CORE:

| Office | Program        | Forms in scope                                    | Recipient types                  | External systems today      |
|--------|----------------|---------------------------------------------------|----------------------------------|------------------------------|
| OCS    | CSBG           | Tribal Plan, Annual Report (Long/Short, Eligible Entities, States) | Tribes, States, Eligible Entities | CORE (this app)             |
| OFA    | TANF           | ACF-196R, ACF-199, ACF-209, ACF-204, ACF-202, SF-424 | States, Territories             | OLDC (GrantSolutions), TANF Data Portal |
| OFA    | Tribal TANF    | ACF-196T + OFA reporting instructions             | Tribes                           | OLDC (GrantSolutions)        |
| OFA    | HMRF (HEART, FORGE) | nFORM 2.0 measures                          | CBOs, faith-based, Tribes (32+50 grantees across 38 states) | nFORM 2.0     |
| OFA    | HPOG           | (dormant; no active awards)                       | Higher ed, Tribes, workforce agencies, gov't, CBOs | n/a now      |
| OFA    | Tribal TANF + Child Welfare Coordination | active NOFO              | Tribes                           | Grants.gov                   |
| Various | SF-424        | Standard federal Application for Federal Assistance | All applicants                  | Grants.gov                   |

**Implication:** The "Federal Staff workflow" we are building is not "OCS reviewers
looking at Tribal CSBG submissions." It is "any ACF program office staff looking at
any submission their program is scoped to receive."

## What's already abstracted (low rework risk)

- `FormFamilies` enum is keyed by OMB control number (`0970-0635`, `0970-0492`).
  Adding TANF (`0970-0338` for ACF-199, etc.) is a one-line enum addition.
- `FormDefinition.family` field exists -- forms can be categorized by family.
- `OrganizationProfile` is generic. No hardcoded "Tribe" assumption -- it's
  name + address + contact + state.
- `State` model with ACF region mapping already in place.
- `UserOrganizationMembership` is org-generic.
- Form schemas live in `form_manager/schema/forms/` as Python modules that
  generate JSON Schema. Adding ACF-196R is "drop a new module + register it"
  per the extensible-template pattern (CORE-27).
- `FormEntry.data` is `JSONField` -- accepts any form shape.
- `FormAuditTrail` / `FormAuditDetail` are form-agnostic.
- Cotton USWDS components in `csfeer/templates/patterns/` are program-agnostic.

## What's CSBG-coupled (will rework if ignored)

### High coupling (will cause rework when adding TANF)

1. **`form_manager/constants.py`** -- Only CSBG form enums exist
   (`CSBGAnnualReportForms`, `CSBGTribalPlanApplicationForms`). Adding TANF
   needs sibling enums (`TANFFinancialForms`, `TANFDataForms`, etc.) and
   `ALL_FORM_NAME_CHOICES` updated.
2. **No `Program` model** -- We jump straight from `FormDefinition` to
   `FormEntry`. There is no entity grouping forms into programs, and no entity
   grouping programs into ACF offices. This means staff permissions can't be
   scoped to "TANF reviewers see TANF submissions only."
3. **My new `staff_*` permissions on FormEntry are global** -- e.g.
   `staff_view_any_submission` implies one Federal Staff pool. Real ACF: an
   OFA staffer should not see OCS submissions (different program, different
   chain of authority).
4. **`OrganizationProfile` has no `org_type`** -- We model state (the
   geographic state via FK) but not the org *type* (Tribe vs State vs
   Territory vs CBO vs Higher Ed vs Workforce Agency). HMRF + HPOG have
   recipients across multiple org types simultaneously. Without org_type,
   filtering "show me TANF submissions from State governments only" is hard.
5. **Status terminology and AO signature assumption** -- "AO" (Authorized
   Official) is a Tribal Plan concept. TANF financial reports don't have an
   AO -- they have a designated "preparer" and "certifier" but different
   workflow. The `FormReturn.ao_signature_cleared` field implies AO existence.

### Medium coupling

6. **Submission cycles assumed annual** -- CSBG Tribal Plan is annual.
   ACF-196R is **quarterly**. ACF-199 / ACF-209 are quarterly per sample
   month. Need `FormDefinition.cycle_type` (annual / quarterly / monthly /
   ad_hoc).
7. **Region-based access (CORE-29) assumes CSBG region structure** -- ACF
   regions exist for all programs but the "cross-region access" rule is
   CSBG-derived. TANF has different access scoping (e.g., state-by-state
   assignment).
8. **No concept of external system integration** -- TANF Data Portal, OLDC
   (via GrantSolutions), and nFORM 2.0 are existing federal systems that
   already collect this data. Do we replace them, mirror them, or aggregate?
   Strategic question, not just data model.
9. **`staff_review/mock_data.py` and prototype copy is Tribal-only** --
   demos will need a TANF state-submission example before we can show
   non-OCS stakeholders.

### Low coupling

10. Staff workflow patterns (review queue, return for revision,
    edit-on-behalf, determination) are largely program-agnostic. Confirmed by
    spot-checking TANF documentation -- OFA reviewers do similar work.

## Recommended "do now" architectural changes (cheap)

These keep optionality without forcing a full multi-program build today.
Each can land as its own migration in the next 1-3 commits:

### 1. Add `Program` model + FK from `FormDefinition.program`

```python
# new file: programs/models.py
class ACFOffice(BaseModel):
    code = models.CharField(max_length=20, unique=True)  # OCS, OFA, ANA, OHS
    name = models.CharField(max_length=200)

class Program(BaseModel):
    code = models.CharField(max_length=50, unique=True)  # CSBG, TANF, TRIBAL_TANF, HMRF, HPOG
    name = models.CharField(max_length=200)
    office = models.ForeignKey(ACFOffice, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
```

Seed with: OCS->CSBG, OFA->TANF, OFA->Tribal_TANF, OFA->HMRF, OFA->HPOG (inactive).

Add `Program` FK to `FormDefinition`. Default existing FormDefinitions to
CSBG. Cost: 1 migration with a data migration to populate.

### 2. Add `org_type` to `OrganizationProfile`

```python
class OrgType(TextChoices):
    TRIBE       = "tribe", "Federally Recognized Tribe"
    TRIBAL_ORG  = "tribal_org", "Tribal Organization"
    STATE       = "state", "State Government"
    TERRITORY   = "territory", "U.S. Territory"
    HIGHER_ED   = "higher_ed", "Higher Education Institution"
    WORKFORCE   = "workforce_agency", "Workforce System Agency"
    CBO         = "cbo", "Community-Based Organization"
    FAITH_BASED = "faith_based", "Faith-Based Organization"
    OTHER       = "other", "Other"

org_type = models.CharField(max_length=30, choices=OrgType.choices, default="tribe")
```

Cost: 1 migration. Today all orgs default to Tribe. Future TANF state orgs
get `state`. Filtering by org_type becomes possible.

### 3. Rename staff permissions to be program-scoped (or add Program FK)

Two options:
- **Simpler:** Keep permission names global; enforce program scoping in
  `get_queryset()` views by filtering `FormEntry.form_definition.program` against
  the user's allowed programs.
- **More explicit:** Permission grants live on `UserOrganizationMembership` or
  a new `UserProgramAssignment` model with `(user, program, role)` rows.

Recommend the simpler path now (`get_queryset` scoping), promote to explicit
model when we have 2+ programs live.

### 4. Add `cycle_type` to `FormDefinition`

```python
class CycleType(TextChoices):
    ANNUAL    = "annual"
    QUARTERLY = "quarterly"
    MONTHLY   = "monthly"
    AD_HOC    = "ad_hoc"

cycle_type = models.CharField(max_length=20, choices=CycleType.choices, default="annual")
```

Used downstream for: submission window calculations, the cycle field shown
on FormDefinition rows, and CSV export grouping.

### 5. Document the decision in an ADR

Mark this doc as ADR-001 in `docs/adr/` so the team knows the architecture
direction. Future PRs reference it.

## Things to NOT do now (deferred)

- Full per-program permissions framework with role hierarchies. Premature.
- Building TANF / HMRF form schemas. Need OFA program-staff input first.
- External system integrations (TANF Data Portal, OLDC, nFORM 2.0). Need
  strategic decision: replace? mirror? aggregate?
- Program-specific workflow variations (e.g., TANF's preparer/certifier
  distinction vs CSBG's AO model). Tackle when first non-CSBG form lands.
- Multi-program audit / compliance UI. Defer to post-MVP.

## Open strategic questions for leadership

Before adding the next program (TANF likely first), stakeholders need to
decide:

1. **Replace vs. augment external systems.** Is CORE intended to *replace*
   OLDC / TANF Data Portal / nFORM 2.0, or sit alongside them as a unified
   staff-review layer pulling data via API? This is the biggest unknown.
2. **Program staff assignment model.** Are staff assigned to programs
   (1:1), regions (1:many), or both? Affects permission model.
3. **Cross-program federated reporting.** Will OCS, OFA, etc. want
   cross-program aggregate views, or each program siloed?
4. **OMB approvals for unified system.** Each form's OMB control number is
   tied to its current collection method. Migrating ACF-196R into CORE may
   require OMB notification.
5. **Data isolation requirements (CORE-5).** Government data isolation is
   already in scope for CSBG. Confirm whether multi-program hosting changes
   the isolation calculus.

## Backlog: scaling tickets

See `docs/backlog.md` for the full prioritized list of multi-program tickets
to file in Jira when ready.
