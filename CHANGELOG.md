# Changelog

This repo ships four independently versioned products. Each has its own section below.

---

# business-blueprint-workflow (skill)

Versioned via the `metadata.version` field in `business-blueprint-workflow/SKILL.md`.

## 0.8.2

- **Reference files brought back in line with the canonical skill** (they had drifted to an older
  artifact vocabulary and step structure while the skill lived only as an installed copy):
  - `references/business-module-checklist.md`, `references/example-prompts.md`, and
    `references/refactor-guide.md` now use the canonical `blueprints/` layout and names
    (`SPECIFICATION.md`, `FLOWCHART.md`, `API_CONTRACT.md`, `VIEW_MAP.md`, `IMPLEMENTATION_PLAN.md`,
    `TEST_PLAN.md`, `TRACEABILITY_MATRIX.md`, `AUDIT.md`) — replacing the legacy
    `module-descriptor/`, `Flow_Chart_Process.md`, `API_Contract.md`, `Module_Implementation_Plan.md`,
    `Test_Routing_Map.md`, `Traceability_Matrix.md`.
  - The missing **VIEW_MAP** step was inserted and steps renumbered to the canonical 0–7 order in
    the checklist, example prompts, and refactor guide.
  - `example-prompts.md` gained the **LIBRARY MODE** and **BRIDGE MODE** prompt sections the main
    skill already advertised (they were previously absent). The LIBRARY prompts are
    library-*specific* (target/runtime constraints, processing/lifecycle flows, build-unit &
    publication ordering, per-runtime coverage, serialization tests) — mirroring the canonical
    Library steps in `SKILL.md`, not just reusing the MODULE prompts. The cross-cutting
    **consistency check** is now split into MODULE/LIBRARY and BRIDGE variants so each lists only
    the artifacts its mode actually produces.
- **Footer nav rule clarified** so it no longer self-contradicts: `Map` is rendered as plain text
  until `blueprints/MAP.md` exists (it is created only at ≥3 blueprints), then linked. `Index` is
  always a link.
- No workflow-behavior change beyond the doc corrections. These fixes came from a ROAR review of the
  restored skill; see the review triage in the working history.

## 0.8.1

- Bridge teardown (Bridge Mode) gains a **north-stars drift scan**: on closing a bridge, run
  `grep -rln "<BridgeName>(BRIDGE)" blueprints/north-stars/` and reconcile every non-historical
  mention in the *same commit* as the `.blueprint-status` flip, so plan and reality move together.
- **Restored to the repo** at this version. Between `2c7c792` (which removed the skill — see
  [`DECISIONS.md`](./DECISIONS.md) D6) and this restore, the skill lived only as an installed copy
  under `~/.claude/skills/`, where it advanced from the last git-tracked `0.8.0` to `0.8.1`.

## 0.8.0 and earlier

Predates this changelog. History is in git: `business-module-workflow` → renamed to
`business-blueprint-workflow` (`09d1568`), Bridge Mode added, artifact names standardized. The
`render_flowchart.py` Gantt/Mermaid tool from the `business-module-workflow` era was dropped during
that lineage and is **not** restored; recover from history (`git show 00ab707:...`) if needed.

---

# systems-blueprint-workflow (skill)

Versioned via the `metadata.version` field in `systems-blueprint-workflow/SKILL.md`.

## 0.2.2

- **Footer nav rule clarified** (Artifact Navigation): `../MAP.md` is created only at 3+ blueprints,
  so `Map` is rendered as plain text until it exists, then linked; `../INDEX.md` is always a link.
  Removes the ambiguity between "only link artifacts that exist" and the always-linked `Map` shown in
  the footer templates (the templates depict the fully-populated state). Documentation-only.

## 0.2.1

- **Reconciles a silent drift.** While the skill lived only as an installed copy (see below), its
  `description` trigger phrases were condensed/reworded **without a version bump** — leaving two
  different `0.2.0`s. This release adopts the reworded description and bumps the version so the
  content and the number agree again. Description-only change; no workflow behavior change.
- **Restored to the repo** at this version. Removed in `2c7c792` (see [`DECISIONS.md`](./DECISIONS.md)
  D6); until this restore the only live copy was under `~/.claude/skills/`.

## 0.2.0 and earlier

Predates this changelog. `0.1.0` was the initial systems skill (`f0e1a43`); `0.2.0` followed
(`15074a3`).

---

# cathedral-premise (skill)

Versioned via the `metadata.version` field in `cathedral-premise/SKILL.md`.

## 1.1.2

- **Corrects the business-domain audit adapter (`references/cathedral-business.md`) to match the
  artifacts `business-blueprint-workflow` actually produces.** The adapter audited for
  `ENTITY_RELATIONSHIP.md`, `PUBLIC_API.md`, `ARCHITECTURE.md`, and a MODULE `IMPLEMENTATION_ORDER.md`
  — none of which the producer emits — so every business cathedral audit would raise false
  "missing artifact" findings and miss the real ones. The Applicable-Modes table and the MODULE/LIBRARY
  checks now reference `SPECIFICATION.md`, `API_SURFACE.md` (LIBRARY), `IMPLEMENTATION_PLAN.md`,
  `TEST_PLAN.md`, and `TRACEABILITY_MATRIX.md`. BRIDGE (which legitimately uses
  `IMPLEMENTATION_ORDER.md`) is unchanged. Surfaced by a ROAR review once producer and adapter were
  co-located (see [`DECISIONS.md`](./DECISIONS.md) D6). Audit-semantics fix; no change to the five
  principles or the audit procedure.

## 1.1.1

- Corrects an internal inconsistency: `SKILL.md` prose referred to "four core principles" in four
  places while `references/cathedral-core.md` defines **five** (the fifth being Incremental
  Discipline). All prose now says five. Documentation-only fix; no behavior change.

## 1.1.0 and earlier

Predates this changelog. `1.1.0` is the first release whose `references/cathedral-core.md` documents
five principles (Incremental Discipline plus the Decision Ledger with falsification conditions); the
`SKILL.md` prose was not updated to match at the time — corrected in 1.1.1 above.

---

# owner-roar-protocol (prompts)

Versioned via the visible `Protocol version` line inside the installed block. Prior to v3 the
protocol and its reviewer role used the acronym **RAR**; see v3 for the rename to **ROAR**.

## v4

- **Adds a reviewer discipline rule to the kickoff prompt** (`roar-reviewer.prompt.md`): *verify
  asserted absences, not just presences.* When a finding rests on "X does not exist / is never read /
  has no write-path," the reviewer must run the search that would surface X before asserting it and
  cite the (empty or non-empty) result — never state the expected outcome of an unrun check — and must
  search one ring beyond the files the analysis already cites.
- The installed protocol block (`owner-roar-protocol.prompt.md`) is **unchanged in substance**; the
  rule lives only in the kickoff. Its visible version line moves to v4 in lockstep because the kickoff
  and the installed block share a single protocol version (see [`DECISIONS.md`](./DECISIONS.md) D4).
- **Migration:** re-pasting v4 replaces a v3 block in place — the `OWNER_ROAR_PROTOCOL` markers are
  unchanged (no marker rename this time; D2 stability holds), so the swap is clean and yields a block
  identical to v3 but for the version line.
- **Packaging:** both prompts now ship as **self-contained, manual-invoke Claude Code skills** —
  `roar-reviewer/` and `owner-roar-protocol/`. Each `SKILL.md` is a thin wrapper that reads and applies the
  canonical prompt bundled in its own `references/` (single source of truth, no forked text). The prompts
  moved out of the repo root into those `references/` dirs and stay paste-able for use in any tool.
  Packaging version `0.1.0`, independent of the protocol version. Rationale in
  [`DECISIONS.md`](./DECISIONS.md) (D5).

## v3

- **Renames the reviewer acronym `RAR` → `ROAR`** (Read-Only Adversarial Reviewer) to avoid collision
  with unrelated acronyms in AI/agent contexts (and with the `.rar` archive format). The change is
  total: prompt filenames, the protocol slug (`owner-rar-protocol` → `owner-roar-protocol`), the wire
  wrapper (`--- BEGIN/END ROAR ---`), the `@ROAR` authority tag, the triage header, and the install
  markers (`OWNER_RAR_PROTOCOL` → `OWNER_ROAR_PROTOCOL`).
- **One-time marker migration:** the v3 installer replaces a block delimited by the new *or* the
  legacy markers, in place, so existing v2 installs upgrade without duplication. This is the sole
  sanctioned marker-name change; D2's version-less-stability guarantee resumes under the new name.
- Rationale recorded in [`DECISIONS.md`](./DECISIONS.md) (D3).

## v2

- Adds a **Persistence** rule: the triage is a working-loop artifact kept in chat; findings and the triage table are never written to durable audit/spec artifacts.
- Promotion to a durable record is explicit and Owner-gated, with fixed routing: blueprint/contract↔code drift → `AUDIT.md`; a decision or deliberate rejection → `LEDGER.md`.
- Stabilizes the install markers (version-less) so upgrades replace in place instead of duplicating; the version is carried by the visible `Protocol version` line.
- Rationale recorded in [`DECISIONS.md`](./DECISIONS.md) (D1, D2) to prevent silent re-litigation.

## v1

- Introduces Owner/RAR distinction (authority, not identity).
- Defines `--- BEGIN RAR ---` / `--- END RAR ---` wrapped reviewer output.
- Requires implementer verification before acting on RAR findings.
- Adds the RAR triage circuit-breaker (Confirmed / Rejected / Stale / Needs owner decision / Unclear).
- Adds fail-safe behavior for untagged reviewer-shaped findings.
