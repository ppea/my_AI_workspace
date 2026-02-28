from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Any

import structlog
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.agents.chief_of_staff import ChiefOfStaff
from src.advisors.career.advisor import CareerAdvisor
from src.advisors.entrepreneurship.advisor import EntrepreneurshipAdvisor
from src.advisors.family.advisor import FamilyAdvisor
from src.advisors.finance.advisor import FinanceAdvisor
from src.advisors.health.advisor import HealthAdvisor
from src.advisors.learning.advisor import LearningAdvisor
from src.advisors.legal.advisor import LegalAdvisor
from src.advisors.mental_health.advisor import MentalHealthAdvisor
from src.advisors.schedule.advisor import ScheduleAdvisor
from src.api.models import (
    AdvisorInfo,
    NoteRequest,
    QueryRequest,
    QueryResponse,
    StatusResponse,
)
from src.core.config import load_secrets
from src.core.context import ConversationContext
from src.core.memory import MemoryManager
from src.core.rag import RAGPipeline

logger = structlog.get_logger(__name__)

# Global state (initialized on startup)
chief: ChiefOfStaff | None = None
rag: RAGPipeline | None = None
memory: MemoryManager | None = None
api_key: str | None = None


def create_chief() -> ChiefOfStaff:
    """Create and configure Chief of Staff with all advisors."""
    chief = ChiefOfStaff()
    chief.register_advisor(HealthAdvisor())
    chief.register_advisor(ScheduleAdvisor())
    chief.register_advisor(FinanceAdvisor())
    chief.register_advisor(CareerAdvisor())
    chief.register_advisor(LegalAdvisor())
    chief.register_advisor(FamilyAdvisor())
    chief.register_advisor(MentalHealthAdvisor())
    chief.register_advisor(LearningAdvisor())
    chief.register_advisor(EntrepreneurshipAdvisor())
    return chief


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown."""
    global chief, rag, memory, api_key

    logger.info("Starting NextMe API server")

    # Load secrets for API key
    secrets = load_secrets()
    api_key = secrets.api_key if secrets.api_key else None

    # Initialize services (lazy on first request)
    yield

    logger.info("Shutting down NextMe API server")


def create_app() -> FastAPI:
    """Factory function to create FastAPI application."""
    app = FastAPI(
        title="NextMe API",
        description="Personal AI Life Management System REST API",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        """Validate X-API-Key header if api_key is configured."""
        # Skip auth for health check
        if request.url.path == "/status":
            return await call_next(request)

        # Only enforce auth if api_key is configured
        if api_key:
            provided_key = request.headers.get("X-API-Key")
            if not provided_key or provided_key != api_key:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or missing API key"},
                )

        return await call_next(request)

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        """Log all requests with structlog."""
        logger.info(
            "request",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None,
        )
        response = await call_next(request)
        logger.info("response", status_code=response.status_code)
        return response

    @app.get("/status", response_model=StatusResponse)
    async def get_status() -> StatusResponse:
        """Get system health status."""
        global chief, rag, memory

        # Lazy initialize
        if rag is None:
            rag = RAGPipeline()
        if memory is None:
            memory = MemoryManager()
        if chief is None:
            chief = create_chief()

        rag_stats = rag.get_stats()
        memory_stats = memory.get_stats()
        chief_stats = chief.get_stats()

        return StatusResponse(
            rag_documents=rag_stats["document_count"],
            memory_count=memory_stats["total_memories"],
            advisors_loaded=chief_stats["total_advisors"],
            advisor_names=chief_stats["advisor_names"],
        )

    @app.post("/query", response_model=QueryResponse)
    async def post_query(request: QueryRequest) -> QueryResponse:
        """Process a query through Chief of Staff."""
        global chief

        # Lazy initialize
        if chief is None:
            chief = create_chief()

        context = ConversationContext(
            session_id=request.session_id,
            channel="api",
            active_advisor=request.advisor,
        )

        try:
            response = await chief.process(request.text, context)

            return QueryResponse(
                text=response.text,
                advisor=response.advisor,
                action_items=[item.title for item in response.action_items],
                follow_ups=[fu.question for fu in response.follow_ups],
                caveat=response.caveat,
            )
        except Exception as e:
            logger.error("query_processing_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing query: {str(e)}",
            )

    @app.post("/notes", status_code=status.HTTP_201_CREATED)
    async def post_note(request: NoteRequest) -> dict[str, str]:
        """Add a note to the knowledge base."""
        area_dir = (
            Path(f"knowledge/areas/{request.area}")
            if request.area != "inbox"
            else Path("knowledge/inbox")
        )
        if not area_dir.exists():
            area_dir.mkdir(parents=True, exist_ok=True)

        today = date.today().isoformat()
        filename = f"{today}-api.md"
        filepath = area_dir / filename

        # If file exists, append; otherwise create
        if filepath.exists():
            with open(filepath, "a") as f:
                f.write(f"\n\n## {today}\n{request.text}\n")
        else:
            frontmatter = (
                f"---\ntype: note\ndate: {today}\n"
                f"tags: {request.tags}\nadvisor: {request.area}\n"
                f"confidentiality: normal\n---\n\n"
                f"# Note — {today}\n\n{request.text}\n"
            )
            filepath.write_text(frontmatter)

        return {"status": "created", "path": str(filepath)}

    @app.get("/advisors", response_model=list[AdvisorInfo])
    async def get_advisors() -> list[AdvisorInfo]:
        """List all registered advisors."""
        global chief

        # Lazy initialize
        if chief is None:
            chief = create_chief()

        # Get all advisors from chief
        advisors_list = []
        for advisor in chief._advisors.values():
            advisors_list.append(
                AdvisorInfo(
                    name=advisor.name,
                    display_name=advisor.display_name,
                    description=advisor.description,
                )
            )

        return advisors_list

    @app.post("/webhook/telegram")
    async def telegram_webhook(update: dict[str, Any]) -> dict[str, Any]:
        """
        Handle Telegram webhook updates.
        Synchronous webhook response style.
        """
        global chief

        # Lazy initialize
        if chief is None:
            chief = create_chief()

        try:
            # Extract message from Telegram Update
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            if not chat_id or not text:
                return {"ok": False, "error": "Invalid update format"}

            # Process query
            context = ConversationContext(
                session_id=f"telegram-{chat_id}",
                channel="telegram",
            )

            response = await chief.process(text, context)

            # Return Telegram sendMessage response
            return {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": response.render_for("telegram"),
                "parse_mode": "Markdown",
            }
        except Exception as e:
            logger.error("telegram_webhook_error", error=str(e))
            return {
                "method": "sendMessage",
                "chat_id": chat_id if "chat_id" in locals() else 0,
                "text": f"Sorry, I encountered an error: {str(e)}",
            }

    return app
