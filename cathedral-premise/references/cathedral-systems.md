# Cathedral Audit — Systems Domain

Domain-specific audit checks for projects using `systems-blueprint-workflow`.
These checks supplement the universal principles in `cathedral-core.md`.

---

## Applicable Modes

| Mode | Directory Suffix | Artifacts |
|------|-----------------|-----------|
| SUBSYSTEM | `(SUBSYSTEM)` | BRIEF, DESIGN, ARCHITECTURE, C_API, COMPAT, IMPLEMENTATION_PLAN, TEST_PLAN, TRACEABILITY, AUDIT |
| FEATURE | `(FEATURE)` | BRIEF, DESIGN, C_API, IMPLEMENTATION_PLAN, TEST_PLAN, AUDIT |
| PATCH | `(PATCH)` | BRIEF, CHANGESET, TEST_PLAN, AUDIT |

---

## Established Patterns Reference

When checking Principle 4 (Established Patterns Over Novel Invention), these are
the domain-standard approaches for systems-level software. Flag any custom alternative
that lacks explicit justification:

| Area | Established Pattern |
|------|-------------------|
| Intermediate representations | SSA, sea-of-nodes, CPS |
| Garbage collection | Generational GC, mark-sweep, mark-compact |
| JIT compilation | Tiered JIT (interpreter → baseline → optimizing) |
| Memory management | Arena allocation, slab allocators, RAII |
| Concurrency | CSP, actor model, lock-free data structures |
| Dispatch | vtable, inline caching, polymorphic inline caches |
| Parsing | Recursive descent, Pratt parsing, PEG |
| Type checking | Hindley-Milner, bidirectional type checking |
| Optimization | Constant folding, dead code elimination, loop-invariant code motion |

---

## Principle Alignment Checks

### Universal Checks (applied via cathedral-core.md)

These apply to every blueprint regardless of domain:

| Check | What to look for |
|-------|-----------------|
| **Correctness over speed** | Any artifact that documents or endorses a shortcut, workaround, or "temporary" hack without a `[SPIKE]` tag and bounded scope. |
| **General over ad-hoc** | Design that hardcodes a single use case when the domain clearly has N cases. Struct layouts or APIs that paint themselves into a corner. |
| **Clean abstractions** | Implementation details bleeding across component boundaries, or coupling between subsystems that should be independent. |
| **Established patterns** | Novel/custom approaches where a well-known pattern exists (see table above). Check DESIGN.md "Alternatives Considered" for justification. |
| **Spike hygiene** | Any `[SPIKE]` work that shipped as-is without being rewritten under a full blueprint. Check git log for `[SPIKE]` tags. |

### Systems-Specific Checks

| Check | What to look for | Applies to |
|-------|-----------------|------------|
| **ABI discipline** | COMPAT.md fractures must be current. Re-run grep counts against the codebase — stale counts are a finding. | SUBSYSTEM |
| **Struct layout integrity** | DESIGN.md struct definitions must match actual `sizeof()` and field order in code. Any mismatch is High severity. | SUBSYSTEM, FEATURE |
| **C_API consistency** | Function signatures in C_API.md must match actual header declarations. New symbols must appear in the correct header. | SUBSYSTEM, FEATURE |
| **Hot-path awareness** | ARCHITECTURE.md must identify hot paths. Any design change touching a hot path without a performance test in TEST_PLAN.md is a warning. | SUBSYSTEM |
| **Blast radius accuracy** | BRIEF.md blast radius claims must match the actual set of files changed. Undocumented changes are a violation. | PATCH |
| **Changeset fidelity** | CHANGESET.md before/after descriptions must match the actual diff. Any undocumented change is a violation. | PATCH |
| **Blueprint completeness** | Missing artifacts for the mode, empty sections, stale dates, TODOs that block implementation. Cross-reference against the skill's Definition of Done for each step. | ALL |
| **Blueprint ↔ code drift** | If source code exists, compare design claims (struct layouts, function signatures, call graphs) against actual implementation. Every discrepancy is a finding. | ALL |
| **AUDIT.md currency** | Every blueprint must have an AUDIT.md. Check that it was updated within the current sprint. | ALL |
| **TRACEABILITY.md progress** | Gantt chart and Design → Code → Test table must reflect actual state. Stale entries are a warning. | SUBSYSTEM |

---

## Escalation Triggers

Flag these as **warnings** even if all other checks pass:

- A FEATURE blueprint touches >10 files across >3 directories → should be SUBSYSTEM
- A PATCH blueprint's blast radius grew beyond BRIEF.md scope → should escalate
- A SUBSYSTEM blueprint has no performance tests in TEST_PLAN.md
- Any blueprint has been in `ACTIVE` status for >4 weeks without TRACEABILITY.md updates

---

## Project Config Schema

The project's `CLAUDE.md` must contain these fields:

```markdown
## Premise: cathedral
Follow the cathedral premise.

### Project config
- Blueprint skill: systems-blueprint-workflow
- Blueprint root: blueprints/
- Build verification: [e.g., make && bin/linux/gcc/hbtest]
- Project language: [e.g., C/C++]
- Test formats: [e.g., .prg, .c, hbtest assertions]
```
