---
name: business-blueprint-workflow
metadata:
  version: 0.11.0
description: >
  Artifact workflow for designing and tracking business software in Claude Code.
  Produces blueprints/ with Markdown specs, INDEX.md, and per-blueprint AUDIT.md.
  Use immediately — even without explicit request — when starting or planning software.

  MODULE MODE — new app module (ERP, CRM, WMS, SaaS, internal tooling).
  Triggers: "new module", "build a module", "start a module", "diseñar módulo",
  multi-entity scope, or requests for specs + flowcharts + API contracts together.

  LIBRARY MODE — reusable SDK or library (KMP, npm, Maven, pip, etc.).
  Triggers: "new library", "build a library", "SDK", "KMP library",
  "package for other apps", primary output is a published artifact (.jar/.tgz/.whl).

  BRIDGE MODE — feature/entity connecting two existing modules, permanent or temporary.
  Triggers: "functionality between X and Y", "bridge between modules", "extend module",
  "connect X to Y", "puente entre módulos", "funcionalidad entre entidades".

  Artifacts: (MODULE) suffix for modules, (LIBRARY) for libraries, (BRIDGE) for bridge
  features. Step-by-step mode workflows live in references/mode-*.md (see mode map).
  Each blueprint carries DIRECTIVE.md — the Owner's current objective authority — and
  three working gates anchor every implementer session to it.
---

# Business Module Workflow

A repeatable, Claude Code–assisted methodology for building modules, libraries, or inter-module
features in a large-scale business software system.

This file carries the **shared core**: mode selection, the mode→reference map, shared artifacts
(INDEX.md, `.blueprint-status`, MAP.md), and navigation conventions. The full step-by-step
workflow for each mode lives in its own reference file.

---

## Mode Selection

Before starting any work, determine which mode applies and tell the user:

### MODULE MODE
Use when:
- Building a new application module from scratch with its own data model, routes, and UI
- The module has no pre-existing architectural patterns to inherit
- Scope spans multiple weeks / multiple developers
- Users interact with the module directly (screens, forms, dashboards)

→ Artifacts go in `blueprints/<ModuleName>(MODULE)/`

### LIBRARY MODE
Use when:
- Building a reusable SDK, library, or package (KMP, npm, Maven, pip, etc.)
- Primary output is a published artifact (`.jar`, `.tgz`, `.whl`) consumed by other code
- No REST endpoints or application screens — instead: a public API surface (types, interfaces, functions, utilities) that other code imports
- May include optional UI building blocks (React hooks, Angular components, KVision building blocks, etc.) that consumer apps assemble
- Consumers are developers, not end users

→ Artifacts go in `blueprints/<LibraryName>(LIBRARY)/`

### BRIDGE MODE
Use when:
- Adding a feature, entity, or workflow that sits *between* two or more existing modules
- The codebase architecture is already established (models, services, views patterns are known)
- Scope is typically 1–2 developers, days to 1–2 weeks
- The task is primarily: new entity + inter-module contracts + a few new/modified views

→ Artifacts go in `blueprints/<FeatureName>(BRIDGE)/`

### Decision guide — evaluate in this order:

1. **Is the primary output a published artifact consumed by other code** (`.jar`, `.tgz`, `.whl`, npm package)?
   → **LIBRARY MODE** — stop here, regardless of entity count.

2. **Does the scope span ≥3 new entities OR ≥3 new route groups**, with no pre-existing architecture to inherit?
   → **MODULE MODE**

3. **Otherwise** (existing architecture, 1–2 new entities, days-to-weeks scope)
   → **BRIDGE MODE**

When in doubt, ask the user: how many new entities, new views/screens, new routes, and which
existing modules are touched? Is the primary output a published artifact consumed by other code,
or an application users interact with?

---

## Mode → Reference Map (mandatory loading)

| Mode | Directory suffix | Workflow reference |
|------|-----------------|--------------------|
| MODULE | `(MODULE)` | `references/mode-module.md` |
| LIBRARY | `(LIBRARY)` — legacy: `(MODULE)`, see below | `references/mode-library.md` |
| BRIDGE | `(BRIDGE)` | `references/mode-bridge.md` |

> **Before working a blueprint, resolve its mode and read its reference file. Do not proceed
> on SKILL.md alone.** The reference files are normative — they carry the step sequence and
> the per-step Definitions of Done that cathedral audits cross-reference.

### Resolving the mode of an existing blueprint

1. **Unambiguous suffix** — `(LIBRARY)` or `(BRIDGE)` → that mode. Done.
2. **`(MODULE)` is ambiguous during the compatibility period**: legacy LIBRARY blueprints may
   still use it (libraries predating the `(LIBRARY)` suffix). Resolve in order:
   BRIEF.md `Mode` header row → INDEX.md declaration (see below) → else assume MODULE and
   state the assumption.
3. **A suffix outside this catalog** (e.g. `(FEATURE)`) → stop and tell the user; never borrow
   another skill's workflow for it.

**INDEX declarations** exist via exactly two mechanisms: the **Mode column** of the blueprint's
row (Active Modules & Libraries), or the **section→mode map** — *Active Bridges* ⇒ BRIDGE.
All other INDEX sections (Deferred, Deprecated, organizational groupings) declare nothing.

**BRIEF `Mode` row**: every new BRIEF carries its mode's fixed literal (`| Mode | MODULE |`,
`| Mode | LIBRARY |`, `| Mode | BRIDGE |`) — required by each mode's Step 0/B0 DoD. In
pre-existing BRIEFs its absence is never a violation — add it opportunistically on next touch.
**Recognizer**: a BRIEF declares its mode via a `Mode` field in the header region (before the
first `##` heading) — either the table row `| Mode | <MODE> |` or an inline `Mode: <MODE>`
(bold markers allowed). The value must be the bare catalog literal; anything else is not a
BRIEF declaration.

---

## DIRECTIVE.md — Per-Blueprint Objective Authority

One per blueprint: the **current, authoritative Owner mandate**. It is *stable* — never a
"living" document — changed only by explicit Owner amendment. The directional dual of
`.blueprint-status`: status says where we are; DIRECTIVE says where we are going and what must
not be violated getting there. **Hard cap: the normative body (title through Amendment Rule)
fits one screen, ~30 lines.** Amendment History is cap-exempt; a history beyond ~5 entries is a
directive-churn signal for Owner re-examination.

### Template

The canonical template lives in **`references/directive-template.md`** — load it at Step 0/B0
creation and at legacy adoption. The rules of form (one-screen cap, constraint grammar, ledger
reference grammar) travel with it; only the lifecycle rules the working gates consume every
session remain below.

### Authority lifecycle

- **DRAFT confers nothing.** Owner approval is the act that confers authority; the header flip
  to `APPROVED` records it. The header is a durable process record — not proof of cognition or
  consent.
- **Revocation is an amendment**: it increments Revision, records who/when/why in the amendment
  store, and **flips the header to `REVOKED` in the same commit**. On disagreement between
  record and header, **the revocation record wins** (fail toward absence of authority); the
  mismatch is an audit synchronization finding. A REVOKED directive is never quoted as authority.
- **`Revision: N` ⇒ N−1 recorded amendments**, and the R-sequence is **unique and contiguous**:
  cathedral — ledger rows whose Decision cell begins with the literal `DIRECTIVE R<N>:`;
  non-cathedral — Amendment History lines R1 (adoption) through RN, exactly once each.

### Directive Completeness — criterion-side rollup

Every OC needs an **Owner-approved coverage set** and a **derived state**, in a
`## Directive Completeness` section of the mode's mapping carrier — never in DIRECTIVE.md
(status is mutable, DIRECTIVE is amendment-only, and a ticked box is self-attestation).
Carriers: MODULE/LIBRARY `TRACEABILITY_MATRIX.md` · BRIDGE `IMPLEMENTATION_ORDER.md` ·
SUBSYSTEM `TRACEABILITY.md` · FEATURE `IMPLEMENTATION_PLAN.md` · PATCH `CHANGESET.md`.

- **States** (closed): `UNMAPPED` (violation) · `NOT STARTED` · `IN PROGRESS` · `BLOCKED` ·
  `FAILED` · `MET`. `DEFERRED`/`NOT APPLICABLE` require a DIRECTIVE amendment.
- **Assurance** (independent axis): `REPLAYABLE` · `ATTESTED` · `MIXED`. `MET` is reachable on
  attested evidence; audits report `MET · ATTESTED` distinctly from `MET · REPLAYABLE`.
- **Derived, never declared.** `FAILED` (latest applicable verification disproves the
  criterion) and `BLOCKED`/`UNMAPPED` block completion claims.

Table schema, attestation fields, worked example and coverage-set integrity rules:
`references/directive-template.md` §Completeness rollup.

### Relationship to BRIEF.md

BRIEF is the **immutable origin record** — why the work was opened, discovery evidence,
stakeholders, initial conditions, the Mode row. At DIRECTIVE adoption, BRIEF gains a one-time
authority banner (see `references/legacy-migration.md`) and is frozen thereafter except
factual corrections explicitly labeled as such. Its Goal/scope/DoD language is historical, not
authority.

**Legacy blueprints** (any pre-directive artifact shape): all migration **procedures** —
adoption, baseline rules, banner text, and the migration map — live in
`references/legacy-migration.md`; read it before adopting or touching a legacy shape. The core
retains only runtime **compatibility** (mode reconciliation, the gates' legacy branches).

---

## Working Gates — every implementer session

Three act-gated rituals bind sessions to the directive. Their lines are emitted in chat —
they activate behavior in-session and are **never audit oracles** (all audit oracles are
file-based). Each line must be **derived from a read performed at that event, not from memory**.
Read-only sessions (ROAR review, cathedral audit) perform the gate *reads* silently as
evidence-gathering, emit no gate lines, and write nothing.

1. **Orientation gate** — at session start/resume on a blueprint, and at every session boundary:
   read DIRECTIVE + `.blueprint-execution`; emit:
   `Directive: <"Owner Directive sentence, quoted" | DRAFT pending Owner approval (no authority) | REVOKED — no current authority | none adopted (legacy — BRIEF §Goal is historical)> · Active: <OC-# · plan item | Step N (<artifact>) | idle> · Resuming: <plan item | excursion | Step N artifact>`
   For legacy blueprints with no dotfile, `Active`/`Resuming` fall back to approximate pipeline
   inference (`~Step N (inferred)`, confirmed in-session). Quoting forces loading.
2. **Focus-change gate** — when switching plan item, moving between pipeline steps, or entering
   a blocker; emit one of:
   `Serves OC-# via <plan item>`
   `Serves directive (design phase) via Step N (<artifact>)`
   `Serves pipeline Step N (pre-adoption legacy | approval pending | revoked)`
   `EXCURSION: <problem> — blocks <OC-# | directive (design phase) | pipeline (legacy | approval pending | revoked)>; return when <verifiable condition>`
   Update `.blueprint-execution` in the same move.
   **`approval pending` and `revoked` are holding states, not licenses.** Approval-pending
   permits only completing the adoption packet (or explicit Owner direction); after revocation,
   substantive work **stops and surfaces to the Owner** for re-approval, amendment, or a new
   directive — only Owner-directed remediation proceeds.
3. **Decision/completion gate** — when proposing a design choice or claiming done: read the
   premise checklist (where configured) and the ledger — every entry cited in Governing
   Constraints, a scan for rejections relevant to the proposal, **and a scan of APPROVED entries
   for fired falsification conditions** (the ledger rule is bidirectional; a fired falsifier is
   flagged due-for-review, never silently inherited). Emit:
   `Decision gate: serves <OC-# | pipeline Step N (pre-adoption legacy | approval pending | revoked)> · premise: checked P#/P# — <no conflict | violation + why> | none configured · ledger: honors <refs> | none relevant (checked) | none exists · reopened: <none | ref> · falsifiers: <none fired | fired: <ref> — flagged due-for-review>`
   Any submission for review — a completion claim, a design proposal, a protocol or tooling change —
   goes through the Owner/ROAR implementer preflight, which contains the Producer Coverage Census.
   Reference the census table you already produced; do not re-run it per gate.
   **Completion is measured against every OC-#, never against the latest resolved blocker** —
   a completion claim **reads the §Directive Completeness rollup and enumerates all criteria
   with state and assurance**, and is therefore **only possible under an APPROVED directive**:
   with no criteria in force (DRAFT, REVOKED, legacy), there is nothing to measure done against
   — surface to the Owner instead. Any OC in `FAILED`, `BLOCKED` or `UNMAPPED` **blocks the
   claim**; an OC resting on `ATTESTED` obligations is reported as `MET · ATTESTED`, never as
   reproduced.

---

## `.blueprint-execution` — Standing Execution State

A per-blueprint operational dotfile, sibling of `.blueprint-status`, identical in every mode.
Created at Step 0 (and at DIRECTIVE adoption for existing blueprints). It is operational state —
never part of any mode's content requirements, never in navigation footers, never merged into
DIRECTIVE or `.blueprint-status`. This is the sanctioned home for the "current work" narrative
that otherwise swells status files past their one-line contract.

```markdown
## Current Execution
- Active: <OC-02 · plan item P3 | Step 2 (FLOWCHART) | idle>   <!-- always present -->
- Excursion[1]: <problem> · opened <date> · return when: <verifiable check> · resume at: P3.2
```

- **Hard cap 7 lines**; excursion frames are one line each; **excursion depth hard cap 3**.
- Updated at every focus-change gate; excursion frames **persist on open** (session-boundary
  crossing is ex-ante undecidable) and clear on close.
- **Tripwire → semantic reassessment**: at depth ≥2, a session boundary with an open excursion,
  or expansion beyond the mapped plan item, answer in writing, one line each: does this change
  the Directive or its criteria? exceed approved scope? require an Owner trade-off? lack a
  bounded return condition? The answers determine escalation — **except depth >3, which always
  stops the work and surfaces to the Owner** (accumulated distance from the directive is itself
  the finding).
- **Version control: tracked, riding ordinary commits** — never gitignored, never forcing its
  own commits. Concurrent-implementer conflicts are resolved by **re-orientation, never textual
  merge**: re-derive the Active line from plan and reality, re-open only verified-open
  excursions as one parent-consistent stack; two branches claiming different active excursions
  is a disagreement for the Owner.

---

## Overview of Artifacts

### Root (`blueprints/`)
| File | Purpose |
|------|---------|
| `INDEX.md` | Global status board — all modules, libraries, bridges |
| `MAP.md` | System roadmap — dependency graph, focus, blockers, north star |

### MODULE MODE
| Step | Artifact | Purpose |
|------|----------|---------|
| — | `.blueprint-status` | Single-line status file; source of truth for INDEX.md |
| — | `.blueprint-execution` | Standing operational state: active OC/plan item, excursion stack |
| — | `DIRECTIVE.md` | Current Owner mandate: outcome criteria (OC-#), non-goals, constraints |
| — | `(LEDGER.md)` | Conditional — required when cathedral-governed: decisions, adoption + amendment provenance |
| 0 | `BRIEF.md` | Context, owner, justification |
| 1 | `SPECIFICATION.md` | What the module does |
| 2 | `FLOWCHART.md` | How it flows (Mermaid diagrams) |
| 3 | `API_CONTRACT.md` | How it connects to other modules |
| 4 | `VIEW_MAP.md` | Every screen, view, and UI change |
| 5 | `IMPLEMENTATION_PLAN.md` | How it will be built |
| 6 | `TEST_PLAN.md` | How it will be verified |
| 7 | `TRACEABILITY_MATRIX.md` | Living progress tracker (init after Step 5, update always) |
| — | `AUDIT.md` | Drift detection between blueprint and actual implementation |

### LIBRARY MODE
| Step | Artifact | Purpose |
|------|----------|---------|
| — | `.blueprint-status` | Single-line status file; source of truth for INDEX.md |
| — | `.blueprint-execution` | Standing operational state: active OC/plan item, excursion stack |
| — | `DIRECTIVE.md` | Current Owner mandate: outcome criteria (OC-#), non-goals, constraints |
| — | `(LEDGER.md)` | Conditional — required when cathedral-governed: decisions, adoption + amendment provenance |
| 0 | `BRIEF.md` | Context, owner, library scope, platform/runtime targets, consumer modules |
| 1 | `SPECIFICATION.md` | What the library provides — functional requirements, entities, constraints |
| 2 | `FLOWCHART.md` | Data flows, processing pipelines, async patterns, lifecycle diagrams |
| 3 | `API_SURFACE.md` | Public API: types, interfaces, functions, utilities, published artifact coordinates |
| 4 | `VIEW_MAP.md` | *(Optional)* UI building blocks — only if library provides UI components |
| 5 | `IMPLEMENTATION_PLAN.md` | Build phases — build units, platform/runtime targets, publication steps |
| 6 | `TEST_PLAN.md` | Unit/integration tests per build unit, platform/runtime coverage, serialization |
| 7 | `TRACEABILITY_MATRIX.md` | Living progress tracker |
| — | `AUDIT.md` | Drift detection between API_SURFACE.md and actual implementation |

### BRIDGE MODE
| Step | Artifact | Purpose |
|------|----------|---------|
| — | `.blueprint-status` | Single-line status file; source of truth for INDEX.md |
| — | `.blueprint-execution` | Standing operational state: active OC/plan item, excursion stack |
| — | `DIRECTIVE.md` | Current Owner mandate: outcome criteria (OC-#), non-goals, constraints |
| — | `(LEDGER.md)` | Conditional — required when cathedral-governed: decisions, adoption + amendment provenance |
| B0 | `BRIEF.md` | Scope, actors, affected modules, lifecycle type |
| B1 | `ENTITY_DESCRIPTOR.md` | New entity/entities: states, rules, data model |
| B2 | `SERVICE_CONTRACTS.md` | API / service boundaries between touched modules |
| B3 | `VIEW_MAP.md` | New views + existing views to modify |
| B4 | `IMPLEMENTATION_ORDER.md` | Flat execution order with checkboxes |
| — | `AUDIT.md` | Drift detection between blueprint and actual implementation |
| — | `ARCHIVED.md` | Created on deprecation |

> **TRACEABILITY_MATRIX.md is a living document.** Initialize it after Step 5 and update it
> continuously as work progresses. It is never "done."
>
> **AUDIT.md** is created after initial implementation and revisited at the start of each sprint
> or before onboarding a new developer.
>
> **blueprints/INDEX.md** is updated every time a blueprint is created, deprecated, or its status changes.
> Its status column is sourced from each blueprint's `.blueprint-status` file — never edited manually.
>
> **blueprints/MAP.md** is updated when development focus shifts, blockers change, or the dependency
> graph evolves. It is the roadmap view of the system; INDEX.md is the status board.
>
> **ARCHIVED.md** is created only for Temporary bridges, when their expiry condition is met.

---

## blueprints/INDEX.md — Global Blueprint Index

Create this file the first time any module, library, or bridge is started. Update it every time a
blueprint is created, changes status, or is deprecated. It is the single source of truth for the
state of the entire system design.

> **Status column is derived from `.blueprint-status` files** — see the section below.
> Never edit the Status column manually; instead update the corresponding `.blueprint-status` file
> and then refresh INDEX.md from it.

### Structure

```markdown
# Blueprints Index
**Updated**: [date]

## Active Modules & Libraries
| Name | Mode | Status | Phase | Owner | Notes |
|------|------|--------|-------|-------|-------|
| [ImportManagement(MODULE)](ImportManagement(MODULE)/BRIEF.md) | MODULE | 🟡 In Progress | Step 4 | @dev | Blocked on API contract review |
| [marketPlazeLib(LIBRARY)](marketPlazeLib(LIBRARY)/BRIEF.md) | LIBRARY | ✅ Complete | — | @team | |

## Active Bridges
| Bridge | Connects | Type | Status | Expiry Condition |
|--------|----------|------|--------|-----------------|
| [StockSync(BRIDGE)](StockSync(BRIDGE)/BRIEF.md) | Inventory ↔ WMS | Temporary | 🟡 Active | When WMS v2 ships |
| [PlanReparacion(BRIDGE)](PlanReparacion(BRIDGE)/BRIEF.md) | Orders ↔ Service | Permanent | 🟢 Stable | — |

## Deprecated
| Name | Reason | Deprecated On |
|------|--------|---------------|
| [OldImport(BRIDGE)](OldImport(BRIDGE)/ARCHIVED.md) | Absorbed by ImportManagement | 2024-Q1 |

## Dependency Map (optional)
```mermaid
graph LR
  Inventory --> StockSync
  StockSync --> WMS
  Orders --> PlanReparacion
```
```

The *Active Modules & Libraries* table's **Mode column** and the *Active Bridges* **section
membership** are this file's two mode declarations (see "Resolving the mode" above). Other
sections declare nothing about mode.

### Status Legend
| Icon | Status | Meaning |
|------|--------|---------|
| 🔵 | `PLANNING` | Blueprint in progress, no code yet |
| 🟡 | `ACTIVE` | Active development |
| 🎯 | `FOCUSED` | Current sprint's primary focus (1–2 max) |
| ⏸️ | `PAUSED` | Halted intentionally; reason in `.blueprint-status` |
| 🔴 | `BLOCKED` | Waiting on external dependency; reason in `.blueprint-status` |
| 🟢 | `STABLE` | In production, blueprint aligned |
| ⚠️ | `DRIFTED` | AUDIT.md flags misalignment |
| 🗄️ | `CLOSED` | Deprecated bridge — ARCHIVED.md exists |

---

## `.blueprint-status` — Per-Blueprint Status File

Every blueprint directory contains a single plain-text file called `.blueprint-status`.
It is the **authoritative source** for that blueprint's current status — INDEX.md reads from it,
never the other way around. Directory names are **never renamed** to encode status.

### Format

One line. Status keyword, optionally followed by `: <reason>`.

```
ACTIVE
```
```
PAUSED: waiting for UX sign-off on VIEW_MAP
```
```
BLOCKED: WMS v2 must deploy before this can continue
```

### Status Values

| Status | Icon | Meaning |
|--------|------|---------|
| `PLANNING` | 🔵 | Blueprint in progress, no code yet |
| `ACTIVE` | 🟡 | Under active development |
| `FOCUSED` | 🎯 | Current sprint's primary development focus (use sparingly — 1–2 at a time) |
| `PAUSED` | ⏸️ | Work halted intentionally; will resume. Always add `: <reason>` |
| `BLOCKED` | 🔴 | Waiting on an external dependency before work can continue. Always add `: <dependency>` |
| `STABLE` | 🟢 | In production; blueprint aligned with implementation |
| `DRIFTED` | ⚠️ | AUDIT.md flags misalignment between blueprint and implementation |
| `CLOSED` | 🗄️ | Temporary bridge that has been deprecated and archived |

> **`FOCUSED` is a sprint-level signal, not a permanent state.** At most 1–2 blueprints should
> carry `FOCUSED` at any time. When a sprint ends, update them back to `ACTIVE`.

**Why a file instead of a directory prefix?** Status changes are single-file edits (no git
renames, no shell-quoting pain), the reason field carries context a prefix can't, it's
grep-friendly (`find blueprints -name .blueprint-status | xargs grep BLOCKED`), and INDEX.md
derives from it — a single source of truth.

---

## blueprints/MAP.md — System Roadmap

`MAP.md` answers a different question than `INDEX.md`:

| File | Question |
|------|----------|
| `INDEX.md` | *What exists and what state is it in right now?* — **status board**: exhaustive, row-per-blueprint, always current |
| `MAP.md` | *Where is the system going? What depends on what? What's next?* — **roadmap**: curated, forward-looking, sequence and intent |

Create `MAP.md` when you have ≥3 blueprints and a multi-sprint horizon. Update it when focus
shifts, blockers change, or the dependency graph evolves. They reference each other; neither
duplicates the other's data.

### Structure

```markdown
# System Roadmap
**Updated**: [date]
**Current Focus**: [1–2 blueprint names that are FOCUSED right now]

## Dependency Graph

```mermaid
graph LR
  Inventory --> StockSync
  StockSync --> WMS
```

> Arrows mean "must complete or be stable before the downstream work begins."

## Sprint / Cycle Focus

| Blueprint | Status | Goal This Sprint |
|-----------|--------|-----------------|
| [OrderManagement(MODULE)](OrderManagement(MODULE)/BRIEF.md) | 🎯 FOCUSED | Complete API contract review |

## Upcoming (Next 2–3 Sprints)

| Blueprint | Mode | Unblocked By | Notes |
|-----------|------|-------------|-------|
| Billing(MODULE) | MODULE | OrderManagement stable | Q3 target |

## Blocked / Waiting

| Blueprint | Blocked On | Owner | Est. Resolution |
|-----------|-----------|-------|----------------|
| WMS(MODULE) | Vendor API contract | @vendor-team | 2024-Q3 |

## North Star

[1–2 sentences: where is the overall system heading in the next 2–4 quarters?]
```

---

## Artifact Navigation

Every `.md` artifact must include a navigation footer so readers can jump between documents without leaving their editor or browser.

### Rules

1. **Always at the bottom** — the nav block is the very last content in the file, after all sections.
2. **Current artifact is bold and not a link** — so the reader knows where they are.
3. **Only link artifacts that already exist** — if an artifact hasn't been generated yet, render it as plain text (no brackets, no link). This includes `../MAP.md`, and it is how `DIRECTIVE` and `LEDGER` behave on legacy blueprints that never adopt them: plain text, never a broken link.
4. **Always include the INDEX link; include the MAP link once it exists** — `INDEX.md` exists from the first blueprint, so `Index` is always a link. `MAP.md` is created only at ≥3 blueprints; until then render `Map` as plain text.
5. **Regenerate when a new artifact is created** — when generating artifact N, update the footer of all previously generated artifacts in the same blueprint directory to add the new link.

### MODULE MODE footer template

```markdown
---
[← Index](../INDEX.md) · [Map](../MAP.md) · [DIRECTIVE](DIRECTIVE.md) · **BRIEF** · [SPEC](SPECIFICATION.md) · [FLOWCHART](FLOWCHART.md) · [API](API_CONTRACT.md) · [VIEWS](VIEW_MAP.md) · [PLAN](IMPLEMENTATION_PLAN.md) · [TESTS](TEST_PLAN.md) · [MATRIX](TRACEABILITY_MATRIX.md) · [LEDGER](LEDGER.md) · [AUDIT](AUDIT.md)
```

Replace **BRIEF** with the name of the current file in bold. Files not yet created appear as plain text without brackets:

```markdown
---
[← Index](../INDEX.md) · Map · [DIRECTIVE](DIRECTIVE.md) · [BRIEF](BRIEF.md) · **SPEC** · FLOWCHART · API · VIEWS · PLAN · TESTS · MATRIX · Ledger · AUDIT
```

### LIBRARY MODE footer template

```markdown
---
[← Index](../INDEX.md) · [Map](../MAP.md) · [DIRECTIVE](DIRECTIVE.md) · **BRIEF** · [SPEC](SPECIFICATION.md) · [FLOWCHART](FLOWCHART.md) · [API SURFACE](API_SURFACE.md) · [VIEWS](VIEW_MAP.md) · [PLAN](IMPLEMENTATION_PLAN.md) · [TESTS](TEST_PLAN.md) · [MATRIX](TRACEABILITY_MATRIX.md) · [LEDGER](LEDGER.md) · [AUDIT](AUDIT.md)
```

`VIEW_MAP.md` is optional in LIBRARY MODE — if the library provides no UI components, omit it from the footer.

### BRIDGE MODE footer template

```markdown
---
[← Index](../INDEX.md) · [Map](../MAP.md) · [DIRECTIVE](DIRECTIVE.md) · **BRIEF** · [ENTITY](ENTITY_DESCRIPTOR.md) · [CONTRACTS](SERVICE_CONTRACTS.md) · [VIEWS](VIEW_MAP.md) · [ORDER](IMPLEMENTATION_ORDER.md) · [LEDGER](LEDGER.md) · [AUDIT](AUDIT.md)
```

---

## Prompt Patterns

Reusable Claude Code prompt patterns for INDEX/status/MAP updates, artifact generation, and
navigation footers live in `references/example-prompts.md`.
