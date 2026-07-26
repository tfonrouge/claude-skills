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

## D6 — The blueprint-workflow skills live in this repo, alongside their cathedral adapters

**Status:** decided 2026-07-21 · reverses the eviction in `2c7c792`

**Decision.** `business-blueprint-workflow` and `systems-blueprint-workflow` are tracked **in this
repo**, next to `cathedral-premise`. This repo is their **single source of truth**; the copies under
`~/.claude/skills/` are a downstream install target, kept in sync by `install.sh` — never the master.

**Why.**

- **`cathedral-premise` has a hard reference to them.** Its `SKILL.md` routes on a `Blueprint skill`
  config, and `cathedral-{systems,business}.md` are explicitly *"audit checks for projects using
  `<...>-blueprint-workflow`."* The governor and the producer it audits belong in one repo; a repo
  that ships the auditor but not the audited leaves a dangling reference.
- **The eviction inverted the source of truth and caused exactly the drift this ledger exists to
  prevent.** `2c7c792` ("Restructure repo: consolidate into cathedral-premise skill") deleted both
  skills, leaving the only live copies under version-control-free `~/.claude/skills/`. They then
  drifted ahead of git: `business` `0.8.0`→`0.8.1`, and `systems` changed its `description` **without
  a version bump** — two different `0.2.0`s, the same "which vN?" failure D2/D4 guard against.
- **Restore used the installed copies, not git history**, because those were newest and were what was
  actually running. The systems silent-drift was reconciled with a `0.2.1` bump (see `CHANGELOG.md`).

**Alternatives rejected.**

- *Keep them only in `~/.claude/skills/`:* not version-controlled, invisible to review, and the proven
  cause of the drift above; rejected.
- *Restore the older git-history versions:* would discard the improvements made while installed
  (business's bridge north-stars scan, systems's description rework); rejected.
- *Publish them as a separate repo:* defensible if they ever grow independent consumers, but today
  their only governor lives here, so co-location is simpler and keeps the audit reference local.

**Reopen only if:** the blueprint skills acquire consumers or a release cadence independent of
`cathedral-premise` — then split them into their own repo and depend on it explicitly (versioned),
rather than relying on co-location.

## D7 — Mode is resolved by reconciliation: BRIEF `Mode` > unambiguous suffix > INDEX declaration; libraries get `(LIBRARY)`

**Status:** decided 2026-07-22 · introduced in business-blueprint-workflow v0.9.0 / cathedral-premise v1.2.0

**Decision.** Business LIBRARY blueprints use a `(LIBRARY)` directory suffix (previously shared
`(MODULE)` with modules). A blueprint's mode is resolved from three sources with fixed precedence —
BRIEF `Mode` header row > *unambiguous* directory suffix > INDEX declaration (Mode column, or the
skill's explicit section→mode map: *Active Bridges* ⇒ BRIDGE) — with legacy `(MODULE)` treated as
ambiguous (never a declaration) during the compatibility period. Catalog validation precedes
reconciliation: out-of-catalog values (e.g. `(FEATURE)` in a business project) never classify and
never borrow another skill's contract; they produce an unclassified-blueprint finding. INDEX
sections outside the section→mode map (Deferred, Deprecated, tiers) declare nothing. The required
BRIEF `Mode` row is enforced only by the authoring Step 0/B0 DoD gate; audits treat its absence as
a low-severity recommendation, never a violation (no cutoff metadata exists to date legacy BRIEFs).

**Why.**

- MODULE and LIBRARY sharing `(MODULE)` made the one genuine legacy library
  (`MarketPlazeLib(MODULE)`) distinguishable only by its INDEX row; fresh BRIEF-only blueprints
  had no discriminator at all. drydock (~45 blueprints) proves suffix-as-mode empirically.
- Precedence rationale: *in-directory beats aggregate; explicit beats conventional* — mirrors the
  existing `.blueprint-status`-over-INDEX authority pattern. Empirically, INDEX lags (mppArel's
  INDEX self-reported a stale skill version).
- Real `(FEATURE)` dirs in marketPlazeLib match neither the systems FEATURE contract nor each
  other — tolerating foreign suffixes without a contract would silently under-audit.

**Alternatives rejected.**

- **Extend `.blueprint-status` with a `MODE:` line** — breaks the documented one-line contract with
  ~75 conforming files in the wild and exact/prefix-content consumers.
- **INDEX Mode column as sole authority** — leaves fresh unregistered blueprints unclassifiable and
  inverts the per-directory-file-is-authoritative principle.
- **Strict suffix-first short-circuit** — misclassifies the legacy library the compatibility rule
  exists to protect.
- **Date-based grandfather cutoff for the BRIEF `Mode` row** — undecidable: legacy BRIEFs carry no
  creation date, marketPlazeLib's INDEX no skill-version header, this repo's CHANGELOG no dates.

**Reopen when.** A business project legitimately needs a mode outside
MODULE/LIBRARY/BRIDGE (e.g. persistent demand for FEATURE — deliberately *not* adopted now, left
as an audit-flagged foreign mode per Owner decision 2026-07-22); or the compatibility period ends
(no `(MODULE)`-as-LIBRARY blueprints remain anywhere), at which point `(MODULE)` becomes
unambiguous and the reconciliation collapses to suffix-first.

---

## D8 — v5 protocol additions are evidence-derived; recall stays uninstrumented and out-of-scope findings reuse the ledger

**Status:** decided 2026-07-24 · introduced in owner-roar-protocol v5 · amended pre-landing
2026-07-24 after adversarial review of the v5 draft itself (see *Corrected before landing*)

**Decision.** v5 adds seven rules to the Owner/ROAR protocol — revision stamp, landing-impact
classification, class-findings-over-instances, a scoped `REVIEW COMPLETE` terminal state, named
audit axes for new harnesses, a constraint-convergence check for design threads, and a **mandatory
implementer preflight**. Each traces to an observed failure in a 13-round review session on a live
project (Drydock DDvm L21); nothing was added speculatively. Two boundaries are decided with them:
a finding confirmed **out of scope** is promoted through the **existing** durable-record mechanism
(a `LEDGER.md` entry or a spawned task, at Owner direction) and never a parallel findings list; and
**recall stays
uninstrumented** — no escape-tracking or seeded-defect machinery ships in the protocol block.

**Why.**

- The session gave measured cost/benefit: the protocol caught a harness deleting files it did not
  create, a "manifest coverage" row that built artifacts and observed nothing, a cross-process
  correlation, and four design proposals each routing around a standing Owner constraint. It also
  spent most rounds rediscovering the *same class* of defect one axis at a time — class findings
  and the preflight target exactly that waste, and would have collapsed ~4–5 of 13 rounds.
- The block rides in **every** session's context in every project that installs it, so growth is a
  permanent per-session cost. Each rule had to earn its place in the wire format specifically;
  items that are practice rather than protocol were routed elsewhere (below).
- Severity and landing impact are different axes. A LOW-severity wording defect that is
  nonetheless a *false operational claim* misleads the next diagnosis — hence the Blocking clause
  reads "changes implementation **or diagnostic** decisions."
- Reviewer silence was becoming implicit approval. A terminal state fixes that only if it is
  scoped: it names the reviewed diff and stated scope, and never authorizes commit or push
  (D1's no-commit-authority rule is unchanged).

**Corrected before landing.** The v5 draft was reviewed under v5's own rules across successive
adversarial rounds. Everything recorded here was confirmed and fixed **while v5 was still an
uncommitted draft** — none of it ever reached a released protocol version. ("Landed" below means
applied to that draft, never released.) This section records the defect *classes* and their final
mechanisms, deliberately **not** a running tally: an exhaustive count is invalidated by every
further round, and three separate record-fidelity failures below were caused by exactly that.
CHANGELOG carries the full per-rule sequence. The
stamp took **two** rounds, recorded separately rather than compressed, because the second round
refuted the first round's fix:

- **The revision stamp did not identify content (round 1).** The draft allowed
  `working-tree @ <ISO-time>`, which records *time*, not *bytes* — it cannot reconstruct or
  compare what was reviewed, so it could falsely certify a finding as current and defeat the very
  stale-review failure the stamp exists to close. Replaced with a content identity built on
  `git stash create` (non-destructive, later inspectable).
- **That stash-only stamp did not cover every cited location (round 2), so it too was rejected.**
  `git stash create` silently omits untracked files, and in a tree whose *only* changes are
  untracked it returns **empty** (verified by experiment) — leaving the stamp covering nothing
  under review. Naming and quoting the untracked file was considered and refused: quoted lines
  belong to no object, so nothing is comparable. Final wire format is
  `<commit-hash>[ + worktree <object-hash>][ + untracked <path>@<blob-hash> …]`, untracked blobs
  from `git hash-object` — read-only (no `-w`; verified to write nothing, remain stable, and
  detect mutation) — under the explicit invariant that **every cited location must be covered by
  some component of the stamp, or must not be cited**. Multi-repository reviews stamp each
  repository on its own line.
- **Asserted absences were not bound to the stamp.** The stamp covered *cited* locations, but an
  absence finding cites none — so the corpus behind an empty result was unidentifiable and the
  result irreproducible. Fixed in the kickoff prompt (where the absence rule has lived since v4)
  by sanctioning only corpora the stamp covers: `git grep <pattern> <object-hash>` against the
  stamped object, or `git grep` over the worktree (tracked content only — exactly what the commit
  and worktree components cover), or an untracked-walking tool **only** if every untracked file in
  the searched scope is hashed. A further round found that *pathname* claims escape content
  hashing entirely — an empty untracked directory has no blob and appears in no Git tree, so every
  other stamp component is byte-identical whether or not it exists (verified by experiment) —
  adding the `+ paths@<digest>` component for path/directory existence claims.
- **The classification schema was neither total nor exclusive.** `Deferred` was folded into the
  landing-impact enum beside `Blocking`/`Non-blocking`, but scope and consequence are
  **orthogonal** — an unsafe defect in an out-of-scope consumer is both, with no precedence to
  resolve it — and the "exhaustive" implementer triage had no bucket for a confirmed-but-
  out-of-scope finding, so it would land in `Confirmed: eligible to fix`, contradicting its own
  definition. Additionally, `severity` was named as a required companion field but never defined
  anywhere normative. Fixed (round 1) by splitting into two required independent axes (landing
  impact × scope), splitting the triage bucket into `Confirmed (in scope)` /
  `Confirmed (out of scope)`, tightening "act only on Confirmed" to "edit only on
  **Confirmed (in scope)**", and demoting severity to explicitly optional, action-free context.
- **The revised triage was still neither total nor exclusive (round 2).** Two gaps survived the
  first fix: a verified in-scope finding whose *remedy* needs an Owner trade-off satisfied both
  `Confirmed (in scope)` and `Needs owner decision` with no precedence; and the landing-stop rule
  was stated only for the out-of-scope bucket, leaving `Blocking` + in-scope with no landing
  action. Fixed by making the buckets **ordered, first match wins** (Unclear → Rejected → Stale →
  Confirmed (out of scope) → Needs owner decision → Confirmed (in scope)), and by generalizing the
  landing rule: **`Blocking` halts the landing from whichever bucket it lands in** — in scope →
  fix or obtain an explicit Owner override; out of scope → surface and STOP; needs-owner-decision
  → STOP. `Non-blocking` never halts a landing on its own.
- **The durable record itself repeatedly drifted from the decided mechanism — one class, several instances.**
  (a) The round-1 correction narrative was inserted with a first-occurrence text match and landed
  inside **D1**, an unrelated decision, while D8 merely pointed back at it; (b) D8's title and
  operative Decision still described the abandoned `Deferred` model after final v5 replaced it
  with the independent `Out-of-scope` axis; (c) after the round-2 fixes landed in the draft, D8's own
  correction bullets still recorded the *intermediate* stash-only stamp and the *round-1* triage
  split as if final; and (d) the section simultaneously claimed everything was fixed "before
  anything shipped" while describing round-2 fixes as having "shipped". These are all one class — a decision is not recorded until every
  consumer surface carries the final version — and all three were caught by review rather than
  by the author. D1 was restored (verified: zero deletions, one purely additive hunk), the
  narrative moved into D8, every bullet above now states the final mechanism, and the fragile
  exhaustive-tally phrasing that kept manufacturing this drift was removed.

That the draft's own rules caught the draft's own defects is the strongest available evidence for
the additions; it is recorded here rather than smoothed away. Two failure modes recur across the
rounds and are worth naming: a schema asserted more complete than it was (what the preflight
exists to prevent), and a durable record lagging the thing it documents — the latter hit this very
entry repeatedly, including once by a careless scripted edit into a neighbouring decision.

**Alternatives rejected.**

- **Escape tracking / seeded-defect audits in the protocol block** — the honest gap is *recall*:
  observed precision was high, but multiple rounds demonstrably missed defects present at review
  time, so "the protocol earned its round-trips" cannot be claimed from catch-data alone. The
  instrument is real but it is **telemetry, not wire format**; putting it in the block would tax
  every session for a measurement almost no session performs. Left as an optional per-project
  practice note.
- **A parallel `Deferred` findings list** — would create a second tracker beside `LEDGER.md`,
  inviting exactly the drift D1 and the ledger discipline exist to prevent. The L86/L87/L88 splits
  in the source session are this pattern already working correctly.
- **Deferring LOW-severity findings wholesale** — rejected on the round-8 counter-example above.
- **Asking the reviewer to propose designs** when a design thread stalls — would forfeit the
  read-only adversarial stance that produced the four refutations. The constraint-convergence
  check gets the earlier signal while keeping the reviewer read-only.
- **"One deep pass" as a request type** — kept the intent (named audit axes) but not the promise;
  a single pass finding everything is unsupported by the session's own recall gaps.

**Reopen when.** Escape data is actually being collected in some project and shows a recall gap
that a wire-format rule (rather than practice) would close; or the block's per-session cost becomes
a measured problem, at which point the axes lists are the first candidates to move into a
`references/` file behind a pointer.
