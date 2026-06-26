# Design decisions — claude-skills prompts

Records the reasoning behind non-obvious choices in the prompt artifacts, so settled questions are
not silently re-litigated. Each entry states the decision, why, the alternatives rejected, and the
only conditions under which it should be reopened (falsification-condition style — reopen on
evidence, not on a whim, and not "never").

## D1 — RAR findings stay out of durable audit/spec artifacts (AUDIT.md, LEDGER.md)

**Status:** decided 2026-06-26 · introduced in owner-rar-protocol v2

**Decision.** The RAR review loop (wrapped reviewer output + implementer triage) lives in chat only.
The implementer must not persist findings or the triage table to `AUDIT.md`, `LEDGER.md`, or any
blueprint/spec file. A finding is promoted to a durable record only at explicit Owner direction, and
only with fixed routing:

- drift between a blueprint/contract and the implementation → the project's audit record (`AUDIT.md`);
- a decision, or a deliberate rejection of a suggested change → the project's decision ledger (`LEDGER.md`).

Everything else lives in the commit message and chat.

**Why.**

- `AUDIT.md` / `LEDGER.md` are durable, signal-dense artifacts with a defined purpose (drift
  detection, principle alignment, the Decision Ledger with falsification conditions). The RAR loop
  is mostly ephemera.
- Of the five triage buckets, four (Rejected, Stale/already-fixed, Unclear, and routine Confirmed)
  have no durable value — the value of a Confirmed finding is the *fix*, which is already in git
  history, not the finding text.
- Provenance (who said it) is already carried by the `--- BEGIN/END RAR ---` wrapper, so a file
  channel was never needed for that purpose. Using a durable artifact as a transport buffer is a
  category error.
- The triage *bucket* is the wrong promotion discriminator. Audit-worthiness is: does it reveal
  drift (→ audit) or record a decision (→ ledger)? That is why promotion is gated on qualification
  plus Owner direction, not on "Confirmed".
- Deliberate rejections are the one ephemeral-looking case with real value (cathedral's *rejection
  amnesia*), but that value belongs in `LEDGER.md` as a decision, not as raw reviewer chatter in
  `AUDIT.md`.

**Alternatives rejected.**

- *Route all RAR findings into `AUDIT.md` as the transport channel* (an earlier suggestion in design
  discussion): pollutes a durable artifact with working-loop noise; rejected.
- *Say nothing — leave the protocol silent about persistence (v1 behavior):* relies on chance.
  Agents over-comply with file-writing cues and could drift toward logging triage into `AUDIT.md`.
  An explicit guard plus positive routing fixes both over-recording and under-recording; rejected.

**Reopen only if:** the project gains a concrete need to audit the *review process itself* (e.g. an
external compliance requirement to retain every reviewer finding and its disposition). Even then,
route to a dedicated review-log artifact — never to `AUDIT.md`/`LEDGER.md`, whose purpose is
unchanged.

## D2 — Install markers are version-less and stable

**Status:** decided 2026-06-26 · introduced in owner-rar-protocol v2

**Decision.** The install markers are `<!-- OWNER_RAR_PROTOCOL:begin -->` /
`<!-- OWNER_RAR_PROTOCOL:end -->` with no version suffix. The version is carried by the visible
`Protocol version: owner-rar-protocol vN` line inside the block.

**Why.** v1 put the version in the marker (`begin v1`). A v2 installer carrying `begin v2` would not
match the installed `begin v1` marker, so "replace in place" would fail and append a duplicate block.
A stable marker lets every future upgrade find-and-replace cleanly; the visible version line still
makes stale installs spottable by eye.

**Reopen only if:** multiple independent protocol blocks ever need to coexist in one file — then
namespacing by id (not version) would be the fix.
