
[OGM Technology Products](../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Forms Engine IPT Meetings](../Forms%20Engine%20IPT%20Meetings.md)

# 2026-02-10- ITB - CORE Meeting Minutes

**Attendees:**   
Jody Smith (ACF/CTR)  
Mohammad Taleb  
Amanda Welch (ACF/CTR)  
Ryan Bagwell  
Phedra Arthur  
Simone Saldanha  
Thomas Oldfield  
Susan Burton  
Tshering Yudon  
Katherine Chase (ACF/CTR)  
Tharunkumar Reddy Chada (ACF/CTR)  
Oyindasola Akisanmi (ACF/CTR)  
Liane Peng

## Summary

This was a technical coordination meeting between ACF staff and Focus team members to discuss project setup, access provisioning, authentication services, and compliance documentation.

Key topics included JIRA/Confluence access, authentication architecture, privacy documentation, and infrastructure planning.

## Discussion Points

### 1. Access and Tracking

- JIRA and Confluence access has been granted to some team members
- Discussion about providing Focus team visibility into ACF's Operations JIRA board/project for tracking work status
- Focus team only needs visibility into tickets related to their work, not all ACF work
- ServiceNow ticket tracking was discussed for monitoring provisioning requests

### 2. Technical Coordination

- Agreement to establish a regular technical series meeting between Katherine Chase's team and Focus team
- This technical call will serve as the venue to review work boards and track progress together
- Will include Matt Ding for [login.gov](http://login.gov) discussions

### 3. Authentication Services

- **Government Users:** Will use Okta authentication via [login.acf.gov](http://login.acf.gov)
- **Non-Government Users:** Separate authentication path (details to be confirmed)
- Roles and permissions managed through Okta groups that sync with the application (similar to AD/SSO integration)
- [Login.gov](http://Login.gov) integration details to be discussed with Matt Ding in technical sessions

### 4. Privacy and Compliance

- Questions raised about system classification for Privacy Impact Assessment (PIA)
- System likely classified as "electronic information collection" but needs confirmation
- Privacy team (Tobi) to provide guidance on classification rubric
- BIA, Contingency Plan, and Incident Response Plan documentation overlap and work together

### 5. Infrastructure

- Mohammad Taleb shared infrastructure diagram for review
- Team can provide comments and updates on the shared page

### 6. GitLab Repository Setup

- Repository setup scheduled for next sprint (starting next Wednesday)
- Will include account bootstrapping and baseline infrastructure
- Option to mirror/sync from existing GitHub repository

## Actions

|     | **Item**                                                                                                                    | **Owner**                           | **Status**   | **Due Date**                          |
|----:|:----------------------------------------------------------------------------------------------------------------------------|:------------------------------------|:-------------|:--------------------------------------|
|   1 | Provide Focus team with visibility (watchers) into relevant JIRA tickets (explore options: board access or regular updates) | Katherine Chase / Jim               | Open         | TBD                                   |
|   2 | Determine method for Focus team to track ServiceNow ticket status for Okta related requests                                 | Katherine Chase                     | Open         | TBD                                   |
|   3 | Set up regular technical series meeting between ACF ops team and Focus team                                                 | Katherine Chase                     | Open         | TBD                                   |
|   4 | Ensure Matt Ding attends technical call to discuss [login.gov](http://login.gov) integration details                        | Katherine Chase                     | Open         | TBD                                   |
|   5 | ~~Facilitate introduction to records management team~~                                                                      | ~~Jody Smith~~                      | ~~Closed~~   | ~~EOD~~                               |
|   6 | Provide rubric/guidance for system classification in PIA (electronic information collection vs. application)                | Oyindasola Akisanmi  (Privacy Team) | Open         | TBD                                   |
|   7 | Review and provide feedback on infrastructure diagram shared by Mohammad                                                    | All team members                    | Open         | Ongoing                               |
|   8 | Set up GitLab repositories, accounts, and baseline infrastructure                                                           | Tharunkumar Reddy Chada             | Open         | Next Wednesday (start of next sprint) |
|   9 | Configure GitHub to GitLab mirroring/sync                                                                                   | Tharunkumar Reddy Chada             | Open         | After next Wednesday                  |

## Risks

|     | **Item**                                                                                                                                                                                                                      | Owner                                |  Status                                                                                                              | Due   |
|----:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------|:---------------------------------------------------------------------------------------------------------------------|:------|
|   1 | **If** the non-government user authentication path is not clarified and confirmed, **then** development and integration work may be delayed or require rework due to incorrect assumptions about authentication architecture. | Tharunkumar Reddy Chada / Jim Cooper | Open <br/> Uncertainty about whether non-GFE users can access through Okta or require a separate authentication path | TBD   |
|   2 | **If** clear documentation/rubric for PIA system classification is not provided, **then** the compliance process may be delayed, potentially blocking system deployment and ATO approval.                                     | Privacy Team                         | Open <br/> Liane is working with RM Team                                                                             | TBD   |

## Next Steps

1. Privacy team to provide PIA classification guidance
2. Jody Smith to introduce project team to records management liaison
3. Infrastructure setup to begin next Wednesday
4. Team to review Mohammad's infrastructure diagram and provide feedback

## Recording

[Recap: IPT - CSFEER (Community Services Forms Engine for Efficient Reporting) Tuesday, February 10 | Meeting | Microsoft Teams](https://teams.microsoft.com/l/meetingrecap?driveId=b%21X1MTJHNRF02FjTvQ4b0otv7-_9yxqktAqGfny4YFNoYo8x8Mt0-EQ6YajXLBtnpv&driveItemId=01EEBYER6HPAPOVM3RVNHKPU3JQGUDP735&sitePath=https%3A%2F%2Fhhsgov-my.sharepoint.com%2F%3Av%3A%2Fg%2Fpersonal%2Ftharunkumarreddy_chada_acf_hhs_gov%2FIQDHeB7qs3GrTqfTaYGoN_99AY_ys37bE1-5-a7A3bzIV9s&fileUrl=https%3A%2F%2Fhhsgov-my.sharepoint.com%2Fpersonal%2Ftharunkumarreddy_chada_acf_hhs_gov%2FDocuments%2FRecordings%2FIPT+-+CSFEER+%28Community+Services+Forms+Engine+for+Efficient+Reporting%29-20260210_145946UTC-Meeting+Recording.mp4%3Fweb%3D1&iCalUid=040000008200E00074C5B7101A82E00807EA020A308EFAFC7C85DC01000000000000000010000000768F83A6100F1C4386EEA56EDC365DD1&masterICalUid=040000008200E00074C5B7101A82E00800000000308EFAFC7C85DC01000000000000000010000000768F83A6100F1C4386EEA56EDC365DD1&threadId=19%3Ameeting_MzhiMDMxZjItMDlkOS00NTNmLTljNTQtNDRmODIzYzM1YjVj%40thread.v2&organizerId=9aa79bfe-3ade-46ad-b8fb-dfe169e83495&tenantId=d58addea-5053-4a80-8499-ba4d944910df&callId=6f98572f-ba12-4ad6-b1c1-52cb677f6135&threadType=Meeting&meetingType=Recurring&subType=RecapSharingLink_RecapCore)
