# PWS Section 2.0: Specific Requirements and Tasks

## Summary

Non-exhaustive, mutable requirements list from the Performance Work Statement defining system capabilities. Most requirements confirm core context; key additions are the no-code form builder (post-year-1), public link sharing for submission excerpts, ATO timeline (18 months), SORN requirement, and the detailed open questions around federal review workflow configurability.

**Source:** B09 SA 0001 - PWS ADMIN_OCS_CSBG_CSFEER_v2.pdf, Section 2.0

---

## Requirements Beyond Core Context

### Security & Compliance Milestones

- **ATO deadline:** Must achieve Authority to Operate within 18 months to collect production data.
- **SORN required:** System of Records Notice needed (implies PII collection beyond just email -- likely grant recipient identity data, organizational data, financial figures).

> **Addition vs. core context:** Core context mentions Login.gov auth but not the ATO timeline or SORN. Both are hard compliance gates with planning implications.

### No-Code Form Builder (Post Year 1)

- PWS calls for a "UI-based, low-code/no-code form builder to allow non-technical staff to build future forms" with a sandbox/testing space.
- Explicitly scoped as **after year 1**, meaning current JSON schema approach is acceptable for now.

> **Addition vs. core context:** Core context does not mention a form builder UI. This is a significant future capability that should influence schema design decisions today -- form definitions need to be expressible through a GUI eventually.

### Public Access Links

- Ability to generate a shareable link enabling public (unauthenticated) access to **specific portions** of a form submission.
- Implies partial-visibility access control at the field/section level, not just full-form sharing.

> **Addition vs. core context:** Not mentioned in core context. Architecturally requires a token-based access layer and field-level visibility controls.

### Write API for Pre-population

- PWS explicitly calls for a **write API** to import pre-populated data, separate from the read/export API.
- This confirms the need for an ingest pipeline (likely from OLDC or prior-year data sources).

### PDF Export of Individual Submissions

- Individual form submissions must be exportable as PDFs.
- Combined with existing CSV and API export requirements, this means three export formats.

### User & Permission Management

- **Self-service user administration** at every organizational tier: subrecipient admins manage their users, state admins manage theirs, federal admins manage theirs.
- Minimum role set at each level: **read-only, write-only, approve**.
- Recipients (not just federal staff) control account creation for their people.

> **Refinement vs. core context:** Core context mentions "multi-person collaboration" generically. The PWS specifies a hierarchical, self-administered permission model with explicit role minimums. This drives the `form_manager/models/` permission design significantly.

### Review Workflow Complexity (Open Questions)

The PWS flags a "visual/no-code workflow builder" for federal review routing but leaves key design questions unresolved:

| Question                                                         | Impact                         |
| ---------------------------------------------------------------- | ------------------------------ |
| Sequential vs. parallel review steps?                            | Workflow engine architecture   |
| Conditional routing (e.g., budget threshold triggers CFO step)?  | Business rules engine scope    |
| Unanimous vs. any-one-approves per step?                         | Approval logic                 |
| Who configures workflows -- IT, program managers, or end users?  | UI complexity / access control |
| Delegation and override rules?                                   | Permission model               |
| Reviewer permission tiers (view-only / comment / final approve)? | Role granularity               |

> **Addition vs. core context:** Core context says "customizable federal review/approval routing." These open questions reveal the requirement is substantially more complex than a simple linear workflow. The no-code builder aspiration combined with conditional logic suggests an eventual need for a rules/workflow engine (not just hardcoded routes).

### Alerts & Notifications (Open Questions)

- Channels: email, dashboard, system alerts (all mentioned as options).
- SLA/deadline enforcement and escalation rules are on the table but unresolved.
- Users need visibility into overall workflow progress (implies a status dashboard).

---

## Government's Prioritized Problem Statements

Ranked "top problems to solve" (subject to change):

1. **Faster form design iteration** -- program staff can design, update, and test forms without engineering.
2. **Intuitive recipient UX** -- replace PDF-era friction.
3. **Submission tracking & collaboration** -- visibility across program staff, lead agencies, and subrecipients.
4. **Real-time validation** -- business-logic-driven errors and warnings during data entry.
5. **Integration validation** -- automated comparison to external data (e.g., UEI mismatches from SAM.gov).
6. **Error correction workflow** -- staff can export, review, and fix data issues.
7. **Reduce variability** -- standardize away from custom state/tribal plan formats and third-party tools.
8. **Real-time data access** -- analytics/reporting without degrading app performance.

> **Note on #5:** UEI mismatch validation implies integration with SAM.gov or similar federal registries. Not mentioned in core context.

---

## Contractual & Process Notes

- All IP (research, designs, code, documentation) is property of ACF.
- Requirements are explicitly described as **non-exhaustive and mutable** -- agile discovery and user research drive changes.
- Priorities managed through standard agile ceremonies (roadmapping, backlog prioritization, sprint planning) with Government as Product Owner.
