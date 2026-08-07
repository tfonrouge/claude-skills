# Cathedral Core — Universal Governance Principles

> "If a simpler path and a right path exist, choose the right path."

These principles govern all architectural and implementation decisions in any project
that adopts the cathedral premise. They are domain-agnostic — the domain-specific
audit checks live in separate reference files.

---

## The Five Principles

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

### 5. Incremental Discipline

Incremental execution is permitted only against a fixed blueprint. Every increment
must (a) cite the blueprint section it advances — no citation means drift, not
progress; (b) declare itself **spike** or **construction** (mixing them is the
largest source of load-bearing spikes); and (c) respect the Decision Ledger in
**both directions** — honoring standing rejections AND surfacing standing approvals
whose falsification conditions have been met. Early "yes" is not bedrock; it is
a hypothesis with a tripwire.

---

## The Decision Ledger

Every blueprint in a cathedral-governed project maintains `LEDGER.md` (the blueprint skills
list it as a conditional artifact — required exactly when cathedral governs) recording
decisions symmetrically:

| ID | Date | Decision | Type | Rationale | Evidence required to revisit |
|----|------|----------|------|-----------|------------------------------|

- **IDs use the `L-###` namespace** (L-001 upward). Legacy ledgers without an ID column gain
  IDs opportunistically on next touch, never by bulk rewrite; until then they are cited by
  `<date> "<first eight words of the Decision cell, verbatim>"` — fewer only if the cell is
  shorter; on a same-date prefix collision, extend by whole words to the shortest
  disambiguating length.
- **Directive attribution**: a row that adopts or amends the blueprint's `DIRECTIVE.md` begins
  its Decision cell with the literal prefix **`DIRECTIVE R<N>:`**. The R-sequence must be
  unique and contiguous, and its highest value must equal the DIRECTIVE header's Revision.

Every **APPROVED** entry must carry a non-empty falsification condition — the
evidence that would force a revisit. Without it, an approval is not a decision;
it is an assumption pretending to be one.

### Two drift modes the ledger prevents

- **Rejection amnesia** — a "no" is forgotten and re-litigated. Protected by
  the standing rejection rule.
- **Approval calcification** — a "yes" becomes invisible bedrock, never
  re-examined as evidence accumulates against it. Protected by falsification
  conditions. This is the more dangerous of the two: rejections are remembered
  as decisions, while approvals dissolve into "the ground we're standing on."

### Reopening rules

**REJECTED entries.** Before proposing any approach, check the ledger. If
previously rejected, do not re-propose without explicit justification citing
what new information makes reopening valid.

**APPROVED entries.** During any audit or design session, scan recent work for
evidence matching each entry's falsification condition. If found, the decision
is flagged **due for review** — not auto-reversed, but consciously re-examined.
Silently inheriting a falsified approval is a Critical finding.

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

## Cathedral Audit — Shared Procedure

When asked to **"run cathedral audit"**, Claude must:

1. **Read the cathedral premise** from this skill and the project's `CLAUDE.md` config.
2. **Read the designated blueprint skill's `SKILL.md`** to discover the suffix catalog,
   shared artifacts, and — **if the skill declares one** — the mode→reference-file map.
3. **Locate all blueprint directories** under the configured blueprint root.
4. **For each blueprint**, **first** read the mode sources — directory suffix, `BRIEF.md`
   (mode-independent, common to all modes), and the blueprint's INDEX row — and reconcile
   per **Mode Reconciliation** below; **then** obtain the mode's artifact set and per-step
   Definitions of Done **from the mode→reference map (`references/mode-<mode>.md`) when the
   skill declares one, else from the skill's `SKILL.md` itself** (already read at step 2);
   load the remaining artifacts and evaluate against the **Directive Integrity checks** (below)
   plus the **domain-specific audit checks**
   (see the appropriate `cathedral-systems.md` or `cathedral-business.md` reference).

### Mode Reconciliation

**Catalog validation precedes reconciliation.** Check every mode source against the designated
skill's own catalog; a source carrying an out-of-catalog value (foreign suffix, foreign BRIEF
`Mode`, foreign INDEX Mode-column value) is **excluded from classification** and routes to the
unclassified-blueprint finding — agreement among foreign sources never classifies, it only
sharpens the finding (e.g. a `(FEATURE)` directory whose BRIEF also says FEATURE ⇒
*unclassified, declared foreign mode FEATURE*). Never borrow another skill's contract for a
foreign mode.

Over the catalog-valid sources, precedence is:

**BRIEF `Mode` > *unambiguous* directory suffix > INDEX declaration > ambiguous-suffix default**

*In-directory beats aggregate; explicit beats conventional; an ambiguous suffix is not a
declaration.* A BRIEF `Mode` declaration is a `Mode` field in the BRIEF's header region (before
the first `##` heading) — the table row `| Mode | <MODE> |` or an inline `Mode: <MODE>` line,
bold markers allowed, value a bare catalog literal. The blueprint skill's `SKILL.md` states
which suffixes are ambiguous (business:
legacy `(MODULE)` may be MODULE or a pre-`(LIBRARY)` library) and defines INDEX declarations —
a Mode column value, or the skill's explicit section→mode map (e.g. *Active Bridges* ⇒ BRIDGE).
Sections outside that map (Deferred, Deprecated, organizational groupings) declare nothing.

| Catalog-valid sources present | Agreement | Result |
|---|---|---|
| Any ≥1 | all agree | classified |
| ≥2 declarations (BRIEF / unambiguous suffix / INDEX) | disagree | classify per precedence + **mode-drift finding** naming the stale source |
| Ambiguous suffix + INDEX (or BRIEF) declaration | — | classify per declaration + **legacy note** (not a violation); recommend rename or BRIEF `Mode` row |
| Ambiguous suffix only | — | assume its default mode + low-severity note |
| None — all sources foreign (validated out) | — | **unclassified-blueprint finding**, declared foreign mode named |
| None — no source at all | — | unclassified-blueprint finding |

A missing BRIEF `Mode` row is **always a low-severity recommendation, never a completeness
violation** — enforcement of the row lives in the authoring workflow's Step 0 Definition of
Done, not in the audit.

### Directive Integrity

**Run `<skill-root>/cathedral-premise/tools/blueprint-lint.py <blueprint-root>` first and
interpret its findings** (it ships inside this skill, so `install.sh` distributes it). It reads the
project's `CLAUDE.md` to learn the **designated blueprint skill** and classifies modes against that
catalog only — a suffix from the other skill is reported *unclassified*, never silently accepted. The
deterministic half of these checks — schema, unique OC ids, R-sequence contiguity, state and
assurance vocabularies, `Verified ≤ obligations`, physical row counts, citation/footer targets,
ledger-section placement, completion-vs-lifecycle gating, and the **denominator** of each OC's
completeness fraction (obligations resolved against carrier rows) — **is owned by the validator,
not by prose.** The validator explicitly does **not** re-derive the *numerator*: "verified"
vocabularies are project-specific and undeclared, so verified counts stay self-reported and the
tool flags them as such. Do not re-perform them by reading: two implementations of one rule drift, which is the
dual-source-of-truth failure this protocol exists to prevent. What remains below for human and
agent judgment is the **semantic** half: whether a coverage set actually proves its OC, whether
an attestation is credible, whether implementation displaced the criteria, whether the premise
was really applied. A validator pass is necessary and never sufficient.

**Severity policy.** The validator reserves **ERROR** for violations of the DIRECTIVE protocol's
own contract on blueprints whose authority is `APPROVED`. Pre-existing **workflow conventions**
that predate this mechanism — navigation-footer hygiene above all — report **WARN** regardless of
adoption: they are real and worth fixing, but a corpus that never opted in is not in violation of
a contract it never signed. Narrative-`.blueprint-status` is the one convention with a genuine
migration trigger (it is a documented row in the migration map), so it escalates to ERROR once the
blueprint has adopted.

Applied per blueprint after mode classification. **Non-adopter guard:** checks 2–8 apply only
where `DIRECTIVE.md` exists; for any blueprint that has not adopted (whatever its status),
check 1 alone applies at its tiered severity and checks 2–8 are a defined
no-op — absence of the directive-mechanism files on a non-adopter is **never** a
blueprint-completeness finding. The audit **never judges the directive against current
reality** — a directive describes the required end-state, and "matching reality" is
goalpost-moving. All oracles are file-based; gate chat lines are never audit evidence.

1. **Presence**: `DIRECTIVE.md` with `Authority: APPROVED`. The adoption trigger is
   action-based and total — *any* legacy blueprint adopts before its next substantive touch;
   **status determines urgency, not applicability**. Severity accordingly: FOCUSED/ACTIVE —
   **violation** (presumed due now); STABLE/CLOSED/archived — **recommendation only** (a note,
   never a finding); **any other non-terminal or unknown status** (PLANNING, PAUSED, BLOCKED,
   DRIFTED, custom legacy values) — **advisory** ("adoption due at next substantive touch" —
   no file records touch-time; that is the maximum file-decidable severity,
   accepted deliberately: enforcement lives in the working gates and Owner review, and the
   threat model is honest-but-drifting sessions, not adversarial evasion).
2. **Authority record complete**: header not `REVOKED`-contradicted; `Revision: N` ⇒ N−1
   recorded amendments — cathedral: ledger rows prefixed `DIRECTIVE R<N>:`; non-cathedral:
   Amendment History lines — with a **unique, contiguous R-sequence** through N, each
   Owner-approved per its record. A revocation record with an unflipped header is a
   **synchronization finding** and the revocation wins.
3. **Traceability — bidirectional.** Coverage is checked in both directions; either direction
   alone is blind to half the failure space.

   **3a — no orphan work** (work → criterion): every plan/traceability item maps to an `OC-#`,
   falls under the adoption record's `baseline-exempt` snapshot (**re-count counted section
   scopes — count *physical rows*, never normalized or compound identifiers; a mismatch is
   itself a finding**), or carries an explicit `unmapped — Owner: … pending` flag. **Mapping
   carriers** are plan/order/changeset items and the Requirement Traceability / Design→Code→Test
   tables; rendered views (Gantt bars, progress charts) inherit their mapping from the source
   items they visualize and are never independently flagged — but they must render **only**
   source items: a rendered element with no corresponding plan/table item is matrix drift (an
   ordinary drift finding, detected by comparing the rendered set against the source set), not
   orphan work. Unmapped and unlisted = **orphan-work finding** (goal displacement detected
   post-hoc); flagged = needs-Owner finding.

   **3b — no uncovered criterion** (criterion → work/evidence): every current `OC-#` has an
   **Owner-approved coverage set** of verification obligations, and a **derived completeness
   state** in the mode's mapping carrier (§Directive Completeness). "At least one mapped item"
   is insufficient — a composite criterion can go green on one trivial task. An OC with no
   approved coverage set is `UNMAPPED` = **violation**. The rollup is never trusted as a source:
   the audit **re-derives each state from the obligations' own rows**, and a mismatch between
   the recorded and re-derived state is a finding. **The `baseline-exempt` snapshot exempts
   individual `Advances:` backfilling on completed historical items — it never exempts an OC
   from having a coverage set** (otherwise a fully historical blueprint adopts N criteria while
   exempting all the evidence that proves them).

   **State model** (closed): `UNMAPPED` · `NOT STARTED` · `IN PROGRESS` · `BLOCKED` · `FAILED` ·
   `MET`. `DEFERRED` and `NOT APPLICABLE` are **not** execution states — they require a
   DIRECTIVE amendment. `FAILED` = at least one required obligation's **latest applicable**
   verification disproves the criterion, with no later superseding successful evidence (a stale
   failure never poisons an OC after a valid rerun); it is a **violation** and blocks completion
   claims. `BLOCKED` also prevents completion; `FAILED` is stronger — evidence currently
   contradicts the target.

   **Assurance axis** (independent of state): `REPLAYABLE` (a repository command/test reproduces
   it) · `ATTESTED` (a named authority records an external observation) · `MIXED` (both
   required). An OC may reach `MET` on attested evidence where the directive permits external
   evidence — otherwise deployment, physical validation and stakeholder acceptance could never
   complete. Report the conclusion by axis: `MET · REPLAYABLE` = independently reproduced ·
   `MET · ATTESTED` = a durable, internally consistent attestation exists; the underlying event
   was **not** independently reproduced · `MET · MIXED` = replayable portion verified, external
   portion attested. An attestation must record **actor, date, exact result, environment, and
   revision/deploy identity** — the last a content stamp (`owner-roar-protocol` v5), never a
   wall-clock date alone; a missing field makes the obligation unverifiable, not `MET`.

   **Coverage-set integrity**: **every** change needs Owner approval and a ledger record —
   additions are not automatically safe (they expand scope, cost and the proof required, and can
   make an OC unreachable). **Removals or narrowings additionally follow the DIRECTIVE amendment
   path** with a recorded rationale, since they make `MET` trivially reachable with no OC text
   change. Additions require an explicit scope/cost impact note but no `Revision` bump when the
   OC's meaning is unchanged.
4. **Displacement**: has implementation advanced/satisfied criteria, or silently displaced them?
   This remains a **semantic** review, but it now consumes 3b's re-derived rollup as its
   evidence base rather than reasoning from scratch.
5. **Provenance**: where BRIEF and DIRECTIVE differ, the divergence is covered by the adoption
   baseline or a post-adoption amendment.
6. **Completion honesty**: any completion claim is evaluated against **all** current OC-#s via
   3b's rollup — never the latest resolved blocker. A claim standing while any OC is `FAILED`,
   `BLOCKED` or `UNMAPPED` is a **violation**; a claim resting on `MET · ATTESTED` obligations
   must say so rather than presenting them as reproduced.
7. **Abandoned excursion**: an excursion frame older than the project's staleness threshold
   (default 14 days; optional `Excursion staleness threshold:` field in the CLAUDE.md cathedral
   config) — or, where the return condition is repository-checkable, satisfied but uncleared.
   A signal for examination, not a violation.
8. **Execution-state consistency** (`.blueprint-execution`): *plan-item mode* — the item exists,
   is open, and its `Advances:` includes the Active OC; *design mode* — the predecessor artifact
   exists (vacuous at Step 0), and artifacts beyond the claimed step draw a **confirmation flag**
   (legitimate during rework, drift otherwise); *idle* — false if open excursion frames or open
   mapped items exist. Disagreement = **execution-drift finding** (low severity; remedy is
   updating the dotfile at next orientation, not editing the plan).

### Output Format

Produce a single **`CATHEDRAL_AUDIT_REPORT.md`** in the project root:

```markdown
# Cathedral Audit Report
> Generated: {date}
> Premise: cathedral
> Skill: {blueprint skill name}
> Blueprint root: {root}

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

- **Rejection Guard (High).** No artifact may contradict a standing REJECTED
  ledger entry without documented justification. Recent work must not silently
  re-introduce a rejected approach under a different name.
- **Approval Review (Critical when silently inherited).** Every APPROVED ledger
  entry must have a non-empty falsification condition. For each entry, scan
  recent artifacts, benchmarks, and commits for evidence matching that
  condition. Any entry whose condition has been met is flagged **due for review**.
- Be strict. The cathedral premise exists precisely so that drift is caught early.
  Do not rationalize violations — flag them and let the developer decide.
- If no code exists yet for a blueprint, skip the drift check but still audit the
  artifacts for internal consistency and principle alignment.
- If a violation is ambiguous, flag it as a **warning** with an explanation rather
  than silently passing it.
