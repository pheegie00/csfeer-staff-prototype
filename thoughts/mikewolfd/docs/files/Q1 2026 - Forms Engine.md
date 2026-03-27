# Forms Engine Q1 2026 Plan

Jan 1, 2026 \- Mar 31, 2026

### **Objective 1: Deliver Working CSBG Forms MVP**

**Key Results (Updated):**

* Launch Tribal Annual Report (Long Form) complete by March 15th   
* Launch Tribal Plan and Application complete by March 31st  
* Implement save/resume functionality across both forms  
* Build pre-population capability from previous submissions  
* Create PDF export functionality for completed forms  
* **Stretch Goal**: Deliver API endpoints for data export

### **Objective 2: Establish Production-Ready Foundation with Continuous Compliance**

**Key Results (Updated):**

* Deploy functional landing page by March 1st *(moved from Feb 28th)*  
* Complete ATO documentation package incrementally and submit by March 31st *(changed from March 15th)*  
* Achieve form data persistence with secure database storage  
* Establish continuous ATO work starting Week 2 through Quarter end *(new)*  
* Deploy to ACF infrastructure with established pipeline

---

## **GOVERNMENT SHUTDOWN STRATEGY EXECUTION**

### **Weeks 1-2: Foundation First (40 story points)**

**Can Execute Without ACF Input:**

* **Complete Django setup and infrastructure (Epic 1: Stories 1.1-1.6) //in-flight**  
* **Begin USWDS component development (Epic 3: Stories 3.1-3.5) //in-flight**  
* **Start ATO documentation framework (Epic 6: Week 2 story) //on-hold**

### **Weeks 3-4: Form 1 Development (35 story points)**

**Minimal ACF Input Required:**

* **Tribal AR form development (Epic 2: Stories 2.1-2.5)**  
* **Continue USWDS components (Epic 3: Stories 3.6-3.10)**  
* **Continue ATO work (Epic 6: Weeks 3-4 stories)**

### **Week 5+: Form 2 and Advanced Features (57 story points)**

**Some ACF Coordination Needed:**

* **Tribal Plan development (Epic 4: All stories)**  
* **API development (Epic 5: All stories)**  
* **Complete USWDS library (Epic 3: Stories 3.11-3.15)**  
* **Finish ATO preparation (Epic 6: Weeks 5-11 stories)**

---

### Epic/Backlog Staging

### **EPIC 1: Foundation Infrastructure & Security**

**Epic Goal**: Establish core technical foundation that enables all other work **Government Shutdown Safe**: 90% \- Minimal ACF input required **Story Points**: 25 total

#### **Weeks 1-2 Priority Stories:**

**Story 1.1: Django Application Bootstrap** (5 pts)

* *As a* developer  
* *I want* a fully configured Django application with PostgreSQL  
* *So that* we can begin form development immediately  
* **Acceptance Criteria:**  
  * Django project structure established with proper settings  
  * PostgreSQL database configured and migrated  
  * Development environment fully functional  
  * Basic authentication middleware configured  
  * Git repository established with CI/CD foundation

**Story 1.2: Core Security Infrastructure** (5 pts)

* *As a* system administrator  
* *I want* foundational security controls implemented  
* *So that* ATO work can begin immediately  
* **Acceptance Criteria:**  
  * HTTPS/TLS encryption enforced  
  * CSRF protection enabled  
  * Security headers configured  
  * Audit logging framework established  
  * Data encryption at rest implemented

**Story 1.3: Session Management System** (3 pts)

* *As a* user  
* *I want* secure session management without Login.gov  
* *So that* I can maintain state across form interactions  
* **Acceptance Criteria:**  
  * Secure session storage implemented  
  * Session timeout configured  
  * Session hijacking protection  
  * Basic user identification system  
  * Session cleanup processes

**Story 1.4: Data Persistence Layer** (5 pts)

* *As a* developer  
* *I want* robust data storage and retrieval capabilities  
* *So that* forms can save and restore user data  
* **Acceptance Criteria:**  
  * Form data models designed and implemented  
  * Save/resume functionality backend ready  
  * Data validation framework  
  * Backup and recovery procedures  
  * Performance optimization for rural connections

**Story 1.5: Landing Page Foundation** (4 pts)

* *As a* tribal user  
* *I want* a clear entry point to access forms  
* *So that* I can easily navigate to needed forms  
* **Acceptance Criteria:**  
  * Responsive landing page design  
  * Form navigation and routing  
  * Basic help and guidance content  
  * USWDS-compliant styling  
  * Mobile-optimized experience

**Story 1.6: ATO Planning and Initial Documentation** (3 pts)

* *As a* compliance officer  
* *I want* ATO planning and documentation begun immediately  
* *So that* submission timeline is achievable  
* **Acceptance Criteria:**  
  * System Security Plan template created  
  * Risk assessment framework established  
  * Security controls catalog initiated  
  * Documentation processes defined  
  * Review schedule established

---

### **EPIC 2: Tribal Annual Report (Long Form) \- Form 1**

**Epic Goal**: Deliver complete Tribal AR form with full functionality **Government Shutdown Safe**: 75% \- Can work from existing PDF requirements **Story Points**: 35 total

#### **Weeks 3-4 Priority Stories:**

**Story 2.1: Tribal AR Form Analysis and Data Model** (5 pts)

* *As a* developer  
* *I want* comprehensive understanding of Tribal AR requirements  
* *So that* the form can be built accurately  
* **Acceptance Criteria:**  
  * Complete field inventory from existing PDF  
  * Data validation rules documented  
  * Business logic requirements captured  
  * File attachment requirements defined  
  * Django models created and tested

**Story 2.2: Tribal AR Backend Development** (8 pts)

* *As a* system  
* *I want* robust backend processing for Tribal AR data  
* *So that* submissions are properly handled and validated  
* **Acceptance Criteria:**  
  * Form submission API endpoints  
  * Data validation and business rules  
  * File upload handling with security  
  * Save/resume functionality for this form  
  * Integration with data persistence layer

**Story 2.3: Tribal AR Frontend Implementation** (8 pts)

* *As a* tribal administrator  
* *I want* an intuitive form interface  
* *So that* I can complete reporting efficiently  
* **Acceptance Criteria:**  
  * Multi-page form with progress indicators  
  * Real-time validation and error handling  
  * Save/resume capabilities on frontend  
  * File upload interface  
  * Mobile-responsive design

**Story 2.4: Tribal AR PDF Export** (5 pts)

* *As a* tribal administrator  
* *I want* to export completed forms as PDF  
* *So that* I can maintain records and share submissions  
* **Acceptance Criteria:**  
  * PDF generation matches form structure  
  * Proper formatting and layout  
  * Include all submitted data and attachments  
  * Download and email capabilities  
  * Archive-quality output

**Story 2.5: Tribal AR Testing and Validation** (5 pts)

* *As a* quality assurance lead  
* *I want* comprehensive testing of Tribal AR form  
* *So that* users have a reliable experience  
* **Acceptance Criteria:**  
  * End-to-end user journey testing  
  * Cross-browser compatibility  
  * Mobile device testing  
  * Load testing for rural connections  
  * Accessibility compliance validation

**Story 2.6: Tribal AR Short Form Variant** (4 pts)

* *As a* tribal administrator  
* *I want* a streamlined short form option  
* *So that* I can complete simplified reporting when appropriate  
* **Acceptance Criteria:**  
  * Short form configuration from long form base  
  * Simplified field set and validation  
  * Same save/resume and export capabilities  
  * Clear differentiation in UI  
  * Seamless switching between versions

---

### **EPIC 3: USWDS Component Library (Continuous)**

**Epic Goal**: Build reusable components supporting all forms **Government Shutdown Safe**: 95% \- No external dependencies **Story Points**: 45 total (15 components × 3 points each)

#### **Weeks 1-10 Continuous Stories:**

**Story 3.1-3.5: Core Form Components** (15 pts)

* Text inputs, textareas, selects, checkboxes, radio buttons  
* *As a* developer, *I want* government-compliant form components  
* *So that* forms meet USWDS and accessibility standards

**Story 3.6-3.10: Layout and Navigation Components** (15 pts)

* Headers, footers, navigation, breadcrumbs, progress indicators  
* *As a* user, *I want* consistent navigation patterns  
* *So that* I can easily move through forms and applications

**Story 3.11-3.15: Advanced Form Components** (15 pts)

* File upload, date picker, address validation, calculation fields, repeatable sections  
* *As a* tribal administrator, *I want* specialized government form controls  
* *So that* I can efficiently complete complex reporting requirements

---

### **EPIC 4: Tribal Plan and Application \- Form 2**

**Epic Goal**: Deliver second form leveraging patterns from Tribal AR **Government Shutdown Safe**: 70% \- Can leverage Tribal AR patterns **Story Points**: 32 total

#### **Week 5+ Priority Stories:**

**Story 4.1: Tribal Plan Form Analysis** (4 pts)

* Similar to Story 2.1 but for Tribal Plan form  
* Leverage learnings from Tribal AR implementation

**Story 4.2: Tribal Plan Backend Development** (8 pts)

* Backend processing with pre-population from Tribal AR data  
* Enhanced integration capabilities

**Story 4.3: Tribal Plan Frontend Implementation** (10 pts)

* More complex UI leveraging established component library  
* Pre-population interface from previous submissions

**Story 4.4: Tribal Plan PDF Export and Integration** (5 pts)

* PDF generation plus integration with Tribal AR data  
* Cross-form reporting capabilities

**Story 4.5: End-to-End Integration Testing** (5 pts)

* Testing both forms together with data flows  
* Performance testing with multiple concurrent users

---

### **EPIC 5: Data Management and Export APIs**

**Epic Goal**: Enable data export and integration capabilities **Government Shutdown Safe**: 85% \- Mostly technical implementation **Story Points**: 25 total

**Story 5.1: API Framework Setup** (5 pts) **Story 5.2: Form Data Export APIs** (8 pts) **Story 5.3: Bulk Data Export for ACF** (7 pts) **Story 5.4: API Documentation and Testing** (5 pts)

---

### **EPIC 6: Continuous ATO and Security**

**Epic Goal**: Ensure continuous compliance work throughout quarter **Government Shutdown Safe**: 90% \- Documentation and technical work **Story Points**: 30 total (distributed across 11 weeks)

#### **Weekly 3-Point Stories (Weeks 2-11):**

* Week 2: Security Controls Documentation  
* Week 3: Risk Assessment and Threat Analysis  
* Week 4: System Security Plan Development  
* Week 5: Vulnerability Assessment Planning  
* Week 6: Security Testing Implementation  
* Week 7: Compliance Review and Gap Analysis  
* Week 8: Security Hardening Implementation  
* Week 9: Penetration Testing and Validation  
* Week 10: Documentation Review and Finalization  
* Week 11: ATO Package Preparation and Review  
* (Week 12: Final submission \- included in other epics)

---

### Sprint Planning

## Sprint 6

Dates 1/14-1/28  
9 working days this sprint | MLK Day is Holiday

Goals:

* **Long Form Implementation** \- Continue working on rendering and implementing the CSBG Annual Report (long form) with the design  
* **USWDS Components** \- Continue progressing on US Web Design System components  
* **Review Page Development** \- Build out the review page (sequenced after data saving)  
* Design Iterations  
* Develop Project Onboarding (Service Designer \+ Product Manager)  
* Recurring meeting with security team  
* Plan for monthly demo  
* New Project Name\!  
* Develop Healthy Backlog in case of govt shutdown

Team Capacity

- Tshering traveling to Philly on 1/28

Acceptance Criteria/Dependencies

Story Points

## Sprint 7 TBD

Theme: Complete Long Form Foundation & Enable Basic Workflow

**Complete Long Form Rendering & Data Persistence**

* Finalize rendering of CSBG Annual Report (long form) with real data  
* Complete data saving functionality across all form sections  
* Achievement: Users can start, fill out, and save form data

**Review Page MVP**

* Build basic review page showing saved data  
* Display all form sections in read-only view  
* Achievement: Users can review their completed form (Requirement \#2 \- Edit a form)

**Onboarding**

* Complete researcher onboarding  
* Complete product onboarding

## Sprint 8 TBD

**PDF Export Functionality**

* Generate PDF from review page data  
* Basic formatting with form structure

**Auto-save Implementation \- Phase 1**

* Implement periodic auto-save (every 30-60 seconds)  
* Basic success/failure messaging

**Research Plan \+ Dates Scheduled?**