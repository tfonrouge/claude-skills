# Changelog

## owner-rar-protocol v1

- Introduces Owner/RAR distinction (authority, not identity).
- Defines `--- BEGIN RAR ---` / `--- END RAR ---` wrapped reviewer output.
- Requires implementer verification before acting on RAR findings.
- Adds the RAR triage circuit-breaker (Confirmed / Rejected / Stale / Needs owner decision / Unclear).
- Adds fail-safe behavior for untagged reviewer-shaped findings.
