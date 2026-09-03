#!/usr/bin/env bash
#
# run-tests.sh — harness for ../roar-install-check.sh.
#
# Every fixture is GENERATED here from the canonical prompt at run time: no second copy of the
# protocol block is checked in (DECISIONS.md D5), so the harness cannot itself become a drift source.
# Development-only; install.sh excludes tools/tests from installs. Exit 0 iff every case passes.

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TOOL="$HERE/../roar-install-check.sh"
CANON="$HERE/../../references/owner-roar-protocol.prompt.md"
W="$(mktemp -d)"
trap 'chmod -R u+rwx "$W" 2>/dev/null; rm -rf "$W"' EXIT
PASS=0; FAIL=0

RB='<!-- OWNER_ROAR_PROTOCOL:begin -->'; RE='<!-- OWNER_ROAR_PROTOCOL:end -->'
BLOCK="$W/canonical.block"
awk -v b="$RB" -v e="$RE" '$0==b{p=1} p{print} $0==e{p=0}' "$CANON" > "$BLOCK"
[ -s "$BLOCK" ] || { echo "cannot extract the canonical block from $CANON" >&2; exit 2; }
VER=$(grep -m1 -o -E 'owner-roar-protocol v[0-9]+' "$BLOCK" | sed 's/.* //')
[ -n "$VER" ] || { echo "canonical block carries no version line" >&2; exit 2; }

# mk DIR VARIANT — writes DIR/CLAUDE.md (and AGENTS.md for 'dup') in the requested shape
mk() {
  mkdir -p "$1"
  case "$2" in
    ok)        { echo "# project"; echo; cat "$BLOCK"; echo; echo "prose quoting $RE mid-sentence must not truncate the block"; } > "$1/CLAUDE.md" ;;
    drift)     { echo "# project"; awk '{print} /^_Protocol version/ {print "an extra line inside the block"}' "$BLOCK"; } > "$1/CLAUDE.md" ;;
    legacy)    { echo "# project"; echo "<!-- OWNER_RAR_PROTOCOL:begin -->"; echo "## Session Roles Protocol — Owner vs. RAR"; echo; echo "_Protocol version: owner-rar-protocol v2._"; echo "body"; echo "<!-- OWNER_RAR_PROTOCOL:end -->"; } > "$1/CLAUDE.md" ;;
    inverted)  { echo "$RE"; echo "x"; echo "$RB"; echo "_Protocol version: owner-roar-protocol v8._"; } > "$1/CLAUDE.md" ;;
    truncated) { echo "$RB"; echo "_Protocol version: owner-roar-protocol v8._"; echo "no end marker"; } > "$1/CLAUDE.md" ;;
    fakever)   { echo "prose mentions owner-roar-protocol v99 before the block"; cat "$BLOCK"; } > "$1/CLAUDE.md" ;;
    fakever-noblock) echo "this file says owner-roar-protocol v99 but carries no markers" > "$1/CLAUDE.md" ;;
    none)      echo "# no protocol here" > "$1/CLAUDE.md" ;;
    dup)       cat "$BLOCK" > "$1/CLAUDE.md"; cp "$1/CLAUDE.md" "$1/AGENTS.md" ;;
    *) echo "unknown variant $2" >&2; exit 2 ;;
  esac
}

run() { OUT="$("$TOOL" "$@" 2>&1)"; RC=$?; }
# check NAME EXPECTED_RC [grep -E pattern that must match]... ; a pattern starting with '!' must NOT match
check() {
  local name="$1" want="$2"; shift 2; local ok=1 pat
  [ "$RC" = "$want" ] || { ok=0; echo "  expected exit $want, got $RC"; }
  for pat in "$@"; do
    case "$pat" in
      '!'*) if printf '%s\n' "$OUT" | grep -q -E -- "${pat#!}"; then ok=0; echo "  must not match: ${pat#!}"; fi ;;
      *)    if ! printf '%s\n' "$OUT" | grep -q -E -- "$pat"; then ok=0; echo "  missing: $pat"; fi ;;
    esac
  done
  if [ $ok = 1 ]; then PASS=$((PASS+1)); echo "PASS  $name"; else FAIL=$((FAIL+1)); echo "FAIL  $name"; printf '%s\n' "$OUT" | sed 's/^/      | /'; fi
}

# ---- corpora
CLEAN="$W/clean"; mk "$CLEAN/projOK" ok; mk "$CLEAN/group/projNested" ok; mk "$CLEAN/node_modules/projSkip" ok
MIXED="$W/mixed"; mk "$MIXED/projOK" ok; mk "$MIXED/projDRIFT" drift; mk "$MIXED/projLEGACY" legacy; mk "$MIXED/projDUP" dup
mk "$MIXED/projINV" inverted; mk "$MIXED/projTRUNC" truncated; mk "$MIXED/projFAKE" fakever; mk "$MIXED/projFAKENB" fakever-noblock; mk "$MIXED/projNONE" none
SPACES="$W/sp"; mk "$SPACES/my proj" ok
EMPTY="$W/empty"; mkdir -p "$EMPTY/nothing-here"
printf '%s\n' "# expected" "$MIXED/projOK" "$MIXED/projNONE" "$MIXED/projZ   # does not exist" > "$W/expected.txt"
ALTCANON="$W/alt-canonical.prompt.md"; awk '{print} /^_Protocol version/ {print "canonical-only line"}' "$CANON" > "$ALTCANON"

# ---- cases
run --verify --root "$CLEAN";                                   check "clean corpus verifies with exit 0" 0 "match canonical 2" "OK +$VER +.*projNested" '!projSkip' "exit|digest"
run --check --root "$CLEAN";                                    check "check mode counts ROAR blocks" 0 "ROAR 2" '!DRIFT'
run --verify --root "$MIXED";                                   check "drift is reported" 1 "DRIFT +$VER +.*projDRIFT" "lines / .* bytes vs canonical" "drift 1"
                                                                check "legacy v2 is reported from its block" 1 "LEGACY +v2 +.*projLEGACY" "legacy OWNER_RAR_PROTOCOL blocks within this corpus: 1"
                                                                check "duplicate CLAUDE.md+AGENTS.md is reported" 1 "DUPLICATE +.*projDUP" "duplicate projects 1"
                                                                check "inverted markers are malformed" 1 "MALFORMED +v8 +.*projINV.*out of order"
                                                                check "truncated block is malformed" 1 "MALFORMED +v8 +.*projTRUNC.*begin=1 end=0"
                                                                check "version comes from the block, not the file" 1 "OK +$VER +.*projFAKE/" '!v99'
                                                                check "file with a fake version but no markers is a no-block file" 1 "no-block files 2" "projFAKENB"
                                                                check "malformed count" 1 "malformed 2"
run --verify --root "$MIXED" --expected "$W/expected.txt";      check "expected-but-absent, both kinds" 1 "ABSENT +.*projNONE \(directory exists, no block found\)" "ABSENT +.*projZ \(directory missing\)" "expected-absent 2"
run --verify --root "$W/does-not-exist";                        check "explicit missing root is an error" 2 "does not exist"
run --verify --root "$EMPTY";                                   check "empty corpus is an error" 2 "empty corpus"
run --verify --root "$EMPTY" --allow-empty;                     check "empty corpus allowed on request" 0 "files scanned : 0"
run --verify --root "$CLEAN/projOK";                            check "a project directory works as --root" 0 "match canonical 1" "OK +$VER +.*projOK/CLAUDE.md"
run --verify --root "$SPACES";                                  check "paths with spaces" 0 "match canonical 1" "my proj/CLAUDE.md"
run --verify --root "$CLEAN" --canonical "$ALTCANON";           check "canonical disagreeing with installs is flagged" 1 "canonical differs from the most common installed block" "drift 2"
run --verify --root "$CLEAN" --canonical "$W/nope.md";          check "unreadable canonical is an error" 2 "canonical"
run --depth x;                                                  check "bad --depth is a usage error" 2 "integer"
run --bogus;                                                    check "unknown argument is a usage error" 2 "unknown arg"
run --verify --root "$CLEAN" --expected "$W/no-such-list";      check "unreadable --expected is an error" 2 "expected"
run --verify --root "$CLEAN" --quiet;                           check "quiet prints the summary only" 0 "^Summary" '!^Corpus'
run --verify --root "$CLEAN"; D1=$(printf '%s\n' "$OUT" | grep 'inventory digest'); run --verify --root "$CLEAN"; D2=$(printf '%s\n' "$OUT" | grep 'inventory digest')
[ -n "$D1" ] && [ "$D1" = "$D2" ] && { PASS=$((PASS+1)); echo "PASS  inventory digest is deterministic"; } || { FAIL=$((FAIL+1)); echo "FAIL  inventory digest is deterministic"; echo "      | $D1"; echo "      | $D2"; }


# ---- receiver mode: exactly one named file, no corpus, no recursion (0.1.3)
CAP="Protocol capabilities: advisory-v1"
mkrecv() {  # mkrecv FILE VARIANT
  mkdir -p "$(dirname "$1")"
  case "$2" in
    ok)         { echo "$RB"; echo "_Protocol version: owner-roar-protocol v9._"; echo "$CAP"; echo "body"; echo "$RE"; } > "$1" ;;
    multi)      { echo "$RB"; echo "_Protocol version: owner-roar-protocol v9._"; echo "Protocol capabilities: advisory-v1 future-v2"; echo "$RE"; } > "$1" ;;
    nocap)      { echo "$RB"; echo "_Protocol version: owner-roar-protocol v9._"; echo "$RE"; } > "$1" ;;
    twocap)     { echo "$RB"; echo "$CAP"; echo "$CAP"; echo "$RE"; } > "$1" ;;
    capoutside) { echo "$CAP"; echo "$RB"; echo "_Protocol version: owner-roar-protocol v9._"; echo "$RE"; } > "$1" ;;
    othercap)   { echo "$RB"; echo "Protocol capabilities: something-else"; echo "$RE"; } > "$1" ;;
    noblock)    echo "# nothing here" > "$1" ;;
    legacy)     { echo "<!-- OWNER_RAR_PROTOCOL:begin -->"; echo "old"; echo "<!-- OWNER_RAR_PROTOCOL:end -->"; } > "$1" ;;
    orphanend)  { echo "<!-- OWNER_RAR_PROTOCOL:end -->"; echo "$RB"; echo "$CAP"; echo "$RE"; } > "$1" ;;
    orphanbegin){ echo "<!-- OWNER_RAR_PROTOCOL:begin -->"; echo "$RB"; echo "$CAP"; echo "$RE"; } > "$1" ;;
    inverted)   { echo "$RE"; echo "x"; echo "$RB"; echo "$CAP"; } > "$1" ;;
    truncated)  { echo "$RB"; echo "$CAP"; echo "no end"; } > "$1" ;;
    dupblock)   { echo "$RB"; echo "$CAP"; echo "$RE"; echo "$RB"; echo "$CAP"; echo "$RE"; } > "$1" ;;
  esac
}
R="$W/recv"
for v in ok multi nocap twocap capoutside othercap noblock legacy orphanend orphanbegin inverted truncated dupblock; do mkrecv "$R/$v/CLAUDE.md" "$v"; done

run --receiver "$R/ok/CLAUDE.md" --require-capability advisory-v1
check "receiver: capability declared" 0 "receiver: OK" "capability advisory-v1 declared" "block v9"
run --receiver "$R/multi/CLAUDE.md" --require-capability advisory-v1
check "receiver: capability among several" 0 "receiver: OK"
run --receiver "$R/ok/CLAUDE.md"
check "receiver: no capability required" 0 "receiver: OK"
run --receiver "$R/nocap/CLAUDE.md" --require-capability advisory-v1
check "receiver: no capability line" 1 "no 'Protocol capabilities:' line"
run --receiver "$R/twocap/CLAUDE.md" --require-capability advisory-v1
check "receiver: two capability lines" 1 "exactly one is required"
run --receiver "$R/capoutside/CLAUDE.md" --require-capability advisory-v1
check "receiver: capability outside the block" 1 "no 'Protocol capabilities:' line"
run --receiver "$R/othercap/CLAUDE.md" --require-capability advisory-v1
check "receiver: different capability token" 1 "not declared"
run --receiver "$R/noblock/CLAUDE.md" --require-capability advisory-v1
check "receiver: file without a block" 1 "no OWNER_ROAR_PROTOCOL block"
run --receiver "$R/legacy/CLAUDE.md" --require-capability advisory-v1
check "receiver: legacy block" 1 "legacy OWNER_RAR_PROTOCOL marker present"
run --receiver "$R/orphanend/CLAUDE.md" --require-capability advisory-v1
check "receiver: orphan legacy end marker" 1 "legacy OWNER_RAR_PROTOCOL marker present"
run --receiver "$R/orphanbegin/CLAUDE.md" --require-capability advisory-v1
check "receiver: orphan legacy begin marker" 1 "legacy OWNER_RAR_PROTOCOL marker present"
run --receiver "$R/inverted/CLAUDE.md" --require-capability advisory-v1
check "receiver: inverted markers" 1 "out of order"
run --receiver "$R/truncated/CLAUDE.md" --require-capability advisory-v1
check "receiver: truncated block" 1 "not well formed"
run --receiver "$R/dupblock/CLAUDE.md" --require-capability advisory-v1
check "receiver: duplicated block" 1 "not well formed"
run --receiver "$R/missing/CLAUDE.md" --require-capability advisory-v1
check "receiver: file does not exist" 1 "file does not exist"
run --receiver "relative/CLAUDE.md" --require-capability advisory-v1
check "receiver: relative path refused" 2 "absolute path"
run --receiver "$R/ok/CLAUDE.md" --check
check "receiver: corpus option refused" 2 "cannot be combined"
run --receiver "$R/ok/CLAUDE.md" --root "$R"
check "receiver: --root refused" 2 "cannot be combined"
run --require-capability advisory-v1 --check --root "$CLEAN"
check "capability without receiver refused" 2 "only valid with --receiver"
mkrecv "$R/nested-root/CLAUDE.md" noblock; mkrecv "$R/nested-root/sub/CLAUDE.md" ok
run --receiver "$R/nested-root/CLAUDE.md" --require-capability advisory-v1
check "receiver: a nested file cannot satisfy the root" 1 "no OWNER_ROAR_PROTOCOL block"
run --receiver "$R/ok/CLAUDE.md" --require-capability "advisory-v1 --root /etc"
check "receiver: capability token must be a single token" 2 "single token matching"
run --receiver "$R/ok/CLAUDE.md" --require-capability "bad token!"
check "receiver: capability token rejects punctuation" 2 "single token matching"
run --receiver "$R/ok/CLAUDE.md" --require-capability advisory-v1 --canonical /nonexistent
check "receiver: --canonical refused rather than ignored" 2 "no effect in receiver mode"
mkrecv "$R/spaced dir/CLAUDE.md" ok
run --receiver "$R/spaced dir/CLAUDE.md" --require-capability advisory-v1
check "receiver: path with spaces" 0 "receiver: OK"

if [ "$(id -u)" = 0 ]; then
  echo "SKIP  access error (running as root, permissions are not enforced)"
else
  LOCKED="$W/locked"; mk "$LOCKED/open/projOK" ok; mk "$LOCKED/closed/projHidden" ok; chmod 000 "$LOCKED/closed"
  run --verify --root "$LOCKED"; chmod u+rwx "$LOCKED/closed"
  check "access error is exit 2 and reported" 2 "access errors: [1-9]" "Access errors" "corpus is incomplete"
fi

echo; echo "passed $PASS, failed $FAIL"
[ "$FAIL" -eq 0 ]
