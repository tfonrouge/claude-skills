# Changelog

This repo ships four independently versioned products. Each has its own section below.

---

# business-blueprint-workflow (skill)

Versioned via the `metadata.version` field in `business-blueprint-workflow/SKILL.md`.

## 0.9.0

- **Progressive-disclosure split.** `SKILL.md` (1499 lines — observed to truncate mid-load in real
  sessions) now carries only the shared core (~390 lines): mode selection, mode→reference map,
  INDEX/`.blueprint-status`/MAP, artifact overviews, navigation. The full step-by-step workflows
  moved verbatim to `references/mode-module.md`, `references/mode-library.md`,
  `references/mode-bridge.md` — **normative**, loaded per blueprint via the map. Shared
  INDEX/status/MAP/navigation prompt patterns moved to `references/example-prompts.md`; the
  "Why This Workflow" sales section was dropped.
- **`(LIBRARY)` directory suffix.** LIBRARY blueprints now use `blueprints/<Name>(LIBRARY)/`;
  `(MODULE)` remains valid for MODULE and, during the compatibility period, may denote a legacy
  library — resolved via BRIEF `Mode` row → INDEX declaration → assume MODULE (see D7).
- **BRIEF `Mode` header row** (fixed literal per mode) + INDEX registration added to every
  Step 0/B0 Definition of Done. Absence in pre-existing BRIEFs is never an audit violation.
- **INDEX section→mode map** documented: *Active Bridges* ⇒ BRIDGE; other sections declare nothing.

## 0.8.3

- **Removes the last reference to an HTML/docs-build mechanism.** The Bridge teardown step
  (Bridge Mode) dropped its parenthetical about wiring up `scripts/build_dashboard.py` as a
  "passive detector … on the next docs build." Blueprint artifacts are pure Markdown with inline
  Mermaid (rendered natively by GitHub/editors, no build step); the skill no longer alludes to any
  `.md → .html` build tool. The north-stars grep-scan — the actual, build-free drift check — is
  unchanged. Documentation-only.

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

## 1.2.0

- **Mode Reconciliation procedure** added to `cathedral-core.md` §Shared Procedure: audits now
  resolve each blueprint's mode *before* loading its artifact set, from three sources with fixed
  precedence — BRIEF `Mode` > unambiguous suffix > INDEX declaration > ambiguous-suffix default —
  with catalog validation first (foreign modes like a business `(FEATURE)` never classify and never
  borrow another skill's contract; they yield an unclassified-blueprint finding). Disagreements
  yield mode-drift findings; legacy `(MODULE)`-as-LIBRARY yields a legacy note, not a violation.
- **Map-conditional artifact loading**: per-step Definitions of Done are read from the blueprint
  skill's `references/mode-<mode>.md` when the skill declares a mode→reference map, else from its
  `SKILL.md` — keeping audits of unsplit skills (systems) working unchanged. `cathedral-systems.md`
  deliberately untouched.
- `cathedral-business.md`: suffix table gains `(LIBRARY)` with legacy `(MODULE)` compat; blueprint
  completeness cross-references the mode reference files; missing BRIEF `Mode` row is codified as
  recommendation-only.

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

## v5

Derived from a 13-round review session on a live project (Drydock DDvm L21), where the protocol
caught real defects — a harness that deleted files it did not create, a "manifest coverage" row
that built artifacts and observed nothing, a cross-process correlation, and four design proposals
that each tried to route around a standing Owner constraint — but spent most rounds rediscovering
the *same class* of defect one axis at a time. Every addition below traces to an observed failure
in that session; none is speculative.

- **Content-identifying revision stamp in the wire format.** The first line inside the block is
  now `Reviewed at: <commit-hash>[ + worktree <object-hash>][ + untracked <path>@<blob-hash> …]`,
  with the invariant that **every cited location is covered by some component of the stamp**.
  Tracked modifications are identified by a `git stash create` object (non-destructive, later
  inspectable with `git show`); cited untracked files by `git hash-object` (read-only, no `-w`).
  Fixes the one observed false-positive mode: a round that reviewed a pre-commit draft and
  reported findings already fixed in the landed file. Two forms were rejected during pre-landing
  review: a wall-clock timestamp (**not an identity** — it cannot reconstruct or compare bytes),
  and `git stash create` alone, which silently omits untracked files and returns **empty** in a
  tree whose only changes are untracked — leaving the stamp covering nothing reviewed. Multi-repo
  reviews stamp each repository on its own line.
- **Asserted absences are bound to the stamp** (kickoff prompt, where the absence rule has lived
  since v4). An absence cites no file, so the per-file untracked rule cannot cover it and an empty
  result is meaningless once its corpus is unidentifiable. Sanctioned corpora are now exactly
  those the stamp covers: `git grep <pattern> <object-hash>` against the stamped object, `git grep`
  over the worktree (tracked content only), or an untracked-walking tool **only** with every
  untracked file in scope hashed. Pathname claims get their own component — `+ paths@<digest>`
  from a sorted listing — because an empty untracked directory has no blob and appears in no Git
  tree, so every content component is byte-identical whether or not it exists. Commands are quoted
  with their results; an absence whose corpus the stamp does not cover is not a verified absence.
- **Two independent classification axes**, both required on every finding: **landing impact**
  (`Blocking` — unsafe behavior, invalid gate, violated Owner constraint, or a false claim that
  changes implementation **or diagnostic** decisions · `Non-blocking` — clarity/ergonomics with no
  behavioral or decision consequence) and **scope** (`In-scope` / `Out-of-scope` relative to the
  submitted work's contract). Severity alone mis-sorted a LOW-severity finding that was
  nonetheless a false operational claim in a test message. A first draft folded scope into the
  impact enum as a third value `Deferred`; pre-landing review showed the axes are orthogonal — an
  unsafe defect in an out-of-scope consumer is *both* — so they were separated. Severity is now
  explicitly optional, free-form context with no action of its own (it was previously referenced
  as a required companion field while never being defined).
- **Class findings over instances.** When findings share a root cause or instantiate a policy
  (shared-path ownership, cross-process correlation, unverified activation), the reviewer names
  the CLASS: the complete invariant the code must hold — not the local symptom — plus a bounded
  sweep ("check every write/cleanup path in this harness"). One class finding replaces N
  follow-up rounds; in the source session a single shared-path-ownership class finding would have
  collapsed four sequential cleanup rounds into one.
- **A scoped terminal state.** Zero findings has exactly one form —
  `REVIEW COMPLETE — no claims to verify within the reviewed diff and stated scope.` It scopes to
  that diff and stated scope, never asserts global cleanliness, and never authorizes commit or
  push. Prevents reviewer silence from being read as approval without weakening the rule that
  ROAR has no commit authority.
- **Named audit axes for new test/harness submissions**: behavior, negative path,
  cleanup/ownership, concurrency, process correlation, claim-to-oracle alignment. Naming them
  prevents axis-by-axis rediscovery across rounds; explicitly *not* a promise that one pass finds
  everything.
- **Constraint-convergence check for design threads.** Before reviewing option mechanics, the
  reviewer checks each option against already-decided constraints in the project's decision
  ledger; repeated avoidance of a standing constraint across successive proposals is itself a
  finding. The reviewer still does not generate designs.
- **Implementer preflight — MANDATORY** before submitting a new test/harness or a design
  recommendation for review (installed block, implementer section): every green row observes the
  named behavior; every destructive write has ownership and concurrent-run reasoning; every
  cross-process conclusion is same-process or explicitly correlated; every design carrier is
  traced producer → transport → consumer; every standing approved/rejected constraint is listed
  and checked against the proposal. This is the highest-leverage change — all five items map to
  defects that reached review in the source session.
- **The triage table is now total and non-overlapping, with a deterministic action for every
  combination.** Buckets are **evaluated in order, first match wins** (Unclear → Rejected →
  Stale → Confirmed (out of scope) → Needs owner decision → Confirmed (in scope)), which resolves
  the overlap between a confirmed in-scope finding and one whose *remedy* needs an Owner
  trade-off. `Confirmed` splits into in-scope (eligible to fix) and out-of-scope (do **not** edit
  here; surface for Owner routing). Landing behavior is stated once and generally: **`Blocking`
  halts the landing from whichever bucket it lands in** — in scope → fix or obtain an explicit
  Owner override; out of scope → surface and STOP; needs-owner-decision → STOP — so a Blocking
  finding can halt a landing without authorizing an out-of-scope edit. The implementer rule
  tightened from "act only on Confirmed findings" (ambiguous once Confirmed split) to "edit only
  on **Confirmed (in scope)**". An out-of-scope confirmed finding
  is promoted like any durable record — a ledger entry or spawned task at Owner direction —
  **never a parallel findings list**. Rationale in [`DECISIONS.md`](./DECISIONS.md) (D8), which
  also records what was deliberately **left out**.
- **Migration:** re-pasting v5 replaces a v3 or v4 block in place — markers unchanged (D2 holds).
  Both prompts move to v5 in lockstep (D4). Reviewer sessions only gain v5 behavior once the
  **updated** `roar-reviewer.prompt.md` is pasted; an older paste keeps producing v4-shaped
  reviews.

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
