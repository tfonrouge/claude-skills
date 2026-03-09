---
name: business-module-workflow
metadata:
  version: 0.1.0
description: >
  Structured workflow for building modules in large-scale business software systems using Claude Code
  as a development partner. Use this skill whenever a user mentions building, designing, planning, or
  implementing any software module with business logic — e.g. ERP, CRM, WMS, SaaS platform, internal
  tooling, or enterprise application modules (e.g. "Maintenance Orders", "Import Management",
  "Inventory", "Billing", "HR", "Customer Onboarding", "Approval Workflows").
  Also trigger when users ask about module specifications, flow charts, API contracts, implementation
  plans, test routing maps, traceability, or any structured multi-artifact module development process.
  If the user says "let's build a module", "start a new module", "design a feature module", or asks
  for help structuring a software component with business rules and integrations, use this skill
  immediately — even if they haven't named a specific platform or system type.
---

# Business Module Workflow

A repeatable, Claude Code–assisted methodology for building any module in a large-scale business
software system. Each module produces a standard set of artifacts in a shared `module-descriptor/` directory.

## Overview of Artifacts

| Step | Artifact | Purpose |
|------|----------|---------|
| 0 | `BRIEF.md` | Context, owner, justification |
| 1 | `SPECIFICATION.md` | What the module does |
| 2 | `FLOWCHART.md` | How it flows (Mermaid diagrams) |
| 3 | `API_CONTRACT.md` | How it connects to other modules |
| 4 | `IMPLEMENTATION_PLAN.md` | How it will be built |
| 5 | `TEST_PLAN.md` | How it will be verified |
| 6 | `TRACEABILITY_MATRIX.md` | Living progress tracker (init here, update always) |
| 6b | `GANTT.html` | Print-ready timeline snapshot (regenerate every sprint) |

> **TRACEABILITY_MATRIX.md is a living document.** Initialize it after Step 4 and update it
> continuously as work progresses. It is never "done."

---

## Why This Workflow

### Claude Code Efficiency Gains
Claude Code performs significantly better when given structured context. Without artifacts, it guesses intent, invents data models, and makes integration assumptions that conflict with the rest of your system. With this workflow:
- **SPECIFICATION.md** gives Claude a precise contract to code against — no ambiguity, no hallucinated business rules
- **FLOWCHART.md** lets Claude generate code that handles every branch, not just the happy path
- **API_CONTRACT.md** means Claude can write integration code that matches what the other module actually emits
- **TEST_PLAN.md** enables Claude to write tests that trace real requirements, not synthetic ones it invented

The result: less back-and-forth correction, fewer "that's not what I meant" moments, and significantly more of Claude's context window spent on building rather than re-clarifying.

### Team Alignment & Onboarding
Every artifact is a communication tool, not just documentation:
- A new developer can read `SPECIFICATION.md` + `FLOWCHART.md` and be productive on day one without needing a senior developer to explain the module
- Disagreements about scope get resolved at Step 1 (cheap) instead of Step 4 (expensive)
- The standard directory structure means any team member can navigate any module instantly — no "where do I find X?" overhead

### Risk Reduction — Catching Errors Early
The artifact chain creates mandatory checkpoints before expensive work begins:

| Where error is caught | Cost |
|-----------------------|------|
| Step 1 — wrong requirement | Near zero — edit a markdown file |
| Step 3 — integration mismatch | Low — update the contract before coding |
| Step 4 — scope too large | Medium — re-plan before building |
| Step 5 — missing test coverage | Medium — add tests before ship |
| After shipping | High — hotfix, rollback, customer impact |

The workflow front-loads discovery. API contract mismatches — the most common large-team failure mode — are caught at Step 3, before a single line of integration code is written.

### Scalability Across Many Modules
In a large system, consistency compounds. When every module follows the same structure:
- Cross-module reviews become fast — reviewers know exactly where to look
- Traceability across the whole system is trivial to aggregate
- Claude can be given artifacts from *multiple* modules and reason about their interactions reliably
- New modules can be bootstrapped by referencing existing ones as patterns

Without a standard, each module becomes a snowflake. The tenth module is as hard to onboard as the first.

### Stakeholder & Management Buy-In
Each artifact maps cleanly to a stakeholder concern:
- **SPECIFICATION.md** → business owner confirms scope before money is spent
- **IMPLEMENTATION_PLAN.md** → management sees phases, timelines, and risks upfront
- **TRACEABILITY_MATRIX.md** → real-time progress visibility without status meetings
- **TEST_PLAN.md** → QA and compliance teams can verify coverage before sign-off

The workflow produces evidence of rigor — useful when justifying timelines, requesting resources, or demonstrating compliance to auditors.

---

## Step 0: BRIEF.md (Kickoff)

> **Refactoring an existing module?** This workflow applies equally to refactors, but each step
> has important differences. Read `references/refactor-guide.md` before proceeding — it overrides
> and supplements the default behavior of every step below.

### Actions
1. Create the directory:
   ```
   module-descriptor/
   └── <ModuleName>/
   ```
2. Confirm the following with the team before proceeding:

| Field | Description |
|-------|-------------|
| Module Name | PascalCase identifier, e.g. `ImportManagement` |
| Business Owner | Who is accountable for requirements |
| Business Justification | Why this module is needed now |
| Key Stakeholders | Who reviews and signs off |
| Target Go-Live | Rough date or sprint target |
| Integration Surface | Which other modules it touches |

### Claude Code Prompt Pattern
```
I want to start a new module called [ModuleName] for [system/platform name].
Here's the context: [paste kickoff fields above].
Help me validate this scope is well-defined before we write the specification.
```

### Definition of Done
- [ ] Directory created at `module-descriptor/<ModuleName>/`
- [ ] `BRIEF.md` created and all kickoff fields populated
- [ ] Business owner has reviewed and signed off on justification and scope
- [ ] Integration surface identified at a high level
- [ ] No unresolved ambiguities before proceeding to Step 1

---

## Step 1: SPECIFICATION.md

### Purpose
Define *what* the module does — its boundaries, rules, data, and actors.

### Required Sections
1. **Module Objective & Scope** — one paragraph, no ambiguity
2. **Functional Requirements** — numbered list, testable statements ("The system SHALL…")
3. **Business Rules & Constraints** — edge cases, limits, legal/regulatory rules
4. **User Roles & Permissions** — who can read, write, approve, admin
5. **Data Models & Relationships** — key entities, fields, foreign keys, cardinality
6. **Integration Points** — named modules and the data exchanged
7. **Performance Requirements** — response times, batch sizes, concurrency
8. **Security Considerations** — data sensitivity, audit logging, access control

### Claude Code Prompt Pattern
```
Using the kickoff brief for [ModuleName], generate a full SPECIFICATION.md.
The module touches [list integration points].
Key business rules include: [paste any known constraints].
Flag any ambiguities you find and ask me to resolve them before finalizing.
```

### Review Checklist (human)
- Are all requirements testable (no vague words like "fast" or "easy")?
- Does every integration point name a real existing module?
- Are all user roles accounted for?

### Definition of Done
- [ ] All 8 sections present and non-empty
- [ ] No unresolved ambiguities (Claude flags, human resolves)
- [ ] Business owner has reviewed and signed off

---

## Step 2: FLOWCHART.md

### Purpose
Visually map every path through the module using **Mermaid diagrams**.

### Required Diagrams
1. **Happy Path Flow** — the standard, no-errors journey end-to-end
2. **Decision Tree** — every branch point with conditions labeled
3. **Exception Handling Paths** — what happens on errors, rejections, timeouts
4. **Integration Event Flow** — when/what this module sends to or receives from others
5. **Role-Based View** — what each user role sees and can trigger

### Rendering FLOWCHART.md

The `.md` file is the **canonical editable source** — Claude and your team edit this.
To produce a browser-ready version anyone can open without plugins, run:

```bash
python scripts/render_flowchart.py module-descriptor/<ModuleName>/FLOWCHART.md
```

This generates `FLOWCHART.html` in the same directory. Open it in any browser.
Regenerate it whenever the `.md` source changes — the HTML is always disposable.

> **Important — script bootstrap:** `render_flowchart.py` is bundled inside this skill at
> `scripts/render_flowchart.py`. The first time you render a flowchart in a project, copy it
> into the project root's `scripts/` directory:
>
> ```bash
> mkdir -p scripts
> cp <skill-dir>/scripts/render_flowchart.py scripts/render_flowchart.py
> ```
>
> Claude should do this automatically if the file is missing. After the first copy it will
> always be present in the project and does not need to be copied again.

> The script requires only Python 3 (no packages). The HTML loads Mermaid.js from CDN,
> so an internet connection is needed on first open (it caches after that).

### Mermaid Conventions
- Use `flowchart TD` for process flows
- Use `sequenceDiagram` for integration event flows
- Label every arrow with the triggering condition
- Use subgraphs to group related steps

### Claude Code Prompt Pattern — Generate
```
Based on SPECIFICATION.md for [ModuleName], generate FLOWCHART.md.
Use Mermaid diagrams. I need:
1. Happy path flowchart
2. Decision tree with all branch conditions
3. Exception handling paths
4. Integration sequence diagram with [list connected modules]
5. Role-based view for: [list roles]
Be exhaustive — more detail is better here.
```

### Claude Code Prompt Pattern — Render to HTML
```
Render module-descriptor/[ModuleName]/FLOWCHART.md to HTML.
If scripts/render_flowchart.py does not exist in the project root,
copy it from the skill's scripts/ directory first, then run it.
```

### Definition of Done
- [ ] All 5 diagram types present
- [ ] Every requirement from SPECIFICATION.md traceable to at least one flow step
- [ ] Exception paths exist for every decision node
- [ ] Diagrams render without errors in a Mermaid previewer

---

## Step 3: API_CONTRACT.md

### Purpose
Define the integration boundaries precisely so other modules can build against this one
independently. This is the **contract** — changes here require cross-team sign-off.

### Required Sections
1. **Inbound Events / APIs** — what this module accepts (endpoint, payload, auth)
2. **Outbound Events / APIs** — what this module emits (event name, payload, trigger condition)
3. **Shared Data Entities** — any DB tables or DTOs shared across module boundaries
4. **Error Codes & Responses** — standard error envelope, module-specific codes
5. **Versioning Policy** — how breaking changes will be communicated
6. **Consumer Modules** — which modules depend on this contract

### Format for Each API Entry
```markdown
### POST /api/[module]/[resource]
- **Purpose**: ...
- **Auth**: Bearer token, role: [role]
- **Request Body**: (JSON schema or typed fields)
- **Response**: (success + error shapes)
- **Side Effects**: (events emitted, state changes)
- **SLA**: max response time
```

### Claude Code Prompt Pattern
```
Based on SPECIFICATION.md and FLOWCHART.md for [ModuleName],
generate API_CONTRACT.md. This module integrates with: [list modules].
Define all inbound and outbound interfaces. Flag any integration points
that are underspecified and need cross-team clarification.
```

### Definition of Done
- [ ] Every integration point from SPECIFICATION.md has a contract entry
- [ ] All consumer modules listed and notified
- [ ] Error codes defined
- [ ] Reviewed by the tech lead of each consumer module

---

## Step 4: IMPLEMENTATION_PLAN.md

### Purpose
Break the specification into buildable phases with clear milestones, dependencies, and estimates.

### Required Sections
1. **Phase Breakdown** — 3–5 phases, each with a clear deliverable
2. **Milestones Table** — phase, deliverable, owner, estimated effort, dependency
3. **Technical Objectives per Phase** — what gets built, what decisions get made
4. **Component Dependency Graph** — what must be done before what
5. **Resource Allocation** — who works on what
6. **Risk Register** — top 5 risks with mitigation

### Phase Structure Template
```markdown
## Phase N: [Name]
- **Deliverable**: ...
- **Technical Objectives**: ...
- **Dependencies**: (phases or external items that must complete first)
- **Estimated Effort**: X dev-days
- **Owner**: ...
- **Risks**: ...
```

### Claude Code Prompt Pattern
```
Based on SPECIFICATION.md, FLOWCHART.md, and API_CONTRACT.md for [ModuleName],
generate IMPLEMENTATION_PLAN.md.
Our team has [N] developers. Preferred phase size is [1–2 week sprints / other].
Known constraints: [list any].
Flag dependencies on other modules' API contracts not yet finalized.
```

### Definition of Done
- [ ] 3–5 phases defined, each with a shippable deliverable
- [ ] All spec requirements mapped to a phase
- [ ] Risk register has at least 3 entries
- [ ] Tech lead and project owner have approved

---

## Step 5: TEST_PLAN.md

### Purpose
Document complete user journeys that validate the module end-to-end, tracing every path
in the flow chart against every requirement in the spec.

### Required Sections
1. **Test Coverage Matrix** — requirement ID → test ID mapping
2. **Happy Path Scenarios** — step-by-step, role-by-role
3. **Edge Case Scenarios** — boundary values, empty states, max load
4. **Error & Exception Scenarios** — every exception path from the flow chart
5. **Integration Scenarios** — cross-module flows
6. **Success Criteria** — explicit pass/fail definition per test

### Test Entry Format
```markdown
### TEST-[NNN]: [Scenario Name]
- **Covers**: REQ-[N], REQ-[N]
- **Role**: [user role performing this test]
- **Preconditions**: ...
- **Steps**: numbered list
- **Expected Result**: ...
- **Pass Criteria**: ...
- **Edge Variant**: (optional)
```

### Claude Code Prompt Pattern
```
Based on all artifacts for [ModuleName], generate TEST_PLAN.md.
Ensure every requirement in SPECIFICATION.md and every path in
FLOWCHART.md has at least one test. Flag any paths that are
difficult to test automatically vs. require manual QA.
```

### Definition of Done
- [ ] Every requirement has ≥1 test
- [ ] Every flow chart path has ≥1 test
- [ ] All exception paths covered
- [ ] QA lead has reviewed

---

## Step 6: TRACEABILITY_MATRIX.md (Living Document)

### Purpose
Track progress across phases and link completed work to requirements.
**Initialize after Step 4. Update after every PR merge, milestone, or sprint.**

### Structure
```markdown
## Module: [ModuleName]
**Last Updated**: [date]
**Overall Status**: [% complete]

## Timeline (Gantt)

```mermaid
gantt
  title [ModuleName] — Phase Progress
  dateFormat YYYY-MM-DD
  section Phase 1
    [Task name]  :done,    p1a, YYYY-MM-DD, YYYY-MM-DD
    [Task name]  :active,  p1b, YYYY-MM-DD, YYYY-MM-DD
  section Phase 2
    [Task name]  :         p2a, YYYY-MM-DD, YYYY-MM-DD
    [Task name]  :         p2b, YYYY-MM-DD, YYYY-MM-DD
```

> Task states: `done` = completed, `active` = in progress, `crit` = blocked/at risk, *(none)* = not started.
> Update this diagram every sprint alongside the tables below.

## Requirement Traceability
| REQ-ID | Description | Phase | Status | Test ID | Notes |
|--------|-------------|-------|--------|---------|-------|

## Milestone Tracker
| Milestone | Planned | Actual | Delta | Owner | Blockers |
|-----------|---------|--------|-------|-------|----------|

## Time Tracking
| Phase | Estimated (days) | Actual (days) | Variance |
|-------|-----------------|---------------|----------|

## Open Issues
| Issue | Impact | Owner | Target Resolution |
|-------|--------|-------|-------------------|
```

### Rendering GANTT.html

`TRACEABILITY_MATRIX.md` is the **canonical editable source** — Claude and your team edit this.
To produce a print-ready version anyone can open, share, or print without plugins, run:

```bash
python scripts/render_flowchart.py module-descriptor/<ModuleName>/TRACEABILITY_MATRIX.md --output module-descriptor/<ModuleName>/GANTT.html
```

This generates `GANTT.html` in the same directory. Open in any browser and use **File → Print**
to produce a PDF or paper copy. Regenerate it every sprint after updating the `.md` source —
the HTML is always disposable.

> The same `render_flowchart.py` script used for `FLOWCHART.html` handles Gantt diagrams.
> No new tooling required. If the script is missing, copy it from the skill's `scripts/` directory first.

### Claude Code Prompt Pattern (initial generation)
```
Generate an initial TRACEABILITY_MATRIX.md for [ModuleName] based on
IMPLEMENTATION_PLAN.md and SPECIFICATION.md.
Pre-populate REQ IDs from the spec and milestones from the plan.
Set all statuses to "Not Started".
Include a Mermaid Gantt chart under the "Timeline" section using the
phases and date estimates from IMPLEMENTATION_PLAN.md.
Mark all tasks with no state (not started).
Then render GANTT.html from it.
```

### Claude Code Prompt Pattern (update)
```
Update TRACEABILITY_MATRIX.md for [ModuleName].
Completed this sprint: [list items].
Blockers discovered: [list].
Adjust actuals vs estimates and flag any requirements at risk.
Also update the Mermaid Gantt — mark completed tasks as "done",
in-progress as "active", and blocked tasks as "crit".
Then regenerate GANTT.html.
```

### Claude Code Prompt Pattern — Render to HTML only
```
Render the Gantt chart from module-descriptor/[ModuleName]/TRACEABILITY_MATRIX.md
to GANTT.html in the same directory.
If scripts/render_flowchart.py does not exist in the project root,
copy it from the skill's scripts/ directory first, then run it.
```

### Definition of Done
*This document is never "done" — it is complete when the module ships and all requirements show "Verified" and all Gantt tasks show "done".*

> `GANTT.html` should be regenerated and attached to sprint review meetings as a progress snapshot.

---

## Full Workflow Summary

```
Step 0: Kickoff → confirm scope, create directory
Step 1: SPECIFICATION.md → what the module does
Step 2: FLOWCHART.md → how it flows
Step 3: API_CONTRACT.md → how it connects (share with other teams)
Step 4: IMPLEMENTATION_PLAN.md → how it will be built
         └─ Initialize TRACEABILITY_MATRIX.md here
Step 5: TEST_PLAN.md → how it will be verified
Step 6: TRACEABILITY_MATRIX.md → update continuously through development
         └─ Regenerate GANTT.html every sprint for print-ready timeline
```

> See `references/example-prompts.md` for a full set of Claude Code prompts per module type.
> See `references/business-module-checklist.md` for a printable per-module checklist.
> See `references/refactor-guide.md` for step-by-step guidance when refactoring an existing module.
