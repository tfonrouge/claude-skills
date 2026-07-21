#!/usr/bin/env bash
#
# install.sh — sync this repo's skills into the Claude Code user skills dir.
#
# This repo is the single source of truth (see DECISIONS.md D6). The copies under
# ~/.claude/skills are a DOWNSTREAM install target — this script overwrites them
# from the repo, never the other way around.
#
# Usage:
#   ./install.sh            # copy skills into ~/.claude/skills (default)
#   ./install.sh --link     # symlink instead of copy (edits in repo take effect live)
#   ./install.sh --dry-run  # show what would happen, change nothing
#   DEST=/some/dir ./install.sh   # override the destination

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
DEST="${DEST:-$HOME/.claude/skills}"

# Skill directories to install: every top-level dir containing a SKILL.md.
SKILLS=()
for d in "$REPO_DIR"/*/; do
  [ -f "${d}SKILL.md" ] && SKILLS+=("$(basename "$d")")
done

MODE="copy"
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --link)    MODE="link" ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

# Resolve a path to a canonical absolute form even when it does not exist yet
# (equivalent to `realpath -m`): absolutize against the physical CWD, then collapse
# '.' and '..' segments lexically. Needed so the self-install guard below cannot be
# bypassed with a non-existent intermediate such as `foo/..` — where `cd` fails, but
# `mkdir -p` would later materialize the intermediate and make `rm -rf` hit the source.
resolve_path() {
  local input="$1" abs result="" seg oldIFS="$IFS"
  case "$input" in
    /*) abs="$input" ;;
    *)  abs="$(pwd -P)/$input" ;;
  esac
  IFS='/'; set -f            # split on '/', disable globbing of segments
  for seg in $abs; do
    case "$seg" in
      ''|.) ;;               # skip empty and current-dir segments
      ..)  result="${result%/*}" ;;   # pop the last segment
      *)   result="$result/$seg" ;;
    esac
  done
  set +f; IFS="$oldIFS"
  printf '%s' "${result:-/}"
}

# Safety: refuse to install onto the repo itself. If DEST resolves to REPO_DIR,
# each dst ("$DEST/$s") equals its src ("$REPO_DIR/$s"), so `rm -rf "$dst"` would
# delete the source skill dir before `cp -R` could read it. Resolve physically when
# DEST exists (symlink-safe), else lexically (handles non-existent `..` paths).
# Guard runs before mkdir and before the loop, so it fires in --dry-run too.
DEST_REAL="$(cd "$DEST" 2>/dev/null && pwd -P || true)"   # '|| true' so a failed cd doesn't trip set -e
[ -n "$DEST_REAL" ] || DEST_REAL="$(resolve_path "$DEST")"
if [ "$DEST_REAL" = "$REPO_DIR" ]; then
  echo "ERROR: DEST resolves to the repository itself:" >&2
  echo "         $REPO_DIR" >&2
  echo "  Installing here would delete the source skill directories. Set DEST elsewhere." >&2
  exit 3
fi

echo "Source : $REPO_DIR"
echo "Dest   : $DEST"
echo "Mode   : $MODE$([ "$DRY_RUN" = 1 ] && echo ' (dry-run)')"
echo "Skills : ${SKILLS[*]}"
echo

run() { if [ "$DRY_RUN" = 1 ]; then echo "  + $*"; else "$@"; fi; }

[ "$DRY_RUN" = 1 ] || mkdir -p "$DEST"

for s in "${SKILLS[@]}"; do
  src="$REPO_DIR/$s"
  dst="$DEST/$s"
  echo "→ $s"
  run rm -rf "$dst"
  if [ "$MODE" = "link" ]; then
    run ln -s "$src" "$dst"
  else
    run cp -R "$src" "$dst"
  fi
done

echo
echo "Done. ${#SKILLS[@]} skill(s) $([ "$MODE" = link ] && echo linked || echo copied) into $DEST."
