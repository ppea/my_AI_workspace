from __future__ import annotations

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for query endpoint."""

    text: str = Field(..., description="User query text", min_length=1)
    session_id: str = Field(default="api-session", description="Session identifier")
    advisor: str | None = Field(
        default=None, description="Force specific advisor (optional)"
    )


class QueryResponse(BaseModel):
    """Response model for query endpoint."""

    text: str = Field(..., description="Response text")
    advisor: str | None = Field(default=None, description="Advisor that handled query")
    action_items: list[str] = Field(default_factory=list, description="Action items")
    follow_ups: list[str] = Field(default_factory=list, description="Follow-up questions")
    caveat: str | None = Field(default=None, description="Advisory caveat")


class NoteRequest(BaseModel):
    """Request model for adding a note."""

    text: str = Field(..., description="Note content", min_length=1)
    area: str = Field(default="inbox", description="Knowledge area")
    tags: list[str] = Field(default_factory=list, description="Note tags")


class StatusResponse(BaseModel):
    """Response model for status endpoint."""

    rag_documents: int = Field(..., description="Number of RAG documents")
    memory_count: int = Field(..., description="Number of memory entries")
    advisors_loaded: int = Field(..., description="Number of loaded advisors")
    advisor_names: list[str] = Field(default_factory=list, description="Advisor names")


class AdvisorInfo(BaseModel):
    """Information about an advisor."""

    name: str = Field(..., description="Internal advisor name")
    display_name: str = Field(..., description="Human-readable display name")
    description: str = Field(..., description="Advisor description")
