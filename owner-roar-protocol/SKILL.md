---
name: owner-roar-protocol
metadata:
  version: 0.1.3
description: >
  Installs or upgrades the Owner/ROAR Session Roles Protocol block in a project's
  CLAUDE.md (or AGENTS.md / equivalent), delimited by the stable `OWNER_ROAR_PROTOCOL`
  markers — handling in-place replacement and the one-time legacy `OWNER_RAR_PROTOCOL`
  marker migration. Leaves the diff for the Owner; does NOT commit. Invoked with `--check`
  or `--verify` it installs NOTHING: it only runs the bundled audit of the blocks already
  installed across projects, which modifies neither protocol files nor the audited projects.

  MANUAL INVOCATION ONLY — do NOT auto-activate. This skill EDITS CLAUDE.md, and the
  Owner controls when the protocol is installed or upgraded. Invoke only when the user
  explicitly runs `/owner-roar-protocol`, explicitly asks to install / upgrade the
  Owner-ROAR (Owner/ROAR) protocol in this project, or explicitly asks to audit / verify
  its installed copies. Never trigger implicitly.
---

# Owner/ROAR Protocol installer (skill wrapper)

This skill has two modes, and the route is decided **before anything else is read**:

- **Audit mode** — the invocation carries `--check` or `--verify`, or the Owner asks in plain
  words to audit or inventory (→ `--check`) or to verify or compare (→ `--verify`) the blocks
  *already installed*, rather than to install or upgrade one. Run `tools/roar-install-check.sh`
  **resolved from this skill's own directory** (the directory holding this `SKILL.md`), never
  from the current working directory. Forward **only recognized CLI options** — `--check`,
  `--verify`, `--root DIR`, `--depth N`, `--expected FILE`, `--canonical FILE`, `--allow-empty`,
  `--quiet`; anything unrecognized or ambiguous is asked about, never invented or forwarded. Print
  the script's output and report its exit code (`0` clean · `1` findings · `2` error); then stop.
  In audit mode do **not** read the installer prompt, do not apply it, and do not edit protocol
  files, project files, or audited targets.
  The script modifies neither protocol files nor the audited projects; it only uses a temporary
  directory that it removes on exit. See "Install audit" below.
- **Install mode** — everything else. Here the skill is a **thin wrapper** over the canonical,
  paste-able installer prompt bundled with it — `references/owner-roar-protocol.prompt.md` — so
  the skill is self-contained and the two forms can never drift (see `DECISIONS.md` D5):

  1. **Read** the canonical installer prompt bundled with this skill:
     `./references/owner-roar-protocol.prompt.md`.
  2. **Follow it exactly.** Add or replace the marker-delimited protocol block in the project's
     persistent agent-instructions file per its rules: in-place replacement of an existing
     `OWNER_ROAR_PROTOCOL` block; one-time migration of a legacy `OWNER_RAR_PROTOCOL` block;
     otherwise insert as a top-level section.
  3. Copy the block **verbatim** between the markers. Change nothing else.
  4. **Do not commit** — leave the diff for the Owner to review.

The **protocol version** installed is whatever the bundled prompt's `Protocol version:` line says
— read it there, never from here. This skill's packaging `version` is independent (see
`DECISIONS.md` D5). *This paragraph deliberately does not name the version: a copied version
number is a third place to maintain, and it drifted twice before being removed.*

## Install audit (`tools/roar-install-check.sh`)

A read-only companion script shipped with this skill. It inventories where the block is installed
and whether each copy matches the canonical prompt. It modifies neither protocol files nor the
audited projects; it only uses a temporary directory that it removes on exit.

- `--check` — discover projects under the given roots (a collection of projects, or a single
  project directory) and report, per `CLAUDE.md` / `AGENTS.md`: marker kind
  (`OWNER_ROAR_PROTOCOL`, legacy `OWNER_RAR_PROTOCOL`, none, malformed — including markers out of
  order), the `Protocol version` line read from the extracted block, and blocks duplicated across
  both files of one project.
- `--verify` — additionally extract each block and compare it byte for byte with the canonical
  block in `references/owner-roar-protocol.prompt.md`, reporting drift — and reporting when the
  canonical itself disagrees with most installs, because the canonical has drifted before.

- `--receiver FILE` — a different question: not "what is installed across projects?" but "is *this
  exact file* a valid receiver?". It examines only the named absolute path, with no discovery and
  no recursion, and requires exactly one well-formed block; with `--require-capability TOKEN` it
  also requires exactly one `Protocol capabilities:` line **inside** that block carrying the token.
  Exit `0` when all of that holds, `1` when the file exists but fails a requirement, `2` for usage
  or an unreadable file. It cannot be combined with the corpus options. The `acs` skill uses this
  mode as its receiver guard, so the marker rules have one implementation rather than two.

It prints its corpus (roots, exclusions, depth, files scanned, access errors), accepts an
`--expected` list of project directories so an absent install is reported rather than silently
missed, and ends with an inventory digest. An explicitly named root that does not exist, an access
error, or an empty corpus is exit `2`, never a clean result. "Zero legacy blocks" always means zero
within the printed corpus, never zero on the machine.

`tools/tests/run-tests.sh` exercises the script; its fixtures are generated from the canonical
prompt at run time, so no second copy of the block is checked in. `install.sh` excludes
`tools/tests` from installs. Run the tests after touching the script.
