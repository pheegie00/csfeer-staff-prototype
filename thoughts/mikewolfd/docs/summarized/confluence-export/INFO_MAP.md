# INFO_MAP — Confluence Export Intelligence Map

> At-a-glance briefing for building the CSFEER/CORE forms engine.
> Cross-referenced against UNDERSTANDING.md (PRD synthesis) using 36 agent analyses.
> Last updated: 2026-02-23

---

## 1. Directory Structure

```
OGM Tech/
├── INFO_MAP.md (this file)
├── attachments/ (.docx, .mov, .mp4, .pdf, .png, .pptx, .svg, .xlsx, .zip)
└── OGM Tech Home/
    └── OGM Technology Products/
        ├── Product_ Forms Engine (Focus Contract).md
        └── Product_ Forms Engine (Focus Contract)/
            ├── Contract Status Template.md (index)
            │   ├── CSR - Forms Engine CSFEER (140D0425P0190).md
            │   ├── CSR - December 2025.md
            │   └── CSR - January 2026.md
            ├── CSBG Data Files.md
            ├── CSFEER_ ATO Documentation & Compliance Hub.md
            ├── Design & Research.md (index)
            │   └── User Research Plan.md
            ├── Engineering.md (index)
            │   ├── CSFEER Tech Stack.md
            │   └── Tech Specs/ (index)
            │       ├── Okta Authentication DRAFT.md
            │       ├── Tech Spec Template.md
            │       └── Form Manager Application (WIP).md
            ├── Forms Engine IPT Meetings.md (index)
            │   ├── 2026-01-13 ITB - CSFEER.md
            │   ├── 2026-01-27 ITB - CSFEER.md
            │   ├── 2026-02-03 ITB - CSFEER.md
            │   └── 2026-02-10 ITB - CORE.md
            ├── Forms Engine Onboarding Documents.md
            │   ├── Forms Engine Discovery/ (index)
            │   │   ├── CSBG Annual Report.md
            │   │   ├── CSBG Reporting Process.md
            │   │   └── OCS and CSBG Overview.md (414KB - largest)
            │   └── Forms Engine Meeting Notes/ (index)
            │       ├── 2024-06 Initial Conversation with Minette.md
            │       ├── 2025-09-17 Contract kickoff prep.md
            │       ├── 2025-09-25 Kickoff with CSBG Staff.md
            │       ├── 2025-09-29 Kickoff with Focus.md
            │       ├── 2025-11-20 Check-in (CSBG with OGM Tech).md
            │       ├── 2025-11-26 Forms Digitization.md
            │       ├── 2025-12-05 Demo 1 (Focus/ACF).md
            │       ├── 2026-01-28 Q1 Planning Session.md
            │       └── 2026-02-13.md
            ├── Initial Product Spec - MVP.md
            ├── Risk Management.md
            └── Technical Architecture & Security Framework.md
```

---

## 2. Client Mental Model

OCS frames this as **a forms problem with a data problem underneath**. The existing system (OLDC, built 2015) collects 1,000+ data points annually via fillable PDFs, SmartForms, and manual uploads. Two people spend 700+ hours per cycle exporting and cleaning data for Congressional reporting. Tribal recipients upload PDFs to SF-424M requiring manual data extraction. OCS has "no measurable insight" into workflow efficiency, error patterns, or user burden.

**How they think about the project:**

- **Origin story**: Minette Galindo (Branch Chief CSBG) initiated this in June 2024. Informal market research led to vendor evaluation (Focus, Truss, Coforma), an RFI to GCS, and Focus winning the contract (awarded Sept 30, 2025). [Initial Conversation; Onboarding Documents]
- **Replacement, not supplement**: CSFEER replaces GrantSolutions for form filling. Notably, a parallel $1.2M-$1.71M OLDC modernization (CHMT-3186) was scoped before CSFEER — the relationship between these initiatives is never explicitly resolved in the docs, but CSFEER appears to be the chosen path. [CSBG Annual Report]
- **Start small, prove, expand**: CSBG tribal forms first (66 users) → state/territory forms (53+ users) → all OCS programs (LIHEAP, Diaper Program) → eventually all of ACF (60+ forms across 8+ offices). The platform is specifically exciting when a form crosses program offices (e.g., 424M). [Onboarding Documents; OCS Overview]
- **Naming**: The project is called "CSFEER" (pronounced "sphere"), "CORE", or "Forms Engine" interchangeably. Even formal governance documents use inconsistent names (e.g., Feb 10 ITB uses "CORE" in the title). [IPT Meetings index]
- **Shadow systems motivation**: Program offices have built workaround systems around GrantSolutions' limitations. Building forms in GS is "not user-friendly, expensive, and has a long timeline." The Forms Engine is positioned to eliminate this duplication. [Onboarding Documents]
- **Establishing a baseline**: A core but underappreciated goal is creating the **first measurable baseline** for tribal reporting performance. OCS currently cannot measure time-to-complete, error patterns, or submission cycle timelines. [Product Spec]

**How the framing has evolved**: From "modernize OLDC" (June 2024) → "build a reusable forms platform starting with CSBG" (Sept 2025) → "production system with ATO on NGSC AWS" (Jan 2026). The ambition has grown but the core pitch remains: make forms easier for tribal users while giving OCS actionable data.

---

## 3. Stakeholder Map

### Decision-Makers & Sponsors

| Name                            | Title / Role                                                  | What They Care About                                                                                                                   |
| ------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Minette Galindo** (FED)       | Branch Chief CSBG, Executive Sponsor                          | "It's a forms problem, lots of time spent to make it work, OCS is not the only office that struggles with this." Broader ACF adoption. |
| **Madeline (Maddie) Solan**     | Executive Sponsor (per team directory), Data Science champion | Wants to prioritize this work; taps Melanie for updates.                                                                               |
| **Harold Jones** (FED)          | Tech stack approval authority                                 | Approves architectural decisions.                                                                                                      |
| **Sarah Ignacio**               | Contracting Officer (CO)                                      | Main point of contact during government shutdown.                                                                                      |
| **Tiffany Tatham-Miller** (FED) | COR, Acquisitions for OCS                                     | Monthly milestone meetings; course correction.                                                                                         |

### OCS Program Staff (DES — Division of Evaluation and Systems)

Regional portfolio assignments; these are the people who know the forms intimately.

| Name                        | Regions   | Key Responsibilities                                                                                                                                                          |
| --------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Melanie Durley** (FED)    | 1, 2, 3   | **Product Owner**, contract lead, congressional reporting, PRA approval (half the forms). "Minette's right hand, in the trenches."                                            |
| **Monique Alcantara** (FED) | 4, 6, 7   | OLDC business intelligence lead, testing lead, COR/PO for Performance Management website, SmartForms cooperative agreement lead. **Critical institutional knowledge holder.** |
| **Kayla Lennon** (FED)      | 5, 9      | COR admin support (bridges forms contract and Performance Management contract), CQI facilitator, disaster relief collections.                                                 |
| **Lena (Elena) Kotanchyan** | 8, 9(/10) | Data Analyst, first line for data calls, Python/R/ArcGIS. Program-side support.                                                                                               |
| **Niki Frazier-Curry**      | —         | Sr. Records Specialist. Records retention for OLDC transition, front-facing website, YouTube, 508 remediation.                                                                |

### OGM Tech / OCTO (Technical Leads)

| Name                     | Role                                                                                                 |
| ------------------------ | ---------------------------------------------------------------------------------------------------- |
| **Liane Peng** (FED)     | Design Strategist / Product Manager. Helped write PWS. OCS data strategy lead.                       |
| **Kira Tebbe** (FED)     | Technical Lead. "The tech achieves outcomes for our users, but also fits within the broader system." |
| **Amanda Welch** (CTR)   | Strategic Operations, Digital Services Team, Login.gov liaison, government shutdown continuity.      |
| **Mark Levy** (FED)      | Strategic Operations / Data Consultant.                                                              |
| **Michael Chelen** (FED) | ORR technical resource.                                                                              |

### ACF Tech Operations

| Name                                | Role                                                               |
| ----------------------------------- | ------------------------------------------------------------------ |
| **Jody Smith** (CTR)                | ACF Tech Project Lead, IPT meeting facilitator.                    |
| **Katherine (Kat) Chase** (CTR)     | Ops Team Lead, Login.gov coordination.                             |
| **Thomas Oldfield** (FED)           | Data structure liaison, upstream systems (OLDC integration point). |
| **Tharun(kumar Reddy) Chada** (CTR) | NGSC Engineer, environment provisioning.                           |
| **Bruce Mbithi** (CTR)              | DBA Leader.                                                        |
| **Jon Warren** (CTR)                | DBA Manager (assigns people).                                      |
| **Darin Hall** (CTR)                | Project Delivery.                                                  |

### Security & ATO

| Name                           | Role                                               |
| ------------------------------ | -------------------------------------------------- |
| **Oyindasola Akisanmi** (CTR)  | ISSO, ATO Lead/Coordinator, Privacy Team.          |
| **Beatrice Adenigbagbe** (CTR) | SCA (Security Control Assessor), ATO Support.      |
| **Diana Rosner** (CTR)         | Completed System Registration Form (Jan 27, 2026). |
| **Ablavi Zolome** (CTR)        | PIA owner (under review as of Feb 9).              |

### Authentication

| Name                     | Role                                           |
| ------------------------ | ---------------------------------------------- |
| **Matt Ding/Dang** (CTR) | Okta/Login.gov engineer (replaced Jim Cooper). |
| **Jim Cooper** (CTR)     | Original Okta/Login.gov provisioning contact.  |

### Focus Consulting (Contractor Team)

| Name                          | Role              | Notes                                              |
| ----------------------------- | ----------------- | -------------------------------------------------- |
| **Phedra Arthur** (CTR)       | Product Lead      | Healthcare.gov quality payments background.        |
| **Tshering Yudon** (CTR)      | Design Lead       | Owns design artifacts, research plan.              |
| **Mohammad (Mo) Taleb** (CTR) | Tech Lead         | Auth tech spec author, PIV card received Feb 2026. |
| **Simone Saldanha** (CTR)     | Service Designer  |                                                    |
| **Ryan Bagwell** (CTR)        | Software Engineer | Form Manager tech spec author.                     |
| **Logan Ricard** (CTR)        | Software Engineer |                                                    |
| **Michael Kalish**            | CTO               | Executive support.                                 |
| **Anteneh (Ant) Addis**       | CEO               | Logistics and executive support.                   |

### IPT Composition

The full IPT includes: OCS, OGM Tech, ACF Tech Operations, **Customer Engagement**, and **Cybersecurity/Privacy**. The last two are not documented in UNDERSTANDING.md but have formal seats. [IPT Meetings index]

---

## 4. What the Client Wants

### MVP (Phase I) — Tribal Forms

**Three forms**: Tribal Annual Report (long form), Tribal Annual Report (Short Form), Tribal Plan and Application.

| Metric                                 | Product Spec Target                            | UNDERSTANDING.md Target  |
| -------------------------------------- | ---------------------------------------------- | ------------------------ |
| Tribal recipients submitting digitally | **20+** without reverting to PDFs              | ≥10 tribal orgs in pilot |
| User satisfaction                      | **≥80%** report digital easier than PDFs       | ≥4/5 satisfaction score  |
| Compliance                             | **Zero** ACF OCIO security/compliance findings | ATO achieved             |
| Accessibility                          | **100%** Section 508 compliance                | WCAG 2.0 Level AA        |

**User counts** (from CSBG Annual Report discovery doc): ~30 long form users, ~30 short form users ($50K funding threshold determines which), ~66 tribal plan users. The "66" figure is the safeguard maximum.

**Additional MVP deliverables** the client expects:

- Architecture documentation complete for Phase II [Product Spec]
- Platform that supports both simple and complex forms [Product Spec]
- First measurable baseline for tribal reporting performance (telemetry) [Product Spec]
- Reusable USWDS component library ("we hope to break it out into its own project and eventually make it open source") [Form Manager tech spec]

### Phase II — State/Territory Forms

State/Territory Annual Report, Plan and Application, and Local Agency List. ~53+ users. Opt-in migration with legacy running in parallel. DCLs (Dear Colleague Letters) as communication mechanism to manage state expectations. [Kickoff prep]

### Long-Term Vision

| Office   | Forms Count | Notes                                                     |
| -------- | ----------- | --------------------------------------------------------- |
| OCS      | 14          | Starting here                                             |
| CB       | 18          | Interested; Title IV-E has complex 238-page form packages |
| OCSS     | 7           |                                                           |
| OCC      | 5           |                                                           |
| OFA      | 5           |                                                           |
| ANA      | 3           | Interested; has offline/in-person assessment needs        |
| OFVPS    | 2           | 424M crosses offices                                      |
| ORR      | 2           |                                                           |
| ACF-Wide | 4           |                                                           |

Cross-program office forms and funding from multiple program offices are key to the long-term strategy. [Onboarding Documents; Forms Digitization meeting]

### Technical Expectations

- Production on NGSC AWS with ECS and Postgres (confirmed Feb 3 ITB; devops/ Helm charts are a discrepancy)
- Full OIDC auth: government users via login.acf.gov (Okta); non-government users via Login.gov (path still being confirmed)
- PDF export and API access (two-way data flow)
- Data export to existing Performance Management website (Monique Alcantara is COR/PO)
- GitHub-to-GitLab mirroring (GitLab setup scheduled Feb 18, 2026)

---

## 5. What the Client Is Concerned About

### Documented Risks (from CSR Risk Logs)

| Risk                           | Probability | Impact | Classification | Key Mitigation                                                                                                   |
| ------------------------------ | ----------- | ------ | -------------- | ---------------------------------------------------------------------------------------------------------------- |
| Government shutdown            | Medium      | Medium | External       | Non-blocking work sequenced first; ATO prep parallel. **Already realized** (Feb 3 meeting had federal absences). |
| Tribal consultation            | Low         | High   | External       | Opt-in approach, transparent communication, respect for sovereignty.                                             |
| Login.gov complexity           | Low         | Medium | Internal       | Early technical spikes; staged integration.                                                                      |
| Data migration                 | Medium      | Medium | Internal       | MVP limited to "high-confidence data only"; expansion path for Phase II.                                         |
| User adoption                  | Medium      | High   | External       | Tribal-informed design, usability testing, training, phased onboarding, help desk support.                       |
| ATO/Security reviews           | Low         | High   | Internal       | Weekly syncs; front-loading documentation.                                                                       |
| Dependency on external reviews | Medium      | Medium | Internal       | Flexible sequencing.                                                                                             |

### Implicit Concerns (Not in Risk Logs)

- **State resistance to adoption**: States have existing vendor relationships (e.g., NJ uses "empower"). "Our network talks" — once OCS reaches out to one state, others hear quickly. Historical pattern is "talk to everyone before making changes"; deviation causes anxiety. [Kickoff with CSBG Staff; Kickoff prep]
- **Vendor sensitivity**: Avoid directly talking with CSBG vendors due to potential conflict-of-interest. [Kickoff with CSBG Staff]
- **Staffing gaps**: As of Jan 2026, 2.5-3.5 of 8.5 planned positions vacant (Product Manager, Delivery/Project Manager, 0.5 Architect). [CSRs]
- **ATO documentation weight**: Appendix X requires effort "as much as all other ATO documents combined." [Jan 27 ITB]
- **Non-government auth path**: Whether non-GFE users can access through Okta or require a separate path is an open risk that could require development rework. [Feb 10 ITB]
- **PIA classification**: Whether system is "electronic information collection" vs "application" — rubric needed from privacy team (Tobi/Oyindasola). Delay could block deployment. [Feb 10 ITB]
- **Offline use case**: ANA and CB have fully-offline, in-person assessment workflows (printed PDF stacks, live interviews). MVP's "low-connectivity resilience" would not cover this. [Forms Digitization meeting]
- **Form complexity underestimation**: CB Title IV-E has 26-page instrument + 62-page instructions + 150-page guide. Forms can be inseparable from extensive guidance documentation. [Forms Digitization meeting]

---

## 6. Unresolved Questions & Ambiguities

These contradictions were **spot-checked against source files** (not just agent summaries).

### Contract Duration

**Kickoff prep (Sept 17, 2025)** says "contract is one year with 9 month option" (21 months total). UNDERSTANDING.md says "24 months (12-month base + 12-month option)." The CSRs show "Base Period" and "Option Period 1" as separate financial tracking categories but don't specify duration. **Unresolved — affects timeline planning.**

### FISMA Classification

ATO Compliance Hub tracks an artifact literally named **"Selected Controls Rev5-Low_System"**, referencing NIST SP 800-53 Revision 5 **Low** baseline. UNDERSTANDING.md states "**FISMA Moderate** classification with NIST SP 800-53 Moderate baseline." **Directly contradictory — needs clarification from Oyindasola/security team.**

### MVP Success Targets

Product Spec (Confluence) says **"20+ Tribal grant recipients"** must submit via CORE. UNDERSTANDING.md says **"≥10 tribal orgs successfully submit during pilot."** These may describe different milestones (pilot cohort vs full MVP target) but the distinction is not documented.

### User Satisfaction Metric

Product Spec: "≥80% of users report digital experience is easier than PDFs" (comparative). UNDERSTANDING.md: "User satisfaction ≥4/5" (absolute). Different measurement frameworks; unclear which is authoritative.

### Validation Timing

Form Manager tech spec (Feb 13, 2026): "When a user has filled out all fields, they're taken to a review page. This is where validation happens." And: "any arbitrary data can be entered into fields, whether it's valid or not." UNDERSTANDING.md requirement VE-07: "Real-time validation during data entry (not only on submit)" (Priority: Must). **Directly contradictory — architectural decision needed.**

### MVP Scope Conflicts

The Form Manager tech spec explicitly lists as **out of scope**: API endpoints, authorization/access control, email notifications, approval workflows, multi-user editing. UNDERSTANDING.md lists all of these as **Must** priority requirements (DA-01, DA-02, PM-01-05, NF-01-02, WF-07). **Major scope gap — either the tech spec is outdated or requirements need re-prioritization.**

### GrantSolutions Parallel Implementation

CSBG Annual Report.md documents a **$1.2M-$1.71M** GrantSolutions/OLDC modernization (CHMT-3186) for the same CSBG Annual Report forms, with $135K-$187K annual O&M. The relationship to CSFEER is never stated — whether this was abandoned, is a fallback, or represents the State track (while CSFEER does Tribal) is unknown.

### Authentication Architecture

- Government users authenticate via **login.acf.gov** (Okta endpoint) — not Login.gov directly. [Feb 10 ITB]
- Non-government users have a **separate, unconfirmed authentication path**. [Feb 10 ITB]
- Okta tech spec treats all users uniformly through Okta, with no mention of dual paths. [Okta Auth spec]
- UNDERSTANDING.md says "Login.gov (via Okta as identity broker)" for tribal users and "ACF-approved SSO (Okta or AD, TBD)" for federal staff.
- **Four different descriptions of the same auth architecture — needs canonical resolution.**

### PDF Generation Technology

UNDERSTANDING.md: "HTML-to-PDF via headless Chrome." Tech Stack doc: **WeasyPrint 62.3+** (Python library, not headless Chrome). These are fundamentally different approaches.

### Container Orchestration

Feb 3 ITB confirms "proceeding with ECS." But devops/ directory has Helm charts (Kubernetes tool). UNDERSTANDING.md flagged this as open question #13.

### Name Confusion: Elena vs Lena

Meeting notes variously list "Elena (California, Analyst)" and "Lena Kotanchyan (Data Analyst, DES regions 8/9)." Team directory lists "Elena Kotanchyan." Likely the same person; first name may be Elena with "Lena" as informal variant.

---

## 7. Timeline & Milestones

### Pre-Contract (Discovery)

| Date         | Event                                                                              | Source               |
| ------------ | ---------------------------------------------------------------------------------- | -------------------- |
| June 2024    | Initial conversation with Minette Galindo about OLDC modernization                 | Initial Conversation |
| Oct–Dec 2024 | Market research: meetings with Focus (12/18), Truss (12/19), Coforma. RFI drafted. | Onboarding Documents |
| Nov 25, 2024 | Received buy-in from Minette. Tully refining RFI.                                  | Onboarding Documents |

### Contract Period (Sept 2025 – Present)

| Date              | Event                                                                                        | Source               |
| ----------------- | -------------------------------------------------------------------------------------------- | -------------------- |
| Sept 17, 2025     | Internal ACF/OCS kickoff prep                                                                | Kickoff prep         |
| Sept 25, 2025     | Kickoff with CSBG Staff (5 DES specialists)                                                  | Kickoff CSBG         |
| Sept 29, 2025     | Kickoff with Focus Consulting                                                                | Kickoff Focus        |
| **Sept 30, 2025** | **Contract start** (first invoice period begins)                                             | CSR Dec 2025         |
| Nov 17, 2025      | Onboarding Focus team                                                                        | Onboarding Documents |
| Nov 20, 2025      | Check-in: CSBG stakeholder introductions (Melanie, Monique, Kayla, Lena, Niki)               | Check-in Nov 20      |
| Nov 26, 2025      | Cross-functional meeting with ANA and CB re: Forms Digitization                              | Forms Digitization   |
| Dec 5, 2025       | **Demo 1**: Service blueprint, user flow prototypes, JSON data schema, API endpoints         | Demo 1               |
| Dec 10, 2025      | First two invoices submitted (DOI-ACF-001, DOI-ACF-002) totaling $243,648                    | CSR Dec 2025         |
| Dec 2025          | Sprint 3 complete; 5 risks documented                                                        | CSR Dec 2025         |
| Jan 13, 2026      | **First IPT kickoff meeting**: NGSC AWS confirmed, ATO strategy, auth coordination           | ITB Jan 13           |
| Jan 27, 2026      | ITB: ATO front-loading decision; Appendix X flagged; beta May-June; production pre-Labor Day | ITB Jan 27           |
| Jan 27, 2026      | System Registration Form **completed**                                                       | ATO Hub              |
| Jan 28, 2026      | Q1 Planning Session (recording only, no written notes)                                       | Q1 Planning          |
| Feb 3, 2026       | ITB: Government shutdown impact; ECS confirmed; PIV card received                            | ITB Feb 3            |
| Feb 9, 2026       | PIA submitted, **under review**                                                              | ATO Hub              |
| Feb 10, 2026      | ITB CORE: GitLab setup planned; auth path clarification; PIA classification question         | ITB Feb 10           |
| Feb 13, 2026      | **Sprint 6 demo** to federal leadership (Melanie, Kayla, Thomas)                             | Meeting Feb 13       |
| Feb 18, 2026      | Okta auth tech spec (DRAFT); GitLab repository setup sprint begins                           | Okta Auth spec       |
| Feb 20, 2026      | System-Categorization **under review**                                                       | ATO Hub              |

### Upcoming Targets

| Date               | Milestone                                                              | Source             |
| ------------------ | ---------------------------------------------------------------------- | ------------------ |
| March 1, 2026      | Landing page deployment                                                | UNDERSTANDING.md   |
| March 15, 2026     | Tribal Annual Report completion                                        | UNDERSTANDING.md   |
| March 31, 2026     | Tribal Plan completion; ATO documentation target                       | UNDERSTANDING.md   |
| Early April 2026   | Usability testing Round I (5 participants, Tribal Annual Report)       | User Research Plan |
| Mid-April–May 2026 | Usability testing Round II (8 participants, Tribal Plan & Application) | User Research Plan |
| **May 29, 2026**   | **ATO Security Authorization target**                                  | ATO Hub            |
| May–June 2026      | Beta testing with user groups (may be pre-ATO)                         | ITB Jan 27         |
| **Late Aug 2026**  | **Full production launch target** (pre-Labor Day)                      | ITB Jan 27         |
| FY 2027            | Remainder of tribal recipients; Phase II planning                      | CSBG Annual Report |

---

## 8. File Index

One-line summary of each Confluence file. Category tags: `discovery`, `onboarding`, `meeting`, `product`, `engineering`, `security`, `operations`, `research`, `contract`, `index`.

| File                                               | Category      | Summary                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Product_ Forms Engine (Focus Contract).md**      | `index`       | Team directory listing 6 Focus personnel and 25+ ACF stakeholders with names, roles, and FED/CTR designations.                                                                                                                                                                            |
| **Contract Status Template.md**                    | `index`       | Empty navigation page.                                                                                                                                                                                                                                                                    |
| **CSR - Forms Engine CSFEER (140D0425P0190).md**   | `contract`    | CSR template: financial tracking categories (BAC, ACWP, ETC, EAC), invoice tracking, staffing, risk log structure. FFP contract.                                                                                                                                                          |
| **CSR - December 2025.md**                         | `contract`    | Monthly CSR: 5 filled/3.5 vacant positions, $243,648 invoiced (2 invoices), 3 sprints complete, 5 risks documented.                                                                                                                                                                       |
| **CSR - January 2026.md**                          | `contract`    | Monthly CSR: Sprints 1-5 tracked, 7 active risks (adds ATO/Security Reviews + External Dependencies), 2.5 vacant positions.                                                                                                                                                               |
| **CSBG Data Files.md**                             | `discovery`   | Index of 4 FY24 OLDC export files (State Plan, Modules 1/2/4). Module 3 notably absent. RVW/RPT prefix convention.                                                                                                                                                                        |
| **CSFEER_ ATO Documentation & Compliance Hub.md**  | `security`    | ATO artifact tracker: 9 documents, **May 29, 2026** target. System Registration completed (Jan 27), PIA under review (Feb 9), System-Categorization under review (Feb 20).                                                                                                                |
| **Design & Research.md**                           | `research`    | Design artifact index: Figma "ACF-Exploration" board with ecosystem mapping, service blueprint V0, user flow, clickable prototypes (V1, V1.3). Tribal Plan designs in progress.                                                                                                           |
| **User Research Plan.md**                          | `research`    | Dual-structure research plan: (1) usability testing with 5+8 tribal grant recipients in April-May 2026, (2) semi-structured interviews with 5-8 OCS staff (Jane, Issac, Roneika) in Feb-March 2026. Owned by Tshering Yudon and Simone Saldanha.                                          |
| **Engineering.md**                                 | `index`       | Empty navigation page.                                                                                                                                                                                                                                                                    |
| **CSFEER Tech Stack.md**                           | `engineering` | Full technology inventory: Python 3.12, Django 6.0+, Alpine.js 3.15+, USWDS 3.13+, Django Ninja 1.4+, Pydantic 2.12+, WeasyPrint 62.3+ (PDF), Postgres, Playwright 1.49+, uv 0.7+.                                                                                                        |
| **Tech Specs.md**                                  | `index`       | Empty navigation page.                                                                                                                                                                                                                                                                    |
| **Okta Authentication DRAFT.md**                   | `engineering` | OIDC auth spec: Okta (acf.okta.com) as IdP, oauth2_authcodeflow library, Keycloak dev mock, role-to-group mapping from JWT claims, user auto-provisioning. 6 critical open questions re: production Okta config.                                                                          |
| **Tech Spec Template.md**                          | `engineering` | 15-section tech spec template. Four status levels (Draft→Approved/Deferred). Emphasis on "what happens if key people leave" and "Other Options Considered."                                                                                                                               |
| **Form Manager Application (WIP).md**              | `engineering` | Core architecture: Pydantic schemas as single source of truth, interview-style flow, JSON data storage in FormEntry, 4 data models (FormDefinition, FormEntry, FormAuditTrail, FormAuditDetail), review-page validation. **Out-of-scopes APIs, auth, notifications, approval workflows.** |
| **Forms Engine IPT Meetings.md**                   | `index`       | IPT meeting index. IPT composition: OCS, OGM Tech, ACF Tech Ops, Customer Engagement, Cybersecurity/Privacy.                                                                                                                                                                              |
| **2026-01-13 ITB - CSFEER.md**                     | `meeting`     | First IPT kickoff: NGSC AWS with Django/Postgres confirmed, ATO inheritance strategy, Login.gov via Okta coordination, PIV/GFE requirements. 17 attendees.                                                                                                                                |
| **2026-01-27 ITB - CSFEER.md**                     | `meeting`     | ATO front-loading decision, Appendix X identified as major effort, beta May-June, production pre-Labor Day, government shutdown rated High severity. 17 attendees.                                                                                                                        |
| **2026-02-03 ITB - CSFEER.md**                     | `meeting`     | Short meeting (25 min) due to government shutdown. ECS confirmed, PIV received, NGSC tracked via Ops JIRA board. Okta coordination: Harold Jones, Matt Dang, LCSR team.                                                                                                                   |
| **2026-02-10 ITB - CORE.md**                       | `meeting`     | GitLab setup Feb 18, GitHub-to-GitLab mirroring, gov users via login.acf.gov, non-gov auth path uncertain (Risk #1), PIA classification uncertainty (Risk #2).                                                                                                                            |
| **Forms Engine Onboarding Documents.md**           | `onboarding`  | Project tracking/onboarding doc: chronological status log (Nov 2024–Nov 2025), GrantSolutions as explicit legacy system, shadow systems problem, vendor evaluation history, cross-program office interest, CSBG Performance Management website.                                           |
| **Forms Engine Discovery.md**                      | `index`       | Links to 2 MURAL boards (Process Map, Research Intro) and 3 discovery documents.                                                                                                                                                                                                          |
| **CSBG Annual Report.md**                          | `discovery`   | Discovery doc tracking CSBG Annual Report implementation. **Contains GrantSolutions parallel dev: $1.2M-$1.71M CHMT-3186.** Tribal user counts (~30 long, ~30 short, ~66 plan). SmartForms/XML/XSD legacy tech. Appian and Tableau dependencies.                                          |
| **CSBG Reporting Process.md**                      | `discovery`   | ACF policy guidance: 4-module State Annual Report structure, FY24 tribal two-tier system ($50K threshold), OLDC/SmartForms procedures, submission deadlines (March 31), office hours schedules.                                                                                           |
| **OCS and CSBG Overview.md**                       | `discovery`   | RFI document (414KB): OCS mission ($6.3B across 7 programs), CSBG structure (1,007 entities, 9.5M individuals served), 3-phase rollout plan, ACF-wide forms inventory by office.                                                                                                          |
| **2024-06 Initial Conversation with Minette.md**   | `meeting`     | First exploration: 1,000+ data points in OLDC, SmartForms pain (UEI failures, macro blocking, Box uploads), 700+ hours data export labor, sub-recipient collection limitations from 2015.                                                                                                 |
| **2025-09-17 Contract kickoff prep.md**            | `meeting`     | Internal ACF planning: "contract is one year with 9 month option", NGSC as open question, state resistance risk (NJ "empower"), CLINs for change management, Focus preference for open source.                                                                                            |
| **2025-09-25 Kickoff with CSBG Staff.md**          | `meeting`     | CSBG staff introduction: 5 DES specialists with regional portfolios, pain points via MURAL, state communication dynamics ("our network talks"), NASCSP history, vendor sensitivity, Pennsylvania/Virginia custom systems.                                                                 |
| **2025-09-29 Kickoff with Focus.md**               | `meeting`     | Focus team introduction: Phedra (Healthcare.gov background), Tshering, Mo, Kalish (CTO), Addis (CEO). Success criteria from ACF stakeholders. Jira decision.                                                                                                                              |
| **2025-11-20 Check-in.md**                         | `meeting`     | OGM Tech ↔ CSBG intro: Melanie as contract lead, Monique as OLDC BI lead, Performance Management website as downstream consumer, SmartForms cooperative agreement, DES regional structure.                                                                                                |
| **2025-11-26 Forms Digitization.md**               | `meeting`     | Cross-ACF meeting (ANA, CB): Qualtrics as only ATO'd option ("painful"), offline/in-person assessment use cases (Alaska), CB Title IV-E 238-page form packages, Community Needs Assessment as cross-program candidate.                                                                    |
| **2025-12-05 Demo 1.md**                           | `meeting`     | Sprint progress demo: Figma service blueprint + user flow, JSON blob data schema (hard-coded MVP approach), API endpoints. Conditional narrative questions excited stakeholders.                                                                                                          |
| **2026-01-28 Q1 Planning Session.md**              | `meeting`     | Minimal metadata stub: attendee list + video recording only. No written decisions or notes.                                                                                                                                                                                               |
| **2026-02-13 Meeting Notes.md**                    | `meeting`     | Sprint 6 demo to federal leadership. Two recordings (project background/design + demo/Q&A). PowerPoint "OCS Sprint 6 Demo."                                                                                                                                                               |
| **Initial Product Spec - MVP.md**                  | `product`     | DRAFT spec: 3 objectives (production platform, reusable capabilities, superior UX), 20 functional requirements, 6 NFRs. **20+ tribal recipients target.** Metrics gap as strategic driver. "Not Doing" section empty. ATO inheritance flagged as unvalidated assumption.                  |
| **Risk Management.md**                             | `operations`  | Government shutdown continuity contact directory: 6 roles with emails. Identifies ISSO (Oyindasola), SCA (Beatrice), Login.gov liaison (Amanda Welch).                                                                                                                                    |
| **Technical Architecture & Security Framework.md** | `engineering` | Two architecture diagrams: application architecture (auth flows + export) and AWS infrastructure topology. Confirms Keycloak as dev mock.                                                                                                                                                 |
