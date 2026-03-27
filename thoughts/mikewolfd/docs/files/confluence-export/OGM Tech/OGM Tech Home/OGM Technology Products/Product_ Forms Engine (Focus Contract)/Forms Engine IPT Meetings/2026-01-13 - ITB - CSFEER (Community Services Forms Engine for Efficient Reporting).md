
[OGM Technology Products](../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Forms Engine IPT Meetings](../Forms%20Engine%20IPT%20Meetings.md)

# 2026-01-13 - ITB - CSFEER (Community Services Forms Engine for Efficient Reporting)

## Meeting Minutes: CSFEER IPT Kickoff Meeting

**Date:** January 13, 2026, 3:31 PM  
**Meeting Type:** Initial Integrated Project Team (IPT) Meeting  
**Project:** Community Services Forms Engine for Efficient Reporting (CSFEER)

### Attendees:

- **ACF Tech Team:** Jody Smith (CTR), Thomas Oldfield, Katherine Chase (CTR), John Warren, Oyindasola Akisanmi (CTR)
- **Focus Team:** Phaedra (Product Lead), Mohammad Taleb (Tech Lead), Tshering Yudon (Lead Designer), Ryan Bagwell (Engineer)

### Project Overview:

CSFEER is building a forms engine to collect data from rural tribal areas. The initial phase focuses on CSBG forms (annual report, long form, and short form) with an iterative approach to eventually serve the entire agency.

### Key Discussion Points:

**1. Infrastructure & Environment (NGSC)**

- Project will use ACF's NGSC (Next Generation Secure Cloud) AWS environment
- Lower and upper environments to be provisioned: Dev/Test, Stage, Prod
- Tech stack approved: Django and Postgres (already in NGSC)
- PIV/GFE requirement confirmed - Focus engineers are in process or have received PIVs
- Zscaler being installed to help manage access

**2. Security & ATO Process**

- Intake form has been completed
- System Registration form still needed to obtain UUID number
- Privacy Impact Analysis (PIA) required (system collects email addresses)
- Team interested in inheriting existing NGSC Security Controls / ATO rather than full extensive process
- Impact assessment to be conducted

**3. [Login.gov](http://Login.gov) Integration**

- System will use Okta for [login.gov](http://login.gov) integration
- ServiceNow ticket process for user setup
- Jim Cooper currently handling, new engineer Matt recently started to support Okta efforts
- Elsie (BA on Operations team) will facilitate integration

**4. Data Requirements**

- Need to ingest previous years' data for form pre-population
- APIs being built to expose all database data
- Two-way data flow: PDF export and API access
- Need external API access for user data from other systems (OLDC mentioned)
- Thomas Oldfield identified as liaison for data structure questions

### Decisions Made:

1. Weekly IPT meetings established at this time slot
2. Phased approach to ATO documentation (start with registration form and PIA)
3. Focus team to continue building in their own environment while NGSC provisioning proceeds
4. Two additional Focus engineers to be added to meeting invites

### Actions Table:

| Action Item                                                              | Owner                 | Due Date     | Status                                                                                                                    |
|:-------------------------------------------------------------------------|:----------------------|:-------------|:--------------------------------------------------------------------------------------------------------------------------|
| ~~Send meeting recording and minutes link~~                              | Jody Smith            | Week of 1/13 | Completed. Confluence link added to meeting invite agenda.                                                                |
| Set up recurring weekly IPT meeting                                      | Jody Smith            | Week of 1/13 | Pulled to 10, may need to revisit/deconflict                                                                              |
| ~~Provide names of two additional engineers for meeting invites~~        | Phaedra               | Week of 1/13 | Completed. [ryan.bagwell](mailto:ryan.bagwell@focusconsulting.io), [logan.ricard](mailto:logan.ricard@focusconsulting.io) |
| Send registration form for UUID number                                   | Oyindasola Akisanmi   | ASAP         | Pending                                                                                                                   |
| Send Privacy Impact Analysis (PIA) form                                  | Oyindasola Akisanmi   | ASAP         | Pending                                                                                                                   |
| Review completed intake form                                             | Oyindasola Akisanmi   | Next meeting | Pending                                                                                                                   |
| Identify and invite DBA team member to future IPT calls                  | Katherine Chase/Elsie | Next meeting | Pending                                                                                                                   |
| Identify and invite NGSC engineer to weekly calls                        | Katherine Chase       | Next meeting | Pending                                                                                                                   |
| Provide software version requirements                                    | Katherine Chase       | TBD          | Pending                                                                                                                   |
| Send list of required data from external systems                         | Mohammad Taleb        | TBD          | Pending                                                                                                                   |
| Coordinate Okta/[login.gov](http://login.gov) integration via ServiceNow | Focus Team/Jim Cooper | TBD          | Pending                                                                                                                   |

### Risks/Issues Table:

| Risk/Issue           | Description                                                     | Impact   | Mitigation                                                                       | Owner                          |
|:---------------------|:----------------------------------------------------------------|:---------|:---------------------------------------------------------------------------------|:-------------------------------|
| Timeline Uncertainty | Uncertain times with potential interruptions; need good runway  | Medium   | Starting NGSC provisioning early while continuing development in own environment | Focus Team/ACF Tech            |
| Data Isolation       | System creating users in isolation from existing systems (OLDC) | Medium   | Implement API integration to import existing users                               | Mohammad Taleb/Thomas Oldfield |
| ATO Timeline         | Full ATO process could delay production deployment              | Medium   | Explore inheriting existing AWS ATO; phased documentation approach               | Oyindasola Akisanmi            |
| Keycloak Update      | Keycloak being updated to something else                        | Low      | Monitor updates; adjust as needed                                                | Katherine Chase                |
| PIV/GFE Access       | Developers need PIV/GFE for NGSC access                         | Low      | Already in process/received                                                      | Focus Team                     |

### Next Steps:

- Weekly IPT meetings to begin next week (week of January 20, 2026)
- Focus team to reply to meeting invite with additional engineer names
- ACF Tech to add cross-functional team members (DBA, NGSC engineer) to future calls
- Security team to send registration and PIA forms
- Begin NGSC environment provisioning queue process

### Notes:

- Meeting was recorded and will be shared via Confluence
- IPT = Integrated Project Team (cross-functional team approach)
- Project has approximately one year until contractual production deadline
- Team expressed appreciation for the organized, collaborative approach

---

## Transcript

[ITB - CSFEER (Community Services Forms Engine for Efficient Reporting) 1-13-26.docx](../../../../attachments/.docx)

## Recording

### ACF GFE/PIV:

[Recap: ITB - CSFEER (Community Services Forms Engine for Efficient Reporting) Tuesday, January 13 | Meeting | Microsoft Teams](https://teams.microsoft.com/l/meetingrecap?driveId=b%21mYY0aTcMgEqG5StMJbp-hnsno-sM_EpKlWZr9UcbE-8niWwVL5pETIeIHiL_qwRM&driveItemId=01KWCL7ACIYIKPMNMOV5A3NA5RQPRL5KX5&sitePath=https%3A%2F%2Fhhsgov-my.sharepoint.com%2F%3Av%3A%2Fg%2Fpersonal%2Fjody_smith_acf_hhs_gov%2FIQBIwhT2NY6vQbaDsYPivqr9AbA6zy3vZTchVKvSdTkOsoI&fileUrl=https%3A%2F%2Fhhsgov-my.sharepoint.com%2Fpersonal%2Fjody_smith_acf_hhs_gov%2FDocuments%2FRecordings%2FITB%2520-%2520CSFEER%2520%28Community%2520Services%2520Forms%2520Engine%2520for%2520Efficient%2520Reporting%29-20260113_103144-Meeting%2520Recording.mp4%3Fweb%3D1&iCalUid=040000008200E00074C5B7101A82E008000000007086EDC5CB83DC01000000000000000010000000601B33E723CB284DBDFA85BF881CCA37&threadId=19%3Ameeting_OWQ2OWU0ZDMtY2MwYS00ZjFhLTkxYWEtNmMzOWE1Y2QzMzky%40thread.v2&organizerId=9aa79bfe-3ade-46ad-b8fb-dfe169e83495&tenantId=d58addea-5053-4a80-8499-ba4d944910df&callId=f128aabb-cac4-4f61-9076-3bb6c835abd6&threadType=Meeting&meetingType=Scheduled&subType=RecapSharingLink_RecapCore)

### External:

[ITB - CSFEER (Community Services Forms Engine for Efficient Reporting)-20260113_103144-Meeting Recording.mp4](../../../../attachments/.mp4)
