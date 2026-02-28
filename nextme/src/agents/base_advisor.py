# nextme/src/agents/base_advisor.py
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import structlog

from src.core.context import ConversationContext
from src.core.memory import MemoryManager, format_memories_for_prompt
from src.core.rag import RAGPipeline

logger = structlog.get_logger()


@dataclass
class AdvisorResponse:
    """Structured response from an advisor."""
    text: str
    advisor: str
    action_items: list[str] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    reminders: list[dict[str, Any]] = field(default_factory=list)


class BaseAdvisor(ABC):
    """Base class for all domain advisors."""

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        system_prompt: str,
        rag: RAGPipeline | None = None,
        memory: MemoryManager | None = None,
        tags: list[str] | None = None,
    ):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.system_prompt = system_prompt
        self.rag = rag
        self.memory = memory
        self.tags = tags or []

    async def handle(self, query: str, context: ConversationContext) -> AdvisorResponse:
        """Main entry point — called by Chief of Staff."""
        logger.info("advisor.handling", advisor=self.name, query=query[:80])

        # 1. Gather context
        rag_context = ""
        if self.rag:
            rag_result = self.rag.query_for_advisor(query, self.name)
            rag_context = rag_result.text

        memories = format_memories_for_prompt([])
        if self.memory:
            memories = self.memory.get_advisor_context(self.name, query)

        # 2. Build prompt
        full_prompt = self._build_prompt(query, rag_context, memories, context)

        # 3. Call LLM
        response = await self._call_llm(full_prompt)

        # 4. Post-process
        await self._post_process(query, response)

        return response

    def _build_prompt(
        self,
        query: str,
        rag_context: str,
        memories: str,
        context: ConversationContext,
    ) -> str:
        """Build the full prompt with all context injected."""
        parts = [
            f"# System\n{self.system_prompt}",
            f"\n# User's Personal Context\n{memories}",
        ]
        if rag_context:
            parts.append(f"\n# Relevant Knowledge Base Documents\n{rag_context}")
        if context.history:
            history_text = "\n".join(
                f"{m.role}: {m.content}" for m in context.history[-5:]
            )
            parts.append(f"\n# Recent Conversation\n{history_text}")
        parts.append(f"\n# User's Question\n{query}")
        return "\n".join(parts)

    @abstractmethod
    async def _call_llm(self, prompt: str) -> AdvisorResponse:
        """Call the LLM with the built prompt. Implemented by subclasses."""
        ...

    async def _post_process(self, query: str, response: AdvisorResponse) -> None:
        """Store memories and handle follow-ups after response."""
        if self.memory:
            try:
                self.memory.add(
                    f"Q: {query}\nA: {response.text[:200]}",
                    metadata={"advisor": self.name},
                )
            except Exception as e:
                logger.warning("advisor.memory_save_failed", error=str(e))

    def get_info(self) -> dict[str, Any]:
        """Return advisor info for registry."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "tags": self.tags,
        }
