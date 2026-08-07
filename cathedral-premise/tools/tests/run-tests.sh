#!/usr/bin/env bash
# Negative controls for blueprint-lint. Every fixture is deliberately defective; the run FAILS
# if any expected finding stops firing (a guard that never rejects anything is untested — the
# validator's own first real run shipped two false positives and one silent gap).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
LINT="$HERE/../blueprint-lint.py"
# fixtures are split by DECLARED CATALOG — the validator classifies modes against the designated
# skill only, so validating that split is itself part of the contract
OUT="$(python3 "$LINT" "$HERE/business/blueprints" 2>&1
       python3 "$LINT" "$HERE/systems/blueprints" 2>&1
       python3 "$LINT" "$HERE/badcfg/blueprints" 2>&1)"

EXPECTED=(
  "duplicate OC ids"
  "approval record sits under"
  "verified 3 > obligations 2"
  "is MET but only"
  "assurance 'INVENTADO' outside"
  "has an empty coverage set"
  "state 'CASI' outside the closed model"
  "is not declared in DIRECTIVE.md"
  "attestation line in the rollup"
  "lines (cap 7)"
  "excursion depth 4 exceeds"
  "cites OC-77, not declared"
  "missing target"
  "Authority 'MAYBE' outside"
  "R-sequence in LEDGER not contiguous"
  "!= DIRECTIVE Revision"
  "has no rollup row"
  "a completion claim cannot stand"
  "obligations but its coverage set resolves to"
  "R-sequence in Amendment History not contiguous"
  "no such row in IMPLEMENTATION_PLAN.md"
  "attestation lacks required field"
  "recount mismatch"
  "Blockers BLK-01 state"
  "Blockers has duplicate ids"
  "Dependencies DEP-01 state"
  "references OC-99, not declared"
  ".blueprint-status carries"
  "is not a single line"
  "navigation footer is not the last content"
  "artifact has no navigation footer"
  "mode requires carrier"
  "cannot prove itself"
  'no `**Authority:**` header field'
  'no `**Revision:**` field'
  'declares no `OC-##` outcome criteria'
  "APPROVED but no"
  "normative body is"
  'adopted blueprint has no `.blueprint-execution`'
  'neither a `DIRECTIVE R<N>:` ledger row'
  "duplicate R numbers in"
  'no `.blueprint-status` file'
  "rollup has duplicate row for"
  "unclassified blueprint: no mode declared"
  "no such row in TRACEABILITY_MATRIX.md"
  "is from another skill's catalog"
  "BRIEF declares Mode"
  "mode-drift: sources disagree"
  "INDEX declares Mode"
  "outside every known catalog"
  "is from another skill's catalog"
  "suffix(ambiguous)"
  "is not a known catalog"
  "cannot rest on absent authority"
)

fail=0
for e in "${EXPECTED[@]}"; do
  if ! grep -qF -- "$e" <<<"$OUT"; then
    echo "MISSING GUARD: expected finding not fired — '$e'"
    fail=1
  fi
done

# positive control (MANDATORY): a clean corpus must stay clean, or the guards are trigger-happy.
# Defaults to the bundled minimal-valid blueprint; CLEAN_CORPUS may point at a real project.
# foreign-catalog guard: a systems mode must NOT be flagged foreign inside its own catalog
if python3 "$LINT" "$HERE/systems/blueprints" 2>&1 | grep -qF "is from another skill's catalog"; then
  echo "MISSING GUARD: systems fixture flagged foreign in its OWN catalog"
  fail=1
fi

# POSITIVE CONTROLS (mandatory): conforming corpora for BOTH catalogs, covering all five
# carriers — MATRIX, ORDER, TRACEABILITY, PLAN, CHANGESET. A single business/MODULE corpus left
# four carriers unexercised, so a carrier-selection bug could pass unnoticed.
for CORPUS in "${CLEAN_CORPUS:-$HERE/business/clean/blueprints}" "$HERE/systems/clean/blueprints"; do
  if ! python3 "$LINT" "$CORPUS" --quiet >/dev/null; then
    echo "FALSE POSITIVE: clean corpus $CORPUS reported errors:"
    python3 "$LINT" "$CORPUS" | grep '^ERROR'
    fail=1
  fi
done
# every carrier must actually appear in a clean corpus, or the control proves nothing
for C in TRACEABILITY_MATRIX.md IMPLEMENTATION_ORDER.md TRACEABILITY.md IMPLEMENTATION_PLAN.md CHANGESET.md; do
  find "$HERE" -path '*/clean/*' -name "$C" | grep -q . || { echo "MISSING POSITIVE CORPUS for carrier $C"; fail=1; }
done

if [ "$fail" = 0 ]; then
  echo "OK — all ${#EXPECTED[@]} negative controls fired"
else
  echo "FAILED"
fi
exit "$fail"
