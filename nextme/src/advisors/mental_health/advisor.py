from __future__ import annotations

from src.agents.base_advisor import BaseAdvisor, AdvisorResponse
from src.advisors.mental_health.prompts import SYSTEM_PROMPT
from src.core.rag import RAGPipeline
from src.core.memory import MemoryManager


class MentalHealthAdvisor(BaseAdvisor):
    """Mental Wellness Advisor."""

    def __init__(self, rag: RAGPipeline | None = None,
                 memory: MemoryManager | None = None):
        super().__init__(
            name="mental_health",
            display_name="Mental Wellness Advisor",
            description="Stress management, mindfulness, emotional support, wellbeing tracking",
            system_prompt=SYSTEM_PROMPT,
            rag=rag,
            memory=memory,
            tags=["mental_health", "stress", "mindfulness", "wellbeing", "emotional"],
        )

    async def _call_llm(self, prompt: str) -> AdvisorResponse:
        """Call LLM for mental health advice."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI()
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt.split("# User's Question")[0]},
                    {"role": "user", "content": prompt.split("# User's Question")[-1]},
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            text = response.choices[0].message.content or "I couldn't generate a response."
            return AdvisorResponse(text=text, advisor=self.name)
        except Exception as e:
            return AdvisorResponse(
                text=f"I'm having trouble processing your mental wellness query. Error: {e}",
                advisor=self.name,
            )
