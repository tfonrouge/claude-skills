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

## Root-Level Prompts

Paste-ready prompts that currently live at the repo root (they may move into a `prompts/` directory if more accrue). Unlike skills (which an agent ingests as `SKILL.md`), these are **copied directly into a chat session**:

- **[`owner-rar-protocol.prompt.md`](./owner-rar-protocol.prompt.md)** — installer. Paste once into a project's *implementer* session to add the versioned **Owner/RAR Session Roles Protocol** to that project's `CLAUDE.md` (or `AGENTS.md`).
- **[`rar-reviewer.prompt.md`](./rar-reviewer.prompt.md)** — kickoff. Paste at the start of each *Readonly Adversarial Reviewer (RAR)* session.

### Owner/RAR review workflow

The two prompts support a two-session review loop: an **implementer** (edits, commits, pushes) and a **Readonly Adversarial Reviewer** (verdict + critique only). The Owner shuttles RAR output into the implementer. The protocol lets the implementer tell *authority* apart — **Owner directives** vs. **RAR claims-to-verify** — via a whole-line wrapper (`--- BEGIN RAR ---` / `--- END RAR ---`), and forces a triage circuit-breaker before any edit so the implementer metabolizes the review instead of blindly obeying it.

Lifecycle:

1. **Once per project** — paste `owner-rar-protocol.prompt.md` into the implementer session. It installs a `v1`, marker-delimited block in `CLAUDE.md`; re-paste a newer version to replace it in place.
2. **Each reviewer session** — paste `rar-reviewer.prompt.md` into the RAR session so it wraps output correctly from the first message.
3. **Each review** — copy RAR's wrapped output into the implementer; the implementer triages each finding (Confirmed / Rejected / Stale / Needs owner decision / Unclear) before changing anything.

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
