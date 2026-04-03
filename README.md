# 🧠 AI Skills Repository

Welcome to the **AI Skills Repository**. This repository serves as a centralized collection of robust, all-purpose skill definitions and workflows designed to augment and enhance daily AI-assisted development, engineering, and operational tasks.

## 🎯 Purpose

In the evolving landscape of AI-assisted software engineering, agents require structured context, standardized procedures, and domain-specific knowledge to perform complex tasks effectively. This repository houses these "skills"—structured Markdown documents containing instructions, constraints, and methodologies that an AI agent can ingest to align its behavior with established best practices.

By utilizing these skills, you can ensure that your AI assistants produce more reliable, maintainable, and architecturally sound outputs across varying domains.

## 📂 Repository Structure

The repository is modularized by skill domains. A typical skill module contains:

- **`SKILL.md`**: The core instruction set defining agent constraints, operational context, and step-by-step methodologies.
- **`README.md`**: Human-readable documentation outlining the skill's scope, prerequisites, and intended usage.
- **`references/`**: Supplementary context, checklists, prompt examples, or architectural guidelines referenced by the main skill file.
- **`scripts/`**: Auxiliary scripts, generators, or validation tools that the AI might utilize during task execution.

### Active Modules

- **[`business-blueprint-workflow`](./business-blueprint-workflow/)**: A specialized workflow emphasizing clean architecture, separation of concerns, and robust data integrity operations when designing or refactoring business logic layers.

- **[`systems-blueprint-workflow`](./systems-blueprint-workflow/)**: An artifact workflow for designing and tracking systems-level software—compilers, VMs, runtimes, databases, OS kernels, language toolchains, and embedded firmware. Supports three modes: **Subsystem** (deep structural changes), **Feature** (self-contained additions), and **Patch** (targeted fixes). Produces `blueprints/` with Markdown specs, `INDEX.md`, and per-blueprint `AUDIT.md`.

## 🚀 How to Use

To utilize a skill from this repository within your AI environment (such as Claude, Gemini, or custom Agentic coding workflows):

1. **Mount or specify** the repository within your agent's workspace context.
2. **Direct the agent** to read the relevant `SKILL.md` file for the task at hand (e.g., "Please read `business-module-workflow/SKILL.md` before proceeding").
3. **Provide the task** or specific context. The AI will adopt the defined persona and follow the structured workflows to execute the task with significantly higher precision and structural compliance.

## 🛠️ Contribution & Expansion

When expanding this repository with a new skill:
1. Create a dedicated top-level directory for the new skill domain.
2. Define a comprehensive `SKILL.md` that explicitly dictates the rules of engagement and constraints for the AI.
3. Include reference materials (`references/`) to ground the AI's understanding with concrete examples.

---
*Built to empower intelligent agents with structured engineering workflows.*
