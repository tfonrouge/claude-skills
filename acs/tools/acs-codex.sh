#!/bin/sh
#
# acs-codex.sh — launcher for the ACS advisory run.
#
# All logic lives in acs_codex.py (standard library only). This file exists for one reason: a
# Python script cannot report that Python is missing. Resolution order:
#   1. $ACS_PYTHON, used exclusively — if it is unusable this fails rather than falling back;
#   2. otherwise python3, then python3.13 … python3.8, taking the FIRST usable one, so an old
#      default python3 does not mask a newer python3.x.
# "Usable" means it runs and reports version >= 3.8.
#
# Exit 2 when no usable interpreter is found; otherwise the Python exit code (0 valid · 1 document
# or renderer validation failed · 2 preflight/usage · 3 Codex invocation failed).

set -u
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
IMPL="$HERE/acs_codex.py"

[ -f "$IMPL" ] || { echo "acs: implementation not found: $IMPL" >&2; exit 2; }

usable() {
  command -v "$1" >/dev/null 2>&1 || [ -x "$1" ] || return 1
  "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1
}

if [ -n "${ACS_PYTHON:-}" ]; then
  if usable "$ACS_PYTHON"; then
    exec "$ACS_PYTHON" "$IMPL" "$@"
  fi
  echo "acs: ACS_PYTHON is not a usable Python 3.8+ interpreter: $ACS_PYTHON" >&2
  exit 2
fi

for candidate in python3 python3.13 python3.12 python3.11 python3.10 python3.9 python3.8; do
  if usable "$candidate"; then
    exec "$candidate" "$IMPL" "$@"
  fi
done

echo "acs: no usable Python 3.8+ interpreter found (tried python3, python3.13 … python3.8)" >&2
echo "acs: set ACS_PYTHON to one, or install Python 3.8 or later." >&2
exit 2
