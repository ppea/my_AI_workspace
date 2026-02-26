# my_AI_workspace

Clone, bootstrap, code. A ready-to-use OpenCode workspace with **257 capabilities** out of the box.

```
git clone <this-repo> my-project && cd my-project && ./scripts/bootstrap.sh
```

## How It Works

```mermaid
graph TB
    You([You]) -->|opencode| OC[OpenCode CLI]

    OC --> L1
    OC --> L2
    OC --> L3
    OC --> L4

    subgraph L1 [oh-my-opencode]
        direction LR
        Agents[11 Agents]
        MCPs[3 MCPs]
        BuiltIn[3 Built-in Skills]
    end

    subgraph L2 [superpowers]
        direction LR
        SP[14 Methodology Skills]
    end

    subgraph L3 [Skill Catalogs]
        direction LR
        AN[Anthropic 16 Skills]
        CP[Copilot 198 Skills]
    end

    subgraph L4 [OpenSpec]
        direction LR
        OS[4 Skills + 4 Commands]
    end

    L1 --> LLM[LLM Provider]
    LLM --> GH[GitHub Copilot]
    LLM --> API[Anthropic / OpenAI API]

    style You fill:#f9f,stroke:#333
    style OC fill:#4a9eff,stroke:#333,color:#fff
    style L1 fill:#ff6b6b22,stroke:#ff6b6b
    style L2 fill:#ffd93d22,stroke:#ffd93d
    style L3 fill:#6bcb7722,stroke:#6bcb77
    style L4 fill:#4d96ff22,stroke:#4d96ff
```

## Quick Start

### 1. Install prerequisites

```bash
brew install git node anomalyco/tap/opencode
```

### 2. Clone and bootstrap

```bash
git clone <this-repo> my-project
cd my-project
./scripts/bootstrap.sh
```

### 3. Authenticate

```bash
opencode auth login    # select GitHub Copilot, Anthropic, or OpenAI
```

### 4. Start coding

```bash
opencode
```

That's it. All 257 capabilities are ready to use.

## What's Inside

```mermaid
graph LR
    subgraph Agents
        S[Sisyphus<br/>Orchestrator]
        H[Hephaestus<br/>Code Gen]
        P[Prometheus<br/>Architecture]
        O[Oracle<br/>Knowledge]
        A[Atlas<br/>Refactoring]
        M[Metis<br/>Planning]
        Mo[Momus<br/>Code Review]
        Li[Librarian<br/>Context]
        Ex[Explore<br/>Search]
        ML[Multimodal<br/>Vision]
        SJ[Sisyphus Jr<br/>Light Tasks]
    end

    subgraph MCPs
        WS[websearch]
        C7[context7]
        GA[grep_app]
    end

    subgraph Skills [239 Skills]
        direction TB
        SP[Superpowers x14<br/>TDD, Planning, Review]
        AN[Anthropic x16<br/>Frontend, Docs, MCP]
        CP[Copilot x198<br/>DevOps, Testing, CI/CD,<br/>Refactoring, Security,<br/>MCP Generators, ...]
        BI[Built-in x3<br/>Playwright, Git, UI/UX]
        OX[OpenSpec x4<br/>Spec-driven Dev]
        CU[Custom x2+<br/>Your own skills]
    end

    style Agents fill:#ff6b6b11,stroke:#ff6b6b
    style MCPs fill:#4d96ff11,stroke:#4d96ff
    style Skills fill:#6bcb7711,stroke:#6bcb77
```

## Key Commands

| Command | What It Does |
|---------|-------------|
| `ultrawork` (or `ulw`) | Full multi-agent orchestration |
| `/brainstorm` | Socratic design refinement |
| `/write-plan` | Create an implementation plan |
| `/execute-plan` | Execute plan with TDD checkpoints |
| `/opsx:propose` | Start a spec-driven change |
| `/opsx:apply` | Implement tasks from a spec |

## Profiles

Switch how much capability is active:

```bash
./scripts/switch-profile.sh <profile>
```

```mermaid
graph LR
    subgraph minimal
        direction TB
        m1[7 agents]
        m2[1 MCP]
        m3[1 skill built-in]
    end

    subgraph daily-dev [daily-dev default]
        direction TB
        d1[10 agents]
        d2[3 MCPs]
        d3[all skills]
    end

    subgraph full-stack
        direction TB
        f1[11 agents]
        f2[3 MCPs]
        f3[all skills]
        f4[auto_resume]
    end

    minimal -->|more| daily-dev -->|max| full-stack

    style minimal fill:#ffd93d22,stroke:#ffd93d
    style daily-dev fill:#6bcb7722,stroke:#6bcb77
    style full-stack fill:#ff6b6b22,stroke:#ff6b6b
```

## Bootstrap Flow

```mermaid
flowchart TD
    A[git clone] --> B[bootstrap.sh]
    B --> C[Init submodules]
    C --> D[Install oh-my-opencode]
    D --> E[Copy model config]
    E --> F[Symlink skills]
    F --> F1[superpowers 14]
    F --> F2[anthropic 16]
    F --> F3[copilot 198]
    F --> F4[custom 2+]
    F1 & F2 & F3 & F4 --> G[Init OpenSpec]
    G --> H[Apply daily-dev profile]
    H --> I[Generate registry]
    I --> J[Run doctor.sh]
    J --> K{All checks pass?}
    K -->|Yes| L[Ready to use]
    K -->|No| M[Fix warnings and re-run]

    style L fill:#6bcb77,stroke:#333,color:#fff
    style M fill:#ffd93d,stroke:#333
```

## Directory Layout

```
my-project/
├── .opencode/                # OpenCode config + OpenSpec commands
├── config/                   # Template configs (model assignments)
├── vendor/                   # Git submodules (5 repos)
│   ├── oh-my-opencode/       #   agents + MCPs + built-in skills
│   ├── superpowers/          #   methodology skills
│   ├── anthropic-skills/     #   task skills
│   ├── awesome-copilot/      #   community skills (198)
│   └── openspec/             #   spec-driven dev
├── profiles/                 # minimal / daily-dev / full-stack
├── scripts/                  # bootstrap, doctor, update, switch-profile
├── skills/custom/            # your own skills go here
├── registry.yaml             # capability registry (auto-generated)
└── CATALOG.md                # human-readable catalog (auto-generated)
```

## Add Your Own Skills

Create `skills/custom/<name>/SKILL.md`:

```markdown
---
name: my-skill
description: Use when the user asks for X
---

# Instructions

Your skill instructions here.
```

Run `./scripts/bootstrap.sh` to symlink it, or manually:

```bash
ln -s "$(pwd)/skills/custom/my-skill" ~/.config/opencode/skills/custom-my-skill
```

## Maintenance

```bash
./scripts/update.sh          # update submodules + regenerate registry
./scripts/doctor.sh          # run health checks
./scripts/switch-profile.sh  # switch active profile
```

## Components

| Layer | Repository | Count |
|-------|-----------|-------|
| oh-my-opencode | [code-yeongyu/oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) | 11 agents, 3 MCPs, 3 skills |
| superpowers | [obra/superpowers](https://github.com/obra/superpowers) | 14 skills |
| anthropics/skills | [anthropics/skills](https://github.com/anthropics/skills) | 16 skills |
| awesome-copilot | [github/awesome-copilot](https://github.com/github/awesome-copilot) | 198 skills |
| OpenSpec | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | 4 skills, 4 commands |
| custom | your own | 2+ skills |
