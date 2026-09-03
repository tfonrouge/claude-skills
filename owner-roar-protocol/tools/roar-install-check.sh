#!/usr/bin/env bash
#
# roar-install-check.sh — read-only audit of installed OWNER_ROAR_PROTOCOL blocks across projects.
#
# Modifies neither protocol files nor the audited projects — it only uses a temporary directory that
# it removes on exit. For every CLAUDE.md / AGENTS.md discovered under the scanned roots it reports
# the marker kind (ROAR, legacy RAR, none, malformed — including markers out of order), the
# `Protocol version` line read from the extracted block, blocks duplicated across both files of one
# project and — with --verify — byte-for-byte drift against the canonical block bundled with this
# skill. The corpus (roots, exclusions, depth, files, access errors) is printed every time, so "zero
# legacy blocks" always reads as "zero within this corpus"; an empty or partially unreadable corpus
# is an error, never a clean result.
#
# Usage:
#   roar-install-check.sh [--check] [--verify] [--root DIR]... [--depth N] [--expected FILE]
#                         [--canonical FILE] [--allow-empty] [--quiet]
#   --check         inventory only (default)
#   --verify        inventory + compare every block with the canonical block
#   --root DIR      a collection of projects OR a single project directory (repeatable). Files are
#                   looked for in DIR itself and up to --depth levels below it. Default:
#                   $ROAR_CHECK_ROOTS (colon-separated) or ~/IdeaProjects ~/RustroverProjects ~/git
#                   ~/AndroidStudioProjects. An explicitly given root that does not exist is an error.
#   --depth N       levels below each root to search (default 2: DIR/proj/ and DIR/group/proj/)
#   --expected FILE project directories, one per line ('#' comments, ~ allowed). Each must be
#                   discovered AND carry a block, else it is reported as expected-but-absent
#   --canonical F   installer prompt holding the canonical block
#                   (default: ../references/owner-roar-protocol.prompt.md next to this script)
#   --allow-empty   a corpus with zero candidate files is not an error
#   --quiet         print the summary only
# Exit: 0 clean · 1 findings (drift, legacy, duplicate, malformed, expected-absent)
#       2 error (usage, unreadable canonical, missing explicit root, access errors, empty corpus)
#
# Markers are matched as whole lines: the block's own prose quotes its markers, so an unanchored
# range truncates inside the block (a project-side checker once compared 28 of 48 lines that way).
# Rows are tab-separated internally; a path containing a tab or a newline is not supported.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
MODE="check"; DEPTH=2; EXPECTED=""; QUIET=0; ALLOW_EMPTY=0
CANONICAL="$SCRIPT_DIR/../references/owner-roar-protocol.prompt.md"
ROOTS=(); EXPLICIT_ROOTS=0
FILE_NAMES="CLAUDE.md AGENTS.md"
EXCLUDES="node_modules .git build dist target vendor .Trash"
ROAR_B='<!-- OWNER_ROAR_PROTOCOL:begin -->'; ROAR_E='<!-- OWNER_ROAR_PROTOCOL:end -->'
RAR_B='<!-- OWNER_RAR_PROTOCOL:begin -->';   RAR_E='<!-- OWNER_RAR_PROTOCOL:end -->'
TAB=$'\t'

usage() { sed -n '2,35p' "$0" | sed 's/^# \{0,1\}//'; }
die() { echo "ERROR: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --check) MODE="check" ;;
    --verify) MODE="verify" ;;
    --root) shift; [ $# -gt 0 ] || die "--root needs a DIR"; ROOTS+=("$1"); EXPLICIT_ROOTS=1 ;;
    --depth) shift; [ $# -gt 0 ] || die "--depth needs N"; DEPTH="$1" ;;
    --expected) shift; [ $# -gt 0 ] || die "--expected needs FILE"; EXPECTED="$1" ;;
    --canonical) shift; [ $# -gt 0 ] || die "--canonical needs FILE"; CANONICAL="$1" ;;
    --allow-empty) ALLOW_EMPTY=1 ;;
    --quiet) QUIET=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done
case "$DEPTH" in ''|*[!0-9]*) die "--depth must be an integer" ;; esac

if [ ${#ROOTS[@]} -eq 0 ]; then
  if [ -n "${ROAR_CHECK_ROOTS:-}" ]; then
    OLDIFS="$IFS"; IFS=':'; for r in $ROAR_CHECK_ROOTS; do [ -n "$r" ] && ROOTS+=("$r"); done; IFS="$OLDIFS"
    EXPLICIT_ROOTS=1
  else
    ROOTS=("$HOME/IdeaProjects" "$HOME/RustroverProjects" "$HOME/git" "$HOME/AndroidStudioProjects")
  fi
fi
if [ "$EXPLICIT_ROOTS" = 1 ]; then
  for r in "${ROOTS[@]}"; do [ -d "$r" ] || die "--root does not exist or is not a directory: $r"; done
fi
if [ -n "$EXPECTED" ] && [ ! -r "$EXPECTED" ]; then die "cannot read --expected file: $EXPECTED"; fi

if command -v shasum >/dev/null 2>&1; then sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
elif command -v sha256sum >/dev/null 2>&1; then sha() { sha256sum "$1" | cut -d' ' -f1; }
else die "need shasum or sha256sum"; fi

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
say() { [ "$QUIET" = 1 ] || printf '%s\n' "$*"; }

# extract_block FILE BEGIN END → the block inclusive of its marker lines (whole-line anchored)
extract_block() { awk -v b="$2" -v e="$3" '$0 == b {p=1} p {print} $0 == e {p=0}' "$1"; }
count_line() { grep -c -x -F -- "$2" "$1" 2>/dev/null || true; }
first_line_no() { grep -n -x -F -- "$2" "$1" 2>/dev/null | head -1 | cut -d: -f1; }
block_version() { grep -m1 -o -E 'owner-r(o)?ar-protocol v[0-9]+' "$1" 2>/dev/null | sed 's/.* //'; }

# ---- canonical: exactly one begin and one end, begin before end
CANON_OK=0; CANON_HASH=""; CANON_LINES=0; CANON_BYTES=0; CANON_VER=""
if [ -r "$CANONICAL" ]; then
  cb=$(count_line "$CANONICAL" "$ROAR_B"); ce=$(count_line "$CANONICAL" "$ROAR_E")
  if [ "$cb" = 1 ] && [ "$ce" = 1 ] && [ "$(first_line_no "$CANONICAL" "$ROAR_B")" -lt "$(first_line_no "$CANONICAL" "$ROAR_E")" ]; then
    extract_block "$CANONICAL" "$ROAR_B" "$ROAR_E" > "$TMP/canon.block"
    CANON_OK=1; CANON_HASH=$(sha "$TMP/canon.block")
    CANON_LINES=$(wc -l < "$TMP/canon.block" | tr -d ' '); CANON_BYTES=$(wc -c < "$TMP/canon.block" | tr -d ' ')
    CANON_VER=$(block_version "$TMP/canon.block"); [ -n "$CANON_VER" ] || CANON_VER="?"
  fi
fi
if [ "$MODE" = verify ] && [ "$CANON_OK" != 1 ]; then die "cannot read a single well-formed canonical block from: $CANONICAL"; fi

# ---- discovery
: > "$TMP/files"; : > "$TMP/errors"; MISSING_ROOTS=""
prune=(); for x in $EXCLUDES; do prune+=( -name "$x" -prune -o ); done
names=(); first=1
for n in $FILE_NAMES; do if [ $first = 1 ]; then names+=( -name "$n" ); first=0; else names+=( -o -name "$n" ); fi; done
for root in "${ROOTS[@]}"; do
  if [ ! -d "$root" ]; then MISSING_ROOTS="$MISSING_ROOTS $root"; continue; fi
  # No -mindepth: find skips the -prune tests on entries shallower than -mindepth, so a node_modules/
  # at depth 1 would never be pruned. DIR/CLAUDE.md itself is a candidate on purpose — --root may
  # name a single project.
  find "$root" -maxdepth $((DEPTH + 1)) "${prune[@]}" -type f \( "${names[@]}" \) -print 2>> "$TMP/errors" >> "$TMP/files"
done
sort -u "$TMP/files" -o "$TMP/files"
NFILES=$(grep -c . "$TMP/files" 2>/dev/null || true)

# ---- classify every file → rows: status ⇥ version ⇥ hash ⇥ file ⇥ note
: > "$TMP/rows"; : > "$TMP/noblock"; : > "$TMP/projects_with_block"
while IFS= read -r f; do
  [ -n "$f" ] || continue
  if [ ! -r "$f" ]; then echo "unreadable file: $f" >> "$TMP/errors"; continue; fi
  rb=$(count_line "$f" "$ROAR_B"); re=$(count_line "$f" "$ROAR_E")
  lb=$(count_line "$f" "$RAR_B");  le=$(count_line "$f" "$RAR_E")
  status=""; hash="-"; note=""; ver="-"
  if [ "$rb" = 0 ] && [ "$re" = 0 ] && [ "$lb" = 0 ] && [ "$le" = 0 ]; then
    echo "$f" >> "$TMP/noblock"; continue
  fi
  if [ "$rb" != "$re" ] || [ "$lb" != "$le" ] || [ "$rb" -gt 1 ] || [ "$lb" -gt 1 ]; then
    status="MALFORMED"; note="markers ROAR begin=$rb end=$re · RAR begin=$lb end=$le"
  elif [ "$rb" = 1 ] && [ "$lb" = 1 ]; then
    status="MALFORMED"; note="both ROAR and legacy RAR blocks present"
  else
    if [ "$lb" = 1 ]; then kind=RAR; B="$RAR_B"; E="$RAR_E"; else kind=ROAR; B="$ROAR_B"; E="$ROAR_E"; fi
    bl=$(first_line_no "$f" "$B"); el=$(first_line_no "$f" "$E")
    if [ "$bl" -gt "$el" ]; then
      status="MALFORMED"; note="markers out of order (end at line $el, begin at line $bl)"
    else
      extract_block "$f" "$B" "$E" > "$TMP/blk"; hash=$(sha "$TMP/blk")
      ver=$(block_version "$TMP/blk"); [ -n "$ver" ] || ver="?"
      if [ "$kind" = RAR ]; then
        status="LEGACY"; note="legacy OWNER_RAR_PROTOCOL markers"
      elif [ "$MODE" = verify ]; then
        if [ "$hash" = "$CANON_HASH" ]; then status="OK"
        else status="DRIFT"; note="$(wc -l < "$TMP/blk" | tr -d ' ') lines / $(wc -c < "$TMP/blk" | tr -d ' ') bytes vs canonical $CANON_LINES / $CANON_BYTES"; fi
      else
        status="ROAR"
      fi
    fi
  fi
  if [ "$status" = MALFORMED ]; then
    fv=$(block_version "$f"); if [ -n "$fv" ]; then ver="$fv"; note="$note; version read from the whole file"; fi
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$status" "$ver" "$hash" "$f" "$note" >> "$TMP/rows"
  dirname "$f" >> "$TMP/projects_with_block"
done < "$TMP/files"

# ---- duplicates: one project directory with blocks in more than one file
sort "$TMP/projects_with_block" | uniq -d > "$TMP/dups"
NDUP=$(grep -c . "$TMP/dups" 2>/dev/null || true)

# ---- expected
: > "$TMP/expected_absent"
if [ -n "$EXPECTED" ]; then
  sort -u "$TMP/projects_with_block" > "$TMP/have"
  while IFS= read -r line; do
    line="${line%%#*}"; line="$(printf '%s' "$line" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s#/*$##')"
    [ -n "$line" ] || continue
    case "$line" in "~"*) line="$HOME${line#\~}" ;; esac
    if ! grep -q -x -F -- "$line" "$TMP/have"; then
      if [ -d "$line" ]; then echo "$line (directory exists, no block found)" >> "$TMP/expected_absent"
      else echo "$line (directory missing)" >> "$TMP/expected_absent"; fi
    fi
  done < "$EXPECTED"
fi
NEXP=$(grep -c . "$TMP/expected_absent" 2>/dev/null || true)

# ---- counts
cnt() { awk -F"$TAB" -v s="$1" '$1==s' "$TMP/rows" | grep -c . || true; }
NBLOCK=$(grep -c . "$TMP/rows" 2>/dev/null || true); NOK=$(cnt OK); NROAR=$(cnt ROAR); NDRIFT=$(cnt DRIFT)
NLEG=$(cnt LEGACY); NMAL=$(cnt MALFORMED); NNOB=$(grep -c . "$TMP/noblock" 2>/dev/null || true)
NERR=$(grep -c . "$TMP/errors" 2>/dev/null || true)

# ---- canonical cross-check: does the canonical agree with the installs?
CROSS=""
if [ "$CANON_OK" = 1 ]; then
  awk -F"$TAB" '$1=="OK"||$1=="ROAR"||$1=="DRIFT"{print $3}' "$TMP/rows" | sort | uniq -c | sort -rn > "$TMP/dist"
  if [ -s "$TMP/dist" ]; then
    top_n=$(head -1 "$TMP/dist" | awk '{print $1}'); top_h=$(head -1 "$TMP/dist" | awk '{print $2}')
    total=$(awk '{s+=$1} END{print s+0}' "$TMP/dist")
    if [ "$top_h" = "$CANON_HASH" ]; then CROSS="canonical matches the most common installed block ($top_n of $total)"
    else CROSS="canonical differs from the most common installed block ($top_n of $total share ${top_h:0:12}…): either a new version not yet propagated, or the canonical is what drifted (it has before — see claude-skills commit 3e080f8)"
    fi
  fi
fi

# ---- inventory digest (over the classified rows and the no-block list)
{ cut -f1-4 "$TMP/rows"; sed "s/^/NOBLOCK${TAB}-${TAB}-${TAB}/" "$TMP/noblock"; } | sort > "$TMP/inv"
DIGEST=$(sha "$TMP/inv")

# ---- report
NOW=$(date '+%Y-%m-%dT%H:%M:%S%z')
say "roar-install-check — $NOW — mode: $MODE"
say "Corpus"
say "  roots         :${ROOTS[*]/#/ }"
say "  missing roots :${MISSING_ROOTS:- (none)}"
say "  depth         : $DEPTH  (files in ROOT/ and down to ROOT/$(printf '*/%.0s' $(seq 1 "$DEPTH")))"
say "  file names    : $FILE_NAMES"
say "  excluded dirs : $EXCLUDES"
say "  files scanned : $NFILES   access errors: $NERR"
if [ "$CANON_OK" = 1 ]; then say "  canonical     : $CANONICAL"; say "                  block $CANON_VER · $CANON_LINES lines · $CANON_BYTES bytes · sha256 $CANON_HASH"
else say "  canonical     : (not read: $CANONICAL)"; fi
say "Installed blocks ($NBLOCK)"
if [ -s "$TMP/rows" ]; then
  sort -t"$TAB" -k1,1 -k4,4 "$TMP/rows" | while IFS="$TAB" read -r st ver h f note; do
    if [ -n "$note" ]; then say "  $(printf '%-9s %-4s %s   %s' "$st" "$ver" "$f" "$note")"
    else say "  $(printf '%-9s %-4s %s' "$st" "$ver" "$f")"; fi
  done
fi
if [ "$NDUP" -gt 0 ]; then
  say "Duplicates ($NDUP) — one project with blocks in more than one file"
  while IFS= read -r d; do say "  DUPLICATE  $d"; done < "$TMP/dups"
fi
say "No block ($NNOB) — discovered files without markers"
if [ "$QUIET" != 1 ] && [ -s "$TMP/noblock" ]; then sed 's/^/  /' "$TMP/noblock"; fi
if [ -n "$EXPECTED" ]; then
  say "Expected ($EXPECTED) — absent: $NEXP"
  if [ "$QUIET" != 1 ] && [ -s "$TMP/expected_absent" ]; then sed 's/^/  ABSENT     /' "$TMP/expected_absent"; fi
fi
if [ "$NERR" -gt 0 ]; then say "Access errors ($NERR)"; [ "$QUIET" = 1 ] || sed 's/^/  /' "$TMP/errors"; fi
[ -n "$CROSS" ] && say "Canonical cross-check" && say "  $CROSS"
echo "Summary"
if [ "$MODE" = verify ]; then
  echo "  blocks $NBLOCK · match canonical $NOK · drift $NDRIFT · legacy $NLEG · malformed $NMAL · duplicate projects $NDUP · expected-absent $NEXP · no-block files $NNOB · access errors $NERR"
else
  echo "  blocks $NBLOCK · ROAR $NROAR · legacy $NLEG · malformed $NMAL · duplicate projects $NDUP · expected-absent $NEXP · no-block files $NNOB · access errors $NERR"
fi
echo "  legacy OWNER_RAR_PROTOCOL blocks within this corpus: $NLEG"
echo "  inventory digest: sha256 $DIGEST"

# ---- exit: errors (2) dominate findings (1) dominate clean (0)
if [ "$NERR" -gt 0 ]; then echo "ERROR: $NERR access error(s) — the corpus is incomplete, the result is not a clean audit" >&2; exit 2; fi
if [ "$NFILES" -eq 0 ] && [ "$ALLOW_EMPTY" != 1 ]; then echo "ERROR: empty corpus — no candidate files under the scanned roots (pass --allow-empty if intended)" >&2; exit 2; fi
FINDINGS=$((NDRIFT + NLEG + NMAL + NDUP + NEXP))
[ "$FINDINGS" -eq 0 ] && exit 0 || exit 1
