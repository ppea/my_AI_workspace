from __future__ import annotations

from datetime import datetime
from typing import Any

import structlog
from google.auth.exceptions import TransportError
from googleapiclient.discovery import Resource, build

from src.integrations import BaseIntegration
from src.integrations.google_calendar.auth import authenticate_google_calendar

logger = structlog.get_logger()


class GoogleCalendarIntegration(BaseIntegration):
    def __init__(self, scopes: list[str] | None = None):
        self.scopes = scopes or ["https://www.googleapis.com/auth/calendar"]
        self._service: Resource | None = None

    async def connect(self) -> bool:
        return self._service is not None

    async def health_check(self) -> dict[str, Any]:
        if self._service is None:
            return {"status": "disconnected"}
        return {"status": "connected"}

    async def disconnect(self) -> None:
        self._service = None

    def authenticate(self, credentials_path: str, token_path: str = "data/google_token.json") -> bool:
        credentials = authenticate_google_calendar(
            credentials_path=credentials_path,
            token_path=token_path,
            scopes=self.scopes,
        )
        self._service = build("calendar", "v3", credentials=credentials)
        logger.info("google_calendar.authenticated")
        return self._service is not None

    async def get_events(
        self,
        date_from: datetime,
        date_to: datetime,
        calendar_id: str = "primary",
    ) -> list[dict[str, Any]]:
        if self._service is None:
            logger.warning("google_calendar.get_events_without_connection")
            return []

        try:
            response = (
                self._service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=date_from.isoformat(),
                    timeMax=date_to.isoformat(),
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            return response.get("items", [])
        except TransportError as exc:
            logger.warning("google_calendar.transport_error", error=str(exc))
            return []

    async def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: str = "",
        calendar_id: str = "primary",
    ) -> str:
        if self._service is None:
            msg = "Google Calendar service is not connected"
            logger.error("google_calendar.create_event_failed", reason=msg)
            raise RuntimeError(msg)

        body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
        }
        created = self._service.events().insert(calendarId=calendar_id, body=body).execute()
        return str(created["id"])

    async def check_availability(
        self,
        start: datetime,
        end: datetime,
        calendar_id: str = "primary",
    ) -> bool:
        events = await self.get_events(start, end, calendar_id=calendar_id)
        return len(events) == 0
