
[OGM Technology Products](../../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Engineering](../../Engineering.md) > [Tech Specs](../Tech%20Specs.md)

# Tech Spec: Form Manager Application (WIP)

|                 |                                                                        |
|:----------------|:-----------------------------------------------------------------------|
| **Author**      | Ryan Bagwell (CTR)                                                     |
| **Date**        | 2/13/26 (last updated 2/24/26)                                         |
| **Reviewed by** |                                                                        |
| **Status**      | Draft <br/> ~~Ready for review~~ <br/> ~~Approved~~ <br/> ~~Deferred~~ |

## Table of Contents:

- [Table of Contents:](#table-of-contents)
- [Overview](#overview)
  - [Features](#features)
- [Goals and Product Requirements](#goals-and-product-requirements)
  - [Broad product goals for requirements for the MVP (maintained here) are:](#broad-product-goals-for-requirements-for-the-mvp-maintained-here-are)
- [Out of Scope](#out-of-scope)
- [Approach](#approach)
  - [User Flow Overflow](#user-flow-overflow)
  - [Form Rendering](#form-rendering)
  - [USWDS component library](#uswds-component-library)
  - [Validation and draft data](#validation-and-draft-data)
  - [Form statuses](#form-statuses)
- [Data Models](#data-models)
- [Test Plan](#test-plan)
  - [Unit Tests](#unit-tests)
  - [End-to-End Tests](#end-to-end-tests)

## Overview

The **Form Manager** application is a Python application built to run in the Django web framework. This application will be responsible for handling all form operations, including form definitions, user submissions, versioning, audit trails, and PDF generation

### Features

The Form Manager enables:

- **Dynamic Form Creation**: Forms are defined as Python/Pydantic schemas that generate both UI structure and validation rules from a single source of truth
- **Draft Management**: Users can save progress and return to incomplete forms
- **Version Control**: Multiple form versions per organization with complete submission history
- **Audit Compliance**: Field-level change tracking with ability to reconstruct historical snapshots
- **Role-Based Access**: Organization-level permissions (admin, editor, viewer)
- **PDF Export**: Generate compliance-ready PDF documents of submitted forms

---

## Goals and Product Requirements

### Broad product goals for requirements for the MVP ([maintained here](https://confluence.acf.gov/spaces/OXT/pages/168823288/Initial+Product+Spec+-+MVP)) are:

1. Deploy a production-ready forms platform that replaces all three PDF-based Tribal CSBG reporting processes.
   1. All three Tribal forms live in production
   2. Full end-to-end workflow supported
   3. 20+ Tribal grant recipients submit via CORE without reverting to PDFs
2. Build reusable platform capabilities that demonstrate the forms engine can scale beyond Tribal forms.
   1. [Login.gov](http://login.gov/) authentication, role-based access, PDF + CSV exports operational
   2. Platform supports both simple and complex forms
   3. Architecture documentation complete for Phase II
3. Deliver superior user experience while meeting federal compliance requirements.
   1. ≥80% of users report digital experience is easier than PDFs
   2. 100% Section 508 compliance
   3. Zero ACF OCIO security or compliance findings

---

## Out of Scope

The following items are explicitly **not** included in the Form Manager MVP:

- Low code/no code form builder application
- Simultaneous multi-user editing
- Approval workflows or routing between users
- Email notifications for status changes
- API endpoints
- Authorization and access control

---

## Approach

Our approach starts with creating a common form schema that can be used to generate any type of form experience desired. Each form schema is a Python/Pydantic class that includes 1) metadata about the form (i.e. name, version, etc); 2) a standard Django Form class that contains form field definitions and ultimately handles validation, and 3) a user experience definition that determines how each form will be rendered and presented to the user.

There is currently only one type of user experience - an interview-style view that presents users with a few fields to complete on each page. However, the UI definition can be customized to accommodate a variety of user experiences. The schema can also be modified to accommodate other desired user flows.

Although form schemas are hard-coded in Python, they must ultimately be imported into the database as FormDefinition objects for users to select for completion. Each FormDefinition record contains the name of the schema class.

### User Flow Overflow

A form's interview-style lifecycle looks like this:

1. After authenticating, users are taken to a page where they can select a form to start working on.
2. When a user starts a form, a new `FormEntry` model instance is created and saved in the database. The user is then redirected to the first page of the form.
3. The user enters data, and clicks the button to move to the next page with a `POST` request. This adds the saved data to the `FormEntry`  model in JSON format.
4. The server processes the request, determines what page to display next, and provides a response with HTML for the next page.
5. When a user has filled out all fields, they're taken to a review page. This is where validation happens and any form errors are displayed.
6. Users can go back to a page to edit form fields and correct any validation errors.
7. When all errors have been fixed and the form has been validated in its entirety, users can submit the form for staff review.

### Form Rendering

Rendering is accomplished by using the Django template framework. We've created series of custom UI component blocks in Python that are subclassed from the same rendering logic as Django form fields. Each block can have children, forming a tree of of component blocks on each page. Each block can have its own template. Templates receive the following context:

|                                               |                                                    |
|:----------------------------------------------|:---------------------------------------------------|
| <br/>```<br/>prev_url<br/>```<br/>            | the url of the previous page                       |
| <br/>```<br/>form<br/>```<br/>                | the Django form object                             |
| <br/>```<br/>is_last_page<br/>```<br/>        | boolean value that indicates this is the last page |
| <br/>```<br/>current_step_number<br/>```<br/> | the current step number                            |
| <br/>```<br/>current_page_number<br/>```<br/> | the current page number                            |

Field Rendering

Fields are rendered using the built-in Django form field rendering API. We've created custom templates that allow us to use the USWDS Django component library.

### USWDS component library

We've built a library of [US Web Design System](https://designsystem.digital.gov/) components to use for rendering Django form fields. While this library is a separate application inside this Django project, we hope to break it out into its own project and eventually make it open source.

### Validation and draft data

To provide the ability for users to partially save a form and come back and work on it later, any arbitrary data can be entered into fields, whether it's valid or not. Forms cannot, however, be submitted for final review until all validation error have been resolved.

Validation is achieved through Django's built-in form API. Form fields use default validation rules but custom rules can be specified at both the form and field level.

### Form statuses

Forms can have the following statuses:

| Status                              | Description                                                                                      |
|:------------------------------------|:-------------------------------------------------------------------------------------------------|
| <br/>```<br/>draft<br/>```<br/>     | The form is being completed. Users can continue to edit these forms. This is the initial status. |
| <br/>```<br/>submitted<br/>```<br/> | All validation rules have passed, and the form has been submitted for agency review.             |
| <br/>```<br/>archived<br/>```<br/>  | The form submission is available but hidden from the user's view.                                |

 

---

## Data Models

The Form Manager has a handful of core database models:

|                                           |                                                                                                                                                         |
|:------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| <br/>```<br/>FormDefinition<br/>```<br/>  | Represents a specific form schema that users can complete                                                                                               |
| <br/>```<br/>FormEntry<br/>```<br/>       | Represents an instance of a FormDefinition that belongs to an organization and a user has started to work on. Form field data is saved in a JSON field. |
| <br/>```<br/>FormAuditTrail<br/>```<br/>  | Represents a log of an action that a specific user took pertaining to a specific form entry.                                                            |
| <br/>```<br/>FormAuditDetail<br/>```<br/> | Represents a more detailed log of changes that a user made to a specific form entry, including changes to fields.                                       |

 

![](/download/attachments/182916642/csfeer_form_manager.png?version=1&modificationDate=1771864688756&api=v2)

---

## Test Plan

### Unit Tests

- Model creation and validation
- Field validation and calculated fields
- Conditional field visibility
- Utility functions (save, audit, reconstruct)

### End-to-End Tests

- Selenium/Playwright tests for full workflow
