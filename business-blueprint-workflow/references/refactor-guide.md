# Refactoring Guide — Business Module Workflow

When working on an **existing module** rather than a greenfield one, this guide overrides or
supplements the default behavior of each step in `SKILL.md`. Read this file at the start of
any refactoring engagement and follow it alongside the main workflow.

---

## Key Differences: Refactor vs. Greenfield

| Concern | Greenfield | Refactor |
|---------|------------|----------|
| Scope source | Intent & requirements | Existing code + pain points |
| Spec starting point | Blank slate | Reverse-engineered current behavior |
| Flow chart | Ideal target state | Current state → gap → target state |
| API contract | Define freely | Preserve compatibility or plan migration |
| Implementation plan | Build phases | Migration path + strangler fig slices |
| Tests | Validate new behavior | Regression baseline + new behavior |
| Traceability | Track new requirements | Track what changed vs. what stayed |

---

## Step 0: Module Kickoff (Refactor Mode)

Before anything else, conduct a **module audit**. You cannot plan a refactor without
understanding what currently exists.

### Additional Kickoff Fields (refactor-specific)

| Field | Description |
|-------|-------------|
| Refactor Trigger | Why is this being refactored? (performance, tech debt, new requirements, compliance) |
| Current State Summary | Brief description of what the module does today |
| Known Pain Points | What specifically is broken, slow, or unmaintainable |
| What Must Not Change | Behavior, APIs, or data structures that are frozen (consumers depend on them) |
| Consumer Modules | Which other modules call this one — they are at risk |
| Live Data | Does the module have production data that needs migrating? |
| Rollback Strategy | Can we revert if the refactor causes issues in production? |

### Claude Code Prompt Pattern — Kickoff
```
I need to refactor an existing module called [ModuleName] in [system/platform name].

Current state: [brief description of what it does today]
Refactor trigger: [why we're doing this]
Known pain points: [list]
What must not change: [frozen interfaces, behaviors, data structures]
Consumer modules: [list of modules that depend on this one]
Live data: [yes/no — describe if yes]

Help me scope this refactor clearly. Identify what we're changing,
what we're preserving, and what risks we need to plan for before
we write the target specification.
```

### Definition of Done (Refactor Mode)
- [ ] Module audit complete — current behavior documented
- [ ] Refactor trigger clearly stated
- [ ] "What must not change" list signed off by consumer module owners
- [ ] Live data migration need assessed
- [ ] Rollback strategy identified
- [ ] All standard Step 0 items complete

---

## Step 1: SPECIFICATION.md (Refactor Mode)

A refactor spec has **two states**: current and target. Both must be documented.

### Additional Required Sections
Add these to the standard 8 sections:

9. **Current State Description** — what the module does today, as-is, no judgment
10. **Delta Summary** — a clear diff of what is changing, what is being removed, and what is new
11. **Frozen Interfaces** — explicit list of APIs, behaviors, and data structures that will not change
12. **Deprecation Plan** — anything being removed must have a sunset notice and timeline

### Claude Code Prompt Pattern
```
Generate a SPECIFICATION.md for the refactor of [ModuleName].

Current behavior: [paste current state summary or point to existing docs/code]
Target behavior: [describe what we want after the refactor]
What must not change: [list frozen interfaces]
Known constraints: [backward compatibility requirements, regulatory, etc.]

Include all standard sections plus:
- Current State Description
- Delta Summary (what changes, what stays, what is removed)
- Frozen Interfaces
- Deprecation Plan for anything being removed

Flag any conflicts between the target state and the frozen interface list.
```

### Definition of Done (Refactor Mode)
- [ ] All standard 8 sections present
- [ ] Current State Description written
- [ ] Delta Summary reviewed by tech lead
- [ ] Frozen Interfaces signed off by consumer module owners
- [ ] Deprecation Plan includes timeline and consumer notification

---

## Step 2: Flow_Chart_Process.md (Refactor Mode)

A refactor flow chart requires **three diagrams** not present in greenfield:

### Additional Required Diagrams
6. **Current State Flow** — the existing process as it works today (warts and all)
7. **Gap Analysis Diagram** — side-by-side or annotated diff showing what changes between current and target
8. **Migration Transition Flow** — how the system behaves *during* the refactor (if delivered incrementally)

The Migration Transition Flow is critical if the refactor ships in slices — it shows which
code path is active at each stage of the rollout.

### Claude Code Prompt Pattern
```
Generate Flow_Chart_Process.md for the refactor of [ModuleName].

In addition to the standard 5 diagrams, I need:
- Current State Flow: [describe existing flow or paste pseudocode/notes]
- Gap Analysis: annotate what changes between current and target
- Migration Transition Flow: we plan to deliver in [N] slices — show
  which path is live at each stage

Use Mermaid. Mark deprecated paths in the current state flow clearly.
```

---

## Step 3: API_Contract.md (Refactor Mode)

This is the highest-risk step in a refactor. Existing consumers depend on the current contract.

### Mandatory Additional Sections
7. **Current Contract (Preserved)** — document the existing API exactly as it is today
8. **Breaking Changes** — list every change that would break a consumer
9. **Migration Path for Consumers** — how and when consumers should migrate to the new contract
10. **Deprecation Timeline** — when old endpoints/events will be removed
11. **Versioning Strategy** — v1 → v2 approach, or parallel endpoints, or feature flags

### Rule: No Silent Breaking Changes
Any change to an existing endpoint signature, payload shape, event name, or error code
is a **breaking change** and requires:
- Explicit entry in the Breaking Changes section
- Sign-off from every affected consumer module's tech lead
- A migration timeline that gives consumers adequate runway

### Claude Code Prompt Pattern
```
Generate API_Contract.md for the refactor of [ModuleName].

Current contract (what exists today): [paste or describe existing APIs/events]
Planned changes: [what we're adding, modifying, or removing]
Consumer modules: [list — they must sign off on breaking changes]
Versioning approach: [parallel endpoints / v1→v2 / feature flags / other]

Flag every breaking change explicitly. For each one, suggest a
migration path that minimizes consumer disruption.
```

### Definition of Done (Refactor Mode)
- [ ] Current contract documented in full
- [ ] Every breaking change listed and justified
- [ ] All consumer module tech leads have signed off
- [ ] Migration path defined for each breaking change
- [ ] Deprecation timeline communicated to consumers

---

## Step 4: Module_Implementation_Plan.md (Refactor Mode)

Refactor plans must account for incremental delivery alongside the running system.
A "big bang" refactor that ships all at once is a high-risk antipattern for production systems.

### Additional Required Sections
7. **Migration Strategy** — strangler fig, feature flags, parallel run, or big bang (with justification)
8. **Data Migration Plan** — if live data is affected: scripts, validation, rollback
9. **Cutover Plan** — how and when traffic/usage switches from old to new
10. **Rollback Plan** — concrete steps to revert each phase if it fails in production

### Recommended Phase Pattern for Refactors
```
Phase 1: Audit & baseline — document current behavior, write regression tests
Phase 2: Parallel build — new implementation behind a feature flag
Phase 3: Incremental cutover — migrate consumers one by one
Phase 4: Old path deprecation — remove legacy code once all consumers migrated
Phase 5: Cleanup — remove feature flags, finalize documentation
```

### Claude Code Prompt Pattern
```
Generate Module_Implementation_Plan.md for the refactor of [ModuleName].

Migration strategy: [strangler fig / feature flags / parallel run / big bang]
Live data affected: [yes/no — describe migration need]
Consumer modules to migrate: [list]
Team size: [N] developers, sprint length: [duration]

Include a Rollback Plan for each phase. Flag any phase where
a rollback would be difficult or destructive.
```

---

## Step 5: Test_Routing_Map.md (Refactor Mode)

A refactor test plan has a layer greenfield doesn't: **regression coverage**.
You must prove the refactor doesn't break existing behavior before validating new behavior.

### Additional Required Sections
7. **Regression Baseline** — tests that capture current behavior as it exists today,
   written *before* refactoring begins. These must pass throughout the entire refactor.
8. **Parity Tests** — tests that verify the refactored module behaves identically to
   the old one for all frozen interfaces
9. **Migration Tests** — tests that validate data migration correctness
10. **Cutover Tests** — tests run at the moment of traffic switch to catch live issues

### Order of Test Creation
```
1. Write Regression Baseline FIRST — before touching any code
2. Write Parity Tests — verify frozen interfaces are intact
3. Write new behavior tests — validate target state requirements
4. Write Migration Tests — if data is being migrated
5. Write Cutover Tests — for the go-live moment
```

### Claude Code Prompt Pattern
```
Generate Test_Routing_Map.md for the refactor of [ModuleName].

Frozen interfaces (must have parity tests): [list]
Current behavior to preserve (regression baseline): [describe or paste]
New behavior to validate: [from SPECIFICATION.md delta summary]
Data migration: [yes/no]

Clearly separate regression tests from new behavior tests.
Flag any current behavior that is untestable without refactoring
the test infrastructure first.
```

---

## Step 6: Traceability_Matrix.md (Refactor Mode)

The traceability matrix for a refactor tracks three things the greenfield version doesn't:

### Additional Tracking Columns
- **Change Type** — `new` / `modified` / `preserved` / `deprecated` for each requirement
- **Consumer Impact** — which consumer modules are affected by this requirement's change
- **Migration Status** — for each consumer: `not started` / `in progress` / `migrated` / `verified`

### Additional Table: Regression Health
```markdown
## Regression Health
| Test ID | Covers | Status | Last Run | Notes |
|---------|--------|--------|----------|-------|
```
This table should be updated after every CI run during the refactor.

### Claude Code Prompt Pattern (initial)
```
Generate an initial Traceability_Matrix.md for the refactor of [ModuleName].

Source requirements from SPECIFICATION.md delta summary.
For each requirement, add a Change Type column: new / modified / preserved / deprecated.
Add a Consumer Impact column using this consumer list: [list].
Add a Migration Status column for each consumer.
Initialize a Regression Health table from Test_Routing_Map.md regression baseline tests.
```

---

## Common Refactor Pitfalls — Watch for These

| Pitfall | How This Workflow Prevents It |
|---------|-------------------------------|
| Scope creep ("while we're in here...") | Delta Summary in Step 1 locks scope |
| Silent breaking changes | Step 3 requires explicit sign-off for every breaking change |
| Regression in production | Step 5 mandates regression baseline before code changes |
| Consumer modules not notified | Step 3 lists all consumers; Steps 0 and 3 require their sign-off |
| No rollback if things go wrong | Step 4 requires rollback plan per phase |
| Data loss during migration | Step 4 data migration plan + Step 5 migration tests |
| "Big bang" refactor fails at go-live | Step 4 recommends incremental delivery patterns |
