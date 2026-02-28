# lifeos/src/mcp/server.py
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

import structlog

logger = structlog.get_logger()

server = Server("lifeos")

# Lazy-loaded shared instances
_rag: Any = None
_memory: Any = None


def _get_rag() -> Any:
    global _rag
    if _rag is None:
        from src.core.rag import RAGPipeline
        _rag = RAGPipeline()
    return _rag


def _get_memory() -> Any:
    global _memory
    if _memory is None:
        from src.core.memory import MemoryManager
        _memory = MemoryManager()
    return _memory


@server.list_tools()  # type: ignore[untyped-decorator,no-untyped-call]
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="rag_search",
            description="Search the personal knowledge base via RAG. Returns relevant document chunks.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "advisor": {"type": "string", "description": "Optional: scope to advisor domain (health, finance, schedule, etc.)"},
                    "top_k": {"type": "integer", "description": "Number of results (default 5)", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="memory_recall",
            description="Search long-term memory for relevant personal context (preferences, decisions, facts).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to recall"},
                    "limit": {"type": "integer", "description": "Max results (default 10)", "default": 10},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="memory_save",
            description="Save an important fact, preference, or decision to long-term memory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Memory to save"},
                    "advisor": {"type": "string", "description": "Related advisor domain"},
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="note_add",
            description="Add a note to the personal knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Note content"},
                    "area": {"type": "string", "description": "Knowledge area (health, finance, schedule, etc.)", "default": "inbox"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for the note"},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="note_search",
            description="Search notes in the knowledge base by keyword.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "area": {"type": "string", "description": "Optional: limit to specific area"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_advisor_prompt",
            description="Load a domain advisor's system prompt. The LLM should adopt this persona when responding.",
            inputSchema={
                "type": "object",
                "properties": {
                    "advisor": {
                        "type": "string",
                        "description": "Advisor name: health, finance, schedule, career, legal, family, mental_health, learning, entrepreneurship",
                    },
                },
                "required": ["advisor"],
            },
        ),
        Tool(
            name="system_status",
            description="Get LifeOS system health status (RAG index, memory count, advisors).",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()  # type: ignore[untyped-decorator]
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    match name:
        case "rag_search":
            rag = _get_rag()
            advisor = arguments.get("advisor")
            top_k = arguments.get("top_k", 5)
            if advisor:
                result = rag.query_for_advisor(arguments["query"], advisor, top_k=top_k)
            else:
                result = rag.query(arguments["query"], top_k=top_k)

            if not result.chunks:
                return [TextContent(type="text", text="No relevant documents found.")]

            parts = []
            for chunk in result.chunks:
                source = chunk.source
                parts.append(f"**Source:** {source}\n{chunk.text}")
            return [TextContent(type="text", text="\n\n---\n\n".join(parts))]

        case "memory_recall":
            memory = _get_memory()
            results = memory.search(arguments["query"], limit=arguments.get("limit", 10))
            if not results:
                return [TextContent(type="text", text="No relevant memories found.")]
            lines = [f"- {m.text}" for m in results]
            return [TextContent(type="text", text="Relevant memories:\n" + "\n".join(lines))]

        case "memory_save":
            memory = _get_memory()
            metadata = {}
            if "advisor" in arguments:
                metadata["advisor"] = arguments["advisor"]
            memory_id = memory.add(arguments["content"], metadata=metadata)
            return [TextContent(type="text", text=f"✅ Memory saved (ID: {memory_id})")]

        case "note_add":
            text = arguments["text"]
            area = arguments.get("area", "inbox")
            tags = arguments.get("tags", [])
            today = date.today().isoformat()

            area_dir = Path(f"knowledge/areas/{area}" if area != "inbox" else "knowledge/inbox")
            area_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{today}-note.md"
            filepath = area_dir / filename

            if filepath.exists():
                with open(filepath, "a") as f:
                    f.write(f"\n\n## {today}\n{text}\n")
            else:
                frontmatter = (
                    f"---\ntype: note\ndate: {today}\ntags: {tags}\n"
                    f"advisor: {area}\nconfidentiality: normal\n---\n\n"
                    f"# Note — {today}\n\n{text}\n"
                )
                filepath.write_text(frontmatter)

            return [TextContent(type="text", text=f"📝 Note saved to {filepath}")]

        case "note_search":
            rag = _get_rag()
            query = arguments["query"]
            area = arguments.get("area")
            if area:
                result = rag.query_for_advisor(query, area)
            else:
                result = rag.query(query)
            if not result.chunks:
                return [TextContent(type="text", text="No matching notes found.")]
            parts = [f"**{c.source}**\n{c.text[:200]}..." for c in result.chunks]
            return [TextContent(type="text", text="\n\n".join(parts))]

        case "get_advisor_prompt":
            advisor_name = arguments["advisor"]
            prompts = _load_advisor_prompts()
            if advisor_name not in prompts:
                return [TextContent(type="text", text=f"Unknown advisor: {advisor_name}. Available: {', '.join(prompts.keys())}")]
            return [TextContent(type="text", text=prompts[advisor_name])]

        case "system_status":
            parts = ["**LifeOS System Status**\n"]
            try:
                rag = _get_rag()
                stats = rag.get_stats()
                parts.append(f"RAG Index: ✅ {stats['document_count']} documents")
            except Exception as e:
                parts.append(f"RAG Index: ❌ {e}")
            try:
                memory = _get_memory()
                stats = memory.get_stats()
                parts.append(f"Memory: ✅ {stats['total_memories']} memories")
            except Exception as e:
                parts.append(f"Memory: ❌ {e}")
            return [TextContent(type="text", text="\n".join(parts))]

        case _:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]


def _load_advisor_prompts() -> dict[str, str]:
    """Load all advisor prompts."""
    prompts: dict[str, str] = {}
    try:
        from src.advisors.health.prompts import SYSTEM_PROMPT as health_prompt
        prompts["health"] = f"## You are now: Health Management Advisor\n\n{health_prompt}"
    except ImportError:
        pass
    try:
        from src.advisors.schedule.prompts import SYSTEM_PROMPT as schedule_prompt
        prompts["schedule"] = f"## You are now: Schedule & Productivity Advisor\n\n{schedule_prompt}"
    except ImportError:
        pass
    return prompts


async def main() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
