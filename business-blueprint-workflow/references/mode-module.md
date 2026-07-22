<!-- Loaded via the mode→reference map in ../SKILL.md. This file is NORMATIVE: it carries
     the full step-by-step workflow and the per-step Definitions of Done that cathedral audits
     cross-reference. Do not work a blueprint in this mode from SKILL.md alone. -->

# MODULE MODE — Full Application Module Workflow

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
- [ ] `BRIEF.md` created and all kickoff fields populated, including the `| Mode | MODULE |` header row
- [ ] Registered in `blueprints/INDEX.md` — *Active Modules & Libraries* row with Mode column value
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

## Step 4: VIEW_MAP.md

### Purpose
Enumerate every UI surface the module introduces or modifies — before implementation planning,
so the frontend scope is explicit and nothing gets missed or over-built.

### Required Sections
1. **View Inventory by Domain Area** — group views into logical sections
2. **New Views** — each new page/screen/modal/component with purpose and actor
3. **Modified Views** — each existing view that changes, with an explicit diff description
4. **Role-Based Access Matrix** — rows = views, columns = roles, cells = read / write / hidden
5. **State-to-View Traceability** — every state from the FLOWCHART.md state machine must map to ≥1 view
6. **Navigation Changes** — new routes, menu entries, permission guards
7. **Shared Components** — new reusable components introduced by this module
8. **Empty / Error / Loading States** — explicit design decisions for each view

### Format for Each View Entry
```markdown
### [ViewName] — NEW | MODIFIED
- **Group**: (domain area this view belongs to)
- **Type**: Page / Modal / Component / Section
- **Route**: /path/to/view (if applicable)
- **Actors**: which roles access this (read / write)
- **Purpose**: one sentence
- **Key Elements**: table, form, status badge, action buttons…
- **Data Sources**: which API endpoints / services feed this view
- **States Displayed**: which entity states from the state machine appear here
- **Empty State**: what the user sees when there is no data
- **Error State**: what the user sees on load failure or validation error
- **Loading State**: skeleton, spinner, or other pattern
- **Modifications** (if MODIFIED): describe the delta only — not a full rewrite
```

### Definition of Done
- [ ] All views grouped by domain area
- [ ] Every state from FLOWCHART.md state machine has ≥1 view
- [ ] Every actor from SPECIFICATION.md has ≥1 entry point
- [ ] Role-based access matrix complete for all roles × all views
- [ ] Empty, error, and loading states defined for every view
- [ ] All modified views have explicit diff descriptions

---

## Step 5: IMPLEMENTATION_PLAN.md

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

### Definition of Done
- [ ] 3–5 phases defined, each with a shippable deliverable
- [ ] All spec requirements mapped to a phase
- [ ] All views from VIEW_MAP.md assigned to a phase
- [ ] Risk register has at least 3 entries
- [ ] Tech lead and project owner have approved

---

## Step 6: TEST_PLAN.md

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
```

### Definition of Done
- [ ] Every requirement has ≥1 test
- [ ] Every flow chart path has ≥1 test
- [ ] Every view in VIEW_MAP.md has ≥1 UI test
- [ ] All exception paths covered
- [ ] QA lead has reviewed

---

## Step 7: TRACEABILITY_MATRIX.md (Living Document)

### Purpose
Track progress across phases and link completed work to requirements.
**Initialize after Step 5. Update after every PR merge, milestone, or sprint.**

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
```

> Task states: `done` = completed, `active` = in progress, `crit` = blocked/at risk, *(none)* = not started.

## Requirement Traceability
| REQ-ID | Description | Phase | Status | Test ID | Notes |
|--------|-------------|-------|--------|---------|-------|

## Milestone Tracker
| Milestone | Planned | Actual | Delta | Owner | Blockers |
|-----------|---------|--------|-------|-------|----------|

## Open Issues
| Issue | Impact | Owner | Target Resolution |
|-------|--------|-------|-------------------|
```

### Definition of Done
*This document is never "done" — it is complete when the module ships and all requirements show "Verified" and all Gantt tasks show "done".*

---

## AUDIT.md — Blueprint vs. Implementation Drift Detection

Create `AUDIT.md` after initial implementation is underway. Revisit at the start of each sprint
or before onboarding a new developer.

### Structure

```markdown
# Audit — [ModuleName]
**Last Audit**: [date]
**Audited By**: [person or "Claude Code assisted"]
**Overall Status**: ✅ Aligned | ⚠️ Partial Drift | 🔴 Stale

## Drift Log
| Artifact | Section | Blueprint Says | Reality | Severity | Action |
|----------|---------|---------------|---------|----------|--------|

## Audit Checklist
- [ ] Every FR in SPECIFICATION.md has a corresponding implementation or explicit deferral
- [ ] API_CONTRACT.md (MODULE) or API_SURFACE.md (LIBRARY) matches current signatures
- [ ] VIEW_MAP.md matches current views in codebase (if applicable)
- [ ] TRACEABILITY_MATRIX.md status reflects actual completion
- [ ] BRIEF.md scope still matches what was built

## Notes
[Free-form observations — decisions made during implementation that diverge from the blueprint]
```

### Claude Code Prompt Pattern
```
Perform a blueprint audit for [ModuleName].
Read all artifacts in blueprints/[ModuleName](MODULE)/.
Then inspect the actual codebase: [describe where to look, e.g. "src/modules/[ModuleName]/"].
For each artifact, compare blueprint claims against reality and populate the Drift Log.
Flag every discrepancy with a severity (Low / Medium / High / Critical).
At the end, set the Overall Status and list recommended actions.
```

### Severity Guide
| Level | Meaning |
|-------|---------|
| Low | Minor wording or format difference, no functional impact |
| Medium | Missing feature or changed behavior, no blocker |
| High | Contract mismatch or missing requirement that affects other modules |
| Critical | Blueprint actively misleads — must update before next onboarding |

---

## MODULE MODE — Full Workflow Summary

```
blueprints/INDEX.md        → create on first module/bridge; refresh status from .blueprint-status files
blueprints/MAP.md          → create when ≥3 blueprints exist; update when focus or blockers change

Step 0: Kickoff → confirm scope, create directory, create .blueprint-status (initial: PLANNING)
Step 1: SPECIFICATION.md → what the module does
Step 2: FLOWCHART.md → how it flows
Step 3: API_CONTRACT.md → how it connects (share with other teams)
Step 4: VIEW_MAP.md → every screen and UI change
Step 5: IMPLEMENTATION_PLAN.md → how it will be built
         └─ Initialize TRACEABILITY_MATRIX.md here; update .blueprint-status → ACTIVE
Step 6: TEST_PLAN.md → how it will be verified
Step 7: TRACEABILITY_MATRIX.md → update continuously through development
AUDIT.md → create after initial implementation; revisit each sprint
.blueprint-status → update on every status change (PLANNING → ACTIVE → FOCUSED / PAUSED / BLOCKED → STABLE)
```

> See `references/example-prompts.md` for a full set of Claude Code prompts per module type.
> See `references/business-module-checklist.md` for a printable per-module checklist.
> See `references/refactor-guide.md` for step-by-step guidance when refactoring an existing module.

---

