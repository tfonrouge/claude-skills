# Changelog

This repo ships two independently versioned products. Each has its own section below.

---

# cathedral-premise (skill)

Versioned via the `metadata.version` field in `cathedral-premise/SKILL.md`.

## 1.1.1

- Corrects an internal inconsistency: `SKILL.md` prose referred to "four core principles" in four
  places while `references/cathedral-core.md` defines **five** (the fifth being Incremental
  Discipline). All prose now says five. Documentation-only fix; no behavior change.

## 1.1.0 and earlier

Predates this changelog. `1.1.0` is the first release whose `references/cathedral-core.md` documents
five principles (Incremental Discipline plus the Decision Ledger with falsification conditions); the
`SKILL.md` prose was not updated to match at the time — corrected in 1.1.1 above.

---

# owner-roar-protocol (prompts)

Versioned via the visible `Protocol version` line inside the installed block. Prior to v3 the
protocol and its reviewer role used the acronym **RAR**; see v3 for the rename to **ROAR**.

## v4

- **Adds a reviewer discipline rule to the kickoff prompt** (`roar-reviewer.prompt.md`): *verify
  asserted absences, not just presences.* When a finding rests on "X does not exist / is never read /
  has no write-path," the reviewer must run the search that would surface X before asserting it and
  cite the (empty or non-empty) result — never state the expected outcome of an unrun check — and must
  search one ring beyond the files the analysis already cites.
- The installed protocol block (`owner-roar-protocol.prompt.md`) is **unchanged in substance**; the
  rule lives only in the kickoff. Its visible version line moves to v4 in lockstep because the kickoff
  and the installed block share a single protocol version (see [`DECISIONS.md`](./DECISIONS.md) D4).
- **Migration:** re-pasting v4 replaces a v3 block in place — the `OWNER_ROAR_PROTOCOL` markers are
  unchanged (no marker rename this time; D2 stability holds), so the swap is clean and yields a block
  identical to v3 but for the version line.

## v3

- **Renames the reviewer acronym `RAR` → `ROAR`** (Read-Only Adversarial Reviewer) to avoid collision
  with unrelated acronyms in AI/agent contexts (and with the `.rar` archive format). The change is
  total: prompt filenames, the protocol slug (`owner-rar-protocol` → `owner-roar-protocol`), the wire
  wrapper (`--- BEGIN/END ROAR ---`), the `@ROAR` authority tag, the triage header, and the install
  markers (`OWNER_RAR_PROTOCOL` → `OWNER_ROAR_PROTOCOL`).
- **One-time marker migration:** the v3 installer replaces a block delimited by the new *or* the
  legacy markers, in place, so existing v2 installs upgrade without duplication. This is the sole
  sanctioned marker-name change; D2's version-less-stability guarantee resumes under the new name.
- Rationale recorded in [`DECISIONS.md`](./DECISIONS.md) (D3).

## v2

- Adds a **Persistence** rule: the triage is a working-loop artifact kept in chat; findings and the triage table are never written to durable audit/spec artifacts.
- Promotion to a durable record is explicit and Owner-gated, with fixed routing: blueprint/contract↔code drift → `AUDIT.md`; a decision or deliberate rejection → `LEDGER.md`.
- Stabilizes the install markers (version-less) so upgrades replace in place instead of duplicating; the version is carried by the visible `Protocol version` line.
- Rationale recorded in [`DECISIONS.md`](./DECISIONS.md) (D1, D2) to prevent silent re-litigation.

## v1

- Introduces Owner/RAR distinction (authority, not identity).
- Defines `--- BEGIN RAR ---` / `--- END RAR ---` wrapped reviewer output.
- Requires implementer verification before acting on RAR findings.
- Adds the RAR triage circuit-breaker (Confirmed / Rejected / Stale / Needs owner decision / Unclear).
- Adds fail-safe behavior for untagged reviewer-shaped findings.
