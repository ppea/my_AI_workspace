from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Test QuietHoursGuard
def test_quiet_hours_disabled():
    from src.scheduler.quiet_hours import QuietHoursGuard
    from src.core.config import QuietHoursConfig
    guard = QuietHoursGuard(QuietHoursConfig(enabled=False))
    assert guard.is_quiet_now() is False

def test_quiet_hours_urgent_never_deferred():
    from src.scheduler.quiet_hours import QuietHoursGuard
    from src.core.config import QuietHoursConfig
    guard = QuietHoursGuard(QuietHoursConfig(enabled=True))
    assert guard.should_defer("urgent") is False

def test_quiet_hours_spans_midnight():
    # 22..8 spans midnight — hour 23 should be quiet
    from src.scheduler.quiet_hours import QuietHoursGuard
    from src.core.config import QuietHoursConfig
    guard = QuietHoursGuard(QuietHoursConfig(enabled=True, start_hour=22, end_hour=8))
    with patch("src.scheduler.quiet_hours.datetime") as mock_dt:
        mock_now = MagicMock()
        mock_now.hour = 23
        mock_dt.now.return_value = mock_now
        assert guard.is_quiet_now() is True

# Test ReminderStore
@pytest.mark.asyncio
async def test_reminder_store_initialize(tmp_path):
    from src.scheduler.reminder_store import ReminderStore
    store = ReminderStore(db_path=str(tmp_path / "test.db"))
    await store.initialize()  # should not raise

@pytest.mark.asyncio
async def test_reminder_store_add_and_get_due(tmp_path):
    from src.scheduler.reminder_store import ReminderStore, Reminder
    store = ReminderStore(db_path=str(tmp_path / "test.db"))
    await store.initialize()
    r = Reminder(
        id="r1", text="Take medicine", advisor="health", source="manual",
        urgency="normal", due_at=datetime(2000, 1, 1),  # past = due
        created_at=datetime(2000, 1, 1),
    )
    await store.add(r)
    due = await store.get_due(now=datetime.utcnow())
    assert len(due) == 1
    assert due[0].text == "Take medicine"

@pytest.mark.asyncio
async def test_reminder_store_mark_sent(tmp_path):
    from src.scheduler.reminder_store import ReminderStore, Reminder
    store = ReminderStore(db_path=str(tmp_path / "test.db"))
    await store.initialize()
    r = Reminder(id="r2", text="Buy groceries", advisor="schedule", source="manual",
                 urgency="normal", due_at=datetime(2000,1,1), created_at=datetime(2000,1,1))
    await store.add(r)
    await store.mark_sent("r2")
    due = await store.get_due(now=datetime.utcnow())
    assert all(x.id != "r2" for x in due)

# Test daily briefing
@pytest.mark.asyncio
async def test_daily_briefing_sends_message():
    from src.scheduler.jobs.daily_briefing import send_daily_briefing
    from src.core.config import SchedulerConfig, QuietHoursConfig
    cfg = SchedulerConfig(quiet_hours=QuietHoursConfig(enabled=False))
    sent = []
    async def capture(msg): sent.append(msg)
    await send_daily_briefing(capture, cfg, gcal_integration=None, todoist_integration=None)
    assert len(sent) == 1
    assert "morning" in sent[0].lower() or "briefing" in sent[0].lower()

# Test weekly review
@pytest.mark.asyncio
async def test_weekly_review_sends_message():
    from src.scheduler.jobs.weekly_review import send_weekly_review
    from src.core.config import SchedulerConfig, QuietHoursConfig
    cfg = SchedulerConfig(quiet_hours=QuietHoursConfig(enabled=False))
    sent = []
    async def capture(msg): sent.append(msg)
    await send_weekly_review(capture, cfg, todoist_integration=None)
    assert len(sent) == 1

# Test NextMeScheduler
@pytest.mark.asyncio
async def test_scheduler_start_stop(tmp_path):
    from src.scheduler.scheduler import NextMeScheduler
    from src.core.config import SchedulerConfig, QuietHoursConfig
    cfg = SchedulerConfig(db_path=str(tmp_path / "sched.db"), quiet_hours=QuietHoursConfig(enabled=False))
    sched = NextMeScheduler(config=cfg)
    await sched.start()
    jobs = sched.get_jobs()
    assert len(jobs) == 4  # daily_briefing, weekly_review, reminder_dispatcher, event_triggers
    sched.stop()

def test_scheduler_config_loads():
    from src.core.config import load_scheduler_config
    cfg = load_scheduler_config()
    assert cfg.daily_briefing_hour == 7
    assert cfg.quiet_hours.enabled is True
