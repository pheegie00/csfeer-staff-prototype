# Plan: Integrate Confluence Analysis into INFO_MAP.md

## Context

The previous session dispatched 36 sub-agents to cross-reference every Confluence export file against UNDERSTANDING.md (the PRD synthesis). All 36 completed successfully and their results are compiled in
`recovered_agent_results.md` (221K chars, ~2378 lines). The INFO_MAP.md skeleton exists but the "File Analyses" and "Cross-Cutting Findings" sections are still stubs.

**The purpose is context engineering for building the forms engine product.** INFO_MAP.md should be an at-a-glance source of truth for what's in the Confluence space — conveying enough information on its own to orient someone
without reading every doc. It's framed around the goal of building this product: what the client thinks, wants, needs, and worries about. Not every detail, but enough to navigate confidently.

## Target File

`thoughts/shared/confluence-export/OGM Tech/INFO_MAP.md`

## Source Material

`thoughts/shared/confluence-export/OGM Tech/recovered_agent_results.md` — 36 agent analyses, each containing:
- Category + Summary
- New facts not in UNDERSTANDING.md
- Inconsistencies between sources
- Missing details / oversights in UNDERSTANDING.md

Also read the interstitial sections: directory tree (line 17), summary (line 86), cross-reference analyses (lines 1920, 2314), and analysis summary (line 2366).

## Reading Order

Read the agent results in this order, not file order. Each layer builds on the previous one so context accumulates naturally.

### Layer 1 — "What is this project?" (foundational context)

Read these first to understand the agency, the problem space, and how the project started.

| Order | Lines       | File                                | Category               |
|-------|-------------|-------------------------------------|------------------------|
| 1     | 1461–1551   | OCS and CSBG Overview.md            | Discovery / Background |
| 2     | 110–171     | CSBG Reporting Process.md           | Discovery / Background |
| 3     | 2000–2068   | CSBG Annual Report.md               | Discovery / Forms      |
| 4     | 172–244     | Forms Engine Onboarding Documents.md| Onboarding / Reference |

### Layer 2 — "What was decided?" (early meetings & vision)

Now read the kickoff meetings and product spec, chronologically.

| Order | Lines       | File                                     | Category                     |
|-------|-------------|------------------------------------------|------------------------------|
| 5     | 1720–1779   | 2024-06 Initial Conversation w/ Minette  | Meeting Notes / Early Discovery |
| 6     | 1552–1638   | 2025-09-17 Kickoff Prep                  | Meeting Notes / Kickoff Prep |
| 7     | 1639–1719   | 2025-09-25 Kickoff with CSBG Staff       | Meeting Notes / Kickoff      |
| 8     | 1290–1339   | 2025-09-29 Kickoff with Focus            | Meeting Notes / Kickoff      |
| 9     | 938–1004    | Initial Product Spec - MVP.md            | Product Specification        |

### Layer 3 — "What's the current state?" (recent meetings & status reports)

Chronological run through check-ins, demos, CSRs, and ITB meetings.

| Order | Lines       | File                                     | Category               |
|-------|-------------|------------------------------------------|------------------------|
| 10    | 1340–1418   | 2025-11-20 Check-in (CSBG w/ OGM Tech)  | Meeting Notes          |
| 11    | 1909–1962   | 2025-11-26 Forms Digitization            | Meeting Notes          |
| 12    | 1780–1828   | 2025-12-05 Demo 1 (Focus / ACF)         | Meeting Notes / Demo   |
| 13    | 670–735     | CSR - Forms Engine CSFEER (initial)      | Contract Status Reports|
| 14    | 736–809     | CSR - December 2025                      | Contract Status Reports|
| 15    | 444–508     | CSR - January 2026                       | Contract Status Reports|
| 16    | 810–876     | 2026-01-13 ITB Meeting                   | IPT Meeting Minutes    |
| 17    | 1076–1166   | 2026-01-27 ITB Meeting                   | IPT Meeting Minutes    |
| 18    | 877–937     | 2026-02-03 ITB Meeting                   | IPT Meeting Minutes    |
| 19    | 1005–1075   | 2026-02-10 ITB CORE Meeting             | IPT Meeting Minutes    |
| 20    | 2193–2229   | 2026-01-28 Q1 Planning Session           | Meeting Notes / Planning|
| 21    | 2069–2116   | 2026-02-13 Meeting Notes                 | Meeting Notes          |

### Layer 4 — "How are we building it?" (technical decisions)

Technical docs are easier to evaluate after understanding the meetings that drove them.

| Order | Lines       | File                                     | Category                     |
|-------|-------------|------------------------------------------|------------------------------|
| 22    | 370–443     | CSFEER Tech Stack.md                     | Engineering                  |
| 23    | 588–669     | Tech Spec: Form Manager Application (WIP)| Engineering / Tech Specs     |
| 24    | 509–587     | Tech Spec: Okta Authentication DRAFT     | Engineering / Tech Specs     |
| 25    | 245–302     | CSFEER Tech Spec Template                | Engineering / Templates      |
| 26    | 1230–1289   | ATO Documentation & Compliance Hub       | Security / Compliance        |
| 27    | 2117–2156   | Technical Architecture & Security Framework| Architecture / Infrastructure|
| 28    | 1963–1999   | Risk Management.md                       | Operations / Continuity      |

### Layer 5 — "Who and how?" (people, research, process)

Enrichment on top of everything else.

| Order | Lines       | File                                     | Category                |
|-------|-------------|------------------------------------------|-------------------------|
| 29    | 1829–1908   | Product_ Forms Engine (team directory)   | Team Directory / Personnel|
| 30    | 1167–1229   | Design & Research.md (index)             | Design & Research (index)|
| 31    | 303–369     | User Research Plan.md                    | Design & Research        |
| 32    | 2269–2304   | CSBG Data Files.md                       | Reference / Data Files   |

### Layer 6 — Skim (index/navigation pages, minimal content)

These are mostly empty or structural. Skim for any unexpected content but don't expect much.

| Order | Lines       | File                                     | Category            |
|-------|-------------|------------------------------------------|---------------------|
| 33    | 1419–1460   | Index page                               | Index / Navigation  |
| 34    | 2157–2192   | Index page                               | Index / Navigation  |
| 35    | 2230–2268   | Index page                               | Index / Navigation  |
| 36    | 2305–2378   | Contract Status Template + Engineering + Tech Specs (empty pages) | Navigation / Empty |

## Proposed Structure for INFO_MAP.md

Rewrite the file with this structure (keep the directory tree at top):

### 1. Directory Structure (existing — keep as-is)

### 2. Client Mental Model
What the client believes this project is, how they frame it internally, and how that framing has evolved. Synthesized from onboarding docs, meeting notes, product spec.

### 3. Stakeholder Map
Who matters, who has influence, who blocks. Names, roles, and what they care about.

### 4. What the Client Wants
Concrete deliverables and capabilities they've asked for, organized by urgency and confidence level.

### 5. What the Client is Concerned About
Explicit and implicit concerns surfaced across documents — risks, anxieties, political sensitivities.

### 6. Unresolved Questions & Ambiguities
Places where Confluence docs contradict each other or leave gaps.

### 7. Timeline & Milestones
Key dates extracted from all sources, organized chronologically.

### 8. File Index
Brief one-line summary of each Confluence file with category tag. Purpose: quick lookup, not deep reading.

## Execution Approach

**No sub-agents or skills.** Read everything directly.

**Phase 1: Read layer → write scratch → repeat** — Work through `recovered_agent_results.md` following the reading order above. After completing each layer's reads, immediately append scratch notes to the `## Scratch` section at the bottom of INFO_MAP.md. This captures progress incrementally and prevents context window pressure.

Each layer's scratch block should be structured:

```markdown
### Layer N — [title]
**Key facts for INFO_MAP sections:**
- §2 Client Mental Model: ...
- §3 Stakeholder Map: ...
- §4 What the Client Wants: ...
- §5 What the Client is Concerned About: ...
- §6 Unresolved Questions & Ambiguities: ...
- §7 Timeline & Milestones: ...
- §8 File Index entries: ...
```

Only note material that's INFO_MAP-worthy — not every detail from the agent results, but what matters for orienting someone building this product. Each layer should also flag items that need spot-checking against source files.

**Phase 1b: Spot-check source files** — For any contradictions or claims flagged during scratch writing, go back to the actual Confluence source files to verify. Don't propagate interpretation errors from the agent summaries. Annotate the scratch notes with verification results.

**Phase 2: Write INFO_MAP.md** — Synthesize the scratch notes into the final file. Replace the entire file (including scratch section) with the final structure. Write it all at once to ensure coherent voice and cross-referencing between sections.

**Note:** Keep `recovered_agent_results.md` — it's a useful reference artifact with the full per-file analysis detail.

## Verification

- INFO_MAP.md should be self-contained and readable as an at-a-glance briefing
- Every Confluence file should appear in the File Index (section 8)
- No orphaned stubs or "PENDING" placeholders
- Sections should cite source documents by short name when making specific claims
- Contradictions in section 6 should be verified against source files, not just agent summaries
- Target length: 400-600 lines (dense but scannable)
