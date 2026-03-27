# ITB - CSFEER: IPT Kickoff Meeting (2026-01-13)

## Summary

Initial Integrated Project Team (IPT) kickoff between ACF Tech and Focus (the delivery vendor). Establishes the infrastructure path: CSFEER will deploy into ACF's NGSC (Next Generation Secure Cloud) AWS environment with an inherited ATO strategy. Key integration dependencies are Okta-mediated Login.gov auth and OLDC for existing user data. The team has approximately one year to production.

---

## Infrastructure & Deployment (NGSC)

- **Target environment:** ACF's NGSC AWS. Django + Postgres already approved within NGSC.
- **Environments to provision:** Dev/Test, Stage, Prod (lower and upper).
- **Developer access:** PIV cards + GFE required for NGSC access; Zscaler for network access management. Focus engineers were in-process or had received PIVs as of kickoff.
- **Parallel development:** Focus team continues building in their own environment while NGSC provisioning proceeds -- acknowledged as a timeline risk mitigation.

> **Addition vs. core context:** Core context does not mention NGSC, GFE/PIV requirements, or the parallel-environment development strategy. These are operationally significant for CI/CD pipeline design and deployment automation.

## Security & ATO

- **Strategy:** Inherit existing NGSC security controls / ATO rather than pursuing a full standalone ATO. Phased documentation approach: start with System Registration form (for UUID) and Privacy Impact Analysis (PIA).
- **PIA trigger:** System collects email addresses.
- **Status at kickoff:** Intake form completed; System Registration form and PIA still pending (owned by Oyindasola Akisanmi).

> **Refinement vs. core context:** Core context says "must achieve ATO within 18 months." This meeting reveals the *strategy* is ATO inheritance from NGSC, not a ground-up ATO, which significantly reduces the compliance surface area.

## Authentication

- **Login.gov integration path:** Okta serves as the identity broker for Login.gov (not a direct OIDC integration).
- **Provisioning:** ServiceNow ticket process for user setup.
- **Key contacts:** Jim Cooper (Okta), Matt (new Okta engineer), Elsie (BA, Operations team -- facilitates integration).

> **Clarification vs. core context:** Core context lists "Login.gov auth" and codebase has `csfeer/backends.py` (OIDC backend). The meeting reveals an Okta intermediary layer. This is architecturally relevant -- the OIDC relying party is Okta, not Login.gov directly.

> **Risk -- Keycloak update:** Keycloak is being replaced with something else (rated low impact). This could affect the mock-oauth setup used in local dev (`compose.yml`).

## Data Integration

- **Pre-population:** System must ingest previous years' data for form pre-population (confirms core context).
- **External user data:** OLDC (likely the existing OCS grants management system) holds user records. CSFEER creating users in isolation from OLDC is flagged as a **medium-risk issue**. Mitigation: API integration to import existing users.
- **Data exposure:** APIs being built to expose all database data. Two-way data flow: PDF export and API access.
- **Data liaison:** Thomas Oldfield (ACF Tech) for data structure questions.

> **Addition vs. core context:** OLDC integration is not mentioned in core context. This is a key dependency for user onboarding and possibly for grant recipient metadata.

## Timeline & Risks

| Risk                                       | Impact | Notes                                    |
| ------------------------------------------ | ------ | ---------------------------------------- |
| ~1 year to contractual production deadline | High   | Stated in meeting notes                  |
| NGSC provisioning delay                    | Medium | Mitigated by parallel dev environment    |
| User data isolation from OLDC              | Medium | Requires API integration                 |
| ATO process delay                          | Medium | Mitigated by ATO inheritance strategy    |
| Keycloak being replaced                    | Low    | Monitor; may affect local dev mock-oauth |

## Team & Governance

- **Cadence:** Weekly IPT meetings established.
- **Focus team (vendor):** Phaedra (Product Lead), Mohammad Taleb (Tech Lead), Tshering Yudon (Lead Designer), Ryan Bagwell (Engineer). Two additional engineers added: ryan.bagwell, logan.ricard.
- **ACF Tech:** Jody Smith (CTR, meeting coordination), Thomas Oldfield (data), Katherine Chase (CTR, NGSC/infra), John Warren, Oyindasola Akisanmi (CTR, security/ATO).
- **Pending additions to IPT:** DBA team member, NGSC engineer.

## Open Action Items (as of 2026-01-13)

- System Registration form for UUID (Oyindasola)
- PIA form (Oyindasola)
- Review completed intake form (Oyindasola)
- Invite DBA + NGSC engineer to IPT calls (Katherine Chase / Elsie)
- Provide software version requirements for NGSC (Katherine Chase)
- Send list of required external system data (Mohammad Taleb)
- Coordinate Okta/Login.gov integration via ServiceNow (Focus Team / Jim Cooper)
