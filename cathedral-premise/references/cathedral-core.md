# Cathedral Core — Universal Governance Principles

> "If a simpler path and a right path exist, choose the right path."

These principles govern all architectural and implementation decisions in any project
that adopts the cathedral premise. They are domain-agnostic — the domain-specific
audit checks live in separate reference files.

---

## The Four Principles

### 1. Correctness First

No optimization, deadline, or convenience justifies shipping code that is semantically
wrong or structurally unsound. If you discover a defect during implementation, stop
and fix it — even if the fix is expensive.

### 2. Solve the General Problem

Design for the class of problems, not the instance. If a mechanism will need to
handle N cases tomorrow, build for N today — don't hardcode the one case you need
right now. Ask: "what happens when a second X arrives?" If the answer is "rewrite,"
the abstraction is wrong.

### 3. Clean Abstractions Are Load-Bearing

A leaky abstraction is technical debt with compound interest. If the right abstraction
costs more time up front, that cost is an investment, not a loss. Implementation
details must not bleed across component boundaries.

### 4. Established Patterns Over Novel Invention

Use proven design patterns from the relevant domain before inventing project-specific
alternatives. Depart from the literature only with explicit justification documented
in the design artifact's "Alternatives Considered" section.

---

## Exploratory Spikes

Spikes are permitted when the correct design **cannot** be determined without a
working prototype.

### Rules

- The spike is tagged `[SPIKE]` in all commits.
- The spike is time-bounded (define the bound before starting).
- A `BRIEF.md` entry documents the spike's goal and findings.
- Spike code **never** ships as-is — it informs the real implementation,
  then is replaced or rewritten under the full blueprint workflow.

### Audit Implication

Any `[SPIKE]`-tagged work found in production code without a subsequent
blueprint-driven rewrite is a **violation**.

---

## Blueprint Alignment Mandate

All implementation must trace to a blueprint artifact produced by the project's
designated blueprint skill. No unspecified work ships.

### Before Implementation

A corresponding blueprint must exist and be approved (at minimum: `BRIEF.md` +
the mode's primary design artifact).

### During Implementation

If you discover the blueprint is wrong or incomplete, **stop and update the
blueprint first**, then continue. The blueprint is the specification, not a
suggestion.

### After Implementation

The blueprint's `AUDIT.md` must reflect the final state. Drift between blueprint
and code is a defect.

---

## Design Premise Deference

When the cathedral premise and a pragmatic shortcut conflict, the premise wins.
Document the conflict and resolution in the design artifact's "Alternatives
Considered" section.

When running audits, the premise's principle alignment checks take precedence
over the blueprint skill's Definitions of Done. A blueprint can satisfy every
DoD checkbox and still fail the audit if its design choices violate the governing
principles.

---

## CLAUDE.md Configuration Template

Each project that adopts the cathedral premise adds a minimal config block to its
`CLAUDE.md`. The cathedral-premise skill carries the governance; `CLAUDE.md` carries
only what varies per project.

```markdown
## Premise: cathedral
Follow the cathedral premise.

### Project config
- Blueprint skill: [systems-blueprint-workflow | business-blueprint-workflow]
- Blueprint root: blueprints/
- Build verification: [project-specific command]
- Project language: [language(s)]
- Test formats: [project-specific test types]
```

---

## Effort Configuration

| Context | Effort | How to set |
|---------|--------|------------|
| Default | high | settings.json: `{"effortLevel": "high"}` |
| Cathedral audit, architecture work | max | `/effort max` |
| Mechanical edits | low | `/effort low`, then restore |

---

## Cathedral Audit — Shared Procedure

When asked to **"run cathedral audit"**, Claude must:

1. **Read the cathedral premise** from this skill and the project's `CLAUDE.md` config.
2. **Read the designated blueprint skill's `SKILL.md`** to discover the expected
   artifact set, step sequence, and mode-specific requirements.
3. **Locate all blueprint directories** under the configured blueprint root.
4. **For each blueprint**, load every artifact that the skill defines for that
   blueprint's mode, then evaluate against the **domain-specific audit checks**
   (see the appropriate `cathedral-systems.md` or `cathedral-business.md` reference).

### Output Format

Produce a single **`CATHEDRAL_AUDIT_REPORT.md`** in the project root:

```markdown
# Cathedral Audit Report
> Generated: {date}
> Premise: cathedral
> Skill: {blueprint skill name}
> Blueprints scanned: {root}

## Summary
- Blueprints scanned: N
- Passing: N
- Violations: N
- Warnings: N

## Per-blueprint results

### {BlueprintName}({MODE})
**Status:** ✅ Aligned | ⚠️ Warnings | ❌ Violations
**Mode:** {mode}

#### Violations
- [{principle}] {description} — {artifact}:{section}

#### Warnings
- [{principle}] {description} — {artifact}:{section}

#### Notes
- {observations, positive or otherwise}
```

### Audit Rules

- Be strict. The cathedral premise exists precisely so that drift is caught early.
  Do not rationalize violations — flag them and let the developer decide.
- If no code exists yet for a blueprint, skip the drift check but still audit the
  artifacts for internal consistency and principle alignment.
- If a violation is ambiguous, flag it as a **warning** with an explanation rather
  than silently passing it.
