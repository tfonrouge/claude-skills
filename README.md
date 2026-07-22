# AI Skills Repository

A centralized collection of skill definitions for AI-assisted software development. Each skill is a structured Markdown document that an AI agent ingests to align its behavior with established engineering principles and workflows.

## Repository Structure

Each skill module contains:

- **`SKILL.md`**: The core instruction set — agent constraints, operational context, mode selection, and shared artifacts. For split skills it also carries a **mode→reference map** naming the file to load per mode.
- **`references/`**: Supplementary context (checklists, prompt libraries, domain guidelines) — and, for split skills, the **mandatory per-mode instruction bodies** (`references/mode-*.md`): normative step-by-step workflows and Definitions of Done, loaded via the mode→reference map. A split skill's `SKILL.md` is not sufficient on its own to work a blueprint.

### Active Skills

- **[`cathedral-premise`](./cathedral-premise/)**: A governance premise for principled software development. Enforces five core principles — correctness first, solve the general problem, clean abstractions, established patterns over novel invention, and incremental discipline — across all blueprint-driven work. Supports two domains:

  - **Systems** (compilers, VMs, runtimes, GC, JIT) via `references/cathedral-systems.md`
  - **Business** (ERP, CRM, WMS, SaaS modules) via `references/cathedral-business.md`

  The premise governs blueprint skills — it does not replace them. It provides cathedral audits, design decision evaluation, spike hygiene enforcement, and a Decision Ledger with falsification conditions to prevent both rejection amnesia and approval calcification.

- **[`systems-blueprint-workflow`](./systems-blueprint-workflow/)** and **[`business-blueprint-workflow`](./business-blueprint-workflow/)**: the **authoring** workflows that `cathedral-premise` governs. Where the premise *audits*, these *produce* — they define the modes (SUBSYSTEM / FEATURE / PATCH for systems; MODULE / LIBRARY / BRIDGE for business), the `blueprints/` layout, `INDEX.md`, and per-blueprint `AUDIT.md`. `cathedral-{systems,business}.md` are the thin per-domain adapters that teach the premise what each workflow's output should look like. Producer and governor are co-located on purpose (see [`DECISIONS.md`](./DECISIONS.md) D6); this repo is their single source of truth, and `install.sh` syncs them downstream into `~/.claude/skills/`.

- **[`roar-reviewer`](./roar-reviewer/)** and **[`owner-roar-protocol`](./owner-roar-protocol/)**: the
  Owner/ROAR review prompts, each packaged as a **self-contained wrapper skill**. Each `SKILL.md` carries
  only frontmatter and points the agent at the canonical prompt **bundled in its own `references/`**
  (single source of truth — no duplicated text, no external path). Both are **manual-invoke only**
  (`/roar-reviewer`, `/owner-roar-protocol`) and must not auto-activate: `owner-roar-protocol` edits
  `CLAUDE.md`, and `roar-reviewer` flips the session into read-only reviewer mode. Their `metadata.version`
  is a packaging version, independent of the protocol version carried by the prompts. Rationale in
  [`DECISIONS.md`](./DECISIONS.md) (D5).

## Owner/ROAR review prompts

The two skills above each bundle a **paste-ready prompt** in `references/`. Beyond being invoked as skills
inside Claude Code, these prompts are **tool-agnostic** — open the file and copy it directly into any chat
session (for example, to run the ROAR reviewer in a *different* AI for independent perspective):

- **[`owner-roar-protocol/references/owner-roar-protocol.prompt.md`](./owner-roar-protocol/references/owner-roar-protocol.prompt.md)** — installer. Paste once into a project's *implementer* session to add the versioned **Owner/ROAR Session Roles Protocol** to that project's `CLAUDE.md` (or `AGENTS.md`). In Claude Code, invoke as `/owner-roar-protocol`.
- **[`roar-reviewer/references/roar-reviewer.prompt.md`](./roar-reviewer/references/roar-reviewer.prompt.md)** — kickoff. Paste at the start of each *Read-Only Adversarial Reviewer (ROAR)* session. In Claude Code, invoke as `/roar-reviewer`.

> Each prompt is the **single source of truth** for its skill. The `SKILL.md` reads and applies it; it does
> not copy the text. Edit the prompt, and both the paste-able and skill forms stay in sync.

### Owner/ROAR review workflow

The two prompts support a two-session review loop: an **implementer** (edits, commits, pushes) and a **Read-Only Adversarial Reviewer** (verdict + critique only). The Owner shuttles ROAR output into the implementer. The protocol lets the implementer tell *authority* apart — **Owner directives** vs. **ROAR claims-to-verify** — via a whole-line wrapper (`--- BEGIN ROAR ---` / `--- END ROAR ---`), and forces a triage circuit-breaker before any edit so the implementer metabolizes the review instead of blindly obeying it.

Lifecycle:

1. **Once per project** — paste `owner-roar-protocol.prompt.md` into the implementer session. It installs a versioned, marker-delimited block in `CLAUDE.md`; re-paste a newer version to replace it in place.
2. **Each reviewer session** — paste `roar-reviewer.prompt.md` into the ROAR session so it wraps output correctly from the first message.
3. **Each review** — copy ROAR's wrapped output into the implementer; the implementer triages each finding (Confirmed / Rejected / Stale / Needs owner decision / Unclear) before changing anything.

## How to Use

1. **Install** the skills into your agent's workspace. Run [`./install.sh`](./install.sh) to sync every skill in this repo into `~/.claude/skills/` (`--link` to symlink instead of copy so repo edits take effect live; `--dry-run` to preview). This repo is the source of truth — the script only ever writes *downstream*, never back.
2. **Configure** the project's `CLAUDE.md` with the appropriate premise and blueprint skill (see `cathedral-premise/references/cathedral-core.md` for the config template).
3. **Invoke** the skill by trigger phrase (e.g., "run cathedral audit", "premise check") or let the agent activate it automatically when it detects relevant context.

## Adding a New Skill

1. Create a dedicated top-level directory for the skill domain.
2. Define a `SKILL.md` with frontmatter — a top-level `name`, a `metadata:` block holding `version`, and a `description` block scalar that embeds the trigger phrases (there is no separate `triggers` key) — plus the full instruction set.
3. Place domain-specific reference materials in `references/`.

---
*Built to empower intelligent agents with structured engineering workflows.*
