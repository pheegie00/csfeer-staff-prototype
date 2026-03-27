
[OGM Technology Products](../../../../OGM%20Technology%20Products.md) > [Product: Forms Engine (Focus Contract)](../../../Product_%20Forms%20Engine%20(Focus%20Contract).md) > [Engineering](../../Engineering.md) > [Tech Specs](../Tech%20Specs.md)

# CSFEER-2026-mm-dd Tech Spec template

**How to use this template**

- Fill in the table at the top with your name and date.
- Update the status in the top table throughout the process so readers know where the spec is in the process.
- The headings below are guidelines, not rules, so modify your copy as you see fit.
- Remove the instructions below each section heading (including this alert). These are just to help you understand the template and are not important to your spec’s readers.

**What are tech specs?**

Tech specs are a lightweight format for documenting technical research and decision-making. Be rigorous in your research and planning, but balance that with forward progress - if something is uncertain, document that appropriately and move on if you can. Getting feedback early from teammates during tech spec writing can be helpful, too.

Tech specs are considered 'done' when key stakeholders have reviewed and approved the approach.

**Credit:** This template is largely copied from <https://codeburst.io/on-writing-tech-specs-6404c9791159>

|                 |                                                            |
|:----------------|:-----------------------------------------------------------|
| **Author**      |                                                            |
| **Date**        |                                                            |
| **Reviewed by** |                                                            |
| **Status**      | Draft <br/> Ready for review <br/> Approved <br/> Deferred |

## Table of Contents:

- [Table of Contents:](#table-of-contents)
- [Overview](#overview)
- [Goals and Product Requirements](#goals-and-product-requirements)
- [Assumptions](#assumptions)
- [Out of Scope](#out-of-scope)
- [Open Questions](#open-questions)
- [Approach](#approach)
- [Schema Changes](#schema-changes)
- [Security and Privacy](#security-and-privacy)
- [Test Plan](#test-plan)
- [Deployment and Rollout](#deployment-and-rollout)
- [Rollback Plan](#rollback-plan)
- [Monitoring and Logging](#monitoring-and-logging)
- [Metrics](#metrics)
- [Long-term Support](#long-term-support)
- [Timeline](#timeline)

## Overview

Why are you creating this tech spec? Summarize the topic and link to external documents.

- Give context by pointing to product specs, design briefs, and engineering documents.
- Summarize the general approach.

## Goals and Product Requirements

These sections are optional if a product spec has already clearly defined the project goals and requirements; but if not, defining these will be the most important area of your spec.

## Assumptions

An engineering-centric list that digests the product requirements as technical behaviors and limitations. It tells external stakeholders precisely what you will build and how much your system can handle.

## Out of Scope

A list of what’s off the table, in particular features that aren’t included and internal process that you won’t own.

## Open Questions

As you write your tech spec, don’t stop to fill in all holes and TBD items. Just list them in the “Open Questions” section and keep going.

## Approach

Describe your solution in whatever level of detail is appropriate for you and your audience. Each subsystem, new technology choice, standard, etc. should have its own sub-section. You should also describe what other options you considered; or put this in a section “Other Options Considered.”

## Schema Changes

List all data storage changes, no matter how minor.

## Security and Privacy

It’s always a good idea to think about data protection, personal information, encryption, vectors of attack, etc, no matter how small a project may seem. Always include this section so people know you’ve thought about this, even if you just say “There should be no security or privacy concerns here.”

## Test Plan

Describe the testing strategy, both within your engineering team (unit and integration tests) and for QA (manual test plan and automated test suites).

## Deployment and Rollout

Consider the logistics and order of operations for go-live; and for subsequent releases. Discuss configuration management, secrets management, database changes, migrations, and your sign-off process.

## Rollback Plan

Explain what happens if something goes wrong with the deployment. What metrics and alerts should we watch? Is it possible to move backwards and restore our previous system? How?

## Monitoring and Logging

Show how we’ll know if there are problems in our software, know if the system is healthy, and be able to search through logs to track down bugs or customer issues.

## Metrics

Show how we’ll be able to answer business-level questions about the benefits and impact of a feature.

## Long-term Support

Consider questions like: who owns maintaining this software going forward? What are the long-term costs and “gotchas”? What happens if key people leave and we need to transfer knowledge?

## Timeline

Give a rough task break-down, by owner, in day-sized estimates (e.g. “The compliance engineering team creates widget X: ~3 person-days”). Be realistic; use actual person-calendar-days and not theoretical “if we were 100% focused…” estimates; and include padding for integrations, risks, and meetings. Account for tasks required for all teams, not just your own.
