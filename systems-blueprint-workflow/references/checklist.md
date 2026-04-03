# Systems Blueprint Checklist

Print or copy for each workstream.

---

## Workstream: ___________________________
## Mode: SUBSYSTEM / FEATURE / PATCH
## Owner: ___________________________
## Started: ___________________________

---

## SUBSYSTEM MODE

### Step 0 — BRIEF.md
- [ ] Directory created: `blueprints/<Name>(SUBSYSTEM)/`
- [ ] `.blueprint-status` created (initial: PLANNING)
- [ ] Component identified
- [ ] Affected files listed and verified to exist
- [ ] Affected structs listed
- [ ] Compatibility stance specific (not "best effort")
- [ ] Performance stance stated
- [ ] Dependencies checked against INDEX.md

### Step 1 — DESIGN.md
- [ ] Current state documented with file:line references
- [ ] Every struct change shows before/after
- [ ] sizeof() impact analyzed for every struct change
- [ ] Every new function has signature, purpose, callers
- [ ] Memory layout impact assessed
- [ ] Performance impact on hot paths assessed
- [ ] At least one alternative considered and rejected with reasoning

### Step 2 — ARCHITECTURE.md
- [ ] Current call graph (Mermaid)
- [ ] Proposed call graph (Mermaid)
- [ ] Data flow diagram
- [ ] Initialization sequence
- [ ] Hot path identified and annotated
- [ ] All function names verified against actual code

### Step 3 — C_API.md
- [ ] Every new public symbol documented
- [ ] Every changed symbol documented with old→new
- [ ] Every removed symbol has deprecation plan
- [ ] ABI impact stated
- [ ] Header file locations listed
- [ ] Thread safety noted for each function

### Step 4 — COMPAT.md
- [ ] Every fracture has grep-verified call site count
- [ ] Risk percentages assigned
- [ ] Silent vs. loud classified for each fracture
- [ ] Discoverability classified (compile/link/test/runtime)
- [ ] Mitigation for every non-zero fracture
- [ ] Compatibility covenant has testable rules
- [ ] Total risk matches BRIEF.md target

### Step 5 — IMPLEMENTATION_PLAN.md
- [ ] 3-5 phases defined
- [ ] Each phase leaves build green
- [ ] Every file from DESIGN.md assigned to a phase
- [ ] Build verification command per phase
- [ ] Performance checkpoint for hot-path phases
- [ ] Rollback strategy per phase
- [ ] Risk register has 3+ entries
- [ ] TRACEABILITY.md initialized
- [ ] `.blueprint-status` updated → ACTIVE

### Step 6 — TEST_PLAN.md
- [ ] Regression test per struct change
- [ ] Behavior test per new function
- [ ] Compatibility test per COMPAT.md fracture
- [ ] Performance benchmark for hot-path changes
- [ ] Tests are executable (hbtest / .prg / .c)

### Step 7 — TRACEABILITY.md
- [ ] Gantt initialized with all phases
- [ ] Design→Code→Test table populated
- [ ] Updated after last merge/commit

### AUDIT.md
- [ ] Created after implementation starts
- [ ] Drift log populated
- [ ] Checklist completed
- [ ] Overall status set

---

## FEATURE MODE

### F0 — BRIEF.md
- [ ] Directory created: `blueprints/<Name>(FEATURE)/`
- [ ] `.blueprint-status` created (initial: PLANNING)
- [ ] Integration points identified and verified

### F1 — DESIGN.md
- [ ] Feature design documented
- [ ] Integration points with file:line references
- [ ] No unintended architecture changes (or escalate to SUBSYSTEM)

### F2 — C_API.md
- [ ] All new symbols documented
- [ ] Header files specified
- [ ] Thread safety noted

### F3 — IMPLEMENTATION_PLAN.md
- [ ] Build order defined (phases or flat checklist)
- [ ] Each step leaves build green

### F4 — TEST_PLAN.md
- [ ] New behavior tests written
- [ ] Integration point regression tests written

---

## PATCH MODE

### P0 — BRIEF.md
- [ ] Directory created: `blueprints/<Name>(PATCH)/`
- [ ] Root cause identified with file:line
- [ ] Blast radius assessed
- [ ] Rollback strategy defined

### P1 — CHANGESET.md
- [ ] Before/after for every change
- [ ] No unrelated changes included

### P2 — TEST_PLAN.md
- [ ] Fix-proof test (proves bug is fixed)
- [ ] Regression test (proves nothing else broke)
- [ ] Edge case test
