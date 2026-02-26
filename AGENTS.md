# my_AI_workspace

This workspace combines:
- oh-my-opencode as the OpenCode plugin layer
- superpowers as the workflow and methodology skill layer
- anthropic/open-source skills as an additional skill catalog
- OpenSpec as the spec-driven development workflow layer

Primary goals:
1. Local-first operation
2. Out-of-the-box developer productivity
3. Reproducible setup through scripts and pinned submodules

## Architecture

### Layer 1: oh-my-opencode (Plugin)
Registered in `.opencode/opencode.json`. Provides 11 agents (Sisyphus, Hephaestus,
Prometheus, Atlas, Oracle, Librarian, Explore, Metis, Momus, Multimodal-Looker),
3 MCPs (websearch, context7, grep_app), and built-in skills (playwright, git-master,
frontend-ui-ux). Project config at `.opencode/oh-my-opencode.jsonc`.

Use `ultrawork` or `ulw` in prompts to activate full agent orchestration.

### Layer 2: superpowers (Methodology)
Plugin at `~/.config/opencode/plugins/superpowers.js`, skills at
`~/.config/opencode/skills/superpowers/`. Provides 14 development methodology skills.

Key commands: `/brainstorm`, `/write-plan`, `/execute-plan`.
Workflow: brainstorm -> write plan -> execute plan with subagent-driven TDD.

### Layer 3: Anthropic Skills (Task Skills)
16 skills symlinked at `~/.config/opencode/skills/anthropic-*`.
Includes: frontend-design, mcp-builder, webapp-testing, skill-creator,
canvas-design, algorithmic-art, doc-coauthoring, and document skills (docx, pdf, pptx, xlsx).

### Layer 4: OpenSpec (Spec-Driven Development)
Skills at `.opencode/skills/openspec-*`, commands at `.opencode/command/opsx-*.md`.
Use `/opsx:propose` to start a spec-driven change, `/opsx:apply` to implement it.

## Profiles
Switch via `./scripts/switch-profile.sh <name>`:
- `minimal` — lightweight, fewer agents and MCPs
- `daily-dev` — balanced default
- `full-stack` — everything enabled

## Capability Registry

The canonical inventory of all agents, skills, commands, and MCPs lives in
`registry.yaml` (YAML, machine-readable) and `CATALOG.md` (Markdown, human-readable).

Both files are auto-generated. Regenerate after any change:
```bash
python3 scripts/gen-registry.py   # writes registry.yaml
python3 scripts/gen-catalog.py    # writes CATALOG.md from registry.yaml
```

To discover capabilities by category or vendor, read `registry.yaml` directly.

## Directory Layout
- `registry.yaml` — single source of truth for all workspace capabilities
- `CATALOG.md` — human-friendly Markdown view of the registry
- `config/` — template configs (OmO model assignments, copied to ~/.config on bootstrap)
- `vendor/` — git submodules (oh-my-opencode, superpowers, anthropic-skills, openspec)
- `profiles/` — OmO config presets
- `scripts/` — bootstrap.sh, doctor.sh, update.sh, switch-profile.sh, gen-registry.py, gen-catalog.py
- `skills/custom/` — place your own skills here
- `openspec/` — spec-driven development artifacts
