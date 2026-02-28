from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
import aiosqlite
import structlog

logger = structlog.get_logger()

# Cost per 1K tokens in USD
MODEL_COSTS: dict[str, dict[str, float]] = {
    "gpt-4o":             {"input": 0.005,   "output": 0.015},
    "gpt-4o-mini":        {"input": 0.00015, "output": 0.0006},
    "claude-3-5-sonnet":  {"input": 0.003,   "output": 0.015},
}
DEFAULT_COST_PER_1K = 0.005  # fallback

@dataclass
class CostEntry:
    id: str
    advisor: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    timestamp: datetime

    @classmethod
    def compute(cls, id: str, advisor: str, model: str, input_tokens: int, output_tokens: int) -> "CostEntry":
        costs = MODEL_COSTS.get(model, {"input": DEFAULT_COST_PER_1K, "output": DEFAULT_COST_PER_1K})
        cost = (input_tokens / 1000) * costs["input"] + (output_tokens / 1000) * costs["output"]
        return cls(id=id, advisor=advisor, model=model, input_tokens=input_tokens,
                   output_tokens=output_tokens, cost_usd=round(cost, 6), timestamp=datetime.utcnow())

@dataclass
class AdvisorCostSummary:
    advisor: str
    total_calls: int
    total_input_tokens: int
    total_output_tokens: int
    total_cost_usd: float

class CostTracker:
    """Async SQLite-backed LLM cost tracker."""

    def __init__(self, db_path: str = "data/scheduler.db"):
        self.db_path = db_path

    async def initialize(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS llm_costs (
                    id TEXT PRIMARY KEY,
                    advisor TEXT NOT NULL,
                    model TEXT NOT NULL,
                    input_tokens INTEGER NOT NULL,
                    output_tokens INTEGER NOT NULL,
                    cost_usd REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            await db.commit()

    async def record(self, advisor: str, model: str, input_tokens: int, output_tokens: int) -> CostEntry:
        """Record a single LLM call and return the cost entry."""
        import uuid
        entry = CostEntry.compute(str(uuid.uuid4()), advisor, model, input_tokens, output_tokens)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO llm_costs (id, advisor, model, input_tokens, output_tokens, cost_usd, timestamp) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (entry.id, entry.advisor, entry.model, entry.input_tokens,
                 entry.output_tokens, entry.cost_usd, entry.timestamp.isoformat())
            )
            await db.commit()
        logger.info("cost.recorded", advisor=advisor, cost_usd=entry.cost_usd)
        return entry

    async def daily_summary(self, day: date | None = None) -> list[AdvisorCostSummary]:
        """Return per-advisor cost summary for a given day (default: today)."""
        if day is None:
            day = date.today()
        day_str = day.isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """SELECT advisor,
                          COUNT(*) as total_calls,
                          SUM(input_tokens) as input_tokens,
                          SUM(output_tokens) as output_tokens,
                          SUM(cost_usd) as cost_usd
                   FROM llm_costs
                   WHERE timestamp LIKE ?
                   GROUP BY advisor
                   ORDER BY cost_usd DESC""",
                (f"{day_str}%",)
            ) as cursor:
                rows = await cursor.fetchall()
        return [
            AdvisorCostSummary(
                advisor=r["advisor"],
                total_calls=r["total_calls"],
                total_input_tokens=r["input_tokens"],
                total_output_tokens=r["output_tokens"],
                total_cost_usd=round(r["cost_usd"], 6),
            )
            for r in rows
        ]

    async def monthly_summary(self, year: int | None = None, month: int | None = None) -> list[AdvisorCostSummary]:
        """Return per-advisor cost summary for a given month (default: current month)."""
        if year is None or month is None:
            today = date.today()
            year, month = today.year, today.month
        prefix = f"{year:04d}-{month:02d}"
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """SELECT advisor,
                          COUNT(*) as total_calls,
                          SUM(input_tokens) as input_tokens,
                          SUM(output_tokens) as output_tokens,
                          SUM(cost_usd) as cost_usd
                   FROM llm_costs
                   WHERE timestamp LIKE ?
                   GROUP BY advisor
                   ORDER BY cost_usd DESC""",
                (f"{prefix}%",)
            ) as cursor:
                rows = await cursor.fetchall()
        return [
            AdvisorCostSummary(
                advisor=r["advisor"],
                total_calls=r["total_calls"],
                total_input_tokens=r["input_tokens"],
                total_output_tokens=r["output_tokens"],
                total_cost_usd=round(r["cost_usd"], 6),
            )
            for r in rows
        ]

    async def total_cost(self) -> float:
        """Return total lifetime cost in USD."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COALESCE(SUM(cost_usd), 0) FROM llm_costs") as cursor:
                row = await cursor.fetchone()
        return round(row[0], 6) if row else 0.0
