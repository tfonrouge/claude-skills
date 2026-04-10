# AI Skills Repository

A centralized collection of skill definitions for AI-assisted software development. Each skill is a structured Markdown document that an AI agent ingests to align its behavior with established engineering principles and workflows.

## Repository Structure

Each skill module contains:

- **`SKILL.md`**: The core instruction set — agent constraints, operational context, and step-by-step methodologies.
- **`references/`**: Supplementary context, checklists, and domain-specific guidelines referenced by the main skill file.

### Active Skills

- **[`cathedral-premise`](./cathedral-premise/)**: A governance premise for principled software development. Enforces five core principles — correctness first, solve the general problem, clean abstractions, established patterns over novel invention, and incremental discipline — across all blueprint-driven work. Supports two domains:

  - **Systems** (compilers, VMs, runtimes, GC, JIT) via `references/cathedral-systems.md`
  - **Business** (ERP, CRM, WMS, SaaS modules) via `references/cathedral-business.md`

  The premise governs blueprint skills — it does not replace them. It provides cathedral audits, design decision evaluation, spike hygiene enforcement, and a Decision Ledger with falsification conditions to prevent both rejection amnesia and approval calcification.

## How to Use

1. **Install** the skill into your agent's workspace (e.g., as a Claude Code skill directory or by mounting the repo).
2. **Configure** the project's `CLAUDE.md` with the appropriate premise and blueprint skill (see `cathedral-premise/references/cathedral-core.md` for the config template).
3. **Invoke** the skill by trigger phrase (e.g., "run cathedral audit", "premise check") or let the agent activate it automatically when it detects relevant context.

## Adding a New Skill

1. Create a dedicated top-level directory for the skill domain.
2. Define a `SKILL.md` with frontmatter (name, version, description, triggers) and the full instruction set.
3. Place domain-specific reference materials in `references/`.

---
*Built to empower intelligent agents with structured engineering workflows.*
