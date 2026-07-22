<!-- Loaded via the mode→reference map in ../SKILL.md. This file is NORMATIVE: it carries
     the full step-by-step workflow and the per-step Definitions of Done that cathedral audits
     cross-reference. Do not work a blueprint in this mode from SKILL.md alone. -->

# LIBRARY MODE — SDK / Package / Reusable Library Workflow

Use this section when Mode Selection determined **LIBRARY MODE**. This mode is optimized for
libraries, SDKs, and packages where the primary output is a published artifact consumed by other
code — not a user-facing application.

Key differences from MODULE MODE:
- **Step 3 uses `API_SURFACE.md`** instead of `API_CONTRACT.md` — documents the public API surface
  (types, interfaces, functions, utilities) that consumers import, rather than REST endpoints.
- **Step 4 (`VIEW_MAP.md`) is optional** — only include if the library provides UI building blocks
  that consumer apps assemble (e.g. React hooks, Angular directives, KVision components).
- **TEST_PLAN.md** includes required sections for per-target coverage and serialization tests.
  *(If using KMP: JVM/JS/Native target matrix and JSON round-trip tests.)*

---

## Library Step 0: BRIEF.md (Kickoff)

### Purpose
Establish the library's identity, scope, consumer dependencies, and target platforms before any design work begins. This is the contract between the library author and the teams that will depend on it.

### Actions
1. Create the directory:
   ```
   blueprints/
   └── <LibraryName>(LIBRARY)/
   ```
2. Confirm the following fields:

| Field | Description |
|-------|-------------|
| Library Name | PascalCase identifier, e.g. `MarketPlazeLib` |
| Business Owner | Who is accountable |
| Business Justification | Why this library is needed now |
| Platform/Runtime Targets | Which runtimes/targets this library supports. e.g. KMP: JVM/JS/Native · npm: Node 18+ · pip: Python 3.10+ |
| Published Artifacts | Package coordinates (e.g. Maven `com.example:myLib`, npm `@scope/lib`, PyPI `mylib`) |
| Consumer Modules | Apps / modules that will depend on this library |
| Integration Surface | Libraries this library depends on |

### Claude Code Prompt Pattern
```
I want to start a new library called [LibraryName] for [system/platform name].
Here's the context: [paste kickoff fields above].
Help me validate the scope: confirm what is and isn't part of the public API,
and list which consumer modules will depend on this library.
```

### Definition of Done
- [ ] Directory created at `blueprints/<LibraryName>(LIBRARY)/`
- [ ] `BRIEF.md` created and all fields populated, including the `| Mode | LIBRARY |` header row
- [ ] Registered in `blueprints/INDEX.md` — *Active Modules & Libraries* row with Mode column value
- [ ] Consumer modules identified and notified
- [ ] Published artifact coordinates defined (group:artifact)
- [ ] Platform/runtime targets agreed upon (e.g. KMP targets, Node version, Python version)
- [ ] No unresolved ambiguities before proceeding to Step 1

---

## Library Step 1: SPECIFICATION.md

### Purpose
Define *what* the library does — its functional requirements, data contracts, consumer roles, and platform constraints. This is the foundation all subsequent artifacts build on.

### Required Sections
1. **Library Objective & Scope** — one paragraph
2. **Functional Requirements** — numbered list, testable ("The library SHALL…")
3. **Business Rules & Constraints** — calculation rules, precision constraints, edge cases
4. **Consumer Roles** — which consumer types use which parts of the library
5. **Data Models & Relationships** — entities, value types, enums, and language-specific sum types *(e.g. Kotlin sealed classes, TypeScript discriminated unions, Python enums)*
6. **Integration Points** — dependencies (other libraries) and data exchanged
7. **Performance Requirements** — latency constraints, memory footprint
8. **Platform/Target Constraints** — which APIs are available on which targets/runtimes
   *(If KMP: commonMain vs jvmMain vs jsMain availability)*

### Claude Code Prompt Pattern
```
Using the kickoff brief for [LibraryName], generate a full SPECIFICATION.md.
Consumer modules are: [list].
Known business rules or constraints: [paste any].
Flag any requirement that would need to be target-specific (e.g. JVM-only, browser-only).
Flag any ambiguities before finalizing.
```

### Definition of Done
- [ ] All 8 sections present and non-empty
- [ ] Every requirement is testable — no vague language
- [ ] Platform/target constraints noted per API area
- [ ] No unresolved ambiguities (Claude flags, human resolves)
- [ ] Business owner has reviewed and signed off

---

## Library Step 2: FLOWCHART.md

### Purpose
Visually map how data flows through the library, how stateful components behave over time, and how consumer apps interact with the public API. Diagrams surface ambiguities in the spec before any code is written.

### Required Diagrams
1. **Core Processing Flow** — how the library's main algorithm or pipeline works
2. **Lifecycle Diagrams** — for any stateful components (schedulers, sync engines, etc.)
3. **Data Transformation Flow** — how input data flows through the library's functions
4. **Integration Flow** — how consuming apps call the library and what happens
5. **Exception / Error Handling Paths** — what the library returns on failure

### Claude Code Prompt Pattern
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

### Definition of Done
- [ ] All 5 diagram types present
- [ ] Every requirement from SPECIFICATION.md traceable to at least one flow step
- [ ] Error / Result paths explicit for every operation that can fail
- [ ] Diagrams render without errors in a Mermaid previewer

---

## Library Step 3: API_SURFACE.md

### Purpose
Document the complete public API surface of the library — what consumers import and depend on.
This is the **published contract** — breaking changes require a major version bump.

### Required Sections
1. **Published Artifacts** — package coordinates and version *(e.g. Maven `group:artifact`, npm `@scope/lib`, PyPI `mylib`)*, plus platform/runtime targets
2. **Core Entities & Models** — data classes, entities, their fields and constraints
3. **Service & Algorithm Interfaces** — public interfaces, base classes, top-level functions, and other callable API *(e.g. abstract classes in OOP, protocols in Swift/Python, type classes in Haskell)*
4. **Value Types** — enums, discriminated unions, sealed types, and other value-only types *(e.g. Kotlin inline/sealed classes, TypeScript union types, Python enums)*
5. **Utility / Extension API** — utility functions, extension functions, or mixins provided to consumers *(e.g. Kotlin extension functions, JS prototype extensions, Python helper modules)*
6. **UI Building Blocks** *(optional)* — column definitions, filter views, form builders (if applicable)
7. **Error / Result Types** — how the library communicates failure
8. **Versioning Policy** — semantic versioning rules for this library

### Format for Each API Entry

> **Adapt to your language/platform.** The template shows one possible structure; adapt field names and the Signature block to your language.
> For TypeScript: use `package` for `Module/Package`, omit `Platform/Targets`, use TS signatures.
> For Python: use `module path` for `Module/Package`, omit `Platform/Targets`, use Python type hints.

```markdown
### [ClassName] / [FunctionName]
- **Kind**: Entity | Interface | Base Type | Object | Function | Value Type | UI Component
- **Module/Package**: [build unit path, e.g. commonLib/commonMain | @scope/core | mylib.core]
- **Platform/Targets**: [runtimes this symbol is available on, e.g. JVM · JS · Node · Python 3.10+]
- **Purpose**: one sentence
- **Signature**:
  ```
  // language-appropriate signature, type definition, or data class fields
  ```
- **Constraints**: (nullability, ranges, validation rules)
- **Side Effects**: (events, state changes, if any)
- **Consumers**: (which apps/modules use this)
```

### Claude Code Prompt Pattern
```
Based on SPECIFICATION.md and FLOWCHART.md for [LibraryName],
generate API_SURFACE.md.
Consumer modules: [list].
Platform/runtime targets: [list, e.g. JVM+JS, Node 18, Python 3.10+].
Document all: entities, interfaces, base types, top-level functions,
value/utility types, utility/extension API, [and UI building blocks if applicable].
Flag any API that is target-specific (e.g. JVM-only, browser-only, Node-only).
Flag any breaking change vs. the previous version.
```

### Definition of Done
- [ ] All public types documented (no undocumented public symbols)
- [ ] Platform/runtime target availability noted for each entry
- [ ] Consumer modules listed
- [ ] Breaking changes from previous version flagged
- [ ] Reviewed by consumer module leads

---

## Library Step 4: VIEW_MAP.md *(Optional)*

### Purpose
Enumerate every UI building block the library exports so consumer teams know exactly what they can assemble without reading source code. Only needed if the library provides UI components.

Only include this artifact if the library provides **UI building blocks** that consumer apps assemble
(e.g., React hooks, Angular directives, KVision column definitions).

If the library has no UI components, skip this step and omit `VIEW_MAP.md` from the navigation footer.

### When included, required sections:
> **Adapt section names to your UI framework.** The examples below use KVision patterns.
> For React: replace "Column Definitions" with "Component Inventory", "Filter View Builders" with "Hook Catalog", etc.

1. **Building Block Inventory** — grouped by domain area (e.g., "Marketplace columns", "Product forms")
2. **UI Component / Column Definitions** — each exported component or `colDef*()` function: purpose, props/params, display type
3. **Filter / Query Builders** — each filter or query builder: entities filtered, input types
4. **Form Field Builders** — each form builder: fields included, layout
5. **Consumer Assembly Pattern** — how consuming apps use these building blocks (code example)
6. **Samples Module** — reference implementations provided (if applicable)

---

## Library Step 5: IMPLEMENTATION_PLAN.md

### Purpose
Break the library build into phases ordered by dependency — shared/common code first, then platform-specific targets, then publication. Makes the build sequence explicit and assignable.

### Required Sections
Same as MODULE MODE, with these library-specific additions:
- **Build Unit Breakdown** — which build units (packages/modules) get built in which phase *(e.g. Gradle modules, npm workspaces, Python packages)*
- **Target/Runtime Build Order** — the order in which platform targets or runtimes are built *(e.g. KMP: commonMain first, then jvmMain, then jsMain; npm: CJS then ESM; pip: sdist then wheel)*
- **Publication Steps** — when and how to publish to the relevant registry *(Maven Local/Central, npm registry, PyPI, etc.)*

### Phase Structure Template
```markdown
## Phase N: [Name]
- **Deliverable**: [publishable artifact or milestone]
- **Build Units Affected**: [e.g. commonLib + shopifyLib | @scope/core | mylib.core]
- **Target/Runtimes**: [e.g. commonMain/jvmMain | Node 18 CJS+ESM | Python 3.10+]
- **Technical Objectives**: ...
- **Dependencies**: (phases or external libraries)
- **Estimated Effort**: X dev-days
```

### Claude Code Prompt Pattern
```
Based on SPECIFICATION.md and FLOWCHART.md for [LibraryName],
generate IMPLEMENTATION_PLAN.md.
Build units: [list, e.g. Gradle modules / npm workspaces / Python packages].
Platform/runtime targets: [list].
Publication registry: [e.g. Maven Central / npm / PyPI].
Use 3–5 phases, each with a publishable milestone.
Order: shared/common code first, then platform-specific targets, then publication.
Flag any phase that requires coordination with consumer module teams.
```

---

## Library Step 6: TEST_PLAN.md

### Purpose
Document the test strategy that validates every public symbol across every supported platform/runtime. A library ships to many consumers — gaps in test coverage become their production bugs.

### Required Sections
1. **Test Coverage Matrix** — FR-ID → Test ID mapping
2. **Unit Tests by Build Unit** — per package/module, grouped by tested class/function *(e.g. per Gradle module, per npm workspace, per Python package)*
3. **Platform/Runtime Coverage** — which tests run on which targets/runtimes

```markdown
### Platform/Runtime Coverage
| Test Class | [Target A] | [Target B] | [Target C] |
|-----------|------------|------------|------------|
| ExampleTest | ✅ | ⬜ | ⬜ |
```
*(e.g. KMP: JVM / JS / Native · npm: Node / Browser · pip: Python 3.10 / 3.11)*

4. **Serialization / Schema Tests** — round-trip tests for all serializable entities or data contracts
5. **Integration Tests** — end-to-end scenarios using test doubles or in-memory implementations
6. **Known Gaps** — untested areas and justification (e.g., visual components, live API calls)

### Claude Code Prompt Pattern
```
Based on SPECIFICATION.md, FLOWCHART.md, and API_SURFACE.md for [LibraryName],
generate TEST_PLAN.md.
Build units: [list].
Platform/runtime targets: [list — each target needs its own coverage column].
For each public symbol in API_SURFACE.md, include at least one unit test.
Include serialization/schema round-trip tests for all data types.
Use InMemoryRepository or test doubles for integration tests — no live dependencies.
```

### Test Entry Format
Same as MODULE MODE (`TEST-[NNN]` format).

---

## Library TRACEABILITY_MATRIX.md and AUDIT.md

Same structure as MODULE MODE.

### Claude Code Prompt Pattern (initialize TRACEABILITY_MATRIX.md)
```
Based on IMPLEMENTATION_PLAN.md for [LibraryName], generate TRACEABILITY_MATRIX.md.
Initialize the Gantt with all phases and tasks from the plan.
Initialize the Requirement Traceability table with all FR-IDs from SPECIFICATION.md.
Set all statuses to "Not Started". Leave Test ID column blank — fill as tests are written.
```

For `AUDIT.md`, the checklist adapts:

```markdown
## Audit Checklist
- [ ] Every FR in SPECIFICATION.md has a corresponding implementation or explicit deferral
- [ ] API_SURFACE.md matches current public API signatures
- [ ] VIEW_MAP.md (if present) matches current UI building blocks
- [ ] TRACEABILITY_MATRIX.md status reflects actual completion
- [ ] BRIEF.md scope still matches what was built
```

---

## LIBRARY MODE — Full Workflow Summary

```
blueprints/INDEX.md        → create on first use; refresh status from .blueprint-status files
blueprints/MAP.md          → create when ≥3 blueprints exist; update when focus or blockers change

Step 0: BRIEF.md → library name, platform/runtime targets, consumer modules
         └─ Create .blueprint-status (initial: PLANNING)
Step 1: SPECIFICATION.md → functional requirements, entities, business rules
Step 2: FLOWCHART.md → data flows, lifecycle diagrams, processing pipelines
Step 3: API_SURFACE.md → public interfaces, types, functions, published artifact coordinates
Step 4: VIEW_MAP.md → [OPTIONAL] UI building blocks (components, hooks, form builders)
Step 5: IMPLEMENTATION_PLAN.md → build unit phases, target/runtime order, publication steps
         └─ Initialize TRACEABILITY_MATRIX.md here; update .blueprint-status → ACTIVE
Step 6: TEST_PLAN.md → unit tests per build unit, platform/runtime coverage, serialization
Step 7: TRACEABILITY_MATRIX.md → update continuously through development
AUDIT.md → create after initial implementation; revisit each sprint
.blueprint-status → update on every status change

Directory: blueprints/<LibraryName>(LIBRARY)/
Footer: [← Index] · [Map] · BRIEF · SPEC · FLOWCHART · API SURFACE · [VIEWS] · PLAN · TESTS · MATRIX · AUDIT
```

---

