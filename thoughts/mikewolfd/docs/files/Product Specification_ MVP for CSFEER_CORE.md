# **Product Specification: MVP for CSFEER/CORE**

## **1\. Overview**

**System Name (tentative):** Community Outcomes Reporting Engine (CORE)  
 **Phase:** I – Tribal MVP (target cohort: up to 66 tribal organizations)  
 **Objective:** Replace legacy manual processes with a secure, user-centered, digital forms platform to streamline pre-award and post-award reporting for Tribal Community Services Block Grant (CSBG) recipients.

The MVP focuses on **three key forms**:

1. CSBG Tribal Plan and Application

2. CSBG Tribal Annual Report

3. CSBG Tribal Annual Report (Short Form)

## **2\. Goals and Success Metrics**

**Primary Goals**

* Simplify data submission for tribal organizations

* Improve federal staff’s ability to collect, validate, and analyze data

* Provide a scalable platform foundation for expansion in Phase II & III

**Success Metrics**

* ≥75% of participating tribes submit forms through the platform within Year 1

* Reduction in average form completion time by ≥25% compared to legacy method

* ≥90% of forms pass automated validation checks before submission

* User satisfaction score of ≥4/5 among pilot participants

## **3\. Core Features (MVP Scope)**

### **3.1 User Experience & Workflow**

* **Multi-user collaboration:** Allow multiple staff from one tribal organization to work on the same form concurrently.

* **Draft/save progress:** Users can save drafts and return later.

* **Unsubmit/resubmit:** Flexibility to revise and resubmit forms.

* **Notifications:** Email and in-app alerts for form availability, deadlines, and submission confirmations.

* **Role-based permissions:**

  * *Contributor* – can edit forms

  * *Approver* – can submit forms

  * *Viewer* – read-only access

### **3.2 Forms and Data Handling**

* **Form pre-population:** Automatically pull data from prior year submissions.

* **Field types:** Text, numbers, dates, file uploads, multi-select, conditional branching.

* **Validation engine:**

  * Required field checks

  * Mathematical consistency (e.g., totals)

  * Comparison with previous year’s data

  * Soft warnings (recommendations) vs. hard errors (blocking submission)

* **Version control:** Retain historical versions of forms with timestamped submission records.

### **3.3 Technical Requirements**

* **Authentication:** Login.gov integration for all users.

* **Data export:** CSV and PDF exports for recipients and OCS staff.

* **APIs:** Read-only endpoints for ACF staff to extract data.

* **Accessibility:** WCAG 2.0 AA compliance; Section 508 conformance.

* **Design system:** U.S. Web Design System (USWDS).

* **Hosting:** FedRAMP-certified ACF AWS environment.

## **4\. Non-Functional Requirements**

* **Security:** FISMA Moderate; encryption at rest and in transit (FIPS 140-2).

* **Performance:** Form load and save actions ≤ 3 seconds under normal conditions.

* **Scalability:** Support at least 200 concurrent users (headroom for tribal cohorts).

* **Reliability:** System availability ≥ 99.5% uptime.

## **5\. User Cohorts (MVP Scope)**

* **Primary Users:** Staff from 66 tribal organizations receiving CSBG funding.

* **Secondary Users:** OCS program officers reviewing submissions.

* **Support Users:** System admins (contractor \+ ACF IT).

## **6\. Governance & Compliance**

* **Project Governance:** Aligned with ACF OCIO Governance Framework.

  * Project Management Plan (PMP)

  * Bi-weekly dashboards

  * Monthly CSRs

  * Mid-year performance reports

* **ATO Path:** Achieve ATO within 18 months (MVP compliance with core controls in place).

## **7\. Out of Scope (for MVP)**

* Low-code/no-code form builder (planned for post-Year 1).

* State/territory or other ACF program forms (Phase II & III).

* Advanced analytics and dashboards (beyond CSV/API exports).

* Legacy system retirement (planned after Phase III).

## **8\. Release Plan**

* **Months 1–2:** Discovery (user research with tribal orgs, form mapping, technical spikes).

* **Months 3–5:** Wireframes, prototypes, validation workshops.

* **Months 4–8:** MVP development (forms engine \+ 3 pilot forms).

* **Month 9:** MVP launch for tribal organizations (soft rollout).

* **Months 9–12:** Iteration based on feedback; stabilize platform.

## **9\. Acceptance Criteria**

* All three forms available digitally with validation and save/submit features.

* Login.gov authentication working for all pilot users.

* Forms exportable in CSV and PDF.

* At least 10 tribal organizations successfully submit reports through CORE within pilot period.

* Section 508 conformance verified (VPAT available).

