from __future__ import annotations
from collections.abc import Awaitable, Callable
import structlog
from src.scheduler.reminder_store import ReminderStore
from src.scheduler.quiet_hours import QuietHoursGuard
from src.core.config import SchedulerConfig

logger = structlog.get_logger()

async def dispatch_due_reminders(
    send_fn: "Callable[[str], Awaitable[None]]",
    store: ReminderStore,
    config: SchedulerConfig,
) -> None:
    """Check for due reminders and dispatch them, respecting quiet hours."""
    guard = QuietHoursGuard(config.quiet_hours)
    due = await store.get_due()
    
    for reminder in due:
        if guard.should_defer(reminder.urgency):
            logger.info("reminder.deferred", id=reminder.id, reason="quiet_hours")
            continue
        
        msg = f"⏰ *Reminder*\n{reminder.text}"
        if reminder.advisor:
            msg += f"\n_(from {reminder.advisor} advisor)_"
        
        await send_fn(msg)
        await store.mark_sent(reminder.id)
        logger.info("reminder.dispatched", id=reminder.id)
