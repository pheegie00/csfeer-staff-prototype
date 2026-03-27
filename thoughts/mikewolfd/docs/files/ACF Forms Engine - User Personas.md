# Tribal User

## **A. Tribal Users (Contributors / Approvers / Viewers)**

### **1\. “Angela Whitefeather” – Tribal CSBG Program Manager (Approver)**

**Role & context**

* Title: CSBG Program Manager

* Org: Small tribal government serving \~2,500 members

* Location: Rural; spotty broadband, staff often share office space and devices

* Access level: **Approver** – responsible for final submission and attestation

**Goals**

* Submit the **Tribal Plan & Application**, **Annual Report**, and **Short Form** on time with accurate data that aligns with the tribe’s priorities and SF-424M submission. [Administration for Children and Families+1](https://acf.gov/sites/default/files/documents/ocs/CSBG-Tribal-Annual-Report-OLDC-Instructions_1.pdf?utm_source=chatgpt.com)

* Avoid back-and-forth corrections with OCS due to missing or inconsistent information.

* Keep leadership and council informed with easy-to-share summaries/PDFs.

**Behaviors & workflow**

* Starts from internal planning docs and the **CSBG Tribal Plan Toolkit** or webinar slides to understand what’s changed this year. [Administration for Children and Families+1](https://acf.gov/ocs/toolkit/csbg-tribal-plan-and-reporting-toolkit?utm_source=chatgpt.com)

* Coordinates with finance and program staff for different sections of the Plan and Annual Report (outcomes, budget, narrative).

* Needs to **pause work frequently** to attend meetings, chase signatures, or get council approvals (e.g., transmittal letter/attestation).

* Cross-checks data with the **SF-424M** and other forms in OLDC to ensure consistency (award amount, DUNS/UEI, project period, etc.). [NASCSP+1](https://nascsp.org/wp-content/uploads/2019/08/TTA_CSBG_Web-Submitting-SF-424M_FY2020.pdf?utm_source=chatgpt.com)

* Often prints or exports a **PDF copy** for internal review, leadership sign-off, and local records.

**Pain points**

* Fear of losing work when internet drops mid-entry; OLDC-style forms feel brittle and unforgiving. [Grants Solutions](https://home.grantsolutions.gov/home/recipient-oldc-training-resources/?utm_source=chatgpt.com)

* Confusion when the same information appears in multiple places (SF-424M vs Tribal Plan vs internal budget).

* Tight deadlines and small staff; if one person is out, everything slips.

**Design implications**

* **Resilient auto-save \+ local caching** to avoid data loss during intermittent connectivity.

* Clear **“Approver view”** that surfaces: attestation section, signature/transmittal instructions, deadline status.

* Easy **PDF export** that looks like a formal submission for internal approval and records.

* In-context guidance (“What you enter here should match your SF-424M in OLDC”).

# Tribal Data Finance Specialist

### **2\. “David Lonebear” – Tribal Data/Finance Specialist (Contributor)**

**Role & context**

* Title: Grants & Finance Analyst

* Org: Mid-size tribal consortium administering multiple federal grants

* Access level: **Contributor** – fills in quantitative and narrative sections but does not submit

**Goals**

* Compile accurate **program, financial, and outcome data** for CSBG reports.

* Reuse data from last year or other systems to reduce re-keying.

* Validate numbers before the Program Manager reviews.

**Behaviors & workflow**

* Works heavily in **Excel**, local accounting systems, and prior-year PDFs to pull numbers and narratives.

* Frequently toggles between CORE, OLDC, and internal spreadsheets. [Administration for Children and Families+1](https://acf.gov/sites/default/files/documents/ocs/CSBG-Tribal-Annual-Report-OLDC-Instructions_1.pdf?utm_source=chatgpt.com)

* Starts a form early, then returns multiple times as new data comes in from sub-programs.

* Uses error messages and validation checks as a cue that something is off (e.g., totals don’t match funding amount).

**Pain points**

* Manual re-entry of stable data (organization info, contact, some budget lines) every year.

* Unclear which fields are *required*, which are optional, and which will cause a submission to be rejected.

* It’s hard to see “what changed from last year” when leadership asks.

**Design implications**

* **Pre-populate** stable data (org, contacts, some budget baseline) and clearly mark it as editable vs locked.

* **Inline validation** with clear explanations (“Total of Sections A–C must equal your CSBG award amount”).

* Visual indicators for changed fields vs last year (“New / Changed since FY24”).

* Strong **draft support**: David can save partial sections and come back without breaking the form.

# OCS Program Officers

## **B. OCS Program Officers**

### **4\. “Jonathan Reyes” – OCS CSBG Tribal Program Specialist**

**Role & context**

* Title: CSBG Tribal Program Specialist

* Org: Office of Community Services, ACF

* Portfolio: 15–25 Tribal grantees, multiple time zones

* Tools: OLDC, email, CSBG annual report toolkit and performance management website, Excel. [Administration for Children and Families+1](https://acf.gov/ocs/toolkit/csbg-annual-report-toolkit?utm_source=chatgpt.com)

**Goals**

* Ensure each Tribal grantee **submits required reports on time** via the designated system. [Administration for Children and Families+1](https://acf.gov/ocs/policy-guidance/acf-ocs-csbg-25-02-tribal-annual-report-submission-fy24?utm_source=chatgpt.com)

* Check that submissions meet **OMB and statutory requirements** (completeness, internal consistency). [Federal Register+1](https://www.federalregister.gov/documents/2024/04/23/2024-08668/proposed-information-collection-activity-community-services-block-grant-csbg-model-tribal-plan-and?utm_source=chatgpt.com)

* Quickly access data for **monitoring, TA, and policy memos**.

**Behaviors & workflow**

* Monitors upcoming deadlines (e.g., Tribal Plan due dates; Annual Report due March 31). [Administration for Children and Families+1](https://acf.gov/ocs/policy-guidance/acf-ocs-csbg-25-02-tribal-annual-report-submission-fy24?utm_source=chatgpt.com)

* Reviews submissions in batches, often exporting data to CSV or Excel for comparisons and performance management work. [HHS+1](https://www.hhs.gov/sites/default/files/acf-community-services-block-grant-performance-management.pdf?utm_source=chatgpt.com)

* Uses data to identify outliers (e.g., major year-over-year changes) and follows up with grantees.

* Responds to grantee emails about technical issues, missing fields, or policy questions.

**Pain points**

* OLDC is **clunky** for data review; it wasn’t built for easy comparison or performance analysis. [HHS+1](https://www.hhs.gov/sites/default/files/acf-community-services-block-grant-performance-management.pdf?utm_source=chatgpt.com)

* Difficult to get a portfolio-level view: Which tribes are on track, late, or have incomplete submissions?

* Back-and-forth emails to clarify simple data issues that could have been caught by validation.

**Design implications**

* For MVP:

  * A **staff view** that shows status of each Tribal grantee (Not Started / In Progress / Submitted / Needs Correction).

  * Robust **validation** to catch obvious data issues before submission, reducing manual follow-up.

  * **CSV export** for Jonathan to do his own analysis, plus read-only APIs for future integration with CSBG performance tools. [HHS+1](https://www.hhs.gov/sites/default/files/acf-community-services-block-grant-performance-management.pdf?utm_source=chatgpt.com)

* Easy access to **submission history** when responding to grantee questions or preparing TA.

# Executive Asst \+ Council Liaison

### **3\. “Marissa Greyhawk” – Executive Assistant / Council Liaison (Viewer)**

**Role & context**

* Title: Executive Assistant to Tribal Chair

* Org: Tribal leadership office

* Access level: **Viewer** – needs to see submissions and attachments but does not directly edit

**Goals**

* Make sure Tribal leadership can **review and understand** what’s being submitted under CSBG.

* Coordinate signatures for transmittal letters and attestations.

* Keep a local archive of submissions for audits and council meetings.

**Behaviors & workflow**

* Logs in mainly **around deadlines** to download PDFs or summaries.

* Prints or emails exports to internal stakeholders (Chair, Council, CFO).

* Tracks whether required signature materials (e.g., transmittal letter) have been uploaded or are still pending.

**Pain points**

* Hard to find “the latest version” when relying on emails and multiple PDFs.

* Forms are dense, full of federal jargon; leadership wants a simpler high-level view.

**Design implications**

* Simple **read-only dashboard**: “Status by form” (Not Started / In Progress / Ready for Approval / Submitted).

* **PDF export** and maybe a one-page summary view (e.g., funding amount, major goals, key outcomes).

* Clear indication of whether required attachments have been uploaded.

---

* 

# ACF Records \+ System Administrator

## **C. Administrators (ACF \+ Contractor)**

### **5\. “Niki Frazier”– ACF Records / System Administrator**

*(Patterned after real OLDC contact roles in tribal plan tools — e.g., Senior Records Specialist / Project Lead providing OLDC support). [SPIPA+1](https://spipa.org/wp-content/uploads/2024/07/APP_FY25-CSBG-SPIPA-DRAFT-7_22_2024.pdf?utm_source=chatgpt.com)*

**Role & context**

* Title: Senior Records Specialist / System Administrator

* Org: OCS / ACF

* Responsibilities:

  * Manage user accounts and roles (Tribal & internal).

  * Oversee system records, retention, and compliance.

  * Coordinate with security and OCIO on ATO-related evidence.

**Goals**

* Ensure only authorized users can access the system and that roles are assigned correctly.

* Maintain a complete and auditable history of submissions and changes.

* Support smooth operations around key reporting dates (no outages, minimal escalations).

**Behaviors & workflow**

* Uses an **admin console** to:

  * Approve new Tribal users, deactivate old ones.

  * Update roles when staff change.

  * Reset accounts or troubleshoot access issues.

* Pulls system-level logs for **security audits and ATO artifacts**.

* Works closely with help desk / contractor when patterns of issues emerge (e.g., repeated login failures).

**Pain points**

* Current tools often require going into **multiple systems** (OLDC admin screens, email, spreadsheets) to piece together a user’s history.

* Manual account provisioning and de-provisioning is error-prone.

* Limited visibility into which features are causing most support tickets.

**Design implications**

* Admin console should make it easy to:

  * Search by org, person, email, UEI, etc.

  * Change roles and reset access in a **few clicks**, with audit logging.

  * See **high-level analytics** (e.g., failed logins, common validation errors) even if deep analytics are out of scope.

* Clear separation of **grantee vs internal staff accounts** to align with ACF security requirements.

# Contractor Support \+ Help Desk Liaison

### **6\. “Sri Patel” – Contractor Support / DevOps & Help Desk Liaison**

**Role & context**

* Title: Senior Dev/Support Engineer (Contractor)

* Org: Focus \+ CSFEER/CORE engineering team

* Responsibilities:

  * Handle Tier 2/3 technical issues escalated from help desk.

  * Monitor uptime, performance, and security alerts.

  * Support deployments and configuration changes in AWS.

**Goals**

* Keep the system stable, secure, and performant during peak usage (e.g., just before Tribal Plan and Annual Report due dates). [Administration for Children and Families+2Administration for Children and Families+2](https://acf.gov/ocs/policy-guidance/acf-ocs-csbg-25-02-tribal-annual-report-submission-fy24?utm_source=chatgpt.com)

* Quickly diagnose and resolve issues that affect multiple grantees.

* Provide engineering feedback on recurring usability issues that surface in support.

**Behaviors & workflow**

* Monitors logs and metrics around form saves, submissions, and authentication.

* Collaborates with product/design (you, Tshering, Mo) when patterns indicate confusing UI or validation rules.

* Works within **sprints** and uses product specs/user stories you generate to prioritize improvements.

* Helps maintain ATO-required documentation around changes and incidents.

**Pain points**

* Hard to reproduce issues in environments that don’t mirror **real-world low connectivity**.

* Ambiguity around whether bugs stem from policy/OMB form constraints, user error, or actual technical issues.

**Design implications**

* Clear and consistent **error codes and logs** for saves, submissions, and auth events.

* Robust, testable **validation rules** that can be unit-tested and traced when users report “it won’t let me submit.”

* Feature flags / configuration to handle policy changes without heavy redeploys.

