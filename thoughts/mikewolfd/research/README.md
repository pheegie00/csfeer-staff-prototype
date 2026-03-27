# Research — CSFEER/CORE

Project research and requirements documentation for the CSFEER forms platform.

## Document Map

| Document                                                         | Purpose                                                      | Start here if...                                                   |
| ---------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| [UNDERSTANDING.md](UNDERSTANDING.md)                             | Project context, risks, conflicts, open questions            | You need background on the project, its users, or its constraints  |
| [MATRIX.md](MATRIX.md)                                           | Authoritative requirements registry with source traceability | You need the canonical requirement for a feature (by ID)           |
| [requirements-traceability.md](requirements-traceability.md)     | Requirements ↔ codebase ↔ Jira mapping (HOW)                | You need to know which tickets cover a requirement, or find gaps   |
| [mvp-gap-analysis.md](mvp-gap-analysis.md)                      | Prioritized gap analysis with Jira coverage                  | You need to know what's missing for MVP and what to build next     |
| [open-items.md](open-items.md)                                   | All conflicts, risks, decisions, and open questions           | You need to check an open item (C-xx, R-xx, D-xx, Q-xx)           |
| [VALUE_STREAM_ANALYSIS.md](VALUE_STREAM_ANALYSIS.md)             | First-principles value stream decomposition                  | You need the architectural rationale behind deliverable boundaries |
| [csfeer-architectural-review.md](csfeer-architectural-review.md) | Point-in-time codebase architecture snapshot (2026-02-17)    | You want to understand how the current code is structured          |
| [proposed-architecture.md](proposed-architecture.md)              | Spec-driven form infrastructure vision (Phase II+)           | You want the long-term architectural direction beyond current MVP  |

## Subdirectories

| Directory   | Contents                                                                         |
| ----------- | -------------------------------------------------------------------------------- |
| `analysis/` | Exploratory research on form engine approaches (XForms, SHACL, JSON Forms, etc.) |
| `archive/`  | Archived documents                                                               |

## How These Documents Relate

```
UNDERSTANDING.md              ← context, risks, conflicts, open questions
       │
MATRIX.md                     ← authoritative requirements (WHAT)
       │
VALUE_STREAM_ANALYSIS.md      ← value streams and deliverable boundaries (WHY)
       │
requirements-traceability.md  ← req ↔ code ↔ Jira mapping (HOW)
       │
mvp-gap-analysis.md           ← prioritized gaps + Jira coverage (NOW)
       │
open-items.md                 ← all conflicts, risks, decisions, questions (BLOCKERS)

proposed-architecture.md      ← spec-driven form infrastructure vision (NEXT)
```

MATRIX.md is the single source of truth for requirements. All other documents reference it by ID (FE-xx, WF-xx, etc.). Conflicts and risks live in UNDERSTANDING.md. The traceability matrix maps every MATRIX ID to implementation status and Jira tickets (stateless `bd-XXX` references from `.beads/issues.csv`). The gap analysis distills this into a prioritized action list.
