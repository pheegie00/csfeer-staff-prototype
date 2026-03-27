# ACF Project Brief -- Synthesized

ACF's project brief for CSFEER establishes the contract structure, governance obligations, security/compliance mandates, and phased rollout plan. The key engineering-relevant additions beyond core context are: a low-code form builder requirement after Year 1, an 18-month ATO deadline, a 24-month contract with ~4.75 FTE core team, and a long-term vision to scale beyond CSBG to 100+ forms across all ACF programs.

---

## Additions & Clarifications vs. Core Context

### Alternate System Name
The platform has a tentative public-facing name: **Community Outcomes Reporting Engine (CORE)**. CSFEER is the project name; CORE is the system name.

### Long-Term Scale Target
The forms engine is intended to eventually serve **all ACF program offices** -- not just OCS/CSBG. Target: **25,000+ recipients, 100+ forms**. Current scope (CSBG, ~1,100 users) is Phase I-III of a much larger vision.

### Low-Code Form Builder (Post Year 1)
After Year 1, the platform must include a **UI-based, low-code/no-code form builder** so non-technical staff can create and manage future forms. This is a significant architectural requirement -- the schema system must be designed to support visual authoring, not just developer-defined JSON/Pydantic schemas.

### Phase III: Full Migration + Legacy Sunset
Phase III involves **full migration of all users** and **sunsetting the legacy system**. This means the platform must handle data migration from existing systems and achieve feature parity with current PDF workflows.

### Phase II Detail: Opt-In + Legacy Parallel
During Phase II, states/territories **opt in** while the legacy process remains operational. The system must support dual-track operation (some users on legacy, some on CORE).

### Tribal Short Form
Phase I includes a **CSBG Tribal Annual Report [Short Form]** in addition to the full Tribal Annual Report. This is a distinct form variant not mentioned in core context.

---

## Contract & Staffing

| Attribute      | Value                                                         |
| -------------- | ------------------------------------------------------------- |
| Total period   | 24 months (12-month base + 12-month option)                   |
| Core team      | ~4.75 FTE                                                     |
| Surge capacity | 4 additional FTE                                              |
| Key personnel  | Product Manager (government approval for replacement)         |
| Work location  | Contractor facility; occasional travel for in-person meetings |

---

## Governance Obligations

- **Project Intake Form**: due within 5 days of contract award.
- **ACF OCIO Governance Framework**: Cross Function Team (CFT) meetings and Stage Gate Reviews.
- **Reporting cadence**: bi-weekly dashboard, monthly Contract Status Report (CSR), semi-annual Mid-Year Performance Summary.
- **Transition plan**: minimum 4 weeks (2 sprint cycles) for knowledge transfer at contract end.

---

## Security & Compliance (Engineering-Relevant)

| Requirement           | Detail                                                                                                         |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| ATO deadline          | 18 months from contract start                                                                                  |
| Compliance frameworks | FISMA, NIST SP 800-53, FIPS 199, OMB A-130                                                                     |
| Encryption            | FIPS 140-2 validated, in transit and at rest                                                                   |
| Cloud                 | FedRAMP-certified ACF AWS (GFE); contractor implements FedRAMP CRM                                             |
| Zero Trust            | Required per EO 14028; contractor must provide ZT strategy                                                     |
| CUI handling          | Per NIST standards for Controlled Unclassified Information                                                     |
| Personnel             | Background investigations, NDAs, annual security/privacy/records training                                      |
| Incident response     | Must comply with ACF IRT policy; report all suspected/confirmed incidents                                      |
| AI policy             | AI usage must comply with US law + ACF policy; federal data cannot train commercial AI models without approval |

---

## Accessibility

- Standard: **WCAG 2.0 Level AA** (Section 508).
- Contractor must provide **Accessibility Conformance Report (ACR)** via VPAT for any commercial ICT.
- Government reserves right to independently test; non-conforming items remediated at contractor expense.

---

## Notifications Requirement
The brief specifies **customizable, real-time alerts** for events like new form availability, submission rejection, and past-due deadlines. This implies a notification subsystem (email, in-app, or both) needs to be part of the architecture.

## Permissions Model Detail
Recipients should be able to **self-administer accounts** and assign roles (read-only, write-only, approve) at subrecipient, state, and federal levels. This is more granular than what core context describes.

## Version Control for Forms
The system must maintain **multiple simultaneous versions of a form** while preserving data from existing submissions, and provide **version history** for federal staff to review submission state at various points in time. This has schema and data model implications.

---

## Potential Contradictions / Notes

- Core context says "WCAG 2.0 Level AA" which matches the brief. However, WCAG 2.0 is outdated -- WCAG 2.1 or 2.2 AA is the current standard. The contractual obligation is 2.0 AA, but building to 2.1/2.2 AA is advisable.
- Core context mentions ~75 federal staff users; the brief does not specify a federal user count.
- The brief's "bi-weekly release cadence" aligns with but makes explicit what core context implies via agile methodology.
