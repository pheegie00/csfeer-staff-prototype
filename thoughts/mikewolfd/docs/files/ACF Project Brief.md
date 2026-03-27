# **Briefing Document: Community Services Forms Engine for Efficient Reporting (CSFEER)**

## **Executive Summary**

The Administration for Children and Families (ACF), through its Office of Community Services (OCS), is initiating the development of a modern, scalable, and user-centered digital forms platform named the Community Services Forms Engine for Efficient Reporting (CSFEER), with the tentative system name of Community Outcomes Reporting Engine (CORE). This project aims to fundamentally overhaul the grant reporting lifecycle for OCS grant recipients by replacing cumbersome and inefficient data collection processes with a streamlined digital solution.

The core problem addressed is the extensive and complex nature of current reporting forms, which require substantial out-of-system work from grant recipients and hinder the government's ability to efficiently collect, analyze, and report on programmatic outcomes. The CORE platform is envisioned to provide a user-friendly interface for data submission, store data in consistent and accessible formats (via API and CSV), and support the entire grant lifecycle from pre-award planning to post-award performance evaluation.

Development will follow a modern, agile methodology, leveraging Human-Centered Design (HCD) and a risk-reducing iterative approach. The project will launch with a Minimum Viable Product (MVP) targeted at a small cohort of tribal grant recipients before incrementally scaling to include state and territory users. The long-term vision is a robust "forms engine" capable of serving all ACF grant programs, potentially supporting over 25,000 recipients across more than 100 different forms.

This initiative is governed by stringent federal mandates for security, accessibility, and project management. The contractor must adhere to the ACF Office of the Chief Information Officer (OCIO) Governance Framework, achieve an Authority to Operate (ATO) within 18 months, and ensure the system is hosted within ACF's FedRAMP-certified AWS environment. Strict compliance with numerous security standards, including FISMA, NIST, and Zero Trust principles, is required, as is full conformance with Section 508 accessibility standards (WCAG 2.0 Level AA).

## **1\. Project Overview and Strategic Objectives**

### **1.1. Mission and Background**

The mission of the Administration for Children and Families (ACF) is to foster health and well-being through federal leadership and resources for human services. Within ACF, the Office of Community Services (OCS) works to reduce the causes and consequences of poverty by partnering with states, tribes, territories, and community-based organizations. In fiscal year 2022, OCS administered nearly $6.29 billion in funding across seven programs aimed at assisting vulnerable families and revitalizing communities. A fundamental component of this work involves the prudent administration of grants, which includes planning, data collection, evaluation, and performance measurement.

### **1.2. Core Problem Statement**

Current data collection from OCS grant recipients is a significant operational challenge. Recipients are legally required to submit extensive pre-award and post-award information using forms that are difficult to manage. Key issues with the existing process include:

* **Complexity and User Burden:** Forms feature a mix of free-text narratives and structured data, with complex validation rules that often require substantial out-of-system preparation.  
* **Data Inefficiency:** The current system makes it difficult to contextualize new data with historical submissions, track submissions and revisions, and automate data validation.  
* **Analytical and Reporting Hurdles:** Inconsistent data formats and compatibility issues from custom state or tribal reports make it challenging for federal staff to evaluate quantitative and qualitative data and report on programmatic outcomes to Congress and the public.

### **1.3. Project Vision and Objectives**

The CSFEER/CORE project aims to create a centralized, user-friendly digital platform that addresses the current system's deficiencies. The primary objectives are:

* **Streamline Data Collection:** Provide a single, intuitive interface for grant recipients to submit and manage all required pre-award and post-award information.  
* **Improve User Experience:** Design the platform with HCD principles to be intuitive for grant recipients, improving tracking, collaboration, and data entry.  
* **Enhance Data Quality and Accessibility:** Store collected data in a consistent, usable format, available via API endpoints and CSV exports, enabling real-time access and integration with other analytical tools.  
* **Achieve Scalability:** Build the initial system for a single OCS program with the explicit goal of creating a scalable "forms engine" that could eventually serve multiple ACF Program Offices, encompassing over 100 forms and 25,000 recipients.  
* **Increase Operational Efficiency:** Automate data validation, pre-population of data from previous years, and comparison to integrated data sources to reduce manual work for both recipients and federal staff.

## **2\. Scope of Work and Development Approach**

### **2.1. Methodology**

The project requires the contractor to employ a modern, integrated approach combining:

* **Human-Centered Design (HCD):** Continuous discovery, user research, and stakeholder engagement will drive the product roadmap and feature prioritization.  
* **Agile Software Development:** The system will be developed iteratively, with frequent releases to production, using standard agile practices like product roadmapping, backlog prioritization, and sprint planning.  
* **DevSecOps and CI/CD:** Development will incorporate best practices like "Infrastructure as Code," automated testing, and code reviews to ensure secure and efficient feature deployment.  
* **Open Source Preference:** The technology stack will preferably utilize standard, sustainable open-source libraries.

### **2.2. Phased Implementation Strategy**

To minimize risk, the platform will be launched in iterative phases, with the scope of each phase subject to change based on validated learning from user research.

| Phase | User Group | Estimated Users | Key Forms/Reports | Notes |
| :---- | :---- | :---- | :---- | :---- |
| **Phase I** | Tribes and Tribal Organizations | Up to 66 | • CSBG Tribal Plan and Application\<br\>• CSBG Tribal Annual Report\<br\>• CSBG Tribal Annual Report \[Short Form\] | First production launch, serving as the Minimum Viable Product (MVP). |
| **Phase II** | States and Territories | 53+ | • All Phase I forms\<br\>• CSBG Eligible Entity List\<br\>• CSBG State and Territory Plan\<br\>• CSBG Annual Report 3.0 | Incremental scaling where users can opt-in. The legacy process will remain operational. |
| **Phase III** | All Users | 1,100+ | All pre- and post-award forms | Full migration of all users to the new platform, followed by the sunsetting of the legacy system. |

### **2.3. Key Task Areas**

The Performance Work Statement outlines four primary task areas for the contractor:

1. **Discovery and Product Definition:** Conduct extensive user research with grant recipients and ACF staff to understand needs, identify pain points, and define user stories to guide development.  
2. **Design and Development of the MVP:** Build, test, and deploy an impactful MVP based on discovery findings, focusing initially on the three tribal forms outlined in Phase I.  
3. **Continuous Agile Development and Product Management:** After the MVP launch, iteratively develop and deploy additional features and functionalities based on user feedback and evolving priorities, managed through a bi-weekly release cadence.  
4. **Transition In/Out and Retrospective:** Ensure smooth knowledge transfer through comprehensive documentation, playbooks, and a transition plan to be executed over a minimum of four weeks (two sprint cycles).

## **3\. Key System Requirements and Features**

The PWS provides a non-exhaustive list of requirements that will serve as a starting point for development, subject to refinement through user research.

### **3.1. User Experience and Workflow**

* **Collaboration:** Allow multiple users from a grant recipient organization to work on forms, with workflow tools for routing, review, and re-submission.  
* **Flexibility:** Enable users to "unsubmit" forms, submit revisions, save progress, and return later.  
* **Automation:** Automatically create and pre-populate forms based on reporting schedules and previous submissions to show trends and reduce repetitive data entry.  
* **Notifications:** Provide customizable, real-time alerts for key events (e.g., new form available, submission rejected, past due).  
* **Permissions:** A flexible user management module allowing recipients to self-administer accounts and assign roles (e.g., read-only, write-only, approve) at the subrecipient, state, and federal levels.

### **3.2. Data and Form Functionality**

* **Field Types:** Support for manual data entry, auto-calculations, pre-populated data, file attachments, one-to-many responses, conditional fields, and branching logic.  
* **Validation:** A flexible validation engine capable of mathematical checks, comparisons to prior submissions, and displaying both hard errors and soft warnings at the field, group, and form levels.  
* **Version Control:** Maintain multiple simultaneous versions of a form while preserving data from existing submissions. Provide a robust version history for federal staff to review the state of a submission at various points.

### **3.3. Technical and Architectural Requirements**

* **Authentication:** Must integrate with Login.gov.  
* **Interoperability:** Provide a flexible API for interacting with forms and extracting data. Support data exports in CSV, PDF, and other human-readable formats.  
* **Accessibility & Design:** The front end must be Section 508 WCAG AA-compliant and utilize the United States Web Design System (USWDS).  
* **Low-Code Form Builder:** After Year 1, the platform should include a UI-based, low-code/no-code form builder to allow non-technical staff to create and manage future forms.  
* **Hosting:** The system must be hosted in the existing FedRAMP-certified ACF Amazon Web Services (AWS) environment. ACF will provide AWS capacity as Government Furnished Equipment (GFE).

## **4\. Governance, Security, and Compliance Mandates**

The project operates under a strict framework of federal regulations and agency-specific policies.

### **4.1. Project Governance and Reporting**

The contractor is required to adhere to the ACF OCIO Governance Framework. This includes submitting a Project Intake Form within five days of award and participating in Cross Function Team (CFT) meetings and Stage Gate Reviews. Required reporting includes:

* A comprehensive Project Management Plan (PMP).  
* Bi-weekly dashboard status reports.  
* A Monthly Contract Status Report (CSR).  
* A Mid-Year Performance Summary Report every six months.

### **4.2. Security Posture and Requirements**

The system must meet extensive security requirements to protect government information. Key mandates include:

* **Authorization:** Achieve an Authority to Operate (ATO) within 18 months of contract start.  
* **Compliance Frameworks:** Adhere to FISMA, NIST SP 800-53 (Security and Privacy Controls), FIPS 199 (Security Categorization), and OMB Circular A-130.  
* **Data Protection:** All government information must be protected to ensure its Confidentiality, Integrity, and Availability. Controlled Unclassified Information (CUI) must be handled according to specific NIST standards.  
* **Encryption:** All sensitive government data must be encrypted in transit and at rest using FIPS 140-2 validated solutions.  
* **Cloud Security:** The system and its hosting must be FedRAMP-compliant. The contractor is responsible for implementing the FedRAMP Customer Responsibility Matrix (CRM).  
* **Cybersecurity Modernization:** The contractor must provide a strategy for meeting the mandates of Executive Order 14028, including the adoption of a Zero Trust architecture.  
* **Personnel Security:** All contractor staff must undergo background investigations commensurate with their position sensitivity and sign Non-Disclosure Agreements (NDAs). Mandatory annual security, privacy, and records management training is required.  
* **Incident Response:** The contractor must comply with ACF's Incident Response Policy, reporting all suspected and confirmed incidents to the ACF Incident Response Team (IRT).  
* **Artificial Intelligence (AI):** If AI technology is employed, it must adhere to applicable U.S. laws and ACF policies, and federal information cannot be used to improve commercial AI models without approval.

### **4.3. Accessibility (Section 508\)**

All Information and Communications Technology (ICT) developed under this contract must comply with Section 508 of the Rehabilitation Act.

* **Standard:** The system must conform to Level A and Level AA Success Criteria of the Web Content Accessibility Guidelines (WCAG 2.0).  
* **Verification:** The contractor must provide an Accessibility Conformance Report (ACR) using the Voluntary Product Accessibility Template (VPAT) for any commercial ICT items.  
* **Validation:** The government reserves the right to perform its own testing to validate Section 508 conformance claims prior to acceptance. Any non-conforming products or services must be remediated at the contractor's expense.

## **5\. Contract and Personnel Details**

* **Period of Performance:** The contract has a total period of 24 months, structured as a 12-month base period and one 12-month option period.  
* **Place of Performance:** Work will be performed primarily at the contractor's facility. Occasional travel to agency worksites for in-person meetings may be required.  
* **Staffing:** The government envisions a core team of approximately 4.75 Full-Time Equivalents (FTEs) with an optional surge team of 4 FTEs.  
* **Key Personnel:** The Product Manager is designated as "Key Personnel." This individual must have a strong technical background and be experienced in agile software delivery, managing development teams, building roadmaps, and making trade-offs between user, business, and technology needs. The government reserves the right to approve any replacements for this key position.

