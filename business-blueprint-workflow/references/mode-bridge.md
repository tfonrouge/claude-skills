<!-- Loaded via the mode→reference map in ../SKILL.md. This file is NORMATIVE: it carries
     the full step-by-step workflow and the per-step Definitions of Done that cathedral audits
     cross-reference. Do not work a blueprint in this mode from SKILL.md alone. -->

# BRIDGE MODE — Scoped Feature Workflow

Use this section when Mode Selection determined **BRIDGE MODE**. Do not run the full MODULE MODE workflow (Steps 0–7).

Bridge Mode produces 5 core artifacts (B0–B4), plus AUDIT.md and optionally ARCHIVED.md. All live in:
```
blueprints/<FeatureName>(BRIDGE)/
```

## Bridge Artifacts Overview

| Step | Artifact | Purpose |
|------|----------|---------|
| B0 | `BRIEF.md` | Scope, actors, affected modules, justification, lifecycle type |
| B1 | `ENTITY_DESCRIPTOR.md` | New entity/entities: states, rules, data model |
| B2 | `SERVICE_CONTRACTS.md` | API / service boundaries between touched modules |
| B3 | `VIEW_MAP.md` | New views + existing views to modify |
| B4 | `IMPLEMENTATION_ORDER.md` | Flat execution order with checkboxes |
| — | `AUDIT.md` | Drift detection between blueprint and actual implementation |
| — | `ARCHIVED.md` | Created on deprecation — explains what happened and why |

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
| **Lifecycle Type** | **Permanent** or **Temporary** |
| **Expiry Condition** | *(Temporary only)* The condition that makes this bridge obsolete |
| **Absorption Target** | *(Temporary only)* Which module will eventually own this functionality |
| **Planned Deprecation** | *(Temporary only)* Estimated sprint or date for deprecation |

### Claude Code Prompt Pattern
```
I need to implement [FeatureName] — a bridge feature between [ModuleA] and [ModuleB].
Context: [describe the business need in 2-3 sentences].
Existing entities involved: [list].
Architecture pattern: [describe your stack/patterns briefly].

Help me write BRIEF.md. Confirm the scope is tight and explicitly list what is out of scope.
Declare the lifecycle type (Permanent or Temporary) and, if Temporary, define the expiry condition.
```

### Definition of Done
- [ ] All fields filled, including the `| Mode | BRIDGE |` header row
- [ ] Registered in `blueprints/INDEX.md` — *Active Bridges* row
- [ ] Lifecycle type declared (Permanent or Temporary)
- [ ] If Temporary: expiry condition is specific and measurable, not vague
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
- A data model that fits our existing [ORM/schema pattern]
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
2. **Service / API Entries** — one entry per endpoint or service method
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

> **Intentionally simplified** vs MODULE MODE VIEW_MAP. Bridge scope is narrow — no role-based
> access matrix, no empty/error/loading states required. If the feature grows beyond 4–5 views,
> reconsider whether MODULE MODE is the right fit.

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
- **Key Elements**: list of main UI elements
- **Data Sources**: which service/API feeds this view
- **Modifications** (if MODIFIED): describe what changes vs. current behavior
```

### Claude Code Prompt Pattern
```
Based on ENTITY_DESCRIPTOR.md and SERVICE_CONTRACTS.md for [FeatureName],
generate VIEW_MAP.md.
Existing views in affected modules: [list them or say "none"].
Our frontend pattern: [e.g. "Vue 3 + Quasar, one .vue file per view"].
For modified views, describe only the delta — not a full rewrite.
Flag any view change that could break existing functionality for other user roles.
```

### Definition of Done
- [ ] Every state from the state machine has at least one view that displays it
- [ ] Every actor from the actor matrix has at least one entry point
- [ ] All modified views have explicit diff descriptions
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

### Layer 2 — Business Logic
- [ ] B4-03 · Implement [EntityName] service
- [ ] B4-04 · Unit tests for state machine transitions

### Layer 3 — Integration
- [ ] B4-05 · Implement contract: [FeatureName] → [ModuleA].[method]
- [ ] B4-06 · Integration tests for contracts

### Layer 4 — UI
- [ ] B4-07 · Create view: [NewViewName]
- [ ] B4-08 · Modify view: [ExistingViewName] (delta: [description])

### Layer 5 — Validation
- [ ] B4-09 · End-to-end test: [happy path]
- [ ] B4-10 · Smoke test in staging
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

## ARCHIVED.md — Deprecation Record

Create `ARCHIVED.md` when a Temporary bridge reaches its expiry condition and is deprecated.
Do **not** delete the bridge directory — `ARCHIVED.md` serves as the permanent record.

### Required Fields

```markdown
# Archived — [FeatureName](BRIDGE)
**Deprecated On**: [date]
**Deprecated By**: [person]
**Reason**: [the expiry condition from BRIEF.md that was met]
**Absorption Target**: [which module absorbed this functionality, if any]
**Final State**: [was the feature fully shipped, partially shipped, or cancelled?]

## Summary
[2-3 sentences describing what the bridge did and why it no longer exists as a standalone entity]

## Key Artifacts for Reference
- [Link to final ENTITY_DESCRIPTOR.md]
- [Link to final SERVICE_CONTRACTS.md]
- [PR or commit that removed/absorbed the bridge code]
```

### Definition of Done
- [ ] All `IMPLEMENTATION_ORDER.md` tasks marked complete or explicitly cancelled
- [ ] Absorption target documented (or "none — functionality removed")
- [ ] `blueprints/INDEX.md` updated: entry moved from Active Bridges → Deprecated
- [ ] Link to the absorbing module's blueprint added (if applicable)

---

## BRIDGE MODE — Full Workflow Summary

```
B0: BRIEF.md               → confirm scope, lifecycle type, affected modules, out-of-scope
                               └─ Create .blueprint-status (initial: PLANNING)
B1: ENTITY_DESCRIPTOR.md   → states, rules, data model, integration flow diagram
B2: SERVICE_CONTRACTS.md   → API/service boundaries (share with other teams before coding)
B3: VIEW_MAP.md            → new views + existing views to modify
B4: IMPLEMENTATION_ORDER.md → flat checklist ordered by dependency layer
                               └─ Update .blueprint-status → ACTIVE
AUDIT.md                   → create after initial implementation; revisit each sprint
ARCHIVED.md                → create only when deprecating a Temporary bridge
                               └─ Update .blueprint-status → CLOSED

Directory: blueprints/<FeatureName>(BRIDGE)/
```

### Deprecating a Temporary Bridge
When the expiry condition defined in `BRIEF.md` is met:
1. Mark all `IMPLEMENTATION_ORDER.md` tasks as complete or explicitly cancelled
2. Create `ARCHIVED.md` in the bridge directory with: reason for deprecation, date, and which module (if any) absorbed the functionality
3. Update `.blueprint-status` to `CLOSED`
4. Update `blueprints/INDEX.md`: move the entry from Active Bridges to Deprecated
5. Update `blueprints/MAP.md`: remove from Sprint Focus and Upcoming; add a note to the North Star if relevant
6. **Scan `blueprints/north-stars/` for references to this bridge.** Run `grep -rln "<BridgeName>(BRIDGE)" blueprints/north-stars/`. For each hit, check whether the line frames the bridge as a still-active plan step or as historical context. Lines containing ✅, `CLOSED`, `Shipped`, `cerrado`, `delivered`, `subsumido` on the same line are historical and may stay; every other mention is drift and must be updated or archived **in the same commit as the `.blueprint-status` flip**, so plan and reality move together.
7. Do **not** delete the directory — it serves as a record of what existed and why

> See `references/example-prompts.md` for additional Bridge Mode prompt examples per scenario type.
