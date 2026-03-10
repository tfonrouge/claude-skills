# Claude Code Prompt Patterns — Business Module Workflow

A ready-to-use prompt library for each step of the business module workflow.
Copy, fill in the brackets, and paste into Claude Code.

---

## Step 0 — Module Kickoff

```
I'm starting a new module called [ModuleName] for [system/platform name, e.g. "our SaaS billing platform", "internal WMS", "CRM"].

Context:
- Business Owner: [name]
- Business Justification: [why this is needed]
- Key Stakeholders: [list]
- Target Go-Live: [date/sprint]
- Integration Surface: [modules this touches]

Help me validate that this scope is well-defined and flag any gaps
before we start writing the specification.
```

---

## Step 1 — SPECIFICATION.md

### Standard
```
Generate SPECIFICATION.md for the [ModuleName] module.

Kickoff context: [paste Step 0 summary]
Known business rules: [list any known constraints or rules]
Regulatory requirements: [e.g. customs law, ISO standards, none]

Include all 8 required sections. Use numbered, testable requirements
("The system SHALL..."). Flag any ambiguities and ask me to resolve
them before finalizing.
```

### For compliance-heavy modules (e.g. Import Management, Finance, Healthcare, Legal)
```
Generate SPECIFICATION.md for [ModuleName].
This module has regulatory exposure: [describe regulations].
Pay special attention to:
- Audit trail requirements
- Data retention policies
- Role-based access for sensitive operations
- Approval workflow requirements
Flag any requirement that may conflict with [specific regulation].
```

### For high-integration modules (e.g. Procurement, Inventory, Billing, Notifications)
```
Generate SPECIFICATION.md for [ModuleName].
This module is tightly coupled to: [list modules].
Emphasize integration points and shared data entities.
List every data field this module reads from or writes to other modules.
```

---

## Step 2 — Flow_Chart_Process.md

### Standard
```
Based on SPECIFICATION.md for [ModuleName], generate Flow_Chart_Process.md.

Use Mermaid diagrams:
- flowchart TD for process flows and decision trees
- sequenceDiagram for integration event flows

I need all 5 diagram types:
1. Happy path
2. Decision tree with all branch conditions labeled
3. Exception/error handling paths
4. Integration event flow with [list modules]
5. Role-based view for: [list roles]

Be exhaustive. Every branch in the spec should appear in a diagram.
```

### Iteration prompt (after first draft review)
```
The flow chart for [ModuleName] is missing:
- [describe missing path or scenario]
- [describe missing role or exception]

Also, the [DiagramName] diagram has an issue: [describe].
Please update Flow_Chart_Process.md accordingly.
```

---

## Step 3 — API_Contract.md

### Standard
```
Based on SPECIFICATION.md and Flow_Chart_Process.md for [ModuleName],
generate API_Contract.md.

This module integrates with:
- [Module A]: [what data is exchanged]
- [Module B]: [what data is exchanged]

For each integration, define:
- Inbound APIs this module exposes
- Outbound events this module emits
- Shared data entities

Use the standard endpoint format from the skill. Flag anything
underspecified that needs cross-team clarification.
```

### Consumer review prompt (for teams consuming this contract)
```
Review API_Contract.md for [ModuleName].
Our module [ConsumerModuleName] will consume: [list endpoints/events].
Identify any:
- Missing fields we'll need
- Ambiguous response structures
- Missing error codes
- SLA concerns
```

---

## Step 4 — Module_Implementation_Plan.md

### Standard
```
Based on all artifacts for [ModuleName], generate Module_Implementation_Plan.md.

Team size: [N] developers
Sprint length: [1 week / 2 weeks]
Known constraints: [deadlines, dependencies on other teams, etc.]

Break into 3–5 phases. Each phase should be shippable.
Include a risk register with at least 5 risks.
Flag any dependency on API contracts not yet finalized by other teams.
```

### Re-planning prompt (when scope changes)
```
The implementation plan for [ModuleName] needs to be updated.
Changes since last plan:
- [New requirement added: ...]
- [Requirement removed: ...]
- [Technical constraint discovered: ...]

Re-estimate affected phases and update the risk register.
Show me a diff of what changed.
```

---

## Step 5 — Test_Routing_Map.md

### Standard
```
Based on all artifacts for [ModuleName], generate Test_Routing_Map.md.

Ensure:
- Every requirement (REQ-NNN) from SPECIFICATION.md has ≥1 test
- Every path in Flow_Chart_Process.md has ≥1 test
- All exception paths are covered
- Integration scenarios cover flows with: [list modules]

Use the TEST-NNN ID format. Flag tests that require manual QA
vs. those that can be automated.
```

### Gap analysis prompt
```
Review Test_Routing_Map.md for [ModuleName].
Cross-reference against SPECIFICATION.md.
Identify any requirements without test coverage and generate
the missing test cases.
```

---

## Step 6 — Traceability_Matrix.md

### Initial generation
```
Generate an initial Traceability_Matrix.md for [ModuleName].
Source data:
- Requirements from SPECIFICATION.md
- Milestones from Module_Implementation_Plan.md
- Tests from Test_Routing_Map.md

Pre-populate all rows. Set status to "Not Started" for all items.
Add a timestamp of today's date.
```

### Sprint update
```
Update Traceability_Matrix.md for [ModuleName].

Completed this sprint:
- [REQ-001, REQ-002 implemented in PR #42]
- [Milestone: Phase 1 database schema merged]

Blockers discovered:
- [API from InventoryModule not yet finalized — blocks REQ-015]

Actual time for Phase 1: [N] days (estimated was [M] days).
Recalculate variance and flag any requirements at risk of slipping.
```

---

## Cross-cutting Prompts

### Consistency check (run anytime)
```
Review all artifacts for [ModuleName]:
- SPECIFICATION.md
- Flow_Chart_Process.md
- API_Contract.md
- Module_Implementation_Plan.md
- Test_Routing_Map.md

Identify any inconsistencies between them:
- Requirements in the spec not covered by the flow chart
- Integration points in the spec not in the API contract
- Phases in the plan not traceable to requirements
- Tests referencing non-existent requirements
```

### Onboarding a new developer
```
A new developer is joining the [ModuleName] team.
Summarize the module from all its artifacts in a 1-page onboarding brief covering:
- What the module does (2 sentences)
- Key business rules to know
- Current implementation status
- What they'll be working on first
- Who to talk to for questions about each area
```
