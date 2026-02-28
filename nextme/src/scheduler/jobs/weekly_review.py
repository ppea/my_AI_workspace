from __future__ import annotations
from collections.abc import Awaitable, Callable
from typing import Any
import structlog
from src.scheduler.quiet_hours import QuietHoursGuard
from src.core.config import SchedulerConfig

logger = structlog.get_logger()

async def send_weekly_review(
    send_fn: "Callable[[str], Awaitable[None]]",
    config: SchedulerConfig,
    todoist_integration: "Any | None" = None,
) -> None:
    """Send a Friday weekly review digest."""
    guard = QuietHoursGuard(config.quiet_hours)
    if guard.should_defer():
        logger.info("weekly_review.deferred", reason="quiet_hours")
        return

    lines = ["📊 *Weekly Review — Time to reflect!*\n"]
    
    if todoist_integration is not None:
        try:
            tasks = await todoist_integration.get_tasks()
            completed = [t for t in tasks if t.get("is_completed", False)]
            pending = [t for t in tasks if not t.get("is_completed", False)]
            lines.append(f"✅ Completed this week: {len(completed)} tasks")
            if pending[:3]:
                lines.append("\n📋 *Top pending tasks:*")
                for t in pending[:3]:
                    lines.append(f"  • {t['content']}")
        except Exception as e:
            logger.warning("weekly_review.todoist_error", error=str(e))
    
    lines.append("\n💡 *Questions to consider:*")
    lines.append("  1. What went well this week?")
    lines.append("  2. What could be improved?")
    lines.append("  3. What are your top 3 priorities for next week?")
    
    await send_fn("\n".join(lines))
    logger.info("weekly_review.sent")
