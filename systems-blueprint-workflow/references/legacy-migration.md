<!-- The compact DIRECTIVE contract, working gates, and .blueprint-execution spec live in
     ../SKILL.md; the canonical template lives in references/directive-template.md. This file
     carries ALL migration procedures for legacy blueprints, deliberately kept out of the
     always-loaded skill core. -->

# DIRECTIVE Adoption & Legacy Migration

## Migration map — legacy shape → migration → trigger

**Trigger rule: a blueprint lacking `DIRECTIVE.md`/`.blueprint-execution` must adopt before
its next substantive design or implementation touch — status determines urgency, not
applicability** (FOCUSED/ACTIVE are presumed due now; dormant blueprints, whatever their status
— PAUSED, BLOCKED, DRIFTED, STABLE, or custom legacy values — remain untouched until touched;
the adoption pass itself is the sanctioned first touch). **Other legacy shapes migrate per
their row-specific triggers below** — they can occur on blueprints that already adopted, which
cannot "adopt again".

An untouched legacy blueprint never draws a **blueprint-completeness** finding; what applies is
**Directive Integrity check 1** at its tiered severity — violation (FOCUSED/ACTIVE), advisory
(any other non-terminal or unknown status), recommendation only (STABLE/CLOSED/archived) —
stated identically in `cathedral-core.md`.

| Legacy shape | Migration | Trigger | Complete when | Introduced in |
|---|---|---|---|---|
| No `DIRECTIVE.md` / `.blueprint-execution` | Adoption procedure below | Next substantive touch | `Authority: APPROVED`, dotfile present, BRIEF banner + adoption record committed | 0.3.0 |
| LEDGER without an ID column | Add `L-###` IDs; until then cite `<date> "<first eight words, verbatim>"` | Next touch — never bulk renumber | ID column present, IDs unique | cathedral 1.3.0 |
| Plan/changeset/matrix without `Advances: OC-#` | Backfill open items (adoption step 2); completed items covered by the baseline-exempt snapshot | At DIRECTIVE adoption | Every open carrier item mapped or Owner-flagged; snapshot recorded | 0.3.0 |
| Narrative-swollen `.blueprint-status` (>60 words) | Move the "current work" narrative into `.blueprint-execution` | At DIRECTIVE adoption | Status file is one line **and under 60 words** (soft cap; >150 words is a hard error once adopted — a status is a status, not a changelog); the narrative lives in AUDIT/LEDGER and current work in `.blueprint-execution` | 0.3.0 |

"Introduced in" is historical metadata only — migration triggers are always the observed
artifact shape, never a version stamp.

**Retirement policy.** A compatibility period ends only by Owner decision, recorded in
DECISIONS.md, and only when **all supported instances have been migrated or the Owner
explicitly declares the remainder unsupported** — retirement is not migration completion. The
map row then moves to CHANGELOG as history, and any corresponding runtime compatibility in the
skill core is removed **in the same change**.

## Adoption procedure (per blueprint)

1. Implementer **drafts** DIRECTIVE v1 — per `references/directive-template.md` — from BRIEF +
   `.blueprint-status` + LEDGER (where one exists — non-cathedral blueprints may have none)
   (`Authority: DRAFT` — confers nothing). **Same step creates `.blueprint-execution`** with the
   blueprint's actual current state (the DRAFT window needs an orientation source).
2. **Same drafting pass — backfill**: every open item in the **mapping carriers** (plan/
   changeset items and the traceability tables — rendered Gantt/progress views inherit from
   their source items and are skipped) gets `Advances: OC-#`
   or `unmapped — Owner: <defer | cancel | amend-directive> pending` (never force a mapping —
   an unmappable item is evidence the draft is incomplete and feeds its revision). Assemble the
   `baseline-exempt` list for completed items — by ID, else counted section scope
   (`FILE.md §"<section>" — N completed rows as of adoption` — **name the host artifact**; the validator resolves the section inside it and falls back to the carrier only when the filename is omitted; **count physical rows**, never normalized
   or compound identifiers). **Also draft one coverage set per OC** + the
   `## Directive Completeness` rollup: the baseline exemption covers `Advances:` backfilling on
   completed items, **never an OC's coverage set**. Coverage sets are Owner-approved semantic
   input, never derived from OC text.
3. **Owner reviews the full packet** — draft + complete mapping table + baseline-exempt list +
   one coverage set per OC with its assurance class — **and approves** (header → APPROVED). Wrong-but-valid mappings and the exemption set are
   exactly what only the Owner can catch; both are approved inputs, never post-approval additions.
4. **Same commit**: BRIEF authority banner (below) + adoption record — cathedral: ledger entry
   prefixed `DIRECTIVE R1:` (creating `LEDGER.md` with an ID column at `L-001` if missing);
   non-cathedral: Amendment History R1 line — carrying the approved `baseline-exempt` snapshot +
   `.blueprint-execution` refreshed.
5. **Baseline rule**: the adoption record supersedes BRIEF §Goal/§DoD wholesale; provenance is
   required only from adoption forward; audits re-count counted section scopes (mismatch = a
   finding; count-preserving transition pairs are a stated residual — close with per-row IDs for
   high-rigor blueprints). Post-adoption items must carry `Advances:` at creation.

## BRIEF authority banner

```markdown
> **Authority notice:** This BRIEF is the historical origin record. Current objective
> authority: [DIRECTIVE.md](DIRECTIVE.md), adopted under <LEDGER L-### | Amendment History R1>
> on <date>. Goal, scope, and completion language below is historical.
```

Inserted once, immediately after the BRIEF title/metadata; BRIEF is frozen thereafter except
factual corrections explicitly labeled as such.
