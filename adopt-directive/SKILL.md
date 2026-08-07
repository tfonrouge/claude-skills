---
name: adopt-directive
metadata:
  version: 0.1.0
description: >
  Adopts DIRECTIVE.md on ONE existing blueprint, in any project governed by either blueprint
  skill. Resolves the project's designated skill and the blueprint's mode, then runs that
  skill's documented adoption procedure: drafts the directive, backfills open items, assembles
  the coverage sets and baseline snapshot, and presents the packet for Owner approval in two
  parts (criteria first, evidence second). Never confers authority by itself.

  MANUAL INVOCATION ONLY — do NOT auto-activate. Adoption edits blueprint artifacts and ends in
  an Owner approval, so it must be started deliberately. Invoke only when the user explicitly
  runs `/adopt-directive`, or explicitly asks to adopt DIRECTIVE.md on a named blueprint. Do NOT
  trigger on generic "work on this blueprint" requests, and never adopt more than one blueprint
  per invocation — the point is to keep each adoption reviewable.
---

# adopt-directive (skill wrapper)

A **thin wrapper**: it adds no rules. The adoption procedure, migration map, baseline rules and
banner text live in the designated blueprint skill's `references/legacy-migration.md`, and the
DIRECTIVE template plus the OC quality rubric in its `references/directive-template.md`. Read
those and follow them; do not restate or reinterpret them here (see `DECISIONS.md` D5 for why
wrappers point at a single source instead of copying it).

## Arguments

`/adopt-directive <path-to-blueprint-dir> [Owner Directive: "<one sentence>"]`

If the Owner supplies the directive sentence, use it verbatim as the mandate — it is theirs, not
a draft. If not, propose one and flag it as the part most needing their scrutiny.

## Steps

1. **Resolve context before anything else.** Read the project's `CLAUDE.md` for
   `Blueprint skill:` to learn the designated skill, and resolve the blueprint's mode by
   reconciliation (BRIEF `Mode` row → unambiguous suffix → INDEX declaration). A suffix from the
   other skill's catalog, or no resolvable mode, **stops the adoption** — say so and ask.
2. **Load the two references** from the designated skill and follow the procedure they define.
3. **Present the packet in two parts, and stop after each.** First the proposed **Owner Directive
   + Outcome Criteria** alone, checked against the OC quality rubric. Only once the Owner
   approves those, the **coverage sets with their assurance class, the `Advances:` mapping of
   open items, and the `baseline-exempt` snapshot**. Approving bad criteria contaminates
   everything downstream, which is why they are reviewed alone and first.
4. **Never set `Authority: APPROVED` yourself.** The Owner's approval is what confers authority;
   until then the file is `DRAFT` and confers nothing.
5. **On approval**, write the records in one commit-ready change: BRIEF authority banner, adoption
   record (ledger entry or Amendment History R1) carrying the approved snapshot, and
   `.blueprint-execution`.

## Before handing back

Run `cathedral-premise/tools/blueprint-lint.py <blueprint-root>` and report its findings, then
emit the **Producer Coverage Census** table (`owner-roar-protocol` v6) — a blueprint adoption is a
prose artifact, so **Claims** and **Twins** apply and the other axes are named as skipped. A clean
lint is necessary and never sufficient: it cannot judge whether a coverage set actually proves its
criterion. Leave the diff uncommitted for the Owner unless they ask otherwise.

## What this skill deliberately does not do

- Adopt several blueprints in one run, or scan a project for adoption candidates. Adoption is
  triggered by a substantive touch on one blueprint, not by a migration campaign.
- Decide the Outcome Criteria on the Owner's behalf. It drafts; they decide.
- Judge whether the evidence is sufficient. That is Owner and ROAR territory.
