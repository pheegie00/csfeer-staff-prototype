# **PRODUCT SPEC — CORE (CSFEER) Tribal MVP**

**Version:** 2.0 **Date:** Nov 17, 2025 

**Authors:** [Phedra Arthur](mailto:phedra.arthur@focusconsulting.io)  
**Status:** Draft  
**Stakeholders:** OCS Program, ACF OCIO, Engineering, Design, Product, Security

---

# **1\. PROBLEM SUMMARY**

Tribal CSBG grantees currently complete required pre-award and post-award reporting through fragmented, manual processes involving PDFs, Word documents, Excel sheets, OLDC uploads, and email-based collaboration. Many Tribal organizations operate in **low-bandwidth, rural environments**, further complicating data submission.

This workflow is slow, error-prone, and disproportionately impacted by rural connectivity challenges and limited staffing capacity. Today, it’s estimated that it takes many Tribal organizations **12–20 days** to complete and submit a single CSBG Tribal Plan or Annual Report due to data gathering delays, offline drafting, leadership approval cycles, inconsistent upload workflows, and repeated correction requests from OCS. 

The lack of telemetry across existing systems means OCS has **no measurable insight** into workflow efficiency, error patterns, or user burden. The CORE Tribal MVP solves these problems by delivering a secure, resilient, digital forms platform that simplifies data entry, improves data quality, supports low-connectivity environments, and provides the first measurable baseline for Tribal reporting performance.

1800 hours (looking through instructions, reviewing, staff)

---

# **2\. GOALS & NON-GOALS**

## **2.1 Goals (What MVP MUST achieve)**

* Digitize the **three Tribal OMB-approved forms** (Plan & Application, Annual Report, Annual Report Short Form).

* Provide secure authentication via **Login.gov** and role-based access.

* Enable users to **save, submit, unsubmit, and resubmit** forms with audit history.

* Implement **form validation** (math, required fields, logic branches).  
* Provide **read-only APIs** (ACF Access)

* Provide **CSV and PDF exports**

* Deliver**\-resilient** behavior to prevent data loss in low-bandwidth environments.

* Meet **FISMA Moderate**, **FedRAMP hosting**, and **Section 508/WCAG 2.0 AA** requirements.  
* Establish baseline telemetry and metrics for user experience, performance, and data quality

* Provide training, help desk support, and necessary ATO documentation.

## **2.2 Non-Goals (Intentional Exclusions for MVP)**

* Low-code/no-code form builder.

* Dashboards, analytics, visualizations.  
* Mobile apps.  
* State/Territory forms (Phase II).  
* Legacy system retirement (Phase III).  
* SmartSheets or third-party integrations not required by contract.

---

# **3\. USERS & USE CASES**

[ACF Forms Engine - User Personas](https://docs.google.com/document/d/1qi_XQ__PA1YdEFzrYR8CaIzjxS5rx6Ccw02EnUTySnM/edit?usp=sharing) //under construction

## **3.1 Users**

Primary Roles (currently)

* **Authorized official** (needs to be on all the forms \- SF424)  
* **Grant Administrator** 

Other Roles

* **Tribal Contributors** – enter form data  
* **Tribal Approvers** – review, attest, and submit  
* **Tribal Viewers** – leadership / council read-only / sign-off  
* **OCS Program Officers** – review submissions, export data, access APIs  
* **Administrators (ACF \+ Contractor)** – manage accounts, view logs, maintain system

## **3.2 Primary Use Cases**

* Start/edit/save a form  
* Approve and submit forms  
* Automatically validate data  
* Submit and revise reports  
* Export submissions (CSV/PDF)  
* OCS reviews and retrieves data via API  
* Users operate reliably despite poor connectivity  
* Authorized official inputs data that is then pre-populated into the forms  
  * UEI may be a way to carry this data over

---

# **4\. REQUIREMENTS (Functional & Nonfunctional)**

## **4.1 Functional Requirements**

* **FR1 – Authentication:** Login.gov for Tribal users; ACF-approved SSO for staff.  
* **FR2 – Role-based access:** Contributor, Approver, Viewer, Admin roles.  
* **FR3 – Form lifecycle:** Create, edit, save draft, submit, unsubmit, resubmit.  
* **FR4 – Auto-save \+ local caching** for low connectivity.  
* **FR5 – Validation engine:** required fields, math checks, logic branching.  
* **FR6 – Pre-population** using previous-year data where applicable.  
* **FR7 – File uploads** where required by OMB forms.  
* **FR8 – CSV and PDF export** for users and OCS staff.  
* **FR9 – Read-only APIs** with OpenAPI documentation.  
* **FR10 – Audit trails:** timestamps, version history, submission logs.  
* **FR11 – Section 508 compliance:** screen reader support, keyboard navigation.  
* **FR12 – Admin console** for user/role management and system monitoring.

## **4.2 Nonfunctional Requirements**

* **NFR1 – Performance:** form load/save ≤ 3 seconds on typical 4G.  
* **NFR2 – Scalability:** ≥ 200 concurrent users.  
* **NFR3 – Reliability:** ≥ 99.5% uptime (excluding maintenance).  
* **NFR4 – Security:** FISMA Moderate, FedRAMP hosting, FIPS 140-2 encryption.  
* **NFR5 – Browser support:** Modern Chrome, Firefox, Edge, Safari.  
* **NFR6 – Responsive design:** optimized for tablets and laptops.

---

# **5\. LOW CONNECTIVITY BEHAVIOR** 

Low-connectivity behavior is required by the contract, **not** full offline editing.

MVP behavior includes:

* Automatic incremental saves when connected.  
* Temporary **local browser storage (IndexedDB/localStorage)** to prevent loss of work during connection drops.  
* Syncing cached data to the server upon reconnection.  
* Clear indicators:

  * “Saved”

  * “Connection lost—your work is stored locally”

  * “Reconnected—sync successful”

Goal: **Users in rural areas never lose work**, even with intermittent internet.

---

# **6\. USER EXPERIENCE & FLOW SUMMARY**

**High-Level Workflow (placeholder for [Tshering Yudon](mailto:tshering.yudon@focusconsulting.io)):**

`User logs in (Login.gov) →` 

`Screener→` 

`Selects Tribal Form or presented with best form based on answers →` 

`Form opens with pre-populated fields →` 

`User edits fields →` 

`Auto-save triggers as they progress →` 

`If connection drops → local cache stores changes →` 

`Connection resumes → data syncs to server →` 

`User validates → submits →` 

`Approver reviews → final submission →` 

`OCS exports or pulls via API.`

Design uses **USWDS 3.x**, progressive disclosure, clear labels, mobile-resilient layouts.

---

# **7\. DEPENDENCIES & RISKS**

### **Dependencies**

* Login.gov integration  
* ACF internal auth provider for staff  
* ACF AWS hosting environment & access patterns  
* ATO timelines and control requirements  
* OMB-approved forms and policy interpretations  
* OCS availability for validation logic review

### **Risks**

* Shutdown-related delays in ATO/governance (this can happen again in January)  
* Tribal connectivity variability impacting testing  
* Unclear legacy data structure for pre-population  
* OCS reliance on API integrations requiring extra review  
* Potential expansion of scope without clear change control  
* Submission attestation / signature workflow clarity  
* Policy interpretations affecting form logic

---

# **8\. MVP → V1 ROADMAP**

### **MVP (Contract Required)**

* 3 OMB-approved Tribal forms  
* Login.gov auth  
* Role-based access  
* Save/submit/unsubmit/resubmit  
* Validation \+ prepopulation (available data only)  
* Resilient auto-save \+ caching  
* Read-only APIs  
* CSV/PDF exports  
* Admin panel \+ audit trails  
* 508 & FISMA Moderate compliance  
* Tribal \+ OCS training, help desk  
* ATO documentation baseline  
* Out of system touchpoints (ex: PDFs, Signed forms to upload as part of app)

### **V1 (Post-MVP Enhancements)**

* Improved offline capability  
* Full submission dashboards for OCS  
* Batch export tools  
* Enhanced reporting UX  
* Expanded support materials  
* Better analytics for ACF staff

---

# **9\. OUT OF SCOPE (Not Required in MVP)**

### 

### **Functionality NOT included in MVP**

 ❌ Low-code form builder  
 ❌ Dashboards/analytics  
 ❌ SmartSheets or external integrations  
 ❌ Automated workflows beyond simple submit/unsubmit  
 ❌ Mobile apps  
 ❌ Legacy system decommissioning  
 ❌ SFTP or EDW pipelines  
 ❌ Bulk data migration  
 ❌ State/Territory forms

### **Forms NOT included in MVP**

❌ CSBG State & Territory Plan  
 ❌ CSBG Eligible Entity List  
 ❌ CSBG Annual Report 3.0  
 ❌ All other OCS/ACF program forms

### **Program Activities Out of Scope**

❌ Mandatory government-wide migration  
 ❌ Tribal outreach campaigns beyond training/help desk  
 ❌ Enterprise analytics or reporting systems

# **10\. METRICS STRATEGY: MVP VS FORMS ENGINE**

## **10.1 MVP Metrics**

**Adoption & Submission**

* ≥ 75% Tribal orgs submit digitally  
* 100% pilot orgs successful submission  
* ≥ 90% submissions pass validation without OCS help

**Performance**

* Load/save ≤ 3s  
* Uptime ≥ 99.5%

**Connectivity Resilience**

* Autosave success ≥ 98%  
* 0% data loss

**User Experience**

* Satisfaction ≥ 4/5  
* ≤ 1 help desk ticket per org

**Data Quality**

* ≥ 85% errors resolved without OCS  
* 30% reduction in OCS follow-up emails

---

## **10.2 Long-Term Forms Engine Metrics**

**Platform Growth**

* Increase in programs/forms onboarded  
* % of States/Territories opting in

**Configurability**

* New form configuration ≤ 6 weeks  
* ≥ 70% component reuse

**Operational Efficiency**

* OCS review time reduced ≥ 50%  
* Error rate reduced ≥ 60%

**Integration Maturity**

* % of data accessed via API  
* API uptime ≥ 99.9%

**Scalability**

* Support 5–10× users  
* Submission latency ≤ 2 seconds

---

# **11\. CURRENT STATE METRICS GAP**

The existing Tribal CSBG reporting process—spanning PDFs, Word docs, Excel, OLDC, and email—collects **no telemetry** on user behavior, performance, or data quality. OCS cannot measure:

* Time to complete a form  
* Which sections create the most errors  
* How often users lose work  
* Submission cycle timelines  
* How often users must resubmit  
* Help desk issues tied to specific steps

CORE will be the **first platform** to provide measurable, structured data on Tribal reporting workflows.

---

# **12\. BASELINE ESTABLISHMENT PLAN (First 90 Days)**

**User Interaction**

* Sessions per submission  
* Time per section  
* Autosave frequency & success  
* Sync patterns during reconnect

**Submission Quality**

* Validation error types & frequency  
* Resolution rates  
* Submit → unsubmit cycles

**Performance**

* Load times  
* Save/sync times  
* Export performance

**Operational**

* Ticket volume  
* Time-to-resolution  
* OCS review time

These baselines guide future improvements and long-term modernization.

---

# **13\. LEGACY WORKFLOW TIME (CURRENT STATE)**

### **\*\*Tribal organizations currently require:**

# **👉 12–20 days to complete and submit one CSBG Tribal form\*\***

**Breakdown:**

* 1–3 days: locating correct forms and guidance

* 5–10 days: internal data gathering

* 3–5 days: offline drafting across multiple files

* 2–5 days: leadership review & signatures

* 1–2 days: OLDC upload \+ formatting

* 1–5 days: corrections and resubmissions

This is the baseline burden CORE aims to dramatically reduce.

---

# **14\. OKRs ALIGNED TO ACF PRIORITIES** 

# **OBJECTIVE 1: Reduce administrative burden for Tribal Nations**

* KR1.1 Reduce time from 12–20 days → 3–7 days → less than an hour (maybe)  
* KR1.2 ≥ 75% Tribal adoption  
* KR1.3 ≥ 30% reduction in corrections  
* KR1.4 Satisfaction ≥ 4/5

---

## **OBJECTIVE 2: Improve data quality & program integrity**

* KR2.1 ≥ 90% submissions pass validation  
* KR2.2 ≥ 20% increase in year-over-year consistency  
* KR2.3 ≥ 30% reduction in OCS follow-up  
* KR2.4 OCS review time reduced ≥ 25%

---

## **OBJECTIVE 3: Deliver an accessible, secure, modern experience (21st Century IDEA)**

* KR3.1 Full Section 508/WCAG 2.0 AA compliance  
* KR3.2 Load/save ≤ 3 seconds  
* KR3.3 Autosave success ≥ 98% with 0% data loss  
* KR3.4 System uptime ≥ 99.5%  
* KR3.5 Zero critical vulnerabilities

---

## **OBJECTIVE 4: Establish a scalable forms engine**

* KR4.1 70% component reuse  
  KR4.2 New form configuration ≤ 6 weeks  
* KR4.3 Capture full telemetry  
* KR4.4 Scalability to 5–10× users  
* KR4.5 API uptime ≥ 99.9%

---

## **OBJECTIVE 5: Strengthen trust & partnership with Tribal Nations**

* KR5.1 Usability testing with ≥ 9 Tribal orgs (max)  
* KR5.2 Incorporate ≥ 80% Tribal feedback into UX  
* KR5.3 ≥ 90% helpfulness rating for help content  
* KR5.4 Zero instances of data loss during reporting cycles

---

