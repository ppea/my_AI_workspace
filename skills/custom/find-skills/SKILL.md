---
name: find-skills
description: >-
  Helps users discover agent skills — checks the local workspace registry first,
  then searches the remote skills.sh ecosystem. Use when users ask "how do I do X",
  "find a skill for X", "is there a skill that can...", or want to extend capabilities.
---

# Find Skills

Discover and install agent skills. **Always check local inventory first**, then
search the remote ecosystem if needed.

## When to Use This Skill

- User asks "how do I do X" where X might be a common task with an existing skill
- User says "find a skill for X" or "is there a skill for X"
- User asks "can you do X" where X is a specialized capability
- User wants to search for tools, templates, or workflows
- User mentions they wish they had help with a specific domain

## Step 1: Check Local Registry First

Before searching remotely, check the workspace's own capability registry:

```bash
cat registry.yaml
```

This file contains ALL locally installed agents, skills, commands, and MCPs with
their categories, vendors, paths, and descriptions. Filter by category or keyword
to find matches.

**Also check the human-readable catalog:**

```bash
cat CATALOG.md
```

If a matching capability is found locally, tell the user:
- The skill/agent name and what it does
- Which vendor it comes from
- Which profiles it's available in
- How to use it (e.g. skill trigger phrases, slash commands)

**Only proceed to Step 2 if no local match is found.**

## Step 2: Search the Remote Ecosystem

If no local skill matches, use the Skills CLI to search the open agent skills
ecosystem:

```bash
npx skills find [query]
```

Examples:
- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

The command searches https://skills.sh/ and returns matching skills with install
commands.

## Step 3: Present Options

When you find relevant skills (local or remote), present them clearly:

### For local skills:
```
Found locally! The "frontend-design" skill (from anthropic-skills) creates
production-grade frontend interfaces. It's already installed and active in
your daily-dev and full-stack profiles.
```

### For remote skills:
```
I found a skill that might help! The "vercel-react-best-practices" skill
provides React/Next.js optimization guidelines from Vercel Engineering.

To install it:
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -y

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

## Step 4: Install Remote Skills (with user confirmation)

If the user wants to install a remote skill, run:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (to `~/.config/opencode/skills/`).
The `-y` flag skips confirmation prompts.

After installation, remind the user to regenerate the registry:

```bash
python3 scripts/gen-registry.py && python3 scripts/gen-catalog.py
```

## Common Skill Categories

| Category | Example Queries | Local Sources |
|----------|----------------|---------------|
| Web Development | react, nextjs, typescript, css | anthropic-skills, superpowers |
| Testing | testing, jest, playwright, e2e | superpowers, anthropic-skills |
| DevOps | deploy, docker, git, ci-cd | superpowers, oh-my-opencode |
| Documentation | docs, readme, docx, pdf, pptx | anthropic-skills |
| Code Quality | review, refactor, lint, simplify | superpowers, custom |
| Design | ui, ux, design-system, canvas | anthropic-skills, oh-my-opencode |
| Workflow | brainstorm, plan, execute, spec | superpowers, openspec |
| AI Tooling | mcp, browser, search, agent | oh-my-opencode |

## When No Skills Are Found

If neither local registry nor remote search finds a match:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using general capabilities
3. Suggest creating a custom skill:
   ```bash
   npx skills init my-custom-skill
   # Then place it in skills/custom/my-custom-skill/
   ```

## Tips

- **Local first**: The workspace already has 50+ skills — check registry.yaml before
  going remote
- **Use specific keywords**: "react testing" beats just "testing"
- **Try alternative terms**: "deploy" → "deployment" or "ci-cd"
- **Browse online**: https://skills.sh/ for the full ecosystem catalog
