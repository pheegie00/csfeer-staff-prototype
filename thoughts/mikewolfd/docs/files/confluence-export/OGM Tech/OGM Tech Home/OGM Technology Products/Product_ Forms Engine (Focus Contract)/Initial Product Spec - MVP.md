---
designer: Tshering Yudon (CTR)
developers: Mohammad Taleb (CTR)
document_owner: Phedra Arthur (CTR) <br/>
document_status: DRAFT
reviewers: Minette Galindo (FED) Amanda Welch (CTR) Liane Peng (FED) Melanie Durley
  (FED) Kayla Lennon (FED) Mark Levy (FED) Thomas Oldfield (FED) Michael Chelen (FED)
  Ryan Bagwell (CTR) Mohammad Taleb (CTR) Logan Ricard (CTR) <br/>
tags:
  - '#requirements'
target_release: Version 2.0
---

[OGM Technology Products](../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../Product_%20Forms%20Engine%20(Focus%20Contract).md)

# Initial Product Spec - MVP

## Goals

\*Note these are ideas, we want to work with our client's to better define success

# **OBJECTIVE 1:** Deploy a production-ready forms platform that replaces all three PDF-based Tribal CSBG reporting processes.

Key Results:

- All three Tribal forms live in production
- Full end-to-end workflow supported
- 20+ Tribal grant recipients submit via CORE without reverting to PDFs

## **OBJECTIVE 2:** Build reusable platform capabilities that demonstrate the forms engine can scale beyond Tribal forms.

Key Results:

- [Login.gov](http://Login.gov) authentication, role-based access, PDF + CSV exports operational
- Platform supports both simple and complex forms
- Architecture documentation complete for Phase II

## **OBJECTIVE 3:** Deliver superior user experience while meeting federal compliance requirements.

Key Results:

- ≥80% of users report digital experience is easier than PDFs
- 100% Section 508 compliance
- Zero ACF OCIO security or compliance findings

## Background and strategic fit

Tribal CSBG grantees currently complete required pre-award and post-award reporting through fragmented, manual processes involving PDFs, Word documents, Excel sheets, OLDC uploads, and email-based collaboration. Many Tribal organizations operate in **low-bandwidth, rural environments**, further complicating data submission.

This workflow is slow, error-prone, and disproportionately impacted by rural connectivity challenges and limited staffing capacity. Today, it’s estimated that it takes many Tribal organizations **12–20 days\* (need to quantify 1800 hours in relation to our piece)** to complete and submit a single CSBG Tribal Plan or Annual Report due to data gathering delays, offline drafting, leadership approval cycles, inconsistent upload workflows, and repeated correction requests from OCS. 

The lack of telemetry across existing systems means OCS has **no measurable insight** into workflow efficiency, error patterns, or user burden. The CORE Tribal MVP solves these problems by delivering a secure, resilient, digital forms platform that simplifies data entry, improves data quality, supports low-connectivity environments, and provides the first measurable baseline for Tribal reporting performance.

## Assumptions



## Requirements

|   # | Title                                                                  | User Story   | Importance   | Notes              |
|----:|:-----------------------------------------------------------------------|:-------------|:-------------|:-------------------|
|   1 | Start a form                                                           |              |              | <ul><li></li></ul> |
|   2 | Edit a form                                                            |              |              |                    |
|   3 | Save a form                                                            |              |              |                    |
|   4 | Approve a form                                                         |              |              |                    |
|   5 | Submit a form                                                          |              |              |                    |
|   6 | Automatically validate data (validation engine)                        |              |              |                    |
|   7 | Submit report                                                          |              |              |                    |
|   8 | Revise report                                                          |              |              |                    |
|   9 | Review data via API                                                    |              |              |                    |
|  10 | Retrieve data via API                                                  |              |              |                    |
|  11 | Export CSV                                                             |              |              |                    |
|  12 | Export PDF                                                             |              |              |                    |
|  13 | Operate reliably despite poor connectivity (Auto save + local caching) |              |              |                    |
|  14 | Pre-population of data available into the form                         |              |              |                    |
|  15 | Authentication login.gov tribal users                                  |              |              |                    |
|  16 | Authentication ACF SSO for staff                                       |              |              |                    |
|  17 | Role based access                                                      |              |              |                    |
|  18 | File upload where required for OMB forms                               |              |              |                    |
|  19 | Audit trails                                                           |              |              |                    |
|  20 | Compliance (ex: 508)                                                   |              |              |                    |

## NFRs

- **NFR1 – Performance:** form load/save ≤ 3 seconds on typical 4G.
- **NFR2 – Scalability:** ≥ 200 concurrent users.
- **NFR3 – Reliability:** ≥ 99.5% uptime (excluding maintenance).
- **NFR4 – Security:** FISMA Moderate, FedRAMP hosting, FIPS 140-2 encryption.
- **NFR5 – Browser support:** Modern Chrome, Firefox, Edge, Safari.
- **NFR6 – Responsive design:** optimized for tablets and laptops.

## User interaction and design

## Current State Metrics Gap

- Time to complete a form
- Which sections create the most errors
- How often users lose work
- Submission cycle timelines
- How often users must resubmit
- Help desk issues tied to specific steps

## Potential Metrics

**User Interaction**

- Sessions per submission
- Time per section
- Autosave frequency & success
- Sync patterns during reconnect

**Submission Quality**

- Validation error types & frequency
- Resolution rates
- Submit → unsubmit cycles

**Performance**

- Load times
- Save/sync times
- Export performance

**Operational**

- Ticket volume
- Time-to-resolution
- OCS review time

## Questions

Below is a list of questions to be addressed as a result of this requirements document:

| Question                                                                                                                                    | Outcome   |
|:--------------------------------------------------------------------------------------------------------------------------------------------|:----------|
| When can we have access to ACF AWS + Github?                                                                                                |           |
| What is the ACF's AWS deployment method (Kubernetes vs ECS)?                                                                                |           |
| What's the source, format, and location of previous years data?                                                                             |           |
| We need to validate the assumption that we can inherit the existing ATO for current infra & we're doing more of <br/> an impact assessment. |           |
| Access to gov login                                                                                                                         |           |

## Not Doing
