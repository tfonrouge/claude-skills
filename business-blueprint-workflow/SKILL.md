---
name: business-blueprint-workflow
metadata:
  version: 0.3.0
description: >
  Two-mode workflow for building business software with Claude Code. Use immediately when any of
  these appear — even without an explicit request for a structured workflow.

  MODULE MODE: Building a full module from scratch (ERP, CRM, WMS, SaaS, internal tooling).
  Triggers: "new module", "build a module", "start a module", module specs, flow charts, API
  contracts, implementation plans, traceability, or any multi-artifact module development process.

  BRIDGE MODE: Adding a feature/entity that connects existing modules without building a standalone
  module. Triggers: "functionality between X and Y", "bridge between modules", "new entity that
  integrates with", "extend existing module", "connect X to Y", "puente entre módulos",
  "funcionalidad entre entidades existentes", single entity + inter-module contracts + a few views.
  Produces scoped artifacts in a directory with the (BRIDGE) suffix.
  Module Mode artifacts use the (MODULE) suffix. Both live under blueprints/.
---

# Business Module Workflow

A repeatable, Claude Code–assisted methodology for building modules or inter-module features in a
large-scale business software system.

---

## Mode Selection — Do This First

Before starting any work, determine which mode applies and tell the user:

### MODULE MODE
Use when:
- Building a new module from scratch with its own data model, routes, and UI
- The module has no pre-existing architectural patterns to inherit
- Scope spans multiple weeks / multiple developers

→ Follow the full workflow below (Steps 0–6). Artifacts go in:
```
blueprints/<ModuleName>(MODULE)/
```

### BRIDGE MODE
Use when:
- Adding a feature, entity, or workflow that sits *between* two or more existing modules
- The codebase architecture is already established (models, services, views patterns are known)
- Scope is typically 1–2 developers, days to 1–2 weeks
- The task is primarily: new entity + inter-module contracts + a few new/modified views

→ Follow the **Bridge Mode workflow** (Section at bottom of this file). Artifacts go in:
```
blueprints/<FeatureName>(BRIDGE)/
```
The `(BRIDGE)` suffix makes the directory's purpose immediately identifiable when browsing the repo.

### When in doubt, ask:
```
Claude Code prompt:
"I need to implement [description]. Should this be a full module or a bridge feature?
Summarize: how many new entities, new views, new routes, and which existing modules are touched."
```
Use the answer to pick the mode. If it's ≥3 new entities or ≥3 new route groups → MODULE MODE.
Otherwise → BRIDGE MODE.

---

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
| 6b | `GANTT.html` | Visual Gantt chart only — generated from the Mermaid block in TRACEABILITY_MATRIX.md (regenerate every sprint) |

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
   blueprints/
   └── <ModuleName>(MODULE)/
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
- [ ] Directory created at `blueprints/<ModuleName>(MODULE)/`
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
python scripts/render_flowchart.py blueprints/<ModuleName>(MODULE)/FLOWCHART.md
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
Render blueprints/[ModuleName](MODULE)/FLOWCHART.md to HTML.
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
To produce a focused, chart-only HTML file showing just the Gantt timeline, run:

```bash
python scripts/render_flowchart.py blueprints/<ModuleName>(MODULE)/TRACEABILITY_MATRIX.md \
  --gantt-only \
  --output blueprints/<ModuleName>(MODULE)/GANTT.html
```

This generates `GANTT.html` containing **only the Gantt chart** — no tables, no prose, no issue tracker — so it stays compact and focused as a timeline snapshot. Open it in any browser and use **File → Print** to produce a PDF or paper copy. Regenerate it every sprint after updating the Mermaid Gantt block in the `.md` source — the HTML is always disposable.

> The `--gantt-only` flag extracts only `gantt` diagram blocks from the markdown and discards all other content. If no Gantt diagram is found, the HTML will display a "no diagrams found" notice.
> If the script is missing, copy it from the skill's `scripts/` directory first.

### Claude Code Prompt Pattern (initial generation)
```
Generate an initial TRACEABILITY_MATRIX.md for [ModuleName] based on
IMPLEMENTATION_PLAN.md and SPECIFICATION.md.
Pre-populate REQ IDs from the spec and milestones from the plan.
Set all statuses to "Not Started".
Include a Mermaid Gantt chart under the "Timeline" section using the
phases and date estimates from IMPLEMENTATION_PLAN.md.
Mark all tasks with no state (not started).
Then render GANTT.html using:
  python scripts/render_flowchart.py blueprints/[ModuleName](MODULE)/TRACEABILITY_MATRIX.md \
    --gantt-only --output blueprints/[ModuleName](MODULE)/GANTT.html
```

### Claude Code Prompt Pattern (update)
```
Update TRACEABILITY_MATRIX.md for [ModuleName].
Completed this sprint: [list items].
Blockers discovered: [list].
Adjust actuals vs estimates and flag any requirements at risk.
Also update the Mermaid Gantt — mark completed tasks as "done",
in-progress as "active", and blocked tasks as "crit".
Then regenerate GANTT.html using:
  python scripts/render_flowchart.py blueprints/[ModuleName](MODULE)/TRACEABILITY_MATRIX.md \
    --gantt-only --output blueprints/[ModuleName](MODULE)/GANTT.html
```

### Claude Code Prompt Pattern — Render to HTML only
```
Render the Gantt chart from blueprints/[ModuleName](MODULE)/TRACEABILITY_MATRIX.md
to GANTT.html in the same directory.
If scripts/render_flowchart.py does not exist in the project root,
copy it from the skill's scripts/ directory first, then run:
  python scripts/render_flowchart.py blueprints/[ModuleName](MODULE)/TRACEABILITY_MATRIX.md \
    --gantt-only --output blueprints/[ModuleName](MODULE)/GANTT.html
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

---

---

# BRIDGE MODE — Scoped Feature Workflow

Use this section when Mode Selection determined **BRIDGE MODE**. Do not run the full Steps 0–6 workflow.

Bridge Mode produces 5 focused artifacts — no more. All artifacts live in:
```
blueprints/<FeatureName>(BRIDGE)/
```

## Bridge Artifacts Overview

| Step | Artifact | Purpose |
|------|----------|---------|
| B0 | `BRIEF.md` | Scope, actors, affected modules, justification |
| B1 | `ENTITY_DESCRIPTOR.md` | New entity/entities: states, rules, data model |
| B2 | `SERVICE_CONTRACTS.md` | API / service boundaries between touched modules |
| B3 | `VIEW_MAP.md` | New views + existing views to modify |
| B4 | `IMPLEMENTATION_ORDER.md` | Flat execution order with checkboxes |

> No FLOWCHART.md (use a single integration diagram inside ENTITY_DESCRIPTOR.md instead).
> No TRACEABILITY_MATRIX.md — use IMPLEMENTATION_ORDER.md checkboxes for progress tracking.

---

## B0: BRIEF.md

### Purpose
Confirm scope and boundaries before any design work. Keep it short — this is a bridge, not a module.

### Required Fields

| Field | Description |
|-------|-------------|
| Feature Name | PascalCase, e.g. `PlanReparacion` |
| Business Problem | One sentence: why this feature exists |
| Affected Modules | List every existing module touched (read or write) |
| New Entities | List new DB entities / models |
| Out of Scope | Explicit list of what this feature does NOT do |
| Owner | Who is accountable |
| Target | Rough date or sprint |

### Claude Code Prompt Pattern
```
I need to implement [FeatureName] — a bridge feature between [ModuleA] and [ModuleB].
New entities involved: [list].
Help me write a BRIEF.md that clearly defines scope and explicitly marks what is out of scope.
Flag anything that sounds like scope creep.
```

### Definition of Done
- [ ] All fields filled
- [ ] Out of Scope section has ≥3 explicit exclusions
- [ ] Affected modules confirmed with their tech leads
- [ ] No ambiguities before proceeding to B1

---

## B1: ENTITY_DESCRIPTOR.md

### Purpose
Define the new entity (or entities) precisely: its states, transitions, business rules, and data model.
Also includes a single integration flow diagram showing how data moves between affected modules.

### Required Sections
1. **Entity Overview** — one paragraph, what it represents in the domain
2. **State Machine** — all states, transitions, and trigger conditions (Mermaid `stateDiagram-v2`)
3. **Business Rules** — numbered, testable statements ("The system SHALL…")
4. **Data Model** — fields, types, constraints, foreign keys to existing entities
5. **Integration Flow** — sequence diagram showing data flow across affected modules (Mermaid `sequenceDiagram`)
6. **Actor Matrix** — who can create / read / update / transition this entity

### Claude Code Prompt Pattern
```
Based on BRIEF.md for [FeatureName], generate ENTITY_DESCRIPTOR.md.
Existing modules involved: [list with their key entities/models].
Known business rules: [paste any].
I need:
- A state machine diagram for [EntityName]
- A sequence diagram showing the flow between [ModuleA] → [FeatureName] → [ModuleB]
- Data model that fits our existing [ORM/schema pattern]
Flag any rules that are ambiguous or conflict with existing module behavior.
```

### Definition of Done
- [ ] State machine covers all states — including error/rejection states
- [ ] Every transition has a named trigger condition
- [ ] Data model lists FK relationships to existing tables
- [ ] Integration sequence diagram includes all affected modules
- [ ] Business rules are numbered and testable

---

## B2: SERVICE_CONTRACTS.md

### Purpose
Define the exact API / service boundaries between this feature and every module it touches.
This is the document you share with other teams before writing a single line of integration code.

### Required Sections
1. **Contract Summary Table** — one row per integration point: direction, caller, method, purpose
2. **Service / API Entries** — one entry per endpoint or service method (see format below)
3. **Events Emitted** — any domain events this feature publishes
4. **Events Consumed** — any domain events this feature listens to
5. **Shared Entities / DTOs** — any data structures crossing module boundaries

### Format for Each Contract Entry
```markdown
### [METHOD] [ServiceName].[methodName] / POST /api/[resource]
- **Direction**: [FeatureName] → [ModuleName] | [ModuleName] → [FeatureName]
- **Trigger**: when does this get called?
- **Input**: (typed fields or JSON schema)
- **Output**: (success shape + error shape)
- **Side Effects**: state changes, events emitted
- **Owner**: which team owns this contract
```

### Claude Code Prompt Pattern
```
Based on BRIEF.md and ENTITY_DESCRIPTOR.md for [FeatureName],
generate SERVICE_CONTRACTS.md.
Integration points are:
- [FeatureName] reads from [ModuleA]: [what data]
- [FeatureName] writes to [ModuleB]: [what data]
- [FeatureName] triggers [action] in [ModuleC]
Use our existing service pattern: [describe pattern, e.g. "repository + service layer, REST endpoints"].
Flag any integration point that requires a breaking change to an existing module.
```

### Definition of Done
- [ ] Every integration point from BRIEF.md has a contract entry
- [ ] All affected module tech leads have reviewed
- [ ] No breaking changes undocumented
- [ ] Events section complete (even if empty — explicitly state "no events")

---

## B3: VIEW_MAP.md

### Purpose
Enumerate every UI change required: new views to create and existing views to modify.
This scopes the frontend work precisely so nothing is missed or over-built.

### Required Sections
1. **New Views** — each new view/screen/component with its purpose and actor
2. **Modified Views** — each existing view that changes, with a diff description
3. **Navigation Changes** — new routes, menu entries, or permission guards
4. **Shared Components** — any new reusable components introduced

### Format for Each View Entry
```markdown
### [ViewName] — NEW | MODIFIED
- **Type**: Page / Modal / Component / Section
- **Route**: /path/to/view (if applicable)
- **Actor**: which roles access this
- **Purpose**: one sentence
- **Key Elements**: list of main UI elements (table, form, status badge, action buttons…)
- **Data Sources**: which service/API feeds this view
- **Modifications** (if MODIFIED): describe what changes vs. current behavior
```

### Claude Code Prompt Pattern
```
Based on ENTITY_DESCRIPTOR.md and SERVICE_CONTRACTS.md for [FeatureName],
generate VIEW_MAP.md.
Existing views in affected modules: [list them].
Our frontend pattern: [e.g. "Vue 3 + Quasar, one .vue file per view, views in /src/views/[Module]/"].
For each modified view, describe only the delta — not a full rewrite.
Flag any view change that could break existing functionality for other user roles.
```

### Definition of Done
- [ ] Every state from the state machine has at least one view that displays it
- [ ] Every actor from the actor matrix has at least one entry point
- [ ] All modified views have explicit diff descriptions (not "update as needed")
- [ ] Frontend lead has reviewed

---

## B4: IMPLEMENTATION_ORDER.md

### Purpose
Define the exact execution sequence for building the feature — a flat, ordered checklist.
Not phases, not sprints — just the order that respects dependencies so nothing blocks.

### Structure
```markdown
# Implementation Order — [FeatureName](BRIDGE)
**Updated**: [date]
**Status**: [X/N tasks complete]

## Checklist

### Layer 1 — Data
- [ ] B4-01 · Create migration for [EntityName] table
- [ ] B4-02 · Add FK [field] to [ExistingTable]
- [ ] B4-03 · Create [EntityName] model / schema

### Layer 2 — Business Logic
- [ ] B4-04 · Implement [EntityName] service: create, transition states
- [ ] B4-05 · Implement [specific rule] logic
- [ ] B4-06 · Unit tests for state machine transitions

### Layer 3 — Integration
- [ ] B4-07 · Implement contract: [FeatureName] → [ModuleA].[method]
- [ ] B4-08 · Implement contract: [ModuleB] → [FeatureName].[method]
- [ ] B4-09 · Integration tests for contracts

### Layer 4 — UI
- [ ] B4-10 · Create view: [NewViewName]
- [ ] B4-11 · Modify view: [ExistingViewName] (delta: [description])
- [ ] B4-12 · Wire navigation / route guards

### Layer 5 — Validation
- [ ] B4-13 · End-to-end test: [happy path description]
- [ ] B4-14 · End-to-end test: [rejection/error path]
- [ ] B4-15 · Smoke test in staging with [affected module] team
```

### Claude Code Prompt Pattern (generate)
```
Based on all artifacts for [FeatureName](BRIDGE), generate IMPLEMENTATION_ORDER.md.
Our stack: [e.g. "Node.js + Mongoose + Vue 3"].
Order by dependency: data layer first, then business logic, then integration contracts,
then UI, then validation. Number each task B4-NN.
Flag any task that has an external dependency (another team, another module's deploy).
```

### Claude Code Prompt Pattern (update progress)
```
Update IMPLEMENTATION_ORDER.md for [FeatureName](BRIDGE).
Mark as complete: [list task IDs].
Blocked: [list task IDs + reason].
Add any new tasks discovered: [describe].
```

### Definition of Done
*This document is done when all checkboxes are checked and the feature is in production.*

---

## Bridge Mode — Full Workflow Summary

```
B0: BRIEF.md               → confirm scope, affected modules, out-of-scope
B1: ENTITY_DESCRIPTOR.md   → states, rules, data model, integration flow diagram
B2: SERVICE_CONTRACTS.md   → API/service boundaries (share with other teams before coding)
B3: VIEW_MAP.md            → new views + existing views to modify
B4: IMPLEMENTATION_ORDER.md → flat checklist ordered by dependency layer

Directory: blueprints/<FeatureName>(BRIDGE)/
```

### Bridge Mode Claude Code Kickoff Prompt
```
I need to implement [FeatureName] — a bridge feature between [ModuleA] and [ModuleB].
Context: [describe the business need in 2-3 sentences].
Existing entities involved: [list].
Architecture pattern: [describe your stack/patterns briefly].

Start with B0: help me write BRIEF.md, confirm the scope is tight,
and explicitly list what is out of scope. Then we'll proceed step by step.
```

> See `references/example-prompts.md` for additional Bridge Mode prompt examples per scenario type.
