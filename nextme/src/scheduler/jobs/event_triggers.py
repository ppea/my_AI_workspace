from __future__ import annotations
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta
from typing import Any
import structlog
from src.core.config import SchedulerConfig

logger = structlog.get_logger()

async def check_upcoming_events(
    send_fn: "Callable[[str], Awaitable[None]]",
    config: SchedulerConfig,
    gcal_integration: "Any | None" = None,
    prep_window_minutes: int = 30,
) -> None:
    """Notify about events starting within prep_window_minutes."""
    if gcal_integration is None:
        return
    
    try:
        now = datetime.utcnow()
        window_end = now + timedelta(minutes=prep_window_minutes)
        events = await gcal_integration.get_events(start=now, end=window_end)
        
        for ev in events:
            title = ev.get("summary", "Untitled")
            start_str = ev.get("start", {}).get("dateTime", "")
            msg = f"🗓️ *Upcoming event in ~{prep_window_minutes} min*\n{title}"
            if start_str:
                msg += f"\n_Starts at {start_str[11:16]}_"
            await send_fn(msg)
            logger.info("event_trigger.notified", event=title)
    except Exception as e:
        logger.warning("event_trigger.error", error=str(e))
