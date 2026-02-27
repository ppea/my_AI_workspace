# lifeos/src/core/context.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


@dataclass
class Message:
    """A single message in conversation history."""
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ConversationContext:
    """Passed through the entire request lifecycle."""
    session_id: str
    channel: Literal["opencode", "cli", "telegram", "api"]
    history: list[Message] = field(default_factory=list)
    active_advisor: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
