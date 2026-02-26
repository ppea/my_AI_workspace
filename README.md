# my_AI_workspace

Local-first OpenCode workspace integrating four complementary layers for
AI-assisted software development.

## Components

| Layer | Repository | Role |
|-------|-----------|------|
| **oh-my-opencode** | [code-yeongyu/oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) | Agent orchestration plugin (11 agents, 3 MCPs) |
| **superpowers** | [obra/superpowers](https://github.com/obra/superpowers) | Development methodology skills (TDD, planning, code review) |
| **anthropics/skills** | [anthropics/skills](https://github.com/anthropics/skills) | Task skills (frontend, docs, MCP builder, testing) |
| **OpenSpec** | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | Spec-driven development workflow |

## Prerequisites

- **Git** (any recent version)
- **Node.js** >= 20 and **npm** (or **Bun**)
- **OpenCode** >= 1.0.150 (`brew install anomalyco/tap/opencode`)
- An API key for at least one LLM provider (Anthropic recommended)

## Quick Start

```bash
git clone <this-repo> my-project
cd my-project
./scripts/bootstrap.sh
```

The bootstrap script will:
1. Initialize and sync all git submodules
2. Install oh-my-opencode via `npx`/`bunx`
3. Symlink superpowers plugin and skills
4. Symlink Anthropic skills
5. Install OpenSpec CLI and initialize project assets
6. Apply the `daily-dev` profile
7. Run `doctor.sh` to verify the setup

Then authenticate your provider:

```bash
opencode auth login
```

## Usage

Start OpenCode in your project directory:

```bash
cd my-project
opencode
```

### Key Commands

| Command | Source | Description |
|---------|--------|-------------|
| `ultrawork` / `ulw` | oh-my-opencode | Full agent orchestration in prompt |
| `/brainstorm` | superpowers | Socratic design refinement |
| `/write-plan` | superpowers | Create implementation plan |
| `/execute-plan` | superpowers | Execute plan with checkpoints |
| `/opsx:propose` | OpenSpec | Start a spec-driven change |
| `/opsx:apply` | OpenSpec | Implement tasks from spec |
| `/opsx:explore` | OpenSpec | Free-form exploration |
| `/opsx:archive` | OpenSpec | Archive completed change |

### Available Skills

**Superpowers (14):** brainstorming, dispatching-parallel-agents, executing-plans,
finishing-a-development-branch, receiving-code-review, requesting-code-review,
subagent-driven-development, systematic-debugging, test-driven-development,
using-git-worktrees, using-superpowers, verification-before-completion,
writing-plans, writing-skills

**Anthropic (16):** algorithmic-art, brand-guidelines, canvas-design,
doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder,
pdf, pptx, skill-creator, slack-gif-creator, theme-factory,
web-artifacts-builder, webapp-testing, xlsx

**OmO Built-in (3):** playwright, git-master, frontend-ui-ux

**OpenSpec (4):** openspec-propose, openspec-explore, openspec-apply-change,
openspec-archive-change

## Profile Presets

Switch the active OmO configuration:

```bash
./scripts/switch-profile.sh minimal      # lightweight, fewer agents/MCPs
./scripts/switch-profile.sh daily-dev    # balanced (default)
./scripts/switch-profile.sh full-stack   # everything enabled
```

Profiles are stored in `profiles/` and copied to `.opencode/oh-my-opencode.jsonc`.

## Maintenance

Update all submodules and regenerate OpenSpec assets:

```bash
./scripts/update.sh
```

Run diagnostics:

```bash
./scripts/doctor.sh
```

Re-link Anthropic skills after submodule update:

```bash
./scripts/install-anthropic-skills.sh
```

## Directory Layout

```
my_AI_workspace/
├── .opencode/              OpenCode config + OpenSpec skills/commands
├── config/                 Template configs (OmO model assignments)
├── vendor/                 Git submodules (oh-my-opencode, superpowers, etc.)
├── profiles/               OmO config presets (minimal, daily-dev, full-stack)
├── scripts/                Bootstrap, doctor, update, profile switching
├── skills/custom/          Your own skills (SKILL.md format)
├── openspec/               Spec-driven development artifacts
├── registry.yaml           Capability registry (auto-generated)
├── CATALOG.md              Human-readable capability catalog (auto-generated)
├── AGENTS.md               Agent context for OpenCode
└── README.md               This file
```

## Custom Skills

Create your own skills in `skills/custom/`:

```
skills/custom/my-skill/
  SKILL.md          # Required: YAML frontmatter + instructions
  helper.py         # Optional: supporting files
```

Format for `SKILL.md`:

```markdown
---
name: my-skill
description: Use when the user asks for X
---

# Instructions

Your skill instructions here.
```

## Notes

- Anthropic document skills (`docx`, `pdf`, `pptx`, `xlsx`) are source-available,
  not Apache 2.0. See `vendor/anthropic-skills/THIRD_PARTY_NOTICES.md`.
- The superpowers plugin and skills symlink into `~/.config/opencode/` (user-level).
- Project-level configs in `.opencode/` take priority over user-level.
