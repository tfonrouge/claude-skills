# Business Module Checklist

Print or copy this for each new module. Check off items as they are completed and signed off.

---

## Module: ___________________________
## Owner: ___________________________
## Started: ___________________________

---

## Step 0 — Kickoff
- [ ] Directory created: `module-descriptor/<ModuleName>/`
- [ ] Module name confirmed (PascalCase)
- [ ] Business owner identified
- [ ] Business justification documented
- [ ] Key stakeholders listed
- [ ] Target go-live confirmed
- [ ] Integration surface identified (which modules does this touch?)

---

## Step 1 — SPECIFICATION.md
- [ ] Module Objective & Scope written
- [ ] Functional Requirements numbered and testable (SHALL statements)
- [ ] Business Rules & Constraints documented
- [ ] User Roles & Permissions defined
- [ ] Data Models & Relationships diagrammed or described
- [ ] Integration Points named with data exchanged
- [ ] Performance Requirements specified (response times, batch sizes)
- [ ] Security Considerations addressed
- [ ] No unresolved ambiguities
- [ ] **Business owner sign-off** ✓ Date: ___________

---

## Step 2 — Flow_Chart_Process.md
- [ ] Happy Path flowchart (Mermaid)
- [ ] Decision Tree with all branch conditions labeled
- [ ] Exception Handling paths for every decision node
- [ ] Integration Event sequence diagram
- [ ] Role-Based view for each user role
- [ ] Every requirement traceable to ≥1 flow step
- [ ] All diagrams render without errors
- [ ] **Tech lead review** ✓ Date: ___________

---

## Step 3 — API_Contract.md
- [ ] Inbound APIs documented (endpoint, payload, auth, SLA)
- [ ] Outbound Events documented (name, payload, trigger)
- [ ] Shared Data Entities listed
- [ ] Error Codes & Response envelope defined
- [ ] Versioning Policy stated
- [ ] Consumer Modules listed and notified
- [ ] Every integration point from spec has a contract entry
- [ ] **Consumer module tech leads sign-off** ✓ Date: ___________

---

## Step 4 — Module_Implementation_Plan.md
- [ ] 3–5 phases defined, each with a shippable deliverable
- [ ] Milestones table complete (owner, effort, dependency)
- [ ] Technical objectives per phase written
- [ ] Component dependency graph complete
- [ ] Resource allocation documented
- [ ] Risk register has ≥3 entries with mitigations
- [ ] All spec requirements mapped to a phase
- [ ] **Traceability_Matrix.md initialized** ✓ Date: ___________
- [ ] **Tech lead and project owner sign-off** ✓ Date: ___________

---

## Step 5 — Test_Routing_Map.md
- [ ] Test coverage matrix (REQ-ID → TEST-ID) complete
- [ ] Happy path scenarios written
- [ ] Edge case scenarios written (boundary values, empty states)
- [ ] Error & exception scenarios cover all flow chart exception paths
- [ ] Integration scenarios cover all cross-module flows
- [ ] Every requirement has ≥1 test
- [ ] Every flow chart path has ≥1 test
- [ ] Automated vs. manual QA tests flagged
- [ ] **QA lead review** ✓ Date: ___________

---

## Step 6 — Traceability_Matrix.md (Living)
- [ ] Initialized with all REQ-IDs (status: Not Started)
- [ ] Milestone tracker pre-populated
- [ ] Updated after Sprint 1
- [ ] Updated after Sprint 2
- [ ] Updated after Sprint 3
- [ ] *(continue per sprint)*
- [ ] All requirements show "Verified" at module ship ✓ Date: ___________

---

## Module Ship Criteria
- [ ] All requirements status = Verified in Traceability Matrix
- [ ] All tests passing (automated + manual sign-off)
- [ ] API contract consumers confirmed compatibility
- [ ] Performance requirements validated under load
- [ ] Security review completed
- [ ] Documentation reviewed by a developer who wasn't on the team
- [ ] **Final sign-off** ✓ Date: ___________
