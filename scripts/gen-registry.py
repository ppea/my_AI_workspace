#!/usr/bin/env python3
"""Generate registry.yaml — single source of truth for all workspace capabilities.

Scans vendor directories for SKILL.md frontmatter, reads profile configs to determine
which entries are active per profile, and emits a structured YAML registry.

Usage:
    python3 scripts/gen-registry.py          # writes registry.yaml at project root
    python3 scripts/gen-registry.py --check  # exits non-zero if registry.yaml is stale
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Category inference from skill name / description
# ---------------------------------------------------------------------------

# Explicit overrides for entries where keyword heuristics fail
CATEGORY_OVERRIDES = {
    # Agents
    "sisyphus": "workflow",
    "hephaestus": "code-quality",
    "oracle": "ai-tooling",
    "librarian": "ai-tooling",
    "explore": "ai-tooling",
    "atlas": "code-quality",
    "prometheus": "workflow",
    "metis": "workflow",
    "momus": "code-quality",
    "multimodal-looker": "ai-tooling",
    "sisyphus-junior": "workflow",
    # Superpowers skills
    "brainstorming": "workflow",
    "dispatching-parallel-agents": "workflow",
    "requesting-code-review": "code-quality",
    "receiving-code-review": "code-quality",
    "using-superpowers": "workflow",
    "writing-plans": "workflow",
    "writing-skills": "workflow",
    # Anthropic skills
    "mcp-builder": "ai-tooling",
    "web-artifacts-builder": "frontend",
    # OpenSpec
    "openspec-explore": "workflow",
    "openspec-propose": "workflow",
    # Custom
    "code-simplifier": "code-quality",
    "find-skills": "ai-tooling",
}

CATEGORY_KEYWORDS = {
    "security": ["security", "threat", "vulnerability", "audit", "pentest"],
    "testing": ["test", "webapp-testing", "qa", "verification", "debugging"],
    "frontend": ["frontend", "ui", "ux", "design", "css", "canvas", "theme", "brand"],
    "devops": ["ci", "deploy", "docker", "cloudflare", "vercel", "git", "worktree"],
    "documentation": ["doc", "readme", "coauthoring", "writing-doc", "comms", "pptx", "docx", "pdf", "xlsx"],
    "workflow": ["plan", "brainstorm", "dispatch", "execute", "finish",
                 "propose", "explore", "apply", "archive", "skill-creator", "superpower"],
    "ai-tooling": ["mcp", "agent", "browser", "websearch", "context7", "grep",
                    "multimodal", "oracle", "librarian", "looker"],
    "code-quality": ["refactor", "lint", "clean", "dead-code", "code-review", "review"],
    "creative": ["algorithmic-art", "gif", "slack-gif", "art", "artifacts"],
}


def infer_category(name: str, description: str = "") -> str:
    """Return the best-guess category for an entry based on name + description."""
    # Check explicit overrides first
    if name in CATEGORY_OVERRIDES:
        return CATEGORY_OVERRIDES[name]
    text = f"{name} {description}".lower()
    scores: dict[str, int] = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[cat] = scores.get(cat, 0) + 1
    if scores:
        return max(scores, key=scores.__getitem__)
    return "workflow"


# ---------------------------------------------------------------------------
# YAML frontmatter parser
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a SKILL.md or command .md file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


# ---------------------------------------------------------------------------
# Profile loader — determine which entries are disabled per profile
# ---------------------------------------------------------------------------

def strip_jsonc_comments(text: str) -> str:
    """Remove single-line // comments from JSONC, preserving // inside strings."""
    result: list[str] = []
    i = 0
    in_string = False
    while i < len(text):
        ch = text[i]
        if in_string:
            result.append(ch)
            if ch == "\\" and i + 1 < len(text):
                i += 1
                result.append(text[i])
            elif ch == '"':
                in_string = False
        elif ch == '"':
            in_string = True
            result.append(ch)
        elif ch == "/" and i + 1 < len(text) and text[i + 1] == "/":
            # skip to end of line
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        else:
            result.append(ch)
        i += 1
    return "".join(result)


def load_profiles() -> dict[str, dict]:
    """Load profile configs (JSONC with // comments) and return parsed dicts."""
    profiles_dir = ROOT_DIR / "profiles"
    profiles = {}
    for p in sorted(profiles_dir.glob("*.jsonc")):
        name = p.stem
        text = p.read_text(encoding="utf-8")
        text = strip_jsonc_comments(text)
        try:
            profiles[name] = json.loads(text)
        except json.JSONDecodeError:
            profiles[name] = {}
    return profiles


def entry_profiles(entry_type: str, entry_name: str, profiles: dict[str, dict]) -> list[str]:
    """Return the list of profile names where this entry is NOT disabled."""
    key_map = {
        "agent": "disabled_agents",
        "skill": "disabled_skills",
        "mcp": "disabled_mcps",
        "command": None,  # commands are never disabled by profiles
    }
    disable_key = key_map.get(entry_type)
    active = []
    for pname, pdata in sorted(profiles.items()):
        if disable_key is None:
            # commands are always active
            active.append(pname)
            continue
        disabled_list = pdata.get(disable_key, [])
        if entry_name not in disabled_list:
            active.append(pname)
    return active


# ---------------------------------------------------------------------------
# Scanners — one per source type
# ---------------------------------------------------------------------------

def scan_skill_dirs(base_dir: Path, vendor: str, path_prefix: str,
                    profiles: dict[str, dict]) -> list[dict]:
    """Scan a directory of skills (each subdir has SKILL.md) and return entries."""
    entries = []
    if not base_dir.is_dir():
        return entries
    for skill_dir in sorted(base_dir.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        fm = parse_frontmatter(skill_md)
        name = fm.get("name", skill_dir.name)
        desc = fm.get("description", "")
        # Truncate long descriptions to first sentence
        if len(desc) > 200:
            dot_idx = desc.find(".", 40)
            if dot_idx > 0:
                desc = desc[: dot_idx + 1]
            else:
                desc = desc[:200] + "..."
        entry: dict = {
            "name": name,
            "type": "skill",
            "category": infer_category(name, desc),
            "vendor": vendor,
            "path": f"{path_prefix}/{skill_dir.name}/SKILL.md",
            "description": desc,
            "profiles": entry_profiles("skill", name, profiles),
        }
        entries.append(entry)
    return entries


def scan_omo_agents(profiles: dict[str, dict]) -> list[dict]:
    """Return hardcoded OmO agent entries (agents are defined in TS, not SKILL.md)."""
    agents_raw = [
        ("sisyphus", "Persistent task executor — primary orchestrator for complex multi-step work", "github-copilot/claude-opus-4.6"),
        ("hephaestus", "Code generation specialist — crafts implementation from specs and plans", "system-default"),
        ("oracle", "Knowledge retrieval and deep question answering", "github-copilot/claude-opus-4.6"),
        ("librarian", "Codebase indexing, file discovery, and context gathering", "github-copilot/claude-sonnet-4.5"),
        ("explore", "Fast codebase exploration — file search, grep, quick reads", "github-copilot/claude-haiku-4.5"),
        ("atlas", "Large-scale refactoring and cross-file changes", "github-copilot/claude-sonnet-4.5"),
        ("prometheus", "Architecture design and system-level reasoning", "github-copilot/claude-opus-4.6"),
        ("metis", "Strategic planning and task decomposition", "github-copilot/claude-opus-4.6"),
        ("momus", "Code review and critical feedback", "github-copilot/claude-opus-4.6"),
        ("multimodal-looker", "Image and visual content analysis", "github-copilot/claude-haiku-4.5"),
        ("sisyphus-junior", "Lightweight task executor for simpler background work", "system-default"),
    ]
    entries = []
    for name, desc, model in agents_raw:
        entry: dict = {
            "name": name,
            "type": "agent",
            "category": infer_category(name, desc),
            "vendor": "oh-my-opencode",
            "path": "vendor/oh-my-opencode/src/agents/",
            "model": model,
            "description": desc,
            "profiles": entry_profiles("agent", name, profiles),
        }
        entries.append(entry)
    return entries


def scan_omo_mcps(profiles: dict[str, dict]) -> list[dict]:
    """Return hardcoded OmO MCP entries."""
    mcps_raw = [
        ("websearch", "Web search via Exa/Tavily MCP", "vendor/oh-my-opencode/src/mcp/websearch.ts"),
        ("context7", "Library documentation lookup via Context7 MCP", "vendor/oh-my-opencode/src/mcp/context7.ts"),
        ("grep_app", "Code search across public repositories via grep.app MCP", "vendor/oh-my-opencode/src/mcp/grep-app.ts"),
    ]
    entries = []
    for name, desc, path in mcps_raw:
        entry: dict = {
            "name": name,
            "type": "mcp",
            "category": "ai-tooling",
            "vendor": "oh-my-opencode",
            "path": path,
            "description": desc,
            "profiles": entry_profiles("mcp", name, profiles),
        }
        entries.append(entry)
    return entries


def scan_commands(profiles: dict[str, dict]) -> list[dict]:
    """Scan .opencode/command/*.md for slash commands."""
    cmd_dir = ROOT_DIR / ".opencode" / "command"
    entries = []
    if not cmd_dir.is_dir():
        return entries
    for cmd_file in sorted(cmd_dir.glob("*.md")):
        fm = parse_frontmatter(cmd_file)
        name = cmd_file.stem  # e.g. "opsx-propose"
        desc = fm.get("description", "")
        vendor = "openspec" if name.startswith("opsx") else "unknown"
        entry: dict = {
            "name": name,
            "type": "command",
            "category": "workflow",
            "vendor": vendor,
            "path": f".opencode/command/{cmd_file.name}",
            "description": desc,
            "profiles": entry_profiles("command", name, profiles),
        }
        entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_registry() -> dict:
    """Build the full registry dict."""
    profiles = load_profiles()

    all_entries: list[dict] = []

    # 1. OmO agents (hardcoded — defined in TypeScript, not SKILL.md)
    all_entries.extend(scan_omo_agents(profiles))

    # 2. OmO built-in skills
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / "vendor" / "oh-my-opencode" / "src" / "features" / "builtin-skills",
        vendor="oh-my-opencode",
        path_prefix="vendor/oh-my-opencode/src/features/builtin-skills",
        profiles=profiles,
    ))
    # Also check OmO's own .opencode/skills/
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / "vendor" / "oh-my-opencode" / ".opencode" / "skills",
        vendor="oh-my-opencode",
        path_prefix="vendor/oh-my-opencode/.opencode/skills",
        profiles=profiles,
    ))

    # 3. OmO MCPs
    all_entries.extend(scan_omo_mcps(profiles))

    # 4. Superpowers skills
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / "vendor" / "superpowers" / "skills",
        vendor="superpowers",
        path_prefix="vendor/superpowers/skills",
        profiles=profiles,
    ))

    # 5. Anthropic skills
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / "vendor" / "anthropic-skills" / "skills",
        vendor="anthropic-skills",
        path_prefix="vendor/anthropic-skills/skills",
        profiles=profiles,
    ))

    # 6. OpenSpec project-level skills
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / ".opencode" / "skills",
        vendor="openspec",
        path_prefix=".opencode/skills",
        profiles=profiles,
    ))

    # 7. Commands
    all_entries.extend(scan_commands(profiles))

    # 8. Custom skills (user's own)
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / "skills" / "custom",
        vendor="custom",
        path_prefix="skills/custom",
        profiles=profiles,
    ))

    # 9. Awesome-Copilot skills (github/awesome-copilot)
    all_entries.extend(scan_skill_dirs(
        ROOT_DIR / "vendor" / "awesome-copilot" / "skills",
        vendor="awesome-copilot",
        path_prefix="vendor/awesome-copilot/skills",
        profiles=profiles,
    ))

    # Collect unique categories
    categories = sorted({e["category"] for e in all_entries})

    # Counts by type
    counts = {}
    for e in all_entries:
        counts[e["type"]] = counts.get(e["type"], 0) + 1

    registry = {
        "meta": {
            "version": 1,
            "updated": str(date.today()),
            "total_count": len(all_entries),
            "counts": counts,
        },
        "categories": categories,
        "entries": all_entries,
    }
    return registry


def main():
    check_mode = "--check" in sys.argv

    registry = build_registry()
    output_path = ROOT_DIR / "registry.yaml"

    # Custom YAML representer to get clean multi-line strings and flow-style lists
    class CleanDumper(yaml.SafeDumper):
        pass

    # Represent lists of short strings in flow style (e.g. profiles: [minimal, daily-dev])
    def represent_str_list(dumper, data):
        if all(isinstance(item, str) and len(item) < 30 for item in data):
            return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)
        return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=False)

    CleanDumper.add_representer(list, represent_str_list)

    new_content = yaml.dump(
        registry,
        Dumper=CleanDumper,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )

    # Prepend header comment
    header = (
        "# registry.yaml — Workspace Capability Registry\n"
        "# Auto-generated by scripts/gen-registry.py — do not edit manually\n"
        "# Re-generate: python3 scripts/gen-registry.py\n"
        "#\n"
        "# This file is the single source of truth for all agents, skills,\n"
        "# commands, and MCPs in the workspace. AI agents can read this file\n"
        "# to discover available capabilities.\n"
        "\n"
    )
    new_content = header + new_content

    if check_mode:
        if output_path.is_file():
            existing = output_path.read_text(encoding="utf-8")
            if existing == new_content:
                print("registry.yaml is up to date")
                sys.exit(0)
            else:
                print("registry.yaml is STALE — run: python3 scripts/gen-registry.py")
                sys.exit(1)
        else:
            print("registry.yaml does not exist — run: python3 scripts/gen-registry.py")
            sys.exit(1)

    output_path.write_text(new_content, encoding="utf-8")
    n = registry["meta"]["total_count"]
    counts = registry["meta"]["counts"]
    parts = [f"{counts.get(t, 0)} {t}s" for t in ["agent", "skill", "command", "mcp"]]
    print(f"[gen-registry] Wrote registry.yaml — {n} entries ({', '.join(parts)})")


if __name__ == "__main__":
    main()
