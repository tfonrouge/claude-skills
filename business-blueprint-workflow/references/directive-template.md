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
- R1 <date> — ADOPTED by @<Owner>[ — baseline-exempt: <ids / counted section scopes>]
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
