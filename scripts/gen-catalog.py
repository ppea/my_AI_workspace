#!/usr/bin/env python3
"""Generate CATALOG.md — human-friendly view of the workspace capability registry.

Reads registry.yaml and outputs a well-formatted Markdown document grouped by
type (Agents > Skills > Commands > MCPs) then by category.

Usage:
    python3 scripts/gen-catalog.py          # writes CATALOG.md at project root
    python3 scripts/gen-catalog.py --check  # exits non-zero if CATALOG.md is stale
"""

import sys
from datetime import date
from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT_DIR / "registry.yaml"
CATALOG_PATH = ROOT_DIR / "CATALOG.md"

TYPE_ORDER = ["agent", "skill", "command", "mcp"]
TYPE_LABELS = {
    "agent": "Agents",
    "skill": "Skills",
    "command": "Commands",
    "mcp": "MCPs",
}


def load_registry() -> dict:
    """Load and parse registry.yaml."""
    if not REGISTRY_PATH.is_file():
        print("Error: registry.yaml not found. Run gen-registry.py first.", file=sys.stderr)
        sys.exit(1)
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def truncate(text: str, max_len: int = 100) -> str:
    """Truncate text for table display."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def escape_pipe(text: str) -> str:
    """Escape pipe chars for Markdown tables."""
    return text.replace("|", "\\|")


def render_agent_table(entries: list[dict]) -> list[str]:
    """Render agents as a Markdown table."""
    lines = [
        "| Name | Category | Model | Description | Profiles |",
        "|------|----------|-------|-------------|----------|",
    ]
    for e in entries:
        name = f"**{e['name']}**"
        cat = e.get("category", "")
        model = e.get("model", "")
        desc = escape_pipe(truncate(e.get("description", ""), 80))
        profs = ", ".join(e.get("profiles", []))
        lines.append(f"| {name} | {cat} | `{model}` | {desc} | {profs} |")
    return lines


def render_skill_table(entries: list[dict]) -> list[str]:
    """Render skills as a Markdown table."""
    lines = [
        "| Name | Vendor | Path | Description | Profiles |",
        "|------|--------|------|-------------|----------|",
    ]
    for e in entries:
        name = f"**{e['name']}**"
        vendor = e.get("vendor", "")
        path = f"`{e.get('path', '')}`"
        desc = escape_pipe(truncate(e.get("description", ""), 80))
        profs = ", ".join(e.get("profiles", []))
        lines.append(f"| {name} | {vendor} | {path} | {desc} | {profs} |")
    return lines


def render_command_table(entries: list[dict]) -> list[str]:
    """Render commands as a Markdown table."""
    lines = [
        "| Command | Vendor | Path | Description | Profiles |",
        "|---------|--------|------|-------------|----------|",
    ]
    for e in entries:
        name = f"`/{e['name']}`"
        vendor = e.get("vendor", "")
        path = f"`{e.get('path', '')}`"
        desc = escape_pipe(truncate(e.get("description", ""), 80))
        profs = ", ".join(e.get("profiles", []))
        lines.append(f"| {name} | {vendor} | {path} | {desc} | {profs} |")
    return lines


def render_mcp_table(entries: list[dict]) -> list[str]:
    """Render MCPs as a Markdown table."""
    lines = [
        "| Name | Vendor | Path | Description | Profiles |",
        "|------|--------|------|-------------|----------|",
    ]
    for e in entries:
        name = f"**{e['name']}**"
        vendor = e.get("vendor", "")
        path = f"`{e.get('path', '')}`"
        desc = escape_pipe(truncate(e.get("description", ""), 80))
        profs = ", ".join(e.get("profiles", []))
        lines.append(f"| {name} | {vendor} | {path} | {desc} | {profs} |")
    return lines


TABLE_RENDERERS = {
    "agent": render_agent_table,
    "skill": render_skill_table,
    "command": render_command_table,
    "mcp": render_mcp_table,
}


def build_catalog(registry: dict) -> str:
    """Build the full CATALOG.md content from registry data."""
    meta = registry.get("meta", {})
    entries = registry.get("entries", [])
    total = meta.get("total_count", len(entries))
    counts = meta.get("counts", {})
    updated = meta.get("updated", str(date.today()))

    lines: list[str] = []

    # Header
    lines.append("# Workspace Capability Catalog")
    lines.append("")
    lines.append("> Auto-generated from `registry.yaml` — do not edit manually")
    lines.append(f"> Re-generate: `python3 scripts/gen-catalog.py`")
    lines.append("")

    # Summary stats
    parts = []
    for t in TYPE_ORDER:
        count = counts.get(t, 0)
        if count:
            parts.append(f"{count} {TYPE_LABELS.get(t, t)}")
    lines.append(f"**Total: {total} entries** | {' | '.join(parts)}")
    lines.append(f"**Updated:** {updated}")
    lines.append("")

    # Vendor summary
    vendors: dict[str, int] = {}
    for e in entries:
        v = e.get("vendor", "unknown")
        vendors[v] = vendors.get(v, 0) + 1
    lines.append("### By Vendor")
    lines.append("")
    lines.append("| Vendor | Count |")
    lines.append("|--------|-------|")
    for v, c in sorted(vendors.items(), key=lambda x: -x[1]):
        lines.append(f"| {v} | {c} |")
    lines.append("")

    # Sections by type
    for entry_type in TYPE_ORDER:
        type_entries = [e for e in entries if e.get("type") == entry_type]
        if not type_entries:
            continue

        label = TYPE_LABELS.get(entry_type, entry_type)
        lines.append(f"---")
        lines.append("")
        lines.append(f"## {label}")
        lines.append("")

        renderer = TABLE_RENDERERS[entry_type]

        if entry_type == "skill":
            # Group skills by category for better readability
            categories: dict[str, list[dict]] = {}
            for e in type_entries:
                cat = e.get("category", "uncategorized")
                categories.setdefault(cat, []).append(e)

            for cat in sorted(categories.keys()):
                cat_entries = categories[cat]
                lines.append(f"### {cat.replace('-', ' ').title()} ({len(cat_entries)})")
                lines.append("")
                lines.extend(renderer(cat_entries))
                lines.append("")
        else:
            lines.extend(renderer(type_entries))
            lines.append("")

    # Profile legend
    lines.append("---")
    lines.append("")
    lines.append("## Profile Legend")
    lines.append("")
    lines.append("| Profile | Description |")
    lines.append("|---------|-------------|")
    lines.append("| minimal | Lightweight — fewer agents and MCPs, low concurrency |")
    lines.append("| daily-dev | Balanced default for normal development |")
    lines.append("| full-stack | Everything enabled, max concurrency |")
    lines.append("")

    return "\n".join(lines)


def main():
    check_mode = "--check" in sys.argv
    registry = load_registry()
    new_content = build_catalog(registry)

    if check_mode:
        if CATALOG_PATH.is_file():
            existing = CATALOG_PATH.read_text(encoding="utf-8")
            if existing == new_content:
                print("CATALOG.md is up to date")
                sys.exit(0)
            else:
                print("CATALOG.md is STALE — run: python3 scripts/gen-catalog.py")
                sys.exit(1)
        else:
            print("CATALOG.md does not exist — run: python3 scripts/gen-catalog.py")
            sys.exit(1)

    CATALOG_PATH.write_text(new_content, encoding="utf-8")
    total = registry.get("meta", {}).get("total_count", 0)
    print(f"[gen-catalog] Wrote CATALOG.md — {total} entries")


if __name__ == "__main__":
    main()
