
[OGM Technology Products](../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Forms Engine IPT Meetings](../Forms%20Engine%20IPT%20Meetings.md)

# 2026-02-03 - ITB - CSFEER Meeting Minutes

## IPT - CSFEER (Community Services Forms Engine for Efficient Reporting)

**Date:** February 3, 2026, 3:01 PM  
**Meeting Type:** Technical Status Update  
**Prepared by:** Credal AI Assistant (based on transcript), Reviewed by Jody S.

---

## Attendees

- Smith, Jody (ACF) (CTR) - Meeting Lead
- Akisanmi, Oyindasola (ACF) (CTR) - Security/ATO Lead
- Chase, Katherine (ACF) (CTR) - Technical Lead
- Jones, Harold (ACF)
- Phedra (Focus Team)
- Mohammad Taleb (MO)
- Tshering Yudon

**Note:** Several federal employees were absent due to government shutdown.

---

## Executive Summary

This was a focused technical status meeting to review progress on security-related items and infrastructure setup for the CSFEER project. The team made significant progress on security documentation, with the project intake completed and ATO documentation submitted. Key discussions centered around access provisioning (Confluence, JIRA, NGSC environment), Okta integration setup, and form submission priorities for ATO assessment. The meeting was efficient, with most action items from the previous meeting completed or in progress.

---

## Key Discussion Points

### 1. **Security & ATO Progress**

- Project intake for security team has been completed and submitted
- ATO documentation list has been sent to the security team
- Appendix X has been noted and added to ATO list by Focus team
- Security Control Assessment (SCA) team has been notified of system plans and will incorporate into assessment schedule

### 2. **Access & Infrastructure Setup**

- Confluence access for Ryan and Logan is pending - Jody to check ticket queue
- NGSC environment setup will be tracked through the Operations team's JIRA board (not ServiceNow)
- Mohammad (MO) received PIV card - no longer a blocker
- Team requested watcher access to Ops JIRA board for visibility

### 3. **Okta Integration**

- ServiceNow link for Okta request to be shared with Focus team
- Harold Jones, Matt Dang, and Operations team will handle the integration process
- Decision made to address in technical discussion rather than formal ticket submission initially

### 4. **Technical Architecture**

- Team proceeding with ECS and Postgres database as discussed in previous technical meeting

### 5. **Friday Meeting Outcomes**

- Focus team meeting on Friday was successful
- Points of contact established for different areas
- No additional actions required from that session

---

## Decisions Made

1. **Meeting minutes location:** Minutes will be moved from current Confluence space to OGM Tech space for broader team access
2. **NGSC environment tracking:** Will use Operations JIRA board for tracking system related epics/stories
3. **Okta integration approach:** Will be handled through direct coordination with Harold Jones, Matt Dang, and LCSR team
4. **Form submission priority:** No specific priority order required - forms can be submitted as completed for ATO assessment

---

## Action Items

|     | Action Item                                                                           | Owner                         | Due Date           | Status      |
|----:|:--------------------------------------------------------------------------------------|:------------------------------|:-------------------|:------------|
|   1 | Check ticket queue for Ryan and Logan Confluence access; submit ticket if not present | Jody Smith                    | Next meeting       | Open        |
|   2 | ~~Move meeting minutes to OGM Tech Confluence space~~                                 | Jody Smith                    | Next meeting       | Complete    |
|   3 | Add Focus team members as watchers to JIRA board                                      | Katherine Chase               | Next meeting       | Open        |
|   4 | Follow up with Liane on OCS data strategy meeting status                              | Jody Smith                    | When Liane returns | Open        |
|   5 | Continue submitting completed forms to Oyinda for ATO assessment                      | Mohammad/Team                 | Ongoing            | In Progress |
|   6 | Track NGSC environment setup through JIRA board                                       | Tharun/Katherine              | Ongoing            | In Progress |
|   7 | Coordinate Okta integration with Focus team                                           | Harold Jones, Matt Dang, LCSR | TBD                | Open        |

---

## Risks

| Risk                                                                                                                                    | Impact                                                      | Mitigation                                                                                                              |
|:----------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------|
| ~~If government shutdown continues, then federal employee availability will remain limited and may delay decision-making or approvals~~ | ~~Project timeline delays, reduced oversight~~              | ~~Continue technical work that doesn't require federal approval; maintain documentation for review when staff returns~~ |
| If Confluence/JIRA access is not granted promptly, then Focus team visibility into project status will be limited                       | Communication gaps, potential rework, reduced collaboration | Expedite access requests; use alternative communication channels (email, direct meetings) in interim                    |
| If ATO documentation is incomplete or delayed, then security assessment timeline may slip                                               | Project go-live delays, compliance issues                   | Oyinda maintaining checklist; proactive submission of completed forms as they're ready                                  |
| If NGSC environment setup encounters technical issues, then development and testing activities may be blocked                           | Development delays, compressed testing timeline             | Early coordination with Tharun; track closely through JIRA board; escalate issues promptly                              |

---

## Parking Lot / Backlog

1. **OCS Data Strategy Meeting** - Liane to schedule/conduct meeting with OCS team; status to be determined upon her return
2. **ServiceNow Ticket for Okta Integration** - While work will proceed directly, formal ticket may be created for documentation purposes
3. **Weekly Technical Updates** - Establish regular cadence for status updates during technical calls to keep Federated team informed of progress

---

## Next Steps

- **Next Technical Session:** TBD
- **Next IPT Meeting:** Next week (February 10, 2026)
- **Focus:** Continue infrastructure setup, complete access provisioning, maintain momentum on ATO documentation

---

**Meeting Adjourned:** Approximately 3:26 PM (25-minute meeting)
