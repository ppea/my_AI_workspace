# lifeos/src/core/message.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


@dataclass
class Attachment:
    """File attachment (photo, document, etc.)."""
    filename: str
    content_type: str
    data: bytes = b""


@dataclass
class IncomingMessage:
    """Channel-agnostic incoming message."""
    text: str
    channel: Literal["opencode", "cli", "telegram", "api"]
    session_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionItem:
    """An action item extracted from advisor response."""
    title: str
    advisor: str
    due_date: str | None = None
    priority: str = "medium"


@dataclass
class FollowUp:
    """A suggested follow-up question."""
    question: str
    advisor: str


@dataclass
class Reminder:
    """A reminder to be scheduled."""
    message: str
    date: str
    advance_days: list[int] = field(default_factory=lambda: [3, 1, 0])
    advisor: str = ""


@dataclass
class OutgoingResponse:
    """Channel-agnostic response."""
    text: str
    advisor: str | None = None
    action_items: list[ActionItem] = field(default_factory=list)
    follow_ups: list[FollowUp] = field(default_factory=list)
    reminders: list[Reminder] = field(default_factory=list)
    caveat: str | None = None
    error: bool = False

    def render_for(self, channel: str) -> str:
        """Format response for specific channel."""
        match channel:
            case "cli" | "opencode":
                return self._render_markdown()
            case "telegram":
                return self._render_telegram()
            case "api":
                return self.text
            case _:
                return self.text

    def _render_markdown(self) -> str:
        """Full Markdown rendering for CLI/OpenCode."""
        parts = []
        if self.advisor:
            parts.append(f"**{self.advisor.replace('_', ' ').title()} Advisor**\n")
        parts.append(self.text)
        if self.caveat:
            parts.append(f"\n> ⚠️ {self.caveat}")
        if self.action_items:
            parts.append("\n**Action Items:**")
            for item in self.action_items:
                parts.append(f"- [ ] {item.title}")
        if self.follow_ups:
            parts.append("\n**You might also ask:**")
            for fu in self.follow_ups:
                parts.append(f"- {fu.question}")
        return "\n".join(parts)

    def _render_telegram(self) -> str:
        """Telegram-compatible Markdown rendering."""
        parts = []
        if self.advisor:
            parts.append(
                f"*{self.advisor.replace('_', ' ').title()} Advisor*\n"
            )
        # Convert **bold** to *bold* for Telegram
        text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", self.text)
        parts.append(text)
        if self.caveat:
            parts.append(f"\n⚠️ {self.caveat}")
        if self.action_items:
            parts.append("\n*Action Items:*")
            for item in self.action_items:
                parts.append(f"• {item.title}")
        return "\n".join(parts)
