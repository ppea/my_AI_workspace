# nextme/src/core/memory.py
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any

_structlog_module = importlib.import_module("structlog")
logger = _structlog_module.get_logger()


@dataclass
class MemoryItem:
    """A single memory entry."""
    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def format_memories_for_prompt(memories: list[MemoryItem]) -> str:
    """Format memories for injection into advisor prompts."""
    if not memories:
        return "No relevant memories found."
    lines = []
    for i, mem in enumerate(memories, 1):
        lines.append(f"- {mem.text}")
    return "Relevant memories:\n" + "\n".join(lines)


class MemoryManager:
    """Cross-session memory powered by Mem0."""

    def __init__(self, persist_dir: str = "data/mem0/",
                 llm_model: str = "gpt-4o-mini",
                 user_id: str = "owner"):
        self.persist_dir = persist_dir
        self.llm_model = llm_model
        self.user_id = user_id
        self._mem0: Any | None = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization of Mem0."""
        if self._initialized:
            return

        mem0_module = importlib.import_module("mem0")
        memory_cls = getattr(mem0_module, "Memory")

        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "nextme_memory",
                    "path": self.persist_dir,
                },
            },
        }

        self._mem0 = memory_cls.from_config(config)
        self._initialized = True
        logger.info("memory.initialized", persist_dir=self.persist_dir)

    def add(self, content: str, metadata: dict[str, Any] | None = None) -> str:
        """Store a memory. Returns memory ID."""
        self._ensure_initialized()
        assert self._mem0 is not None

        result = self._mem0.add(
            content,
            user_id=self.user_id,
            metadata=metadata or {},
        )
        memory_id = result.get("id", "") if isinstance(result, dict) else ""
        logger.info("memory.added", content_preview=content[:50], id=memory_id)
        return memory_id

    def search(self, query: str, limit: int = 10) -> list[MemoryItem]:
        """Search memories by semantic similarity."""
        self._ensure_initialized()
        assert self._mem0 is not None

        results = self._mem0.search(query, user_id=self.user_id, limit=limit)

        items = []
        for r in results:
            if isinstance(r, dict):
                raw_text = r.get("memory", r.get("text", ""))
                items.append(MemoryItem(
                    id=r.get("id", ""),
                    text=raw_text if isinstance(raw_text, str) else "",
                    metadata=r.get("metadata", {}),
                ))
        return items

    def get_advisor_context(self, advisor: str, query: str,
                            limit: int = 5) -> str:
        """Get formatted memories relevant to a specific advisor + query."""
        scoped_query = f"[{advisor}] {query}"
        memories = self.search(scoped_query, limit=limit)
        return format_memories_for_prompt(memories)

    def delete(self, memory_id: str) -> bool:
        """Delete a specific memory."""
        self._ensure_initialized()
        assert self._mem0 is not None

        try:
            self._mem0.delete(memory_id)
            logger.info("memory.deleted", id=memory_id)
            return True
        except Exception as e:
            logger.error("memory.delete_failed", id=memory_id, error=str(e))
            return False

    def list_all(self, limit: int = 100) -> list[MemoryItem]:
        """List all stored memories."""
        self._ensure_initialized()
        assert self._mem0 is not None

        results = self._mem0.get_all(user_id=self.user_id)

        items = []
        for r in (results if isinstance(results, list) else []):
            if isinstance(r, dict):
                raw_text = r.get("memory", r.get("text", ""))
                items.append(MemoryItem(
                    id=r.get("id", ""),
                    text=raw_text if isinstance(raw_text, str) else "",
                    metadata=r.get("metadata", {}),
                ))
        return items[:limit]

    def get_stats(self) -> dict[str, Any]:
        """Get memory statistics."""
        all_memories = self.list_all()
        return {
            "total_memories": len(all_memories),
            "persist_dir": self.persist_dir,
        }
