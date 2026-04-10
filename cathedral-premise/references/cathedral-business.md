# Cathedral Audit — Business Domain

Domain-specific audit checks for projects using `business-blueprint-workflow`.
These checks supplement the universal principles in `cathedral-core.md`.

---

## Applicable Modes

| Mode | Directory Suffix | Artifacts |
|------|-----------------|-----------|
| MODULE | `(MODULE)` | BRIEF, FLOWCHART, ENTITY_RELATIONSHIP, API_CONTRACT, VIEW_MAP, IMPLEMENTATION_ORDER, AUDIT |
| LIBRARY | `(MODULE)` | BRIEF, ARCHITECTURE, PUBLIC_API, IMPLEMENTATION_ORDER, AUDIT |
| BRIDGE | `(BRIDGE)` | BRIEF, ENTITY_DESCRIPTOR, SERVICE_CONTRACTS, VIEW_MAP, IMPLEMENTATION_ORDER, AUDIT, (ARCHIVED) |

---

## Established Patterns Reference

When checking Principle 4 (Established Patterns Over Novel Invention), these are
the domain-standard approaches for business software. Flag any custom alternative
that lacks explicit justification:

| Area | Established Pattern |
|------|-------------------|
| Domain modeling | Domain-Driven Design (bounded contexts, aggregates, entities, value objects) |
| State management | Explicit state machines with named transitions, not implicit boolean flags |
| Data flow | CQRS, event sourcing, saga/orchestration patterns |
| API design | REST with resource-oriented URIs, or GraphQL with schema-first design |
| Authentication/authorization | RBAC, ABAC — never hand-rolled permission checks |
| Integration | Anti-corruption layers, published language, conformist/shared kernel |
| Data validation | Schema validation at boundaries, domain invariants in entity constructors |
| Error handling | Result types or domain exceptions — not generic catch-alls |
| Multi-tenancy | Tenant-aware from day one if the domain requires it, not bolted on later |
| Workflow/processes | Workflow engine patterns (state machines, process managers) — not ad-hoc if/else chains |

---

## Principle Alignment Checks

### Universal Checks (applied via cathedral-core.md)

These apply to every blueprint regardless of domain:

| Check | What to look for |
|-------|-----------------|
| **Correctness over speed** | Any artifact that documents or endorses a shortcut, workaround, or "temporary" hack without a `[SPIKE]` tag and bounded scope. |
| **General over ad-hoc** | Entity models hardcoded to one tenant, locale, or currency when the domain is clearly multi-X. APIs that serve only today's one consumer. |
| **Clean abstractions** | Leaky module boundaries — one module reaching into another's database, bypassing service contracts, or sharing internal DTOs. |
| **Established patterns** | Custom solutions where a well-known pattern exists (see table above). Check design artifacts' "Alternatives Considered" for justification. |
| **Spike hygiene** | Any `[SPIKE]` work that shipped as-is without being rewritten under a full blueprint. Check git log for `[SPIKE]` tags. |

### Business-Specific Checks — MODULE Mode

| Check | What to look for |
|-------|-----------------|
| **Entity model completeness** | ENTITY_RELATIONSHIP.md must define every entity, its fields, types, and relationships. Undocumented entities discovered in code are a violation. |
| **Flowchart ↔ code drift** | FLOWCHART.md state machines and process flows must match actual implemented logic. Missing states, phantom transitions, or unlabeled edges are findings. |
| **API contract fidelity** | API_CONTRACT.md endpoints must match actual route definitions, request/response shapes, and status codes. Undocumented endpoints are a violation. |
| **VIEW_MAP coverage** | Every entity state must have at least one view that displays it. Every actor in the role matrix must have at least one entry point. Missing coverage is a warning. |
| **Role/permission alignment** | If VIEW_MAP.md defines role-based access, verify that the actual permission implementation matches. Roles that exist in the artifact but not in code (or vice versa) are findings. |
| **Data validation boundaries** | Entities should validate invariants at construction/mutation, not just at the API layer. Schema-only validation with no domain enforcement is a warning. |
| **IMPLEMENTATION_ORDER progress** | Task completion must reflect actual code state. Tasks marked done without corresponding code are a violation. |
| **Blueprint completeness** | Missing artifacts for the mode, empty sections, stale dates, TODOs that block implementation. Cross-reference against the skill's Definition of Done for each step. |
| **AUDIT.md currency** | Every blueprint must have an AUDIT.md. Check that it was updated within the current sprint. |

### Business-Specific Checks — LIBRARY Mode

| Check | What to look for |
|-------|-----------------|
| **PUBLIC_API stability** | Public API surface must be explicitly defined. Any public symbol not in PUBLIC_API.md is a violation. Breaking changes to published APIs without a versioning strategy documented are Critical. |
| **ARCHITECTURE.md clarity** | Module boundaries, dependency direction, and extension points must be documented. Circular dependencies are a violation. |
| **Platform coverage** | If the library targets multiple platforms (KMP, cross-platform), each target must be explicitly listed with its constraints and test strategy. |
| **Blueprint completeness** | Same as MODULE mode. |
| **AUDIT.md currency** | Same as MODULE mode. |

### Business-Specific Checks — BRIDGE Mode

| Check | What to look for |
|-------|-----------------|
| **BRIDGE coherence** | BRIEF.md must identify both connected modules, the lifecycle type (Permanent/Temporary), and for Temporary bridges, the expiry condition. Missing any of these is a violation. |
| **SERVICE_CONTRACTS integrity** | Every integration point from BRIEF.md must have a contract entry in SERVICE_CONTRACTS.md. Contracts must specify direction, trigger, input/output shapes, and side effects. Missing contracts are a violation. |
| **Cross-module boundary respect** | The BRIDGE must interact with connected modules exclusively through their documented API contracts — never reaching into another module's database, internal services, or private DTOs. Any such coupling is a Critical violation. |
| **ENTITY_DESCRIPTOR state coverage** | State machine in ENTITY_DESCRIPTOR.md must cover all states including error/rejection states. Every transition must have a named trigger. Missing states are a finding. |
| **VIEW_MAP scope** | Bridge VIEW_MAP.md is intentionally simplified vs MODULE mode. If it lists >4-5 views, flag as a warning — the bridge may need to escalate to MODULE mode. |
| **Temporary bridge hygiene** | If lifecycle is Temporary and the expiry condition has been met, check that ARCHIVED.md exists, `.blueprint-status` is `CLOSED`, and INDEX.md reflects deprecation. Missing archival is a violation. |
| **IMPLEMENTATION_ORDER progress** | Same as MODULE mode. |
| **Blueprint completeness** | Same as MODULE mode. |
| **AUDIT.md currency** | Same as MODULE mode. |

---

## Escalation Triggers

Flag these as **warnings** even if all other checks pass:

- A BRIDGE blueprint has >5 views in VIEW_MAP.md → should be MODULE
- A BRIDGE modifies >3 existing views in other modules → scope concern
- A MODULE blueprint has no FLOWCHART.md state machine for stateful entities
- An entity has >3 boolean flags controlling behavior → should be a state machine
- A Temporary BRIDGE has been `ACTIVE` for >3 months past its estimated expiry
- API_CONTRACT.md has endpoints that don't appear in any VIEW_MAP.md view → orphan API risk
- Any blueprint has been in `ACTIVE` status for >4 weeks without AUDIT.md updates

---

## Project Config Schema

The project's `CLAUDE.md` must contain these fields:

```markdown
## Premise: cathedral
Follow the cathedral premise.

### Project config
- Blueprint skill: business-blueprint-workflow
- Blueprint root: blueprints/
- Build verification: [e.g., npm run test, ./gradlew test]
- Project language: [e.g., Kotlin, TypeScript, Vue 3]
- Test formats: [e.g., unit tests, integration tests, e2e tests]
```
