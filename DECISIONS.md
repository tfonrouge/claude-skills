# Design decisions — claude-skills prompts

Records the reasoning behind non-obvious choices in the prompt artifacts, so settled questions are
not silently re-litigated. Each entry states the decision, why, the alternatives rejected, and the
only conditions under which it should be reopened (falsification-condition style — reopen on
evidence, not on a whim, and not "never").

## D1 — ROAR findings stay out of durable audit/spec artifacts (AUDIT.md, LEDGER.md)

**Status:** decided 2026-06-26 · introduced in owner-roar-protocol v2

**Decision.** The ROAR review loop (wrapped reviewer output + implementer triage) lives in chat only.
The implementer must not persist findings or the triage table to `AUDIT.md`, `LEDGER.md`, or any
blueprint/spec file. A finding is promoted to a durable record only at explicit Owner direction, and
only with fixed routing:

- drift between a blueprint/contract and the implementation → the project's audit record (`AUDIT.md`);
- a decision, or a deliberate rejection of a suggested change → the project's decision ledger (`LEDGER.md`).

Everything else lives in the commit message and chat.

**Why.**

- `AUDIT.md` / `LEDGER.md` are durable, signal-dense artifacts with a defined purpose (drift
  detection, principle alignment, the Decision Ledger with falsification conditions). The ROAR loop
  is mostly ephemera.
- Of the five triage buckets, four (Rejected, Stale/already-fixed, Unclear, and routine Confirmed)
  have no durable value — the value of a Confirmed finding is the *fix*, which is already in git
  history, not the finding text.
- Provenance (who said it) is already carried by the `--- BEGIN/END ROAR ---` wrapper, so a file
  channel was never needed for that purpose. Using a durable artifact as a transport buffer is a
  category error.
- The triage *bucket* is the wrong promotion discriminator. Audit-worthiness is: does it reveal
  drift (→ audit) or record a decision (→ ledger)? That is why promotion is gated on qualification
  plus Owner direction, not on "Confirmed".
- Deliberate rejections are the one ephemeral-looking case with real value (cathedral's *rejection
  amnesia*), but that value belongs in `LEDGER.md` as a decision, not as raw reviewer chatter in
  `AUDIT.md`.

**Alternatives rejected.**

- *Route all ROAR findings into `AUDIT.md` as the transport channel* (an earlier suggestion in design
  discussion): pollutes a durable artifact with working-loop noise; rejected.
- *Say nothing — leave the protocol silent about persistence (v1 behavior):* relies on chance.
  Agents over-comply with file-writing cues and could drift toward logging triage into `AUDIT.md`.
  An explicit guard plus positive routing fixes both over-recording and under-recording; rejected.

**Reopen only if:** the project gains a concrete need to audit the *review process itself* (e.g. an
external compliance requirement to retain every reviewer finding and its disposition). Even then,
route to a dedicated review-log artifact — never to `AUDIT.md`/`LEDGER.md`, whose purpose is
unchanged.

## D2 — Install markers are version-less and stable

**Status:** decided 2026-06-26 · introduced in owner-roar-protocol v2 · marker name updated in v3 (see D3)

**Decision.** The install markers are `<!-- OWNER_ROAR_PROTOCOL:begin -->` /
`<!-- OWNER_ROAR_PROTOCOL:end -->` with no version suffix. The version is carried by the visible
`Protocol version: owner-roar-protocol vN` line inside the block. (In v2 and earlier the markers
were `OWNER_RAR_PROTOCOL`; the v3 acronym rename changed the marker *name* once — see D3 — but the
version-less-stability principle is unchanged.)

**Why.** v1 put the version in the marker (`begin v1`). A v2 installer carrying `begin v2` would not
match the installed `begin v1` marker, so "replace in place" would fail and append a duplicate block.
A stable marker lets every future upgrade find-and-replace cleanly; the visible version line still
makes stale installs spottable by eye.

**Reopen only if:** multiple independent protocol blocks ever need to coexist in one file — then
namespacing by id (not version) would be the fix.

## D3 — Reviewer acronym is ROAR, not RAR

**Status:** decided 2026-07-03 · introduced in owner-roar-protocol v3

**Decision.** The reviewer role is named **ROAR** — **R**ead-**O**nly **A**dversarial **R**eviewer —
everywhere: prompt filenames (`owner-roar-protocol.prompt.md`, `roar-reviewer.prompt.md`), the
protocol slug (`owner-roar-protocol`), the wire wrapper (`--- BEGIN ROAR ---` / `--- END ROAR ---`),
the `@ROAR` authority tag, the triage header, and the install markers (`OWNER_ROAR_PROTOCOL`). The
prior acronym `RAR` is retired.

**Why.** `RAR` collides with unrelated acronyms that show up in AI/agent contexts (and with the
`.rar` archive format), creating ambiguity when the wrapper or tag is read out of context. `ROAR`
is unambiguous, still expands cleanly to the same role, and reads naturally as a review "roar."

**Migration.** The acronym is embedded in the install markers, so the rename breaks D2's
"stable marker" guarantee exactly once. The v3 installer handles it: it replaces a block delimited by
the new `OWNER_ROAR_PROTOCOL` markers *or* the legacy `OWNER_RAR_PROTOCOL` markers, in place,
leaving the file with the new markers. This is the sole sanctioned marker-name change; after v3 the
D2 stability guarantee resumes under the new name.

**Alternatives rejected.**

- *Keep `RAR` and disambiguate by context:* the wrapper and `@RAR` tag are specifically designed to
  be read out of context (that is the point of authority-not-identity), so context can't be relied on;
  rejected.
- *Change the acronym but keep the old markers to preserve D2:* the acronym *is* in the marker string,
  so this is impossible without leaving a visibly stale `RAR` name in every installed `CLAUDE.md`;
  rejected in favor of a one-time dual-matching migration.

**Reopen only if:** `ROAR` itself later proves to collide in a way that outweighs the churn of another
rename — reopen with the same dual-matching migration mechanism.

## D4 — The kickoff prompt and the installed block share one protocol version, bumped in lockstep

**Status:** decided 2026-07-05 · introduced in owner-roar-protocol v4

**Decision.** `roar-reviewer.prompt.md` (the reviewer kickoff) and `owner-roar-protocol.prompt.md`
(the installer and its installed block) carry a single shared `Protocol version: owner-roar-protocol
vN` line. A substantive change to *either* artifact bumps that version in *both*, even when the other
artifact's content is unchanged. v4 is the first case: only the kickoff gained a rule
(absence-verification), yet both version lines advance to v4.

**Why.**

- The two prompts are one protocol expressed in two places (detailed reviewer instructions in the
  kickoff; a compact restatement in the installed block). A change to reviewer behavior must be
  spottable from the version line wherever it is read.
- Letting the versions diverge (kickoff v4, block v3) reintroduces the exact "which v3?" ambiguity the
  version line exists to eliminate — the same failure class D2/D3 guard against.
- The cost of a no-content-change bump on the installed block is nil: re-pasting v4 replaces a v3
  block in place under the stable `OWNER_ROAR_PROTOCOL` markers (D2), producing a block byte-identical
  to v3 except for the version line.

**Alternatives rejected.**

- *Give the kickoff its own independent version:* doubles the version surface and creates a
  "which kickoff pairs with which block?" compatibility matrix for what is a single two-file protocol;
  rejected.
- *Leave the installed block at v3 since its content didn't change:* makes "v3" denote two different
  reviewer behaviors depending on which file you read — the drift the version guards against; rejected.

**Reopen only if:** the kickoff and installed block ever need independent compatibility (e.g. a kickoff
designed to work against several protocol-block versions) — then version them separately.

## D5 — The prompts ship as thin skill wrappers; the `.prompt.md` files stay the single source of truth

**Status:** decided 2026-07-05

**Decision.** `roar-reviewer` and `owner-roar-protocol` are each exposed as a Claude Code skill
(`roar-reviewer/SKILL.md`, `owner-roar-protocol/SKILL.md`). Each `SKILL.md` is a **thin wrapper**: it
carries only frontmatter (`name`, a packaging `version`, a manual-only `description`) and instructs the
agent to read and apply the canonical `.prompt.md` **bundled in the skill's own `references/`**. The
`.prompt.md` files remain the single source of behavioral truth — no protocol text is duplicated into a
`SKILL.md`. Each skill is thereby **self-contained**: the wrapper points at `./references/<prompt>` (not
at an external sibling), so the skill works even when its directory is installed on its own. Both skills
are **manual-invocation only**; their descriptions explicitly forbid auto-activation. The skill's
`metadata.version` is a **packaging** version (starts `0.1.0`), independent of the protocol behavior
version, which stays carried by the `.prompt.md`'s `Protocol version: owner-roar-protocol vN` line.

The prompts live *only* inside their skill's `references/` (they were previously root-level; moved here so
each skill is self-contained). They remain **paste-able**: open the file and copy it into any tool — the
tool-agnostic reviewer/installer text is unchanged.

**Why.**

- Skills add ergonomics (`/roar-reviewer`, `/owner-roar-protocol`) and, for owner-roar, encapsulate the
  marker-replace + legacy-migration logic — the part most error-prone to follow by hand.
- Duplicating prompt text into `SKILL.md` would fork content and invite exactly the version drift D2/D3/D4
  exist to prevent. A thin pointer keeps one source.
- The `.prompt.md` form stays tool-agnostic (paste-able into any chat or agent, e.g. running the reviewer
  in a *different* model for independent perspective); the skill form is Claude Code-specific. Bundling the
  prompt as the skill's `references/` source preserves that portability while keeping the skill
  self-contained.
- Manual-only is mandatory: owner-roar **edits CLAUDE.md** (the Owner gates that), and roar-reviewer flips
  the whole session into read-only reviewer mode — neither should fire on incidental keyword matches.
- Separating packaging version from protocol version avoids a third behavior-version surface and the
  "which combination is compatible?" matrix (the D4 concern): the wrapper has no behavior of its own to
  version.

**Alternatives rejected.**

- *Embed the full prompt text in `SKILL.md` (skill as source):* forks content, drift risk; and the
  paste-able artifact would then point back at a skill, which is awkward to paste; rejected.
- *Give the skill a behavior version tracking the protocol (e.g. `4.0.0`):* implies independent behavior
  the wrapper does not have, and re-creates a version matrix; rejected.
- *Auto-activating descriptions for discoverability:* unacceptable for a CLAUDE.md-editing skill and a
  session-role-flipping skill; rejected.

**Reopen only if:** a skill needs behavior the prompt can't express (then the skill gains real content and
its own behavior version), or the paste-able form proves to have no users (then collapse the prompt inline
into `SKILL.md` and drop `references/`).
