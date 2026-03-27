Administration for Children and Families (ACF) Office of Community Services (OCS)

Performance Work Statement Community Services Forms Engine for Efficient Reporting (CSFEER)

March 1, 2025 Rev 1. August 5, 2025 Rev 2. August 25, 2025

## Performance Work Statement for the

Community Services Forms Engine for Efficient Reporting (CSFEER)

## 1.0 General

## Introduction

The mission of the Administration for Children and Families (ACF) is to foster health and well-being by providing federal leadership, partnership, and resources for the compassionate and effective delivery of human services. The mission of the Office of Community Services (OCS), is to reduce the causes and consequences of poverty, increase opportunity and economic security of individuals and families, and revitalize communities. The social service and community development programs work in a variety of ways to improve the lives of many.

## Objective

OCS is exploring building a scalable, user-centered digital forms platform to streamline data collection, improve user experience, and enhance operational efficiency of the grants reporting lifecycle for OCS grant recipients. The potential system would collect required data points from OCS grant recipients in a user-friendly platform and store data collected in a consistent, usable format available via Application Programming Interface (API) endpoints and Comma Separated Values (CSV) export.

The solution(s) the Government is interested in aligns with the natural life cycle of a federally funded grant to include (1) planning materials for pre-award, (2) post-award data collection, and (3) data availability for evaluating performance outcomes to support a wide array of reporting needs including Congressional reporting and performance trends. The platform would have to be built to prioritize scalability of functionality and performance while also maintaining a streamlined user experience.

While the Government is considering the goal of the potential solution to be initially developed around several targeted forms for one program within OCS, we are interested in leveraging humancentered design (HCD) processes to learn how solution recommendations could differ if this platform were to extend to data collection across additional ACF grant programs use cases. For example, if the Government were to pursue a pilot that demonstrates scalability, assume a user base of 1,100 grant recipients and sub-grant recipients who would need varying permission levels including view-only, view and edit, and view, submit, and 75 federal staff who would need to review, route, approve, analyze, compare historical data, and export data. The tentative name for the system is Community Outcomes Reporting Engine (CORE).

## Background

In the United States, there are approximately 36.8 million people living in poverty. The Office of Community Services (OCS) focuses on this population and partners with states, tribes, non-profit, and community-based organizations to reduce the causes and consequences of poverty, increase opportunity and economic security of individuals and families, and revitalize communities.

In fiscal year (FY) 2022, OCS administered nearly $6.29 billion in funding inclusive of supplemental funding for economic and natural disasters across 7 social and community development programs with goals such as:

- · Economic development investments to assist the nation's most vulnerable families.
- · Flexible funding to aid states, tribes, and territories in targeting the needs of communities.
- · Providing access to vital services such as water, heating, and cooling.

While each of the administered programs are implemented in unique ways, there are fundamental needs to ensure the prudent and efficient administration of the program to include planning, data collection, evaluation, and performance measurement.

OCS grant recipients are required by law, to submit to the government certain information during the pre-award and post-award phases of the grant lifecycle. These forms can be extensive, with complex data validation rules and an operational need to contextualize current data entry with historical data in the interface. The forms are a mix of free text narrative and more structured information entry, including financial details. Once the data has been submitted, the government must evaluate the quantitative and qualitative data and ultimately report to Congress and the public on programmatic outcomes.

## Scope of Work

The scope of this effort requires the contractor to employ HCD and service design techniques, product management methods, and agile software development principles to explore the problem space through discovery and user research activities and develop an initial minimum viable product (MVP) which is iteratively expanded on into the future through continuous development.

## Iterative Development to Reduce Risk

The grant cycle for the selected program is annual, meaning each grant recipient submits forms once a year. ACF staff then review and analyze information collected in the forms. Historically, these forms require substantial preparation and out-of-system work among grant recipients to submit. The platform should be developed using an iterative approach to minimize risk and efficiently capture processes throughout the grant life cycle. Below are notional phases of how we would transition from the current legacy process to the new platform that is subject to change based on learnings during discovery and user research activities (note that this is only based on our

current understanding of the problem space, we would expect substantially more frequent releases to production during the development process based on standard agile best practices).

- · Phase I: First production launch to users would be forms for Tribes and Tribal organizations (no more than 66 end users at the grant recipient level), and include the following three reports:
  - o CSBG Tribal Plan and Application (OMB Approved Form)
  - o CSBG Tribal Annual Report (OMB Approved Form)
  - o CSBG Tribal Annual Report [Short Form] (OMB Approved Form)
- · Phase II: The next iteration would be incrementally scaling up to include the forms of Phase I and additional forms to be used by states and territories with the ability to opt-in to the new reporting process leveraging this platform. During this iteration, the legacy process will remain operational. This is estimated to be more than 53 end users for grant recipients and include:
  - o CSBG Eligible Entity List (OMB Approved Doc)
  - o CSBG State and Territory Plan (OMB Approved Form)
  - o CSBG Annual Report 3.0 (OMB Approved Form)
- · Phase III: All users will migrate pre and post award form reports to the new platform for reporting and the legacy system will sunset.

## Period of Performance

The total period of performance is 24 months, with a 12-month base period and a 12-month option period.

## Place of Performance

The work to be primarily performed under this contract shall be performed at the Contractor facility. Contractor agrees to travel for occasional in-person meetings, including at the agency worksite, based on needs of the project and requirement of the program CO/ACF COR and sponsoring agency leadership.

The Contractor's team shall be readily available on business days from 9 am ET - 5 pm ET, with adjustments / exceptions only as agreed up on with the ACF COR.

## Recognized Holidays

New Year's Day Martin Luther King Jr.'s Birthday President's Day Memorial Day Independence Day Juneteenth

Labor Day Columbus Day Veteran's Day Thanksgiving Day Christmas Day

In addition to the days designated as holidays, the Government observes the following days:

- · Any other day designated by Federal Statute

Performance Work Statement

- · Any other day designated by Executive Order
- · Presidential Inauguration Day
- · Any other day designated by the President's Proclamation

It is understood and agreed between the Government and the Contractor that observance of such days by Government personnel shall not otherwise be a reason for an additional period of performance, or entitlement of compensation except as set forth within the contract. In the event the Contractor's personnel work during the holiday, they may be reimbursed by the Government, however, no form of holiday or other premium compensation will be reimbursed either as a direct or indirect cost, other than their normal compensation for the time worked.

## Applicable Documents

CSBG Annual Report 3.0

CSBG Tribal Annual Report

CSBG Tribal Annual Report (Short Form)

CSBG State Plan

CSBG Tribal Plan

CSBG Eligible Entity List

## 2.0 Specific Requirements and Tasks

The scope for this system is an interface for OCS grant recipients to submit and manage submissions of pre-award and post-award information to ACF; an interface for ACF staff to review submitted information from grant recipients, and the ability to transmit the data collected via API endpoints and data download formats such as CSV for analysis and integration with other data tools. User research with grant recipients, OCS staff, and other relevant stakeholders will drive the product roadmap for this platform.

All research, designs, code, and other related documentation developed during performance of this contract will be the property of ACF and live in the relevant repositories as specified by ACF.

Specific Requirements Below is a non-exhaustive list of assumptions about the requirements of the system based on the Government's current understanding of the problem space.

These serve as a starting point for the contractor as they begin their exploration of the problem space and are not hard-coded requirements; this list is subject to change based on validated learnings during discovery, user research, and the standard agile development process.

## Version Control and Data Integrity

- · Support for multiple simultaneous versions of a form that maintain data from existing submissions when form modifications are published.

- · Robust version history for form actions that allows federal staff to view the state of a form submission at various points in the workflow.
- · Interface that allows recipients to view past form submissions in a comparative manner.

## Form Submission Workflow

- · Automatically create and initialize forms for recipients with pre-populated data based on defined reporting schedules and previous year data to show trends over time.
- · Workflow for form submissions that allows multiple individuals on the grant recipient side to work on forms prior to submission.
- · Functionality that allows recipients to "unsubmit" forms as well as submit revisions to submitted forms.
- · Customizable multi-step and multi-person review and approval process for submitted forms on the Federal side - ideally managed through a visual / no-code workflow builder as workflows will differ by form.
- · Customizable, real-time alerts and notifications linked to various aspects of the form workflow (new form available, form past due, form submission rejected, etc.).

## Form Field Types and Data Entry

- · Support for various form field types:
  - o Manual data entry: Open fields where values are entered by the end user
  - o Auto calculations: Closed fields that use formulas to automatically calculate figures based on numbers input
  - o Pre-populations: Data that connects forms from pre-award to post-award
  - o Validation: Mathematical checks based on numbers input and policy requirements
- · Flexible validation rules engine that can be used to validate form values based on calculations or by comparisons to prior form submissions
  - o Validations should be able to support both hard errors and notification / warningtype validations.
  - o Validations should be able to take place at the individual field level, at the field group level, and at the overall form level.
- · Support for attachment fields that allows recipients to upload files that are stored along with the submission.
- · Support for complex form logic such as conditional fields and branching questions.
- · Support for one-to-many response types where recipients can add multiple responses to several form fields for a single question.

## Security and Authentication

- · Authentication with Login.gov
- · System will need an Authority to Operate (ATO) to collect actual data in production within 18 months.
- · System will need a Systems of Records Notice (SORN)

## Integration and Interoperability

- · Flexible API for interacting with forms, submissions, and extracting data in bulk
- · Write API to import prepopulated data
- · Data exports via API, CSV, and human-readable formats
- · Ability to export individual form submissions as PDFs
- · Ability to generate a link that enables public access to a specific portions of the form submission.
- · Comprehensive and easy to understand API documentation for developers.

## Open Source and Scalability

- · Open-source code base preferred, utilizing standard, sustainable open-source libraries.
- · Affordable scaling of user licenses (if applicable)

## Accessibility and Design

- · Section 508 WCAG AA-compliant front end, ideally using the United States Web Design System (USWDS) .
- · UI-based, low-code/no code form builder to allow non-technical staff to build future forms (after year 1) with sandbox/testing space.

## Collaboration and Workflow Management

- · Workflow tooling for multiple users entering data into one form, routing form, and updating/returning form for re-submission.
- · Support for business logic complexity such as deadlines and notifications.

## User Experience and Form Progress

- · Users should be able to save their progress on a form and return to it at a later date to make revisions.
- · Previously submitted data should be available in forms for users to limit repeat requests for data.

## Permissions and Data Controls

- · Flexible permissions system to ensure appropriate controls on read, write, and export of data.
- · Flexible user management module that allows recipients to manage users who have access to their forms and the permissions assigned to those users. Recipients control the administration of their accounts - so subrecipient administrator can create accounts for their people; states can do the same for their people.
- · At the subrecipient, state, and federal level there will be (at a minimum) read-only, writeonly, and approve rolesand permission levels that each level can self-administer.

Based on the Government's current understanding of the problem space the current "Top Problems to Solve" are:

- · Enable new forms to be designed, updated, and tested more quickly and efficiently by program staff.
- · Improve form interface to be more intuitive and user-friendly for grant recipients.
- · Improve tracking and collaboration on forms between program staff, lead agencies, and sub-recipients around submission, reviews, and revisions.
- · Automate data validation while a grant-recipient fills out a form using business logic, errors, and warnings.
- · Automate comparison to data from integrations (e.g. UIE mismatches.)
- · Enable program staff to easily export, review and correct errors (e.g. addressing missing data, data conflicts, and new elements.)
- · Reduce compatibility issues and variability from custom State/Tribal plans and custom or third-party-enabled State annual reports.
- · Real-time access to system data that does not hinder application performance.

The "top problems to solve" listed above are subject to change based on the natural evolution of the Government's and contractor's understanding of the problem space through continued discovery, user research, and stakeholder engagement.

As is customary in agile development, priorities on this effort may shift over time. These shifting priorities will be accounted for through collaboration between the Government (Product Owner, ACF stakeholders, etc.) and the contractor to establish a shared understanding of the work, which will be planned for and communicated through standard agile practices such as product roadmapping, backlog prioritization and sprint planning. For example, ACF may decide during performance that due to changing real-life circumstances certain functionalities should be prioritized over other previously planned to be built functionalities, at which time the Government would work with the contractor to plan for and prioritize those tasks, as relevant.

## Current State Process - CSBG Recipient Data Collection

As described above, we are interested in leveraging iterative development principles to learn more about how a flexible solution could accommodate a wide variety of recipient reporting needs across ACF grant programs. With this, we anticipate that the initial MVP would be focused on, but not limited to, the Community Services Block Grant (CSBG) grant program managed by OCS.

CSBG grant recipients have two high level reporting requirements:

- · Per Section 676(b) of the CSBG Act, CSBG grant recipients must prepare and submit an application and plan - hereinafter referred to as the CSBG Plan Application - to receive CSBG funding. The plan application can be submitted either annually or biannually by recipients.
- · Per the Section 678E of the CSBG Act, CSBG grant recipients are required to submit an annual report to OCS - hereinafter referred to as the CSBG Annual Report - to report on the measured performance for the recipient and eligible sub-recipients (if applicable).

OCS has operationalized these reporting requirements through various versions of forms that differ by recipient and separate modules for more complex reporting requirements.

- · CSBG Plan Application
  - o CSBG State Plan: Collects information from the State lead agency about how CSBG funds will be used throughout the period covered by the plan.
  - o CSBG Tribal Plan: Collects information from tribal recipients about how CSBG funds will be used throughout the period covered by the plan.
- · CSBG Annual Report
  - o CSBG Tribal Annual Report and Tribal Annual Report (Short Form): Collects information from Tribes and Tribal organizations about how they are addressing the unique needs of the communities they serve.
  - o CSBG Annual Report
    - § Module 1 - State and Territory Administration: collects information related to State administration of CSBG funding
    - § Module 2 -Eligible Entity Administration: collects information on information on funds spent by eligible entities on the direct delivery of local services and strategies and capacity development as well as information on funding devoted to administrative costs by the eligible entities
    - § Module 3 - Individual and Family Level: collects information on services provided to individuals and families, demographic characteristics of people served by eligible entities, and the results of these services.
    - § Module 4 - Community Level: collects information on the implementation and results achieved for community-level strategies.

As part of CSBG, OCS awards funding to State and territory lead agencies that in turn fund local agencies known as eligible entities within the state or territory. To support data collection efforts across the entire CSBG ecosystem, Module 1 is completed by State lead agencies while Module 2, Module 3, and Module 4 are completed by all eligible entities. Conversely, OCS awards funding to Tribes and Tribal organizations who utilize the funding to directly serve Tribal members. Within the Tribal reporting structure, direct-funded Tribes and Tribal organizations submit Modules 1-3 using the Tribal reporting forms.

The purpose of this contract is to develop an initial working MVP that informs future development activities and continuous iteration of the product. The initial MVP will likely be for a single program within OCS for grant recipients to submit data to the government; however, we would also like to explore the feasibility of scaling this platform to be a more robust 'forms engine' that serves as a single platform for ACF grant recipients use to submit required information to ACF across multiple ACF Program Offices. Program Offices across ACF have data collection requirements that are specific to their grant programs. Across all programs there are over 100 forms of varying complexity being competed, reviewed, and submitted by 25,000 recipients and sub-recipients, and then reviewed and analyzed by hundreds of ACF federal staff.

## Objective and Tasks

These notional objectives are intended to help focus the contractor's attention at the outset of the project. Discovery and iterative user research activities will continue to shape the objectives.

## Task Area 1: Discovery and Product Definition Objective

Working in conjunction with the federal product owner and the ACF team, the contractor will conduct discovery around the needs of relevant users and stakeholders (both internal to ACF and potentially external if necessary) to define how this product should meet existing use cases and emerging challenges. The contractor will utilize customer experience and service design techniques, such as those found in the Digital Service Playbook or 18F Methods, to design approaches to meeting these needs in the most impactful manner possible.

Discovery, user research and design activities should continue throughout the performance of the contract and be embedded throughout the development process at every stage, as relevant.

## Specific Tasks

Understand what people need, by exploring and pinpointing the needs of the people who will use the service, and the ways the service will fit into their lives.

- · Early in the project, spend time with current and prospective users of the service.
- · Use a range of qualitative and quantitative research methods, such as stakeholder interviews, to determine people's goals, needs, and behaviors.
- · Document the findings about user goals, needs, behaviors, and preferences.
- · Identify pain points in the current way users interact with the service, and prioritize these according to user needs.
- · Create a prioritized list of tasks the user is trying to accomplish, also known as "user stories" to be utilized in the agile development process.
- · Share findings with the team and agency leadership, if required.

Consider the entire context, by understanding how people will interact with the service within the larger ecosystem, from start to finish.

- · Conduct research into relevant organizations, processes, systems and policies to understand the user landscape.
- · Understand the different points at which people will interact with the service - both online and in person, as relevant.
- · Design the digital parts of the service so that they are integrated with any offline touchpoints people use to interact with the service.
- · When relevant, analyze opportunities for users to better leverage existing systems.
- · Analyze opportunities for leveraging open-source tools as part of the technology stack.
- · Account for accessibility considerations and ensure that Section 508 requirements are considered, designed for, and met.

Ensure new features are expandable and extensible to meet ongoing needs of the Federal government, state/local stakeholders, and other relevant user groups.

User data to drive decisions, to monitor progress at each stage of the project.

- · Establish metrics that will measure how well the service is meeting user needs at each step of the service.
- · Initiate measurable feedback loops, so that people can report issues directly.

## Task Area 2: Design and Development of the MVP

## Objective

Based on learnings through the discovery phase, develop an impactful MVP that informs the next steps for continued development and scaling of the product through validated learning. The contractor shall implement agile development, product management and customer experience methodologies to animate solutions to proposed approaches and deploy them to production.

Below are some high-level objectives of the MVP based on the Government's current understanding of the problem space. For more details, see "Scope of Work" on page 8.

- · Develop a digital "forms engine" platform which supports basic features such as approvals, authentication, review memos or comments, revisions, exports, etc.
- · Launch the "forms engine" in an initial pilot with selected recipients from Tribes and Tribal organizations, replacing 3 fillable PDFs:
- · CSBG Tribal Plan and Application
- · CSBG Tribal Annual Report (OMB Approved Form)
- · CSBG Tribal Annual Report [Short Form] (OMB Approved Form)

As mentioned previously, these initial goals are subject to change based on the natural evolution of the Government's and contractor's understanding of the problem space through continued discovery, user research, and stakeholder engagement. The prioritization of feature development will be managed by the ACF Product Owner, in collaboration with the contractor, and achieved through a regularly updated product road mapping process. These goals are only reflective of the Government's current understanding of the problem space and serves as a starting point for the contractor to work towards during performance.

## Specific Tasks

Understand what people need , by continually testing the products with real people to ensure delivery is focused on what is important.

- · Design with the end user's experience in mind so that the MVP is aligned with end user goals, needs, and behaviors.
- · Iteratively design solutions toward the end user experience so that products meet end user needs and goals. This includes contributing to the development of the product vision, product roadmap, initial features of the MVP, and an initial product backlog with associated user stories.
- · Iteratively establish and prioritize MVP features based on discovery and user research findings in consultation with the Product Owner. Update the product vision, product roadmap, and initial product backlog with associated user stories.
- · Develop and test mock ups or prototypes with real users, in the field if possible.
- · As the MVP is being built, regularly test it with users to ensure it meets people's needs.

Make it simple and intuitive , so that users will succeed the first time unaided.

- · If relevant, use a simple and flexible design style guide for the service. Use the U.S. Web Design Standards as a default.
- · Use the design style guide consistently for related digital services.

- · Incorporate a visual identity consistent with the visual branding of the respective prorams and agency guidelines for cohesion.
- · Give users clear information about where they are in each step of the process.
- · Follow accessibility best practices to ensure all people can use the service.
- · Provide users with a way to exit and return later to complete the process.
- · Use language that is familiar to the user and easy to understand.
- · Use language and design consistently throughout the service, including online and offline touch points.
- · Provide user trainings and product documentation as needed.

## Build with best practices, to ensure efficiency, consistency, and quality

- · Utilize agile development processes to contribute to the writing and managing of epics, user stories, acceptance criteria, and the "definition of done". In this fashion, development work should ramp up immediately and not necessarily wait for the conclusion of the discovery research work.
- · Conduct regular retrospectives, release planning, backlog grooming, blameless postmortems, and other common activities associated with iterative design and agile methodologies.
- · Develop the MVP (and all features and functionalities that follow) leveraging a modern, open source technology stack.
- · Incorporate DevSecOps and CI best practices (e.g. "Infrastructure as Code", automated testing, code reviews) to develop and release new features and functionality. Integrate with any current CI pipelines and the existing ACF environment (if any exist).Implement code management processes, security, 508 compliance, privacy or any other federal or ACFspecific policies that need to be incorporated in order to release the product in a live environment.
- · Resolve defects identified and provide updated releases with the fixes.
- · Take into account ACF's standard "authority to operate" (ATO) processes and timelines when developing the MVP and support ATO-related activities, as needed.
- · Provide recommendations on what should be included in future versions of the product.

Use data to drive decisions, to measure how well the MVP is working for users.

- · Create and track metrics to determine whether the MVP successfully meets user needs.
- · Monitor system-level resource utilization in real time.
- · Monitor system performance in real-time (e.g. response time, latency, throughput, and error rates).
- · Ensure monitoring can measure median, 95th percentile, and 98th percentile performance.
- · Track concurrent users in real-time, and monitor user behaviors in the aggregate to determine how well the service meets user needs.
- · Provide metrics which may be published internally.

- · Provide metrics which may be published externally.
- · Use an experimentation tool that supports multivariate testing in production, as needed.

## Objective

Following development and deployment of the MVP, the contractor shall utilize agile development, DevSecOps and product management methodologies to support the continued development and deployment of additional features and functionalities related to the learnings uncovered during continued during design/discovery.

## Specific Tasks

Understand what people need , by continually testing the products with real people to ensure delivery is focused on what is important.

- · Utilize HCD processes throughout to validate evolving user needs and test the impact of new features and functionalities.
- · Leverage user stories to deliver incremental solutions on a bi-weekly release cadence rather than large features infrequently.
- · Deliver complex features iteratively and work toward full functionality while incorporating real user feedback.
- · Continue practices as established in the design and development of the MVP.

Make it simple and intui te , so that services delivered will not be stressful, confusing, or daunting.

- · Continue practices as established in the design and development of the MVP, such as: incorporating a design style guide, visual identity, accessibility best practices, clear information architecture, and plain language.
- · Provide user trainings and product documentation as needed.

## Build with best practices , to ensure efficiency, consistency, and quality

- · Co-create system features with ACF, which includes the writing and managing of epics, user stories, acceptance criteria, and the "definition of done". Work with the Product Owner to set and prioritize sprint goals during sprint planning activities.
- · Continue practices as established in the design and development of the MVP, such as: agile development methodologies and ceremonies, DevSecOps and CI best practices, and compliance with federal policies.
- · Automate activities (i.e. testing of code, release processes, etc.) to the maximum extent possible from integration and testing through delivery and deployment in order to facilitate low burden and frequent development activities.

- · Fix regressions caused by version updates with high urgency and ensure automated testing is in place to prevent the same regression happening in the future.
- · Establish incident management capabilities for use in responding to and addressing accessibility issues.
- · Work with ACF to ensure that appropriate configuration control and change management processes are aligned with ACF policy and standards.
- · Support agency ATO activities as needed.
- · Improve the system to meet any relevant FISMA-related security requirements. All dependencies should be upgraded to and kept on recent versions. All known security vulnerabilities must be addressed with urgency in respect to their severity.
- · Any code developed will run and be operational 7 days per week, 24 hours per day.

Use data to drive decisions, to measure how well the service is working for users.

- · Define, provision, and track metrics to determine whether the delivered features and functionality meets user needs. Continue practices as established in the design and development of the MVP.

## Task Area 4: Transition In and Out and Retrospective

## Objective

As needed, the contractor shall work in conjunction with the Product Owner and the ACF team and the onboarding contractor development team (when transitioning off the project) to facilitate transition in/out activities. The contractor shall build in knowledge and document-sharing tasks into the normal sprint cadence in order to efficiently manage the transitioning on and/or off of the project. As a baseline, these activities should take place over 2 sprint cycles (4 weeks) at a minimum, although more or less may be needed as required. Additionally, the contractor shall conduct retrospective activities with the Product Owner and ACF team to inform the future roadmap/next steps of the product.

## Specific Tasks

Be good stewards, by responsibly governing publicly-funded systems.

- · Mapping out transition in and out tasks to be incorporated over at least a 2-sprint schedule with the ACF team and either the onboarding contractor.
- · Ensuring that all relevant project-specific knowledge and documentation is either shared or received before the incumbent rolls off the project.
- · Address any knowledge or documentation gaps that could reasonably inhibit the incoming contractor's ability to effectively perform the tasks/roles needed to support the continued development of the system.

- · If needed, develop playbooks and developer how-to documentation that can be passed on to new and potential replacement development teams to ease transitioning in and out of teams. This should be an ongoing activity that occurs throughout performance as needed, not just during the "transition-in and out" 2-sprint period. This activity could include either updating existing documentation (if any exists) or creating original documentation, in both cases the documentation will ultimately be owned and managed by the Government.
- · Ensure that the concept of "ownership" of the system, which is to mean the successful transition of true responsibility for the care and feeding of the system, is transferred from the outgoing contractor to the incoming contractor(s). This would generally be finalized during the 2nd sprint of the transition period.
- · Conduct a project retrospective activity that analyzes data gathered during performance around goals, timeline, major events, and success or failures.
- · Contribute to updating the product roadmap for continued scaling of the product through continuous design and agile processes.
- · Provide a transition-out plan to the Product Owner and COR within 60 days of the end of the period of performance, along with a presentation of the transition-in and out activities performed and executed prior to the end of the period of performance.
- · Provide an accounting of the following, as needed:
  - o Current versions of all system and user documentation
  - o All originals and copies of licensing, renewal information, asset management records, software documentation, and training materials.
  - o Any Government Furnished Equipment (GFE) provided during contract performance.
  - o Any documentation associated with custom code, reports, process automations, scripts and configurations with applicable configuration management information accountability/documentation.
