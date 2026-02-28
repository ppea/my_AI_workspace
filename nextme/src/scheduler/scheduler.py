from __future__ import annotations
from typing import Any, Callable, Awaitable
import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from src.core.config import SchedulerConfig, load_scheduler_config
from src.scheduler.reminder_store import ReminderStore
from src.scheduler.jobs.daily_briefing import send_daily_briefing
from src.scheduler.jobs.weekly_review import send_weekly_review
from src.scheduler.jobs.reminder_dispatcher import dispatch_due_reminders
from src.scheduler.jobs.event_triggers import check_upcoming_events

logger = structlog.get_logger()

class NextMeScheduler:
    """APScheduler-backed proactive job runner."""

    def __init__(
        self,
        config: SchedulerConfig | None = None,
        send_fn: Callable[[str], Awaitable[None]] | None = None,
        gcal_integration: Any | None = None,
        todoist_integration: Any | None = None,
    ):
        self.config = config or load_scheduler_config()
        self.send_fn = send_fn or self._noop_send
        self.gcal = gcal_integration
        self.todoist = todoist_integration
        self.store = ReminderStore(self.config.db_path)
        self._scheduler = AsyncIOScheduler(timezone=self.config.timezone)

    @staticmethod
    async def _noop_send(message: str) -> None:
        logger.info("scheduler.noop_send", message=message[:80])

    async def start(self) -> None:
        await self.store.initialize()
        tz = self.config.timezone

        # Daily briefing
        self._scheduler.add_job(
            self._run_daily_briefing,
            CronTrigger(
                hour=self.config.daily_briefing_hour,
                minute=self.config.daily_briefing_minute,
                timezone=tz,
            ),
            id="daily_briefing",
            replace_existing=True,
        )

        # Weekly review (Friday)
        self._scheduler.add_job(
            self._run_weekly_review,
            CronTrigger(
                day_of_week=self.config.weekly_review_weekday,
                hour=self.config.weekly_review_hour,
                minute=0,
                timezone=tz,
            ),
            id="weekly_review",
            replace_existing=True,
        )

        # Reminder dispatcher — every 5 minutes
        self._scheduler.add_job(
            self._run_reminder_dispatcher,
            IntervalTrigger(minutes=5),
            id="reminder_dispatcher",
            replace_existing=True,
        )

        # Event triggers — every 15 minutes
        self._scheduler.add_job(
            self._run_event_triggers,
            IntervalTrigger(minutes=15),
            id="event_triggers",
            replace_existing=True,
        )

        self._scheduler.start()
        logger.info("scheduler.started", jobs=len(self._scheduler.get_jobs()))

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)
        logger.info("scheduler.stopped")

    async def _run_daily_briefing(self) -> None:
        await send_daily_briefing(self.send_fn, self.config, self.gcal, self.todoist)

    async def _run_weekly_review(self) -> None:
        await send_weekly_review(self.send_fn, self.config, self.todoist)

    async def _run_reminder_dispatcher(self) -> None:
        await dispatch_due_reminders(self.send_fn, self.store, self.config)

    async def _run_event_triggers(self) -> None:
        await check_upcoming_events(self.send_fn, self.config, self.gcal)

    def get_jobs(self) -> list[dict[str, Any]]:
        return [
            {"id": job.id, "next_run": str(job.next_run_time)}
            for job in self._scheduler.get_jobs()
        ]
