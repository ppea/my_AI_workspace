# nextme/src/agents/chief_of_staff.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import structlog

from src.agents.base_advisor import BaseAdvisor, AdvisorResponse
from src.core.context import ConversationContext
from src.core.message import OutgoingResponse, ActionItem, FollowUp
from src.core.memory import MemoryManager

logger = structlog.get_logger()


# Keyword-based routing (fast, no LLM call needed)
ADVISOR_KEYWORDS: dict[str, list[str]] = {
    "health": [
        "health", "medical", "doctor", "blood pressure", "exercise", "fitness",
        "nutrition", "diet", "sleep", "medication", "symptom", "pain", "weight",
        "checkup", "hospital", "clinic", "vaccine", "allergy",
    ],
    "finance": [
        "money", "finance", "invest", "budget", "tax", "expense", "salary",
        "portfolio", "stock", "fund", "savings", "debt", "mortgage", "insurance",
        "retirement", "dividend",
    ],
    "schedule": [
        "schedule", "calendar", "meeting", "appointment", "deadline", "task",
        "productivity", "time", "plan", "agenda", "reminder", "todo",
    ],
    "career": [
        "career", "job", "resume", "interview", "promotion", "skill",
        "networking", "professional", "workplace", "salary negotiation",
    ],
    "legal": [
        "legal", "law", "contract", "lease", "rights", "court", "lawyer",
        "attorney", "dispute", "compliance", "regulation",
    ],
    "family": [
        "family", "parent", "child", "marriage", "relationship", "birthday",
        "anniversary", "spouse", "wife", "husband", "kids", "parenting",
    ],
    "mental_health": [
        "stress", "anxiety", "depression", "mental", "therapy", "meditation",
        "mindfulness", "mood", "emotional", "wellbeing", "burnout", "overwhelm",
    ],
    "learning": [
        "learn", "study", "course", "book", "education", "skill", "tutorial",
        "certification", "training", "knowledge",
    ],
    "entrepreneurship": [
        "startup", "business", "entrepreneur", "venture", "pitch", "market",
        "product", "customer", "revenue", "funding", "investor",
    ],
}

DIRECT_PATTERNS = [
    r"^(hi|hello|hey|good morning|good evening|thanks|thank you)",
    r"^what time",
    r"^who are you",
    r"^help$",
]


@dataclass
class RoutingDecision:
    """Result of intent classification."""
    action: str  # "direct" | "single_advisor" | "multi_advisor"
    advisor: str | None = None
    advisors: list[str] = field(default_factory=list)
    confidence: float = 0.0


def classify_intent(query: str) -> RoutingDecision:
    """Classify user intent using keyword matching.

    Fast, no LLM call. For ambiguous queries, defaults to direct answer.
    """
    query_lower = query.lower().strip()

    # Check for direct-answer patterns
    for pattern in DIRECT_PATTERNS:
        if re.match(pattern, query_lower):
            return RoutingDecision(action="direct", confidence=1.0)

    # Score each advisor by keyword matches
    scores: dict[str, int] = {}
    for advisor, keywords in ADVISOR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[advisor] = score

    if not scores:
        return RoutingDecision(action="direct", confidence=0.5)

    # Sort by score descending
    sorted_advisors = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # If top advisor has significantly higher score, route to single
    if len(sorted_advisors) == 1 or sorted_advisors[0][1] > sorted_advisors[1][1]:
        return RoutingDecision(
            action="single_advisor",
            advisor=sorted_advisors[0][0],
            confidence=min(sorted_advisors[0][1] / 3, 1.0),
        )

    # Multiple advisors with similar scores → multi-advisor
    top_score = sorted_advisors[0][1]
    multi = [name for name, score in sorted_advisors if score >= top_score * 0.5]
    if len(multi) > 1:
        return RoutingDecision(
            action="multi_advisor",
            advisors=multi[:3],  # max 3 advisors
            confidence=0.7,
        )

    return RoutingDecision(
        action="single_advisor",
        advisor=sorted_advisors[0][0],
        confidence=0.6,
    )


class ChiefOfStaff:
    """Router agent — the user's primary interface."""

    def __init__(
        self,
        advisors: dict[str, BaseAdvisor] | None = None,
        memory: MemoryManager | None = None,
    ):
        self.advisors = advisors or {}
        self.memory = memory

    def register_advisor(self, advisor: BaseAdvisor) -> None:
        """Register an advisor for routing."""
        self.advisors[advisor.name] = advisor
        logger.info("chief.advisor_registered", advisor=advisor.name)

    async def process(
        self, query: str, context: ConversationContext
    ) -> OutgoingResponse:
        """Main entry point for all user queries."""
        logger.info("chief.processing", query=query[:80], channel=context.channel)

        # If user is mid-conversation with an advisor, keep routing there
        if context.active_advisor and context.active_advisor in self.advisors:
            return await self._route_to_advisor(
                context.active_advisor, query, context
            )

        # Classify intent
        routing = classify_intent(query)
        logger.info(
            "chief.routing",
            action=routing.action,
            advisor=routing.advisor,
            advisors=routing.advisors,
            confidence=routing.confidence,
        )

        match routing.action:
            case "direct":
                return await self._direct_answer(query, context)
            case "single_advisor":
                if routing.advisor and routing.advisor in self.advisors:
                    return await self._route_to_advisor(
                        routing.advisor, query, context
                    )
                return await self._direct_answer(query, context)
            case "multi_advisor":
                available = [
                    a for a in routing.advisors if a in self.advisors
                ]
                if available:
                    return await self._multi_advisor(available, query, context)
                return await self._direct_answer(query, context)
            case _:
                return await self._direct_answer(query, context)

    async def _direct_answer(
        self, query: str, context: ConversationContext
    ) -> OutgoingResponse:
        """Answer directly without an advisor."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI()

            memory_context = ""
            if self.memory:
                memory_context = self.memory.get_advisor_context("general", query)

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the Chief of Staff for NextMe, a personal AI "
                            "life management system. Answer the user's question "
                            "helpfully and concisely.\n\n"
                            f"User context:\n{memory_context}"
                        ),
                    },
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            text = response.choices[0].message.content or "How can I help you?"
            return OutgoingResponse(text=text)
        except Exception as e:
            logger.error("chief.direct_answer_failed", error=str(e))
            return OutgoingResponse(
                text="I'm having trouble processing your request. Please try again.",
                error=True,
            )

    async def _route_to_advisor(
        self, advisor_name: str, query: str, context: ConversationContext
    ) -> OutgoingResponse:
        """Route to a single advisor."""
        advisor = self.advisors[advisor_name]
        try:
            result = await advisor.handle(query, context)
            return OutgoingResponse(
                text=result.text,
                advisor=result.advisor,
                action_items=[
                    ActionItem(title=item, advisor=advisor_name)
                    for item in result.action_items
                ],
                follow_ups=[
                    FollowUp(question=q, advisor=advisor_name)
                    for q in result.follow_ups
                ],
            )
        except Exception as e:
            logger.error("chief.advisor_failed", advisor=advisor_name, error=str(e))
            return OutgoingResponse(
                text=(
                    f"I'm having trouble reaching the {advisor.display_name}. "
                    "Let me try to help directly."
                ),
                caveat=f"{advisor.display_name} temporarily unavailable",
            )

    async def _multi_advisor(
        self,
        advisor_names: list[str],
        query: str,
        context: ConversationContext,
    ) -> OutgoingResponse:
        """Consult multiple advisors and synthesize."""
        import asyncio

        results: list[tuple[str, AdvisorResponse | Exception]] = []

        async def call_advisor(name: str) -> tuple[str, AdvisorResponse | Exception]:
            try:
                result = await self.advisors[name].handle(query, context)
                return (name, result)
            except Exception as e:
                return (name, e)

        gathered = await asyncio.gather(
            *[call_advisor(name) for name in advisor_names]
        )
        results = list(gathered)

        successful = [
            (name, r) for name, r in results if isinstance(r, AdvisorResponse)
        ]
        failed = [
            (name, r) for name, r in results if isinstance(r, Exception)
        ]

        if not successful:
            return await self._direct_answer(query, context)

        # Combine responses
        parts = []
        all_action_items: list[ActionItem] = []
        for name, resp in successful:
            advisor = self.advisors[name]
            parts.append(f"**{advisor.display_name}:**\n{resp.text}")
            all_action_items.extend(
                ActionItem(title=item, advisor=name)
                for item in resp.action_items
            )

        combined_text = "\n\n---\n\n".join(parts)

        caveat = None
        if failed:
            names = [n for n, _ in failed]
            caveat = f"Could not reach: {', '.join(names)}"

        return OutgoingResponse(
            text=combined_text,
            action_items=all_action_items,
            caveat=caveat,
        )

    def get_advisor_list(self) -> list[dict[str, Any]]:
        """List all registered advisors."""
        return [a.get_info() for a in self.advisors.values()]

    def get_stats(self) -> dict[str, Any]:
        """Get system statistics."""
        return {
            "advisors_loaded": len(self.advisors),
            "advisor_names": list(self.advisors.keys()),
        }
