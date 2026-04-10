---
name: cathedral-premise
metadata:
  version: 1.1.0
description: >
  Governance premise for principled software development. Enforces correctness-first
  design, clean abstractions, established patterns, blueprint alignment, and spike
  hygiene. Supports systems projects (compilers, VMs, runtimes via
  systems-blueprint-workflow) and business projects (ERP, CRM, SaaS via
  business-blueprint-workflow). Governs blueprint skills — does not replace them.

  Trigger IMMEDIATELY when: CLAUDE.md mentions "cathedral" or "premise";
  user says "cathedral audit", "run cathedral audit", "premise check",
  "premisa catedral", "auditoría catedral"; reviewing blueprints or design
  artifacts; evaluating correctness-vs-speed trade-offs; discussing spikes,
  shortcuts, or "temporary" solutions; any mention of "correctness first",
  "clean abstractions", "established patterns", "blueprint alignment",
  "spike hygiene", "drift detection", "principle alignment",
  "incremental discipline", "decision ledger", "falsification condition",
  "approval calcification", "rejection amnesia".
---

# Cathedral Premise

> "If a simpler path and a right path exist, choose the right path."

This skill enforces a governance layer over blueprint-driven development. It ensures
that all design and implementation decisions satisfy four core principles: correctness
first, solve the general problem, clean abstractions, and established patterns over
novel invention.

---

## How to Use This Skill

### Step 1: Load the core principles

Always read `references/cathedral-core.md` first. It contains the four principles,
spike rules, blueprint alignment mandate, and the shared audit procedure. These
apply to every cathedral-governed project regardless of domain.

### Step 2: Determine the domain

Check the project's `CLAUDE.md` for the `Blueprint skill` config value:

| Config value | Domain | Reference to load |
|-------------|--------|-------------------|
| `systems-blueprint-workflow` | Systems (compilers, VMs, runtimes, GC, JIT) | `references/cathedral-systems.md` |
| `business-blueprint-workflow` | Business (ERP, CRM, WMS, SaaS, modules) | `references/cathedral-business.md` |

Load the appropriate domain reference. It contains the mode-specific audit checks,
established pattern references, and escalation triggers for that domain.

If the `CLAUDE.md` does not specify a blueprint skill, ask the user which domain
applies before proceeding.

### Step 3: Apply

Depending on the task:

| Task | What to do |
|------|-----------|
| **Design decision** | Evaluate against the four principles. Flag violations. Cite the specific principle. |
| **Blueprint review** | Check all artifacts against the domain-specific checks. Produce findings. |
| **Cathedral audit** | Follow the full audit procedure in `cathedral-core.md` using the domain-specific checks. Produce `CATHEDRAL_AUDIT_REPORT.md`. |
| **Spike proposal** | Verify it meets all spike rules (tagged, time-bounded, BRIEF.md entry, will not ship as-is). |
| **Trade-off discussion** | Present options through the lens of the four principles. The premise wins when it conflicts with shortcuts. |

---

## Cathedral Audit — Quick Reference

When the user says **"run cathedral audit"** or **"auditoría catedral"**:

1. Read `references/cathedral-core.md` (principles + shared procedure)
2. Read the project's `CLAUDE.md` to get the blueprint skill and config
3. Read the appropriate domain reference (`cathedral-systems.md` or `cathedral-business.md`)
4. Read the designated blueprint skill's `SKILL.md` to know the expected artifacts per mode
5. Scan all blueprint directories under the configured root
6. For each blueprint: load artifacts, apply universal checks + domain-specific checks
7. Produce `CATHEDRAL_AUDIT_REPORT.md` in the project root using the format from `cathedral-core.md`

### Severity Guide

| Level | Meaning |
|-------|---------|
| Low | Minor naming, comment, or formatting difference |
| Medium | Changed approach but same outcome — document the deviation |
| High | Interface mismatch or principle violation affecting other workstreams |
| Critical | Design actively misleads, or a core principle is violated with no justification |

---

## Design Decision Framework

When evaluating any design choice in a cathedral-governed project, apply this
checklist in order:

1. **Is it correct?** Does the design handle all defined cases without semantic errors?
   If not, stop — correctness is non-negotiable.
2. **Is it general?** Does it handle N cases, or just the one needed right now?
   If it handles only one, what's the cost of generalizing now vs. later?
3. **Are the abstractions clean?** Do implementation details leak across boundaries?
   Can you change the internals without touching consumers?
4. **Does it use established patterns?** Is there a well-known approach from the
   domain's literature? If the design departs from it, is there explicit justification?
5. **Is it blueprint-aligned?** Does a blueprint exist for this work? Does the
   implementation match what the blueprint specifies?
6. **Is it incrementally disciplined?** Does it cite a blueprint section? Is it
   labeled spike or construction? Does the Decision Ledger still support it —
   and have any APPROVED entries had their falsification conditions met?

If any answer is "no" and there's no documented justification, that's a finding.

---

## Project Onboarding

To adopt the cathedral premise in a new project:

1. Add the minimal config block to the project's `CLAUDE.md`
   (see the template in `references/cathedral-core.md`)
2. Ensure the appropriate blueprint skill is installed
   (`systems-blueprint-workflow` or `business-blueprint-workflow`)
3. Ensure this skill (`cathedral-premise`) is installed
4. All existing blueprints should be audited on first adoption to establish a baseline

No other setup is required. The governance is carried by this skill; the project's
`CLAUDE.md` carries only the per-project configuration.
