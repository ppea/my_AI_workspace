from __future__ import annotations
from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any
import structlog
from src.scheduler.quiet_hours import QuietHoursGuard
from src.core.config import SchedulerConfig

logger = structlog.get_logger()

async def send_daily_briefing(
    send_fn: "Callable[[str], Awaitable[None]]",
    config: SchedulerConfig,
    gcal_integration: "Any | None" = None,
    todoist_integration: "Any | None" = None,
) -> None:
    """
    Compose and send a morning daily briefing message.
    Falls back gracefully if integrations are unavailable.
    """
    guard = QuietHoursGuard(config.quiet_hours)
    if guard.should_defer():
        logger.info("daily_briefing.deferred", reason="quiet_hours")
        return
    
    lines: list[str] = ["☀️ *Good morning! Here's your daily briefing.*\n"]
    
    # Calendar events today
    if gcal_integration is not None:
        try:
            now = datetime.utcnow()
            end = now.replace(hour=23, minute=59, second=59)
            events = await gcal_integration.get_events(start=now, end=end)
            if events:
                lines.append(f"📅 *Today's calendar* ({len(events)} events):")
                for ev in events[:5]:
                    title = ev.get("summary", "Untitled")
                    start = ev.get("start", {}).get("dateTime", "")
                    lines.append(f"  • {title}" + (f" at {start[11:16]}" if start else ""))
            else:
                lines.append("📅 No calendar events today.")
        except Exception as e:
            logger.warning("daily_briefing.gcal_error", error=str(e))
    
    # Todoist tasks due today
    if todoist_integration is not None:
        try:
            tasks = await todoist_integration.get_tasks()
            today_tasks = [t for t in tasks if t.get("due")][:5]
            if today_tasks:
                lines.append(f"\n✅ *Tasks due* ({len(today_tasks)}):")
                for t in today_tasks:
                    lines.append(f"  • {t['content']}")
            else:
                lines.append("\n✅ No tasks due today.")
        except Exception as e:
            logger.warning("daily_briefing.todoist_error", error=str(e))
    
    lines.append("\n_Have a productive day!_ 🚀")
    message = "\n".join(lines)
    
    await send_fn(message)
    logger.info("daily_briefing.sent")
