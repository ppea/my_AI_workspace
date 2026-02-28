# lifeos/src/core/logging.py
from __future__ import annotations

from pathlib import Path

import structlog


def setup_logging(log_dir: str = "data/logs/") -> None:
    """Configure structured logging."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
