---
name: owner-roar-protocol
metadata:
  version: 0.1.0
description: >
  Installs or upgrades the Owner/ROAR Session Roles Protocol block in a project's
  CLAUDE.md (or AGENTS.md / equivalent), delimited by the stable `OWNER_ROAR_PROTOCOL`
  markers — handling in-place replacement and the one-time legacy `OWNER_RAR_PROTOCOL`
  marker migration. Leaves the diff for the Owner; does NOT commit.

  MANUAL INVOCATION ONLY — do NOT auto-activate. This skill EDITS CLAUDE.md, and the
  Owner controls when the protocol is installed or upgraded. Invoke only when the user
  explicitly runs `/owner-roar-protocol`, or explicitly asks to install / upgrade the
  Owner-ROAR (Owner/ROAR) protocol in this project. Never trigger implicitly.
---

# Owner/ROAR Protocol installer (skill wrapper)

This skill is a **thin wrapper** over the canonical, paste-able installer prompt bundled
with this skill — `references/owner-roar-protocol.prompt.md` — so the skill is
self-contained and the two forms can never drift (see `DECISIONS.md` D5).

When invoked:

1. **Read** the canonical installer prompt bundled with this skill:
   `./references/owner-roar-protocol.prompt.md`.
2. **Follow it exactly.** Add or replace the marker-delimited protocol block in the project's
   persistent agent-instructions file per its rules: in-place replacement of an existing
   `OWNER_ROAR_PROTOCOL` block; one-time migration of a legacy `OWNER_RAR_PROTOCOL` block;
   otherwise insert as a top-level section.
3. Copy the block **verbatim** between the markers. Change nothing else.
4. **Do not commit** — leave the diff for the Owner to review.

The **protocol version** installed is carried by that prompt (currently **owner-roar-protocol
v4**); this skill's packaging `version` is independent (see `DECISIONS.md` D5).
