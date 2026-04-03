# Claude Code Prompt Patterns — Systems Blueprint Workflow

Copy, fill in the brackets, paste into Claude Code.

---

## SUBSYSTEM MODE

### Step 0 — BRIEF.md
```
I need to plan a subsystem change called [Name] for the Harbour compiler/runtime.
Component: [VM / Compiler / RTL / RDD / Preprocessor / Debug]
Motivation: [why this change is needed]
Key files I expect to touch: [list 5-10 files]
Compatibility target: [e.g. 99.5% — no silent data corruption]
Dependencies: [other workstreams that must land first]

Help me write BRIEF.md. Read the affected files to verify they exist and
understand the current state. Flag risks and underspecified areas.
```

### Step 1 — DESIGN.md
```
Based on BRIEF.md for [Name], generate DESIGN.md.
Read the current implementation in [list key source files].
For every proposed change:
- Show the current struct/function with file:line
- Show the proposed modification
- Analyze sizeof() impact and alignment
- Identify all callers that need updating
Flag any change that affects the VM hot loop.
```

### Step 2 — ARCHITECTURE.md
```
Based on DESIGN.md for [Name], generate ARCHITECTURE.md with Mermaid diagrams.
Read the actual source code to trace call chains — do not guess.
I need:
1. Current call graph for [specific execution path]
2. Proposed call graph after changes
3. Data flow through the affected component
4. Initialization sequence showing registration order
5. Hot path annotated with the performance-critical section
Verify every function name against the codebase.
```

### Step 3 — C_API.md
```
Based on DESIGN.md for [Name], generate C_API.md.
List every new, changed, or removed public symbol.
For each: signature, header file, thread safety, ABI impact.
Check include/ headers to confirm current signatures before documenting changes.
```

### Step 4 — COMPAT.md
```
Based on DESIGN.md and C_API.md for [Name], generate COMPAT.md.
For each potential compatibility break:
- grep the codebase to count affected call sites (src/ + contrib/ + tests/)
- Classify as silent/loud and compile-time/runtime discoverable
- Assign a risk percentage
- Propose a specific mitigation
Sum the total risk and verify it matches the target in BRIEF.md.
```

### Step 5 — IMPLEMENTATION_PLAN.md
```
Based on DESIGN.md and COMPAT.md for [Name], generate IMPLEMENTATION_PLAN.md.
Break into 3-5 phases, each leaving the build green.
For each phase: files touched, build verification command, performance checkpoint,
rollback strategy. Order by dependency — nothing blocks.
Also initialize TRACEABILITY.md with all phases and design items set to "Not Started".
```

### Step 6 — TEST_PLAN.md
```
Based on DESIGN.md, COMPAT.md, and IMPLEMENTATION_PLAN.md for [Name],
generate TEST_PLAN.md.
Every struct change needs a regression test.
Every new function needs a behavior test.
Every fracture in COMPAT.md needs a compatibility test.
Performance-critical changes need benchmarks with thresholds.
Write tests as hbtest assertions or compilable .prg/.c code.
```

### Audit
```
Perform a blueprint audit for [Name].
Read all artifacts in blueprints/[Name](SUBSYSTEM)/.
Then inspect the actual code in [list source directories].
For each artifact section, compare design claims against actual code.
Populate the Drift Log with every discrepancy. Assign severity.
Set Overall Status. List recommended actions.
```

---

## FEATURE MODE

### F0 — BRIEF.md
```
I need to add a feature called [Name] to the Harbour [component].
Purpose: [what it does]
Integration points: [where it hooks into existing code]
New syntax: [if any — grammar changes]
New opcodes: [if any]
Scope: [estimated days/weeks]

Help me write BRIEF.md. Check the integration points exist in the codebase.
```

### F1 — DESIGN.md
```
Based on BRIEF.md for [Name], generate DESIGN.md.
Focus on the feature's internal design and how it hooks into existing code.
Read [list integration point files] to understand the hook mechanism.
Include an "Integration Points" section showing exactly where the new code
plugs in (function name, file, insertion point).
```

### F2 — C_API.md
```
Based on DESIGN.md for [Name], generate C_API.md.
Only new symbols — no changed or removed unless the feature deprecates something.
For each: signature, header, thread safety, when it becomes available.
```

### F3 — IMPLEMENTATION_PLAN.md
```
Based on DESIGN.md for [Name], generate IMPLEMENTATION_PLAN.md.
If scope is small (< 1 week), a flat checklist is fine.
Otherwise use phased approach. Each step must leave the build green.
```

### F4 — TEST_PLAN.md
```
Based on DESIGN.md and C_API.md for [Name], generate TEST_PLAN.md.
Focus on new behavior tests. Add regression tests only for the specific
integration points that might break.
```

---

## PATCH MODE

### P0 — BRIEF.md
```
I need to fix [problem] in [component].
Root cause: [why it happens, with file:line if known]
Proposed fix: [one paragraph]
Files touched: [list]
Risk: [low/medium/high — why]

Help me write BRIEF.md. Verify the root cause by reading the affected code.
```

### P1 — CHANGESET.md
```
Based on BRIEF.md for [Name], generate CHANGESET.md.
Read every file listed in the brief. For each change:
- Show the current code (before)
- Show the proposed code (after)
- Explain why the change is correct
Do not include changes that are not directly related to the fix.
```

### P2 — TEST_PLAN.md
```
Based on BRIEF.md and CHANGESET.md for [Name], generate TEST_PLAN.md.
Write 3-5 tests that prove:
1. The bug is fixed (or the improvement works)
2. The surrounding code is not broken
3. Edge cases are handled
```
