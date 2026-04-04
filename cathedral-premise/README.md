# Cathedral Premise

A governance skill for Claude Code that enforces principled software development across all your projects.

## What It Does

Cathedral ensures that every design and implementation decision passes four checks before moving forward:

1. **Correctness first** — no shortcut justifies shipping something semantically wrong.
2. **Solve the general problem** — if you'll need N cases tomorrow, build for N today.
3. **Clean abstractions** — implementation details don't leak across boundaries.
4. **Established patterns first** — use proven approaches before inventing new ones.

It works on top of your blueprint workflow skill (either `systems-blueprint-workflow` or `business-blueprint-workflow`), adding a governance layer that audits your blueprints for principle violations, flags shortcuts, and enforces spike discipline.

## Quick Start

### 1. Install the skill

Copy the `cathedral-premise` folder into your Claude Code skills directory, or install the `.skill` file.

### 2. Add to your project

Add this block to your project's `CLAUDE.md`:

```markdown
## Premise: cathedral
Follow the cathedral premise.

### Project config
- Blueprint skill: business-blueprint-workflow
- Blueprint root: blueprints/
- Build verification: npm run test
- Project language: TypeScript
- Test formats: unit tests, integration tests
```

Adjust the values to match your project. For systems-level work (compilers, VMs, runtimes), use `systems-blueprint-workflow` instead.

That's it. Six lines. The skill carries everything else.

## What You Can Do With It

### Run an audit

```
Run cathedral audit
```

Claude will scan every blueprint under your `blueprints/` directory, check each artifact against the principles, and produce a `CATHEDRAL_AUDIT_REPORT.md` in the project root with violations, warnings, and notes.

### Get a design review

Just describe what you're planning. Cathedral will activate automatically when it detects design decisions, trade-offs, or architecture discussions:

```
I want to add a boolean flag to track whether an order is urgent.
```

Claude will evaluate the proposal against the four principles and tell you if it holds up (spoiler: a boolean flag usually doesn't — it'll suggest a proper enum or state machine).

### Propose a spike

```
I want to prototype a new caching layer. Can I just start coding?
```

Claude will walk you through the spike protocol: tag commits with `[SPIKE]`, set a time bound, write a BRIEF.md, and commit to replacing the prototype with a proper blueprint-driven implementation.

### Navigate a trade-off

```
Can we skip the service contracts doc and wire directly to the other module's DB? We need to ship by Friday.
```

Claude won't just say "no" — it'll explain which principles are at stake, offer concrete alternatives ranked by cathedral compliance, and suggest a spike escape hatch if the deadline is truly immovable.

## How It Works Internally

The skill has three layers:

```
cathedral-premise/
├── SKILL.md                          ← router: triggers on cathedral keywords,
│                                        loads the right references
├── references/
│   ├── cathedral-core.md             ← universal principles, spike rules,
│   │                                    blueprint alignment mandate, audit format
│   ├── cathedral-systems.md          ← audit checks for compilers/VMs/runtimes
│   └── cathedral-business.md         ← audit checks for ERP/CRM/SaaS modules
```

When Claude detects a cathedral-governed project, it loads `cathedral-core.md` (always) and then the domain-specific reference based on your `CLAUDE.md` config. This means updating the principles in one place updates them across every project that uses the skill.

## Supported Domains

| Domain | Blueprint Skill | Modes | Typical Projects |
|--------|----------------|-------|-----------------|
| **Systems** | `systems-blueprint-workflow` | SUBSYSTEM, FEATURE, PATCH | Compilers, VMs, GC, JIT, databases, OS kernels |
| **Business** | `business-blueprint-workflow` | MODULE, LIBRARY, BRIDGE | ERP, CRM, WMS, SaaS, internal tooling |

## Trigger Phrases

Cathedral activates when you mention any of these (English or Spanish):

- "cathedral audit", "run cathedral audit", "auditoría catedral"
- "premise check", "premisa catedral"
- "correctness first", "clean abstractions", "established patterns"
- "blueprint alignment", "spike hygiene", "drift detection"

It also activates automatically when your `CLAUDE.md` contains `Follow the cathedral premise.`

## FAQ

**Do I need to memorize the four principles?**
No. The skill enforces them automatically. But understanding them helps you anticipate what Claude will flag.

**Can I still take shortcuts?**
Yes — as time-bounded spikes. Tag commits with `[SPIKE]`, set a deadline, document the goal, and commit to replacing the spike with a proper implementation. Spikes are the pressure valve; they just can't become permanent.

**What if I disagree with a finding?**
The audit flags everything and lets you decide. It's strict on purpose — it's easier to dismiss a false positive than to catch a missed violation in production.

**Does this replace the blueprint workflow skill?**
No. Cathedral *governs* the blueprint workflow — it doesn't replace it. The blueprint skill defines *what* artifacts to produce. Cathedral defines *what principles those artifacts must satisfy*.
