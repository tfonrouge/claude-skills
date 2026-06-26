# Changelog

## owner-rar-protocol v2

- Adds a **Persistence** rule: the triage is a working-loop artifact kept in chat; findings and the triage table are never written to durable audit/spec artifacts.
- Promotion to a durable record is explicit and Owner-gated, with fixed routing: blueprint/contract↔code drift → `AUDIT.md`; a decision or deliberate rejection → `LEDGER.md`.
- Stabilizes the install markers (now version-less: `OWNER_RAR_PROTOCOL:begin`/`:end`) so upgrades replace in place instead of duplicating; the version is carried by the visible `Protocol version` line.
- Rationale recorded in [`DECISIONS.md`](./DECISIONS.md) (D1, D2) to prevent silent re-litigation.

## owner-rar-protocol v1

- Introduces Owner/RAR distinction (authority, not identity).
- Defines `--- BEGIN RAR ---` / `--- END RAR ---` wrapped reviewer output.
- Requires implementer verification before acting on RAR findings.
- Adds the RAR triage circuit-breaker (Confirmed / Rejected / Stale / Needs owner decision / Unclear).
- Adds fail-safe behavior for untagged reviewer-shaped findings.
