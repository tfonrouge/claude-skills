# Claude Code Prompt Patterns — Business Blueprint Workflow

A ready-to-use prompt library for each step of the business blueprint workflow.
Copy, fill in the brackets, and paste into Claude Code. Artifact names and step order
follow the canonical MODULE / LIBRARY / BRIDGE flows in `SKILL.md`.

---

# MODULE MODE

## Step 0 — BRIEF.md (Module Kickoff)

```
I'm starting a new module called [ModuleName] for [system/platform name, e.g. "our SaaS billing platform", "internal WMS", "CRM"].

Context:
- Business Owner: [name]
- Business Justification: [why this is needed]
- Key Stakeholders: [list]
- Target Go-Live: [date/sprint]
- Integration Surface: [modules this touches]

Create the blueprint directory `blueprints/[ModuleName](MODULE)/` with BRIEF.md and a
`.blueprint-status` file, then help me validate that this scope is well-defined and flag
any gaps before we start writing the specification.
```

---

## Step 1 — SPECIFICATION.md

### Standard
```
Generate SPECIFICATION.md for the [ModuleName] module.

Kickoff context: [paste BRIEF.md summary]
Known business rules: [list any known constraints or rules]
Regulatory requirements: [e.g. customs law, ISO standards, none]

Include all 8 required sections. Use numbered, testable requirements
("The system SHALL..."). Flag any ambiguities and ask me to resolve
them before finalizing.
```

### For compliance-heavy modules (e.g. Import Management, Finance, Healthcare, Legal)
```
Generate SPECIFICATION.md for [ModuleName].
This module has regulatory exposure: [describe regulations].
Pay special attention to:
- Audit trail requirements
- Data retention policies
- Role-based access for sensitive operations
- Approval workflow requirements
Flag any requirement that may conflict with [specific regulation].
```

### For high-integration modules (e.g. Procurement, Inventory, Billing, Notifications)
```
Generate SPECIFICATION.md for [ModuleName].
This module is tightly coupled to: [list modules].
Emphasize integration points and shared data entities.
List every data field this module reads from or writes to other modules.
```

---

## Step 2 — FLOWCHART.md

### Standard
```
Based on SPECIFICATION.md for [ModuleName], generate FLOWCHART.md.

Use Mermaid diagrams:
- flowchart TD for process flows and decision trees
- sequenceDiagram for integration event flows

I need all 5 diagram types:
1. Happy path
2. Decision tree with all branch conditions labeled
3. Exception/error handling paths
4. Integration event flow with [list modules]
5. Role-based view for: [list roles]

Be exhaustive. Every branch in the spec should appear in a diagram.
```

### Iteration prompt (after first draft review)
```
The flow chart for [ModuleName] is missing:
- [describe missing path or scenario]
- [describe missing role or exception]

Also, the [DiagramName] diagram has an issue: [describe].
Please update FLOWCHART.md accordingly.
```

---

## Step 3 — API_CONTRACT.md

### Standard
```
Based on SPECIFICATION.md and FLOWCHART.md for [ModuleName],
generate API_CONTRACT.md.

This module integrates with:
- [Module A]: [what data is exchanged]
- [Module B]: [what data is exchanged]

For each integration, define:
- Inbound APIs this module exposes
- Outbound events this module emits
- Shared data entities

Use the standard endpoint format from the skill. Flag anything
underspecified that needs cross-team clarification.
```

### Consumer review prompt (for teams consuming this contract)
```
Review API_CONTRACT.md for [ModuleName].
Our module [ConsumerModuleName] will consume: [list endpoints/events].
Identify any:
- Missing fields we'll need
- Ambiguous response structures
- Missing error codes
- SLA concerns
```

---

## Step 4 — VIEW_MAP.md

### Standard
```
Based on SPECIFICATION.md, FLOWCHART.md, and API_CONTRACT.md for [ModuleName],
generate VIEW_MAP.md.

Enumerate every screen, view, and UI change. For each view give:
- The entity/state it displays
- The actors/roles that can reach it and their access level
- Whether it is a new view or a modification of an existing one

Ensure every entity state has ≥1 view and every role has ≥1 entry point.
Flag any orphan states (no view) or orphan views (no requirement).
```

---

## Step 5 — IMPLEMENTATION_PLAN.md

### Standard
```
Based on all artifacts for [ModuleName], generate IMPLEMENTATION_PLAN.md.

Team size: [N] developers
Sprint length: [1 week / 2 weeks]
Known constraints: [deadlines, dependencies on other teams, etc.]

Break into 3–5 phases. Each phase should be shippable.
Include a risk register with at least 5 risks.
Flag any dependency on API contracts not yet finalized by other teams.
```

### Re-planning prompt (when scope changes)
```
The implementation plan for [ModuleName] needs to be updated.
Changes since last plan:
- [New requirement added: ...]
- [Requirement removed: ...]
- [Technical constraint discovered: ...]

Re-estimate affected phases and update the risk register.
Show me a diff of what changed.
```

---

## Step 6 — TEST_PLAN.md

### Standard
```
Based on all artifacts for [ModuleName], generate TEST_PLAN.md.

Ensure:
- Every requirement (REQ-NNN) from SPECIFICATION.md has ≥1 test
- Every path in FLOWCHART.md has ≥1 test
- All exception paths are covered
- Integration scenarios cover flows with: [list modules]

Use the TEST-NNN ID format. Flag tests that require manual QA
vs. those that can be automated.
```

### Gap analysis prompt
```
Review TEST_PLAN.md for [ModuleName].
Cross-reference against SPECIFICATION.md.
Identify any requirements without test coverage and generate
the missing test cases.
```

---

## Step 7 — TRACEABILITY_MATRIX.md

### Initial generation
```
Generate an initial TRACEABILITY_MATRIX.md for [ModuleName].
Source data:
- Requirements from SPECIFICATION.md
- Milestones from IMPLEMENTATION_PLAN.md
- Tests from TEST_PLAN.md

Pre-populate all rows. Set status to "Not Started" for all items.
Add a timestamp of today's date.
```

### Sprint update
```
Update TRACEABILITY_MATRIX.md for [ModuleName].

Completed this sprint:
- [REQ-001, REQ-002 implemented in PR #42]
- [Milestone: Phase 1 database schema merged]

Blockers discovered:
- [API from InventoryModule not yet finalized — blocks REQ-015]

Actual time for Phase 1: [N] days (estimated was [M] days).
Recalculate variance and flag any requirements at risk of slipping.
```

---

# LIBRARY MODE

LIBRARY mode reuses `blueprints/<Name>(MODULE)/` but its prompts are library-specific:
the spec, flowchart, plan, and tests all carry platform/runtime and publication concerns
that MODULE mode does not. API_CONTRACT.md is replaced by API_SURFACE.md, and VIEW_MAP.md
is optional (only if the library ships UI components). Use these prompts, not the MODULE ones.

## Step 0 — BRIEF.md (Library Kickoff)
```
I'm starting a new reusable library called [LibraryName] to be published for other modules to consume.

Context:
- Owner: [name]
- Library scope: [what it provides]
- Platform / runtime targets: [e.g. KMP (JVM, iOS, JS), npm, Maven, pip]
- Consumer modules: [who will depend on it]
- Published artifact coordinates: [group:artifact, package name]

Create `blueprints/[LibraryName](MODULE)/` with BRIEF.md and `.blueprint-status`,
then flag any scope or platform-coverage gaps before we specify.
```

## Step 1 — SPECIFICATION.md
```
Using the kickoff brief for [LibraryName], generate a full SPECIFICATION.md.
Consumer modules are: [list].
Known business rules or constraints: [paste any].

Include a Platform/Target Constraints section (which APIs are available on which
targets/runtimes). Flag any requirement that would need to be target-specific
(e.g. JVM-only, browser-only). Flag any ambiguities before finalizing.
```

## Step 2 — FLOWCHART.md
```
Based on SPECIFICATION.md for [LibraryName], generate FLOWCHART.md.
Use Mermaid diagrams. I need:
1. Core processing flow (main algorithm or pipeline)
2. Lifecycle diagram for any stateful components
3. Data transformation flow (input → library → output)
4. Integration flow showing how consumer apps call the library
5. Exception / error handling paths
Be exhaustive on the error paths — a library must never silently swallow errors.
```

## Step 3 — API_SURFACE.md (replaces API_CONTRACT.md)
```
Based on SPECIFICATION.md and FLOWCHART.md for [LibraryName], generate API_SURFACE.md.

Document the full public API:
- Types, interfaces, functions, and utilities exposed to consumers
- Which symbols are public vs. internal
- Published artifact coordinates and versioning strategy
- Per-platform surface differences, if any ([list targets])

Anything not listed here is internal. Flag any symbol that leaks
implementation detail across the public boundary.
```

## Step 4 — VIEW_MAP.md *(Optional — only if the library exports UI building blocks)*

Skip this step and omit `VIEW_MAP.md` from the footer if the library has no UI components.
A library's VIEW_MAP is a catalog of **exported building blocks** consumers assemble — not the
screens/roles/entry-points map used in MODULE mode. Do not reuse the MODULE VIEW_MAP prompt.

```
Based on SPECIFICATION.md and API_SURFACE.md for [LibraryName], generate VIEW_MAP.md.
This library exports UI building blocks for consumer apps to assemble.

UI framework: [e.g. React, Angular, KVision] — adapt section names to it.
Include:
1. Building Block Inventory — grouped by domain area
2. UI Component / Column Definitions — each exported component: purpose, props/params, display type
3. Filter / Query Builders — each builder: entities filtered, input types
4. Form Field Builders — each builder: fields included, layout
5. Consumer Assembly Pattern — a code example of how a consuming app composes these blocks
6. Samples Module — reference implementations provided (if any)

Describe exported building blocks only — no application screens, roles, or entry points.
```

## Step 5 — IMPLEMENTATION_PLAN.md
```
Based on SPECIFICATION.md and FLOWCHART.md for [LibraryName], generate IMPLEMENTATION_PLAN.md.
Build units: [list, e.g. Gradle modules / npm workspaces / Python packages].
Platform/runtime targets: [list].
Publication registry: [e.g. Maven Central / npm / PyPI].
Use 3–5 phases, each with a publishable milestone.
Order: shared/common code first, then platform-specific targets, then publication.
Flag any phase that requires coordination with consumer module teams.
```

## Step 6 — TEST_PLAN.md
```
Based on SPECIFICATION.md, FLOWCHART.md, and API_SURFACE.md for [LibraryName],
generate TEST_PLAN.md.
Build units: [list].
Platform/runtime targets: [list — each target needs its own coverage column].
For each public symbol in API_SURFACE.md, include at least one unit test.
Include serialization/schema round-trip tests for all data types.
Use InMemoryRepository or test doubles for integration tests — no live dependencies.
```

## Step 7 — TRACEABILITY_MATRIX.md
```
Based on IMPLEMENTATION_PLAN.md for [LibraryName], generate TRACEABILITY_MATRIX.md.
Initialize the phase/task tracker from the plan and the requirement traceability
table from all FR-IDs in SPECIFICATION.md. Set every row to "Not Started".
```

## Library-specific: platform coverage check
```
Review API_SURFACE.md and IMPLEMENTATION_PLAN.md for [LibraryName].
For each target platform ([list]), confirm the surface is achievable and
list its constraints and test strategy. Flag any API that can't be supported
uniformly across targets.
```

---

# BRIDGE MODE

BRIDGE connects two existing modules. Directory suffix `(BRIDGE)`; artifacts are
BRIEF → ENTITY_DESCRIPTOR → SERVICE_CONTRACTS → VIEW_MAP → IMPLEMENTATION_ORDER → AUDIT,
plus ARCHIVED.md when a Temporary bridge closes.

## Step B0 — BRIEF.md
```
I'm creating a bridge called [BridgeName] between [ModuleA] and [ModuleB].

Context:
- What the bridge does: [1–2 sentences]
- Actors: [who triggers/consumes it]
- Affected modules: [ModuleA], [ModuleB]
- Lifecycle type: [Permanent | Temporary]
- If Temporary — expiry condition: [what event closes this bridge]

Create `blueprints/[BridgeName](BRIDGE)/` with BRIEF.md and `.blueprint-status`.
Confirm both connected modules, the lifecycle type, and (if Temporary) the expiry
condition are unambiguous before proceeding.
```

## Step B1 — ENTITY_DESCRIPTOR.md
```
Generate ENTITY_DESCRIPTOR.md for [BridgeName].
Define the new entity/entities the bridge introduces:
- States and the named transitions between them (include error/rejection states)
- Data model: fields, types, ownership
- Rules and invariants

Every state must be reachable and every transition must have a named trigger.
```

## Step B2 — SERVICE_CONTRACTS.md
```
Based on BRIEF.md and ENTITY_DESCRIPTOR.md, generate SERVICE_CONTRACTS.md for [BridgeName].
For every integration point between [ModuleA] and [ModuleB], define:
- Direction, trigger, input/output shapes, side effects
- Which module owns each contract

The bridge must talk to each module ONLY through documented contracts — never reach
into another module's database, internal services, or private DTOs. Flag any such coupling.
```

## Step B3 — VIEW_MAP.md
```
Generate VIEW_MAP.md for [BridgeName].
List new views and existing views (in [ModuleA]/[ModuleB]) that must change.
Keep it minimal — a bridge that needs more than 4–5 views probably should be a MODULE.
Flag if that threshold is exceeded.
```

## Step B4 — IMPLEMENTATION_ORDER.md
```
Generate IMPLEMENTATION_ORDER.md for [BridgeName].
Produce a single flat, checkbox execution order across all touched modules.
Order tasks by dependency; each item should be independently verifiable.
```

## Temporary bridge teardown
```
The Temporary bridge [BridgeName] has met its expiry condition: [describe].
Close it out:
- Create ARCHIVED.md describing what it did and why it's closed
- Set `.blueprint-status` to CLOSED and reflect deprecation in blueprints/INDEX.md
- Scan blueprints/north-stars/ for references to this bridge and reconcile any that
  still frame it as an active plan step (see SKILL.md Bridge teardown rules)
Do all of this in a single commit so plan and reality move together.
```

---

# Cross-cutting Prompts

### Consistency check — MODULE / LIBRARY (run anytime)
```
Review all artifacts for [ModuleOrLibraryName]:
- SPECIFICATION.md
- FLOWCHART.md
- API_CONTRACT.md (or API_SURFACE.md for libraries)
- VIEW_MAP.md (if present)
- IMPLEMENTATION_PLAN.md
- TEST_PLAN.md
- TRACEABILITY_MATRIX.md

Identify any inconsistencies between them:
- Requirements in the spec not covered by the flow chart
- Integration points in the spec not in the API contract/surface
- Entity states with no view in VIEW_MAP
- Phases in the plan not traceable to requirements
- Tests referencing non-existent requirements
```

### Consistency check — BRIDGE (run anytime)
```
Review all artifacts for the bridge [BridgeName]:
- BRIEF.md
- ENTITY_DESCRIPTOR.md
- SERVICE_CONTRACTS.md
- VIEW_MAP.md
- IMPLEMENTATION_ORDER.md

Identify any inconsistencies between them:
- Entity states/transitions in ENTITY_DESCRIPTOR with no matching SERVICE_CONTRACTS entry
- Integration points in BRIEF not covered by a contract in SERVICE_CONTRACTS
- Entity states with no view in VIEW_MAP
- SERVICE_CONTRACTS that reach into a connected module's internals rather than its documented API
- IMPLEMENTATION_ORDER items not traceable to a contract or view
```

### Onboarding a new developer
```
A new developer is joining the [BlueprintName] team.
Summarize the blueprint from all its artifacts in a 1-page onboarding brief covering:
- What it does (2 sentences)
- Key business rules to know
- Current implementation status
- What they'll be working on first
- Who to talk to for questions about each area
```
