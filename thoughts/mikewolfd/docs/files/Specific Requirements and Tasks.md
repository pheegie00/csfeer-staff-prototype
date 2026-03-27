# Tab 1

# 2.0 Specific Requirements and Tasks

source : [B09 SA 0001 - PWS ADMIN\_OCS\_CSBG\_CSFEER\_v2.pdf](https://drive.google.com/file/d/1QmkA-te5zg7jr-_MmEOT2XlJs694fGup/view)

The scope for this system is an interface for OCS grant recipients to submit and manage  
submissions of pre-award and post-award information to ACF; an interface for ACF staff to review submitted information from grant recipients, and the ability to transmit the data collected via API endpoints and data download formats such as CSV for analysis and integration with other data tools. User research with grant recipients, OCS staff, and other relevant stakeholders will drive the product roadmap for this platform.

All research, designs, code, and other related documentation developed during performance of  
this contract will be the property of ACF and live in the relevant repositories as specified by ACF.

Specific Requirements Below is a non-exhaustive list of assumptions about the requirements of  
the system based on the Government’s current understanding of the problem space.

These serve as a starting point for the contractor as they begin their exploration of the problem  
space and are not hard-coded requirements; this list is subject to change based on validated  
learnings during discovery, user research, and the standard agile development process.

### Version Control and Data Integrity

* Support for multiple simultaneous versions of a form that maintain data from existing  
  submissions when form modifications are published.  
* Robust version history for form actions that allows federal staff to view the state of a form  
  submission at various points in the workflow.  
* Interface that allows recipients to view past form submissions in a comparative manner.

### Form Submission Workflow

* Automatically create and initialize forms for recipients with pre-populated data based on defined reporting schedules and previous year data to show trends over time.  
* Workflow for form submissions that allows multiple individuals on the grant recipient side to work on forms prior to submission.  
* Functionality that allows recipients to “unsubmit” forms as well as submit revisions to submitted forms.  
* Customizable multi-step and multi-person review and approval process for submitted forms on the Federal side \- ideally managed through a visual / no-code workflow builder as workflows will differ by form. [Q](#customizable-multi-step-and-multi-person-review-and-approval-process:)  
* Customizable, real-time alerts and notifications linked to various aspects of the form workflow (new form available, form past due, form submission rejected, etc.). [Q](#alert-&-notifications:)

### Form Field Types and Data Entry

* Support for various form field types:  
  * Manual data entry: Open fields where values are entered by the end user  
  * Auto calculations: Closed fields that use formulas to automatically calculate figures based on numbers input  
  * Pre-populations: Data that connects forms from pre-award to post-award  
  * Validation: Mathematical checks based on numbers input and policy requirements  
* Flexible validation rules engine that can be used to validate form values based on  
  calculations or by comparisons to prior form submissions  
  * Validations should be able to support both hard errors and notification / warning-type validations.  
  * Validations should be able to take place at the individual field level, at the field group level, and at the overall form level.  
* Support for attachment fields that allows recipients to upload files that are stored along  
  with the submission.  
* Support for complex form logic such as conditional fields and branching questions.  
* Support for one-to-many response types where recipients can add multiple responses to  
  several form fields for a single question.


### Security and Authentication

* Authentication with Login.gov  
* System will need an Authority to Operate (ATO) to collect actual data in production within 18 months.  
* System will need a Systems of Records Notice (SORN)

### Integration and Interoperability

* Flexible API for interacting with forms, submissions, and extracting data in bulk  
* Write API to import prepopulated data  
* Data exports via API, CSV, and human-readable formats  
* Ability to export individual form submissions as PDFs  
* Ability to generate a link that enables public access to a specific portions of the form submission.  
* Comprehensive and easy to understand API documentation for developers. Ope

### Source and Scalability

* Open-source code base preferred, utilizing standard, sustainable open-source libraries.  
* Affordable scaling of user licenses (if applicable) 

### Accessibility and Design

* Section 508 WCAG AA-compliant front end, ideally using the United States Web Design System (USWDS) .  
* UI-based, low-code/no code form builder to allow non-technical staff to build future forms (after year 1\) with sandbox/testing space.

### Collaboration and Workflow Management

* Workflow tooling for multiple users entering data into one form, routing form, and  
  updating/returning form for re-submission.  
* Support for business logic complexity such as deadlines and notifications.  
* User Experience and Form Progress  
* Users should be able to save their progress on a form and return to it at a later date to make revisions.  
* Previously submitted data should be available in forms for users to limit repeat requests for Data.

### Permissions and Data Controls

* Flexible permissions system to ensure appropriate controls on read, write, and export of data.  
* Flexible user management module that allows recipients to manage users who have  
  access to their forms and the permissions assigned to those users.  
* Recipients control the administration of their accounts – so subrecipient administrator can create accounts for their people; states can do the same for their people.  
* At the subrecipient, state, and federal level there will be (at a minimum) read-only, write-  
  only, and approve roles and permission levels that each level can self-administer.

Based on the Government’s current understanding of the problem space the current “Top  
Problems to Solve” are:

* Enable new forms to be designed, updated, and tested more quickly and efficiently by  
  program staff.  
* Improve form interface to be more intuitive and user-friendly for grant recipients.  
* Improve tracking and collaboration on forms between program staff, lead agencies, and sub-recipients around submission, reviews, and revisions.  
* Automate data validation while a grant-recipient fills out a form using business logic, errors, and warnings.  
* Automate comparison to data from integrations (e.g. UEI mismatches.)  
* Enable program staff to easily export, review and correct errors (e.g. addressing missing data, data conflicts, and new elements.)  
* Reduce compatibility issues and variability from custom State/Tribal plans and custom or third-party-enabled State annual reports.  
* Real-time access to system data that does not hinder application performance.

The “top problems to solve” listed above are subject to change based on the natural evolution of  
the Government’s and contractor’s understanding of the problem space through continued  
discovery, user research, and stakeholder engagement.

As is customary in agile development, priorities on this effort may shift over time. These shifting  
priorities will be accounted for through collaboration between the Government (Product Owner,  
ACF stakeholders, etc.) and the contractor to establish a shared understanding of the work, which will be planned for and communicated through standard agile practices such as product  
roadmapping, backlog prioritization and sprint planning. For example, ACF may decide during  
performance that due to changing real-life circumstances certain functionalities should be  
prioritized over other previously planned to be built functionalities, at which time the Government  
would work with the contractor to plan for and prioritize those tasks, as relevant.

# Tab 2

### `Customizable multi-step and multi-person review and approval process:` {#customizable-multi-step-and-multi-person-review-and-approval-process:}

* `What are the typical review/approval stages?`  
  * `(e.g., initial submission → technical review → supervisor approval → legal review → final sign-off)`  
* `Are these steps always sequential, or can they happen in parallel?`  
* `Do steps differ by form type, department, or user role?`  
* `Is there a need for conditional logic?`   
  * `(e.g., “if the budget is over $10K, add a CFO approval step”)`  
* `Who are the reviewers/approvers?`  
* `Titles, departments, or dynamic roles`   
  * `(e.g., “form owner’s supervisor”)?`  
* `Can multiple people review or approve the same step?`  
* `Should all approvers in a step approve, or is one enough?`  
* `Who can reassign, delegate, or override an approval?`  
* `Do reviewers/approvers need different permission levels?`   
  * `(e.g., view-only vs. edit comments vs. final approval)`  
* `Who will configure or modify workflows?`   
  * `IT admins, program managers, or end users?`

### Alert & notifications: {#alert-&-notifications:}

* `How should participants be notified?`  
  * `Email, dashboard, system alerts, etc.`  
* `Are there deadlines or SLAs for each step?`  
* `Should there be escalation rules if a step isn’t completed on time?`  
* `Do users need visibility into overall workflow progress?`

