# Workspace Capability Catalog

> Auto-generated from `registry.yaml` — do not edit manually
> Re-generate: `python3 scripts/gen-catalog.py`

**Total: 59 entries** | 11 Agents | 41 Skills | 4 Commands | 3 MCPs
**Updated:** 2026-02-26

### By Vendor

| Vendor | Count |
|--------|-------|
| oh-my-opencode | 19 |
| anthropic-skills | 16 |
| superpowers | 14 |
| openspec | 8 |
| custom | 2 |

---

## Agents

| Name | Category | Model | Description | Profiles |
|------|----------|-------|-------------|----------|
| **sisyphus** | workflow | `anthropic/claude-opus-4-6` | Persistent task executor — primary orchestrator for complex multi-step work | daily-dev, full-stack, minimal |
| **hephaestus** | code-quality | `system-default` | Code generation specialist — crafts implementation from specs and plans | daily-dev, full-stack, minimal |
| **oracle** | ai-tooling | `anthropic/claude-opus-4-6` | Knowledge retrieval and deep question answering | daily-dev, full-stack |
| **librarian** | ai-tooling | `anthropic/claude-sonnet-4-5` | Codebase indexing, file discovery, and context gathering | daily-dev, full-stack, minimal |
| **explore** | ai-tooling | `anthropic/claude-haiku-4-5` | Fast codebase exploration — file search, grep, quick reads | daily-dev, full-stack, minimal |
| **atlas** | code-quality | `anthropic/claude-sonnet-4-5` | Large-scale refactoring and cross-file changes | daily-dev, full-stack, minimal |
| **prometheus** | workflow | `anthropic/claude-opus-4-6` | Architecture design and system-level reasoning | daily-dev, full-stack, minimal |
| **metis** | workflow | `anthropic/claude-opus-4-6` | Strategic planning and task decomposition | daily-dev, full-stack |
| **momus** | code-quality | `anthropic/claude-opus-4-6` | Code review and critical feedback | daily-dev, full-stack |
| **multimodal-looker** | ai-tooling | `anthropic/claude-haiku-4-5` | Image and visual content analysis | full-stack |
| **sisyphus-junior** | workflow | `system-default` | Lightweight task executor for simpler background work | daily-dev, full-stack, minimal |

---

## Skills

### Ai Tooling (4)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **agent-browser** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/agent-browser/SKILL.md` | Automates browser interactions for web testing, form filling, screenshots, an... | daily-dev, full-stack, minimal |
| **dev-browser** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/dev-browser/SKILL.md` | Browser automation with persistent page state. | daily-dev, full-stack, minimal |
| **mcp-builder** | anthropic-skills | `vendor/anthropic-skills/skills/mcp-builder/SKILL.md` | Guide for creating high-quality MCP (Model Context Protocol) servers that ena... | daily-dev, full-stack, minimal |
| **find-skills** | custom | `skills/custom/find-skills/SKILL.md` | Helps users discover agent skills — checks the local workspace registry first... | daily-dev, full-stack, minimal |

### Code Quality (3)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **receiving-code-review** | superpowers | `vendor/superpowers/skills/receiving-code-review/SKILL.md` | Use when receiving code review feedback, before implementing suggestions, esp... | daily-dev, full-stack, minimal |
| **requesting-code-review** | superpowers | `vendor/superpowers/skills/requesting-code-review/SKILL.md` | Use when completing tasks, implementing major features, or before merging to ... | daily-dev, full-stack, minimal |
| **code-simplifier** | custom | `skills/custom/code-simplifier/SKILL.md` | Simplifies and refines code for clarity, consistency, and maintainability whi... | daily-dev, full-stack, minimal |

### Creative (3)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **algorithmic-art** | anthropic-skills | `vendor/anthropic-skills/skills/algorithmic-art/SKILL.md` | Creating algorithmic art using p5.js with seeded randomness and interactive p... | daily-dev, full-stack, minimal |
| **slack-gif-creator** | anthropic-skills | `vendor/anthropic-skills/skills/slack-gif-creator/SKILL.md` | Knowledge and utilities for creating animated GIFs optimized for Slack. | daily-dev, full-stack, minimal |
| **theme-factory** | anthropic-skills | `vendor/anthropic-skills/skills/theme-factory/SKILL.md` | Toolkit for styling artifacts with a theme. | daily-dev, full-stack, minimal |

### Devops (3)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **git-master** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/git-master/SKILL.md` | MUST USE for ANY git operations. Atomic commits, rebase/squash, history searc... | daily-dev, full-stack, minimal |
| **github-triage** | oh-my-opencode | `vendor/oh-my-opencode/.opencode/skills/github-triage/SKILL.md` | Unified GitHub triage for issues AND PRs. | daily-dev, full-stack, minimal |
| **using-git-worktrees** | superpowers | `vendor/superpowers/skills/using-git-worktrees/SKILL.md` | Use when starting feature work that needs isolation from current workspace or... | daily-dev, full-stack, minimal |

### Documentation (6)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **doc-coauthoring** | anthropic-skills | `vendor/anthropic-skills/skills/doc-coauthoring/SKILL.md` | Guide users through a structured workflow for co-authoring documentation. | daily-dev, full-stack, minimal |
| **docx** | anthropic-skills | `vendor/anthropic-skills/skills/docx/SKILL.md` | Use this skill whenever the user wants to create, read, edit, or manipulate W... | daily-dev, full-stack, minimal |
| **internal-comms** | anthropic-skills | `vendor/anthropic-skills/skills/internal-comms/SKILL.md` | A set of resources to help me write all kinds of internal communications, usi... | daily-dev, full-stack, minimal |
| **pdf** | anthropic-skills | `vendor/anthropic-skills/skills/pdf/SKILL.md` | Use this skill whenever the user wants to do anything with PDF files. | daily-dev, full-stack, minimal |
| **pptx** | anthropic-skills | `vendor/anthropic-skills/skills/pptx/SKILL.md` | Use this skill any time a .pptx file is involved in any way — as input, outpu... | daily-dev, full-stack, minimal |
| **xlsx** | anthropic-skills | `vendor/anthropic-skills/skills/xlsx/SKILL.md` | Use this skill any time a spreadsheet file is the primary input or output. | daily-dev, full-stack, minimal |

### Frontend (5)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **frontend-ui-ux** | oh-my-opencode | `vendor/oh-my-opencode/src/features/builtin-skills/frontend-ui-ux/SKILL.md` | Designer-turned-developer who crafts stunning UI/UX even without design mockups | daily-dev, full-stack |
| **brand-guidelines** | anthropic-skills | `vendor/anthropic-skills/skills/brand-guidelines/SKILL.md` | Applies Anthropic's official brand colors and typography to any sort of artif... | daily-dev, full-stack, minimal |
| **canvas-design** | anthropic-skills | `vendor/anthropic-skills/skills/canvas-design/SKILL.md` | Create beautiful visual art in .png and . | daily-dev, full-stack, minimal |
| **frontend-design** | anthropic-skills | `vendor/anthropic-skills/skills/frontend-design/SKILL.md` | Create distinctive, production-grade frontend interfaces with high design qua... | daily-dev, full-stack, minimal |
| **web-artifacts-builder** | anthropic-skills | `vendor/anthropic-skills/skills/web-artifacts-builder/SKILL.md` | Suite of tools for creating elaborate, multi-component claude. | daily-dev, full-stack, minimal |

### Testing (5)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **finishing-a-development-branch** | superpowers | `vendor/superpowers/skills/finishing-a-development-branch/SKILL.md` | Use when implementation is complete, all tests pass, and you need to decide h... | daily-dev, full-stack, minimal |
| **systematic-debugging** | superpowers | `vendor/superpowers/skills/systematic-debugging/SKILL.md` | Use when encountering any bug, test failure, or unexpected behavior, before p... | daily-dev, full-stack, minimal |
| **test-driven-development** | superpowers | `vendor/superpowers/skills/test-driven-development/SKILL.md` | Use when implementing any feature or bugfix, before writing implementation code | daily-dev, full-stack, minimal |
| **verification-before-completion** | superpowers | `vendor/superpowers/skills/verification-before-completion/SKILL.md` | Use when about to claim work is complete, fixed, or passing, before committin... | daily-dev, full-stack, minimal |
| **webapp-testing** | anthropic-skills | `vendor/anthropic-skills/skills/webapp-testing/SKILL.md` | Toolkit for interacting with and testing local web applications using Playwri... | daily-dev, full-stack, minimal |

### Workflow (12)

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **brainstorming** | superpowers | `vendor/superpowers/skills/brainstorming/SKILL.md` | You MUST use this before any creative work - creating features, building comp... | daily-dev, full-stack, minimal |
| **dispatching-parallel-agents** | superpowers | `vendor/superpowers/skills/dispatching-parallel-agents/SKILL.md` | Use when facing 2+ independent tasks that can be worked on without shared sta... | daily-dev, full-stack, minimal |
| **executing-plans** | superpowers | `vendor/superpowers/skills/executing-plans/SKILL.md` | Use when you have a written implementation plan to execute in a separate sess... | daily-dev, full-stack, minimal |
| **subagent-driven-development** | superpowers | `vendor/superpowers/skills/subagent-driven-development/SKILL.md` | Use when executing implementation plans with independent tasks in the current... | daily-dev, full-stack, minimal |
| **using-superpowers** | superpowers | `vendor/superpowers/skills/using-superpowers/SKILL.md` | Use when starting any conversation - establishes how to find and use skills, ... | daily-dev, full-stack, minimal |
| **writing-plans** | superpowers | `vendor/superpowers/skills/writing-plans/SKILL.md` | Use when you have a spec or requirements for a multi-step task, before touchi... | daily-dev, full-stack, minimal |
| **writing-skills** | superpowers | `vendor/superpowers/skills/writing-skills/SKILL.md` | Use when creating new skills, editing existing skills, or verifying skills wo... | daily-dev, full-stack, minimal |
| **skill-creator** | anthropic-skills | `vendor/anthropic-skills/skills/skill-creator/SKILL.md` | Create new skills, modify and improve existing skills, and measure skill perf... | daily-dev, full-stack, minimal |
| **openspec-apply-change** | openspec | `.opencode/skills/openspec-apply-change/SKILL.md` | Implement tasks from an OpenSpec change. Use when the user wants to start imp... | daily-dev, full-stack, minimal |
| **openspec-archive-change** | openspec | `.opencode/skills/openspec-archive-change/SKILL.md` | Archive a completed change in the experimental workflow. Use when the user wa... | daily-dev, full-stack, minimal |
| **openspec-explore** | openspec | `.opencode/skills/openspec-explore/SKILL.md` | Enter explore mode - a thinking partner for exploring ideas, investigating pr... | daily-dev, full-stack, minimal |
| **openspec-propose** | openspec | `.opencode/skills/openspec-propose/SKILL.md` | Propose a new change with all artifacts generated in one step. | daily-dev, full-stack, minimal |

---

## Commands

| Command | Vendor | Path | Description | Profiles |
|---------|--------|------|-------------|----------|
| `/opsx-apply` | openspec | `.opencode/command/opsx-apply.md` | Implement tasks from an OpenSpec change (Experimental) | daily-dev, full-stack, minimal |
| `/opsx-archive` | openspec | `.opencode/command/opsx-archive.md` | Archive a completed change in the experimental workflow | daily-dev, full-stack, minimal |
| `/opsx-explore` | openspec | `.opencode/command/opsx-explore.md` | Enter explore mode - think through ideas, investigate problems, clarify requi... | daily-dev, full-stack, minimal |
| `/opsx-propose` | openspec | `.opencode/command/opsx-propose.md` | Propose a new change - create it and generate all artifacts in one step | daily-dev, full-stack, minimal |

---

## MCPs

| Name | Vendor | Path | Description | Profiles |
|------|--------|------|-------------|----------|
| **websearch** | oh-my-opencode | `vendor/oh-my-opencode/src/mcp/websearch.ts` | Web search via Exa/Tavily MCP | daily-dev, full-stack |
| **context7** | oh-my-opencode | `vendor/oh-my-opencode/src/mcp/context7.ts` | Library documentation lookup via Context7 MCP | daily-dev, full-stack, minimal |
| **grep_app** | oh-my-opencode | `vendor/oh-my-opencode/src/mcp/grep-app.ts` | Code search across public repositories via grep.app MCP | daily-dev, full-stack |

---

## Profile Legend

| Profile | Description |
|---------|-------------|
| minimal | Lightweight — fewer agents and MCPs, low concurrency |
| daily-dev | Balanced default for normal development |
| full-stack | Everything enabled, max concurrency |
