# Brainstorm → OpenSpec Auto-Registration Design

**Date**: 2026-02-28
**Status**: Approved
**Decision**: Local brainstorming skill override that adds OpenSpec registration as step 7

---

## Problem

The `/brainstorm` → `writing-plans` workflow produces design docs and implementation plans in `docs/plans/`, but these are never registered in OpenSpec. There's no way to track which plans are in-flight, in-progress, or completed. Each project (e.g. nextme) has its own `docs/plans/` but no OpenSpec lifecycle.

---

## Decision

Create `skills/custom/brainstorming/SKILL.md` — a local override of the superpowers brainstorming skill that adds **one extra step** at the end: auto-register the plan in OpenSpec.

User skills take priority over vendor skills (per AGENTS.md), so this override activates automatically whenever `skill(name="brainstorming")` is invoked. The vendor submodule is untouched.

---

## Data Flow

```
/brainstorm
  ↓
docs/plans/YYYY-MM-DD-<topic>-design.md          ← brainstorm output (unchanged)
  ↓
skill(writing-plans)
  ↓
docs/plans/YYYY-MM-DD-<topic>-implementation.md  ← writing-plans output (unchanged)
  ↓ ← NEW: step 7 — OpenSpec registration
openspec new change <topic>
  ├── openspec/changes/<topic>/proposal.md        ← auto-generated WHY summary
  ├── openspec/changes/<topic>/design.md          ← copied from docs/plans/*-design.md
  └── openspec/changes/<topic>/tasks.md           ← copied from docs/plans/*-implementation.md
  ↓
git commit "chore(openspec): register <topic> change"
```

---

## Project-Level Scoping

OpenSpec changes live **in the project being worked on**, not in the workspace. This mirrors `docs/plans/` scoping:

```
~/code/nextme/
├── docs/plans/                    ← nextme design docs
└── openspec/changes/              ← nextme change tracking (requires openspec init)

My_AI_workspace_227/
├── docs/plans/                    ← workspace design docs
└── openspec/changes/              ← workspace change tracking (already initialized)
```

**Pre-condition**: New projects require `openspec init` once before first use. The brainstorming skill override will detect if `openspec/` doesn't exist and run `openspec init` automatically.

---

## OpenSpec Artifact Mapping

| OpenSpec artifact | Source | Content |
|---|---|---|
| `proposal.md` | Auto-generated | 1-2 paragraph WHY summary derived from the design rationale |
| `design.md` | Copied | Full content of `docs/plans/YYYY-MM-DD-*-design.md` |
| `tasks.md` | Copied | Full content of `docs/plans/YYYY-MM-DD-*-implementation.md` |

Artifacts are **copied** (not referenced) so each OpenSpec change is self-contained and `/opsx-apply` works without needing to read `docs/plans/`.

---

## Full Lifecycle

```
/brainstorm                →  design + plan in docs/plans/ + OpenSpec change created
/opsx-apply                →  implement tasks (checkbox tracking in tasks.md)
/opsx-archive              →  marks change done, moves to openspec/specs/
```

---

## What Changes in the Repo

| File | Action |
|---|---|
| `skills/custom/brainstorming/SKILL.md` | **New** — local override with step 7 added |
| `vendor/superpowers/skills/brainstorming/` | **Untouched** — submodule stays clean |
| `docs/plans/` | **Unchanged** — still populated as before |
| `openspec/changes/<name>/` | **New** — auto-created at end of every brainstorm |

---

## Constraints

- `openspec` CLI must be available (`/opt/homebrew/bin/openspec` — confirmed v1.2.0)
- `openspec init` required once per new project before first use
- The brainstorming override must include the full original skill content — no behavior regression
- The added step 7 must be idempotent: if OpenSpec change with same name already exists, skip creation and log a notice
- Override skill uses `spec-driven` schema (default — only schema available in v1.2.0)
