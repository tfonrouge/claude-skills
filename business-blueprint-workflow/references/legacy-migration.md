<!-- Loaded when adopting DIRECTIVE.md on an existing blueprint, or migrating any legacy
     blueprint artifact to the current skill version. The authority lifecycle, working gates,
     and .blueprint-execution spec live in ../SKILL.md; the canonical template in
     references/directive-template.md. This file carries ALL migration procedures,
     deliberately kept out of the always-loaded skill core. -->

# DIRECTIVE Adoption & Legacy Migration

## Migration map — legacy shape → migration → trigger

**Trigger rule: a blueprint lacking `DIRECTIVE.md`/`.blueprint-execution` must adopt before its
next substantive design or implementation touch — status determines urgency, not applicability**
(FOCUSED/ACTIVE are presumed due now; dormant blueprints, whatever their status — PAUSED,
BLOCKED, DRIFTED, STABLE, CLOSED, or custom legacy values — remain untouched until touched; the
adoption pass itself is the sanctioned first touch). **Other legacy shapes migrate per their
row-specific triggers below** — they can occur on blueprints that already adopted, which cannot
"adopt again".

An untouched legacy blueprint never draws a **blueprint-completeness** finding; what applies is
**Directive Integrity check 1** at its tiered severity — violation (FOCUSED/ACTIVE), advisory
(any other non-terminal or unknown status), recommendation only (STABLE/CLOSED/archived) —
stated identically in `cathedral-core.md`.

| Legacy shape | Migration | Trigger | Complete when | Introduced in |
|---|---|---|---|---|
| No `DIRECTIVE.md` / `.blueprint-execution` | Adoption procedure below | Next substantive touch | `Authority: APPROVED`, dotfile present, BRIEF banner + adoption record committed | 0.10.0 |
| LIBRARY blueprint in a `(MODULE)` directory | Mode reconciliation fallback (BRIEF `Mode` row → INDEX declaration); optional one-time rename + ledger entry | Fallback indefinite; rename at Owner convenience | Suffix is `(LIBRARY)` + INDEX link updated | 0.9.0 |
| BRIEF without a `Mode` header row | Add the mode's fixed literal | Next touch — absence is never a violation | Row present per the recognizer | 0.9.0 |
| LEDGER without an ID column | Add `L-###` IDs; until then cite `<date> "<first eight words, verbatim>"` | Next touch — never bulk renumber | ID column present, IDs unique | cathedral 1.3.0 |
| Plan/order/matrix without `Advances: OC-#` | Backfill open items (adoption step 2); completed items covered by the baseline-exempt snapshot | At DIRECTIVE adoption | Every open carrier item mapped or Owner-flagged; snapshot recorded | 0.10.0 |
| Narrative-swollen `.blueprint-status` (>60 words) | Move the "current work" narrative into `.blueprint-execution` | At DIRECTIVE adoption | Status file is one line **and under 60 words** (soft cap; >150 words is a hard error once adopted — a status is a status, not a changelog); the narrative lives in AUDIT/LEDGER and current work in `.blueprint-execution` | 0.10.0 |

"Introduced in" is historical metadata only — migration triggers are always the observed
artifact shape, never a version stamp.

**Retirement policy.** A compatibility period ends only by Owner decision, recorded in
DECISIONS.md, and only when **all supported instances have been migrated or the Owner
explicitly declares the remainder unsupported** — retirement is not migration completion and
never conforms an unmigrated instance. The map row then moves to CHANGELOG as history, and any
corresponding runtime compatibility in the skill core is removed **in the same change** — the
core must not accrete dead compat.

## Adoption procedure (per blueprint)

1. Implementer **drafts** DIRECTIVE v1 — per `references/directive-template.md` — from BRIEF +
   `.blueprint-status` + LEDGER (where one exists — non-cathedral blueprints may have none)
   (`Authority: DRAFT` — the draft confers nothing; auto-generated authority is the disease
   this mechanism cures, with better formatting). **The same step creates
   `.blueprint-execution`** with the blueprint's actual current state — it is operational, not
   authority, and the DRAFT window (including a session boundary during Owner review) needs an
   Active/Resuming source for the orientation gate.
2. **Same drafting pass — backfill the traceability oracle** (before any approval, so
   discoveries can still revise the draft). Every **open** item in the **mapping carriers** —
   plan/order/changeset items and the traceability tables; rendered views (Gantt bars, progress
   charts) inherit from their source items and are skipped — gets exactly one of:
   - `Advances: OC-#` — it serves a drafted criterion;
   - `unmapped — Owner: <defer | cancel | amend-directive> pending` — it serves none. Never
     force a mapping (that launders scope drift); an unmappable open item is evidence the draft
     is incomplete and feeds its revision.
   The same pass assembles the **`baseline-exempt` list** — the completed-item complement — by
   item ID where IDs exist, else by **counted section scope**
   (`FILE.md §"<section>" — N completed rows as of adoption` — **name the host artifact**; the validator resolves the section inside it and falls back to the carrier only when the filename is omitted; **count physical rows**, never normalized
   or compound identifiers — real matrices compress ids like `FR-11/12` into one row, and a
   snapshot is only useful if a dumb re-count reproduces it).
   **It also drafts one coverage set per OC** — the obligations that prove each criterion — and
   the resulting `## Directive Completeness` rollup. **The baseline exemption never exempts an
   OC from having a coverage set**: it exempts completed historical items from individual
   `Advances:` backfilling only. Otherwise a fully historical blueprint adopts N criteria while
   exempting all the evidence that proves them. Coverage sets are **Owner-approved semantic
   input, never implementer-derived from OC text** — name similarity is not evidence.
3. **Owner reviews the full packet — draft + complete mapping table (every open item → OC-# or
   flag) + baseline-exempt list + one coverage set per OC with its assurance class — and
   approves.** Approval is the act that confers authority;
   the header flips to APPROVED. Wrong-but-valid mappings are semantic errors only the Owner
   catches (audits verify mapping *existence*, never correctness), and the exemption set alters
   audit coverage — both must be among the approved inputs, never introduced after approval.
4. **Same commit**: BRIEF authority banner (below) + the adoption record — cathedral: ledger
   entry prefixed `DIRECTIVE R1:` (creating `LEDGER.md` with an ID column at `L-001` if the
   blueprint has none); non-cathedral: Amendment History R1 line — carrying the approved
   `baseline-exempt` snapshot + `.blueprint-execution` refreshed with any state change from the
   review window.
5. **Baseline rule**: the adoption record wholesale supersedes BRIEF §Goal/§DoD as authority.
   Pre-adoption divergence needs no reconstruction; amendment provenance is required only from
   adoption forward. Completed pre-adoption items stay unmapped without finding, identified by
   the `baseline-exempt` snapshot — audits re-count counted section scopes, and a count mismatch
   is a finding. (Known residual: count-preserving transition pairs are undetectable from counts
   alone; high-rigor blueprints close this by assigning per-row IDs at adoption. Post-adoption
   items must carry `Advances:` at creation.)

## BRIEF authority banner

Inserted immediately after the BRIEF title/metadata at adoption — a single position-reliable
edit (legacy BRIEF headings are too heterogeneous for per-heading markers):

```markdown
> **Authority notice:** This BRIEF is the historical origin record. Current objective
> authority: [DIRECTIVE.md](DIRECTIVE.md), adopted under <LEDGER L-### | Amendment History R1>
> on <date>. Goal, scope, and completion language below is historical.
```

After adoption, BRIEF is frozen except factual corrections explicitly labeled as such. Git
holds the pre-banner version; no historical copy is made.

## Post-adoption obligations

- Every new plan/order item carries `Advances: OC-#` at creation.
- A still-flagged (`unmapped — Owner pending`) item is a *needs-Owner* audit finding, never
  orphan-work.
- Directive changes only by Owner amendment: `DIRECTIVE R<N>:` ledger entry or Amendment
  History line + Revision bump (+ header flip for revocation) — same commit, unique contiguous
  R-sequence.
- `owner-loop-goal` loops inside the blueprint declare `Advances: OC-#`; their DoD is a
  falsifiable refinement of that bounded contribution and may claim an OC complete only if the
  DoD proves the whole criterion.
