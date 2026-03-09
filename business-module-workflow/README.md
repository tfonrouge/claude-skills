# business-module-workflow

A Claude skill that gives you a structured, repeatable methodology for building any module in a large-scale business software system — ERP, CRM, WMS, SaaS platforms, internal tooling, and more — using **Claude Code as a development partner**.

Part of the [`claude-skills`](https://github.com/tfonrouge/claude-skills) monorepo.

---

## What it does

When you start or refactor a software module, this skill guides Claude through producing a standard set of artifacts in the right order:

| Step | Artifact | Purpose |
|------|----------|---------|
| 0 | `BRIEF.md` | Context, owner, justification |
| 1 | `SPECIFICATION.md` | What the module does |
| 2 | `FLOWCHART.md` + `.html` | How it flows (Mermaid diagrams, browser-ready) |
| 3 | `API_CONTRACT.md` | How it connects to other modules |
| 4 | `IMPLEMENTATION_PLAN.md` | How it will be built |
| 5 | `TEST_PLAN.md` | How it will be verified |
| 6 | `TRACEABILITY_MATRIX.md` | Living progress tracker |
| 6b | `GANTT.html` | Print-ready timeline snapshot (regenerate every sprint) |

Every step includes **Claude Code prompt patterns**, a **Definition of Done checklist**, and human sign-off requirements. The skill also handles **refactoring existing modules** via a dedicated guide that covers backward compatibility, breaking changes, regression baselines, and migration planning.

---

## Why this workflow

- **Claude Code works better with structure** — SPECIFICATION.md eliminates ambiguity, FLOWCHART.md covers every branch, API_CONTRACT.md prevents integration surprises
- **Errors are caught early** — a wrong requirement fixed in Step 1 costs nothing; the same error found after coding costs days
- **Consistent across modules** — any team member can navigate any module instantly because every module looks the same
- **Scales with your system** — as modules multiply, the standard structure compounds in value; Claude can reason across multiple modules when given their artifacts
- **Stakeholder-ready** — each artifact maps to a stakeholder concern, reducing status meetings and providing audit-ready documentation

---

## Requirements

- [Claude Code](https://code.claude.com) (for CLI usage)
- **or** Claude.ai Pro, Max, Team, or Enterprise (for web upload)
- Python 3 (for the flowchart HTML renderer — no packages needed)

---

## Installation

This skill lives in the `skills/business-module-workflow/` directory of the monorepo.
Clone the whole repo once and all skills are available.

### Claude Code (personal — available across all your projects)

```bash
# Clone the monorepo
git clone https://github.com/tfonrouge/claude-skills.git

# Symlink or copy this skill into your personal Claude skills folder
mkdir -p ~/.claude/skills
ln -s $(pwd)/claude-skills/skills/business-module-workflow ~/.claude/skills/business-module-workflow

# Or copy instead of symlink (if you prefer)
cp -r claude-skills/skills/business-module-workflow ~/.claude/skills/
```

> **Tip:** Using a symlink means `git pull` in the monorepo automatically updates the skill everywhere.

### Claude Code (project-scoped — available only in one project)

```bash
mkdir -p /path/to/your/project/.claude/skills
ln -s /path/to/claude-skills/skills/business-module-workflow \
      /path/to/your/project/.claude/skills/business-module-workflow
```

### Claude.ai (web interface)

1. Download `business-module-workflow.skill` from the [Releases](../../releases) page
2. Go to **claude.ai → Customize → Skills**
3. Click **Upload skill** and select the `.skill` file
4. Toggle it on

### Team / Enterprise (org-wide provisioning)

Organization owners can upload the `.skill` file once in **Organization Settings → Skills** and it will automatically appear for all members.

---

## Usage

Once installed, Claude automatically uses the skill when you mention building or refactoring a software module. You can also invoke it explicitly:

```
Let's start a new module called BillingManagement for our SaaS platform.
```

```
I need to refactor the InventoryModule — it has performance issues and we need to add multi-warehouse support.
```

Claude will walk through the steps, generate each artifact, and prompt you for decisions and sign-offs at the right moments.

### Rendering flowcharts and Gantt charts

After `FLOWCHART.md` is generated, render it to a browser-ready HTML file:

```bash
python scripts/render_flowchart.py module-descriptor/<ModuleName>/FLOWCHART.md
```

Open the resulting `FLOWCHART.html` in any browser — no plugins required.

To render the Gantt chart from `TRACEABILITY_MATRIX.md`:

```bash
python scripts/render_flowchart.py module-descriptor/<ModuleName>/TRACEABILITY_MATRIX.md --output module-descriptor/<ModuleName>/GANTT.html
```

Open `GANTT.html` in any browser and use **File → Print** to produce a PDF. Regenerate every sprint.

> Claude handles rendering automatically if you ask it to render the flowchart or Gantt chart.

---

## What's inside

```
skills/business-module-workflow/
├── README.md                         # This file
├── SKILL.md                          # Main skill — steps 0–6, prompt patterns, DoD checklists
├── scripts/
│   └── render_flowchart.py           # Converts FLOWCHART.md / TRACEABILITY_MATRIX.md → self-contained HTML
└── references/
    ├── refactor-guide.md             # Full refactoring guide — overrides each step for existing modules
    ├── example-prompts.md            # Copy-paste Claude Code prompt library for every step
    └── business-module-checklist.md  # Printable per-module sign-off checklist
```

---

## Keeping it up to date

```bash
# Update all skills at once from the monorepo root
cd claude-skills
git pull
```

If you used symlinks during installation, all skills update automatically. If you copied, re-run the `cp` command for each skill you want to refresh.

---

## Contributing

Issues and pull requests are welcome on the [monorepo](https://github.com/tfonrouge/claude-skills). If you've used this skill on a real system and found gaps — especially around specific module types, edge cases in the refactoring guide, or prompt patterns that work better — please open an issue or PR.

---

## License

MIT

