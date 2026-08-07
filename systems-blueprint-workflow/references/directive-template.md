<!-- Canonical DIRECTIVE.md template. Loaded at blueprint creation (Step 0/B0/F0/P0) and at
     DIRECTIVE adoption on a legacy blueprint (see legacy-migration.md). The authority
     lifecycle rules that the working gates consume every session live in ../SKILL.md.
     BYTE-IDENTICAL TWIN: the other blueprint skill ships the same file — keep in lockstep
     (install.sh verifies equality). -->

# DIRECTIVE.md — Canonical Template

```markdown
# Directive — <BlueprintName>

**Authority:** DRAFT | APPROVED | REVOKED
**Drafted by:** @<implementer> · **Approved by:** @<Owner> | —
**Effective:** <date> | — · **Adoption decision:** LEDGER L-### | Amendment History R1 (non-cathedral)
**Revision:** N

## Owner Directive
<One sentence. The immutable mandate.>

## Outcome Criteria
<!-- Status per criterion is NOT recorded here: DIRECTIVE is amendment-only and a ticked box is
     self-attestation, not an oracle. See the mapping carrier's §Directive Completeness. -->
- OC-01: <falsifiable outcome>
- OC-02: <falsifiable outcome>

## Non-Goals
- <explicit exclusion>

## Governing Constraints
- <one-line invariant>[ — binding: <ledger ref>]

## Amendment Rule
Only an explicit Owner decision may change this file. Each amendment increments
Revision and records provenance: a LEDGER entry (cathedral) or an Amendment
History line below (non-cathedral).

## Amendment History        <!-- REQUIRED non-cathedral; OMITTED where LEDGER holds it -->
- R1 <date> — ADOPTED by @<Owner>[ — baseline-exempt: <ids / `FILE.md §"Section" — N` counted scopes>]
```

Rules of form:

- **Hard cap**: the normative body (title through Amendment Rule) fits one screen (~30 lines);
  Amendment History is cap-exempt (>~5 entries = directive-churn signal for Owner re-examination).
- **Constraints** are one-line invariants; `binding: <ledger ref>` where the constraint
  originates in a ledger decision, omitted where no LEDGER exists. Never copy ledger rationale
  or falsification conditions.
- **Ledger reference grammar**: the ledger's own local ID (`L-004`, `D5`), else
  `<date> "<first eight words of the Decision cell, verbatim>"` — fewer only if the cell is
  shorter; on a same-date prefix collision, extend by whole words to the shortest
  disambiguating length.
- For PATCH-scale work the body is typically 3–4 lines: one OC plus the blast-radius constraint.

## OC quality rubric — apply before approving any directive

A criterion that is immutable, mapped and green is still useless if it was vague. **Bad criteria
make every downstream artifact confidently wrong**, so this test runs at drafting, before the
Owner is asked to approve anything.

A valid OC states, explicitly or unambiguously by reference:

1. **Observable end-state** — what is true when it holds;
2. **Verification method** — how you would check it;
3. **Boundary / environment** — where it must hold (prod? all roles? which target?);
4. **Failure condition** — what observation would show it is *not* met;
5. **No subjective term** (`clean`, `robust`, `maintainable`, `fast`, `secure`) without a
   measurable reading attached.

| VALID (falsifiable) | INVALID (unfalsifiable) |
|---|---|
| "Un distribuidor autenticado completa catálogo → reserva → checkout → pedidos contra datos reales en producción — verificable: smoke e2e verde contra el servidor vivo" | "El portal B2B funciona correctamente" |
| "Ningún response servido a rol cliente/distribuidor divulga costo ni utilidad, ni directa ni derivadamente — verificable: TEST-010/011 sobre todos los response models" | "Los datos sensibles están protegidos" |
| "Cero escrituras a WinCaja producción mientras G1-G6 no cierren — verificable: adapter stub no-op, TEST-053" | "La integración con el ERP es segura" |
| "p95 de `/api/catalog` ≤ 400 ms con 15 productos y 1 llamada a inventario — verificable: spies de conteo" | "El catálogo es rápido" |

If a criterion cannot be written this way, it is usually two criteria, or it is a *constraint*
(→ Governing Constraints), or it is a non-goal.

## Validity / Review Triggers (optional section)

An OC is a desired outcome, not a hypothesis — do **not** attach a falsification condition to
each one. What *can* expire is the premise the whole mandate rests on. When such a premise
exists, record it so the directive cannot become unquestioned bedrock:

```markdown
## Validity / Review Triggers
- Re-evaluate this directive if <business premise or external condition changes> — source: <ledger ref>
```

This keeps the *why* alive without copying frozen BRIEF history forward.

## Completeness rollup

Every OC needs an **Owner-approved coverage set** (the obligations that prove it) and a **derived
state**. Both live in the mode's mapping carrier — the artifact that already carries the
`Advances: OC-#` mappings — under a `## Directive Completeness` section, **never in
DIRECTIVE.md**: status is mutable, DIRECTIVE is amendment-only, and a hand-ticked box is
self-attestation, not an oracle.

| Mode | Carrier |
|---|---|
| MODULE / LIBRARY (business) | `TRACEABILITY_MATRIX.md` |
| BRIDGE (business) | `IMPLEMENTATION_ORDER.md` |
| SUBSYSTEM (systems) | `TRACEABILITY.md` |
| FEATURE (systems) | `IMPLEMENTATION_PLAN.md` |
| PATCH (systems) | `CHANGESET.md` |

Section shape:

```markdown
## Directive Completeness

| OC | Coverage set (Owner-approved obligations) | Verified | State | Assurance | Evidence |
|----|-------------------------------------------|----------|-------|-----------|----------|
| OC-01 | FR-09, FR-10, FR-13 + live smoke | 3/4 | IN PROGRESS | MIXED | TEST-…; attestation below |
| OC-02 | FR-08, FR-08b | 2/2 | MET | REPLAYABLE | TEST-010, TEST-011 |

- OC-01 live smoke — @owner · <date> · <exact result> · <environment> · <content stamp>
```

- **States** (closed): `UNMAPPED` (no approved coverage set — a violation) · `NOT STARTED` ·
  `IN PROGRESS` · `BLOCKED` · `FAILED` · `MET`. `DEFERRED` / `NOT APPLICABLE` are **not**
  execution states — they require a DIRECTIVE amendment.
- **`FAILED`** = an obligation's *latest applicable* verification disproves the criterion with no
  later superseding success. It blocks completion claims and is a violation; `BLOCKED` also
  prevents completion, but `FAILED` is stronger.
- **Assurance** is an independent axis derived from the obligations: `REPLAYABLE` · `ATTESTED` ·
  `MIXED`. `MET` is reachable on attested evidence — otherwise deployment or stakeholder
  acceptance could never complete — but audits report `MET · ATTESTED` distinctly from
  `MET · REPLAYABLE`. Every attestation carries **actor, date, exact result, environment,
  revision/deploy identity** (a content stamp, not a bare date); a missing field makes the
  obligation unverifiable, not `MET`.
- **Derived, never declared.** States are recomputed from the obligations' rows; audits re-derive
  them and a mismatch is a finding. `blueprint-lint` re-derives the **denominator** only — the
  numerator stays self-reported, and free-text obligations are counted but never resolved.
- **Coverage sets are goalpost-protected**: **every** change needs Owner approval + a ledger
  record — additions are *not* automatically safe (they expand scope, cost and required proof).
  **Removals or narrowings additionally take the amendment approval path**; additions carry a
  scope/cost impact note but no `Revision` bump when the OC's meaning is unchanged.

## Registers *(pilot-scoped — add only when the blueprint needs them)*

Blocker and dependency facts otherwise scatter across `.blueprint-status`,
`.blueprint-execution`, the rollup, LEDGER pending entries and plan fields. Those are **not
automatically contradictory** — an ACTIVE blueprint may legitimately have one blocked OC while
another advances. What is missing is a *relationship model*, so the carrier holds the
authoritative registers and everything else **derives** from them:

```markdown
## Blockers

| ID | Blocks | Cause / source | Owner | Clear when | State |
|----|--------|----------------|-------|-----------|-------|
| BLK-01 | OC-03 / P4 | DEP-02 | @owner | staging deploy green | OPEN |

## Dependencies

| ID | Required by | Target | Satisfied when | State | Evidence |
|----|-------------|--------|----------------|-------|----------|
| DEP-01 | OC-02 / P3 | OtherBlueprint:OC-04 | its OC is MET | OPEN | link |
```

States: `OPEN` · `CLEARED` · `SATISFIED` · `WAIVED`. Derivation rules — never restate the same
word in four files:

- rollup `BLOCKED` derives from an **open blocker referencing that OC**;
- `.blueprint-execution` cites the **active** blocker/dependency only while it blocks current work;
- `.blueprint-status = BLOCKED` only when **no meaningful unblocked path remains**;
- LEDGER pending entries are **cited as causes**, never duplicated;
- `MAP.md` is the derived cross-blueprint view; INDEX "Blocked By" a summary.

**Enforcement today (honest):** `blueprint-lint` checks register *shape* — id uniqueness, state
vocabulary, and that `OC-#`s named in the local column exist in the DIRECTIVE. Cross-blueprint
target resolution, evidence checking and cycle detection are **not implemented**; they remain
Owner and ROAR judgment until the pilot shows they are needed.
