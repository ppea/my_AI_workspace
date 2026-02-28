from __future__ import annotations
from datetime import datetime
import zoneinfo
from src.core.config import QuietHoursConfig

class QuietHoursGuard:
    """Determines if the current time is within quiet hours."""
    
    def __init__(self, config: QuietHoursConfig):
        self.config = config
    
    def is_quiet_now(self) -> bool:
        """Return True if current time is within quiet hours."""
        if not self.config.enabled:
            return False
        tz = zoneinfo.ZoneInfo(self.config.timezone)
        now = datetime.now(tz)
        hour = now.hour
        start = self.config.start_hour
        end = self.config.end_hour
        if start > end:  # spans midnight e.g. 22..8
            return hour >= start or hour < end
        return start <= hour < end
    
    def should_defer(self, urgency: str = "normal") -> bool:
        """Return True if message should be deferred. urgent messages never deferred."""
        if urgency == "urgent":
            return False
        return self.is_quiet_now()
