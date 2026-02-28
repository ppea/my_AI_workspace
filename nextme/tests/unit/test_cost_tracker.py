from __future__ import annotations
import pytest
from datetime import date

@pytest.mark.asyncio
async def test_cost_tracker_initialize(tmp_path):
    from src.core.cost_tracker import CostTracker
    tracker = CostTracker(db_path=str(tmp_path / "costs.db"))
    await tracker.initialize()  # no error

@pytest.mark.asyncio
async def test_cost_entry_compute_gpt4o():
    from src.core.cost_tracker import CostEntry
    entry = CostEntry.compute("id1", "health", "gpt-4o", 1000, 500)
    # 1K input @ $0.005 + 0.5K output @ $0.015 = 0.005 + 0.0075 = 0.0125
    assert abs(entry.cost_usd - 0.0125) < 0.0001

@pytest.mark.asyncio
async def test_cost_entry_compute_unknown_model():
    from src.core.cost_tracker import CostEntry
    entry = CostEntry.compute("id2", "finance", "unknown-model", 1000, 1000)
    assert entry.cost_usd > 0  # uses fallback

@pytest.mark.asyncio
async def test_cost_tracker_record(tmp_path):
    from src.core.cost_tracker import CostTracker
    tracker = CostTracker(db_path=str(tmp_path / "costs.db"))
    await tracker.initialize()
    entry = await tracker.record("health", "gpt-4o", 500, 200)
    assert entry.advisor == "health"
    assert entry.cost_usd > 0

@pytest.mark.asyncio
async def test_cost_tracker_daily_summary(tmp_path):
    from src.core.cost_tracker import CostTracker
    tracker = CostTracker(db_path=str(tmp_path / "costs.db"))
    await tracker.initialize()
    await tracker.record("health", "gpt-4o", 500, 200)
    await tracker.record("finance", "gpt-4o-mini", 300, 100)
    summaries = await tracker.daily_summary()
    assert len(summaries) == 2
    advisors = {s.advisor for s in summaries}
    assert "health" in advisors
    assert "finance" in advisors

@pytest.mark.asyncio
async def test_cost_tracker_monthly_summary(tmp_path):
    from src.core.cost_tracker import CostTracker
    tracker = CostTracker(db_path=str(tmp_path / "costs.db"))
    await tracker.initialize()
    await tracker.record("career", "gpt-4o", 1000, 500)
    today = date.today()
    summaries = await tracker.monthly_summary(today.year, today.month)
    assert len(summaries) >= 1

@pytest.mark.asyncio
async def test_cost_tracker_total_cost(tmp_path):
    from src.core.cost_tracker import CostTracker
    tracker = CostTracker(db_path=str(tmp_path / "costs.db"))
    await tracker.initialize()
    await tracker.record("health", "gpt-4o", 1000, 1000)
    total = await tracker.total_cost()
    assert total > 0

@pytest.mark.asyncio
async def test_cost_tracker_empty_returns_zero(tmp_path):
    from src.core.cost_tracker import CostTracker
    tracker = CostTracker(db_path=str(tmp_path / "costs.db"))
    await tracker.initialize()
    total = await tracker.total_cost()
    assert total == 0.0
