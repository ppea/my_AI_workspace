from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import structlog

from src.integrations import BaseIntegration

logger = structlog.get_logger()

try:
    from todoist_api_python.api import TodoistAPI
except ImportError:
    TodoistAPI = None


class TodoistIntegration(BaseIntegration):
    def __init__(self, api_token: str):
        self.api_token = api_token
        self._client: Any = None

    async def connect(self) -> bool:
        if TodoistAPI is None:
            logger.warning("todoist.unavailable", reason="todoist_api_python not installed")
            return False
        if not self.api_token:
            logger.warning("todoist.unavailable", reason="missing api token")
            return False

        self._client = TodoistAPI(self.api_token)
        return True

    async def health_check(self) -> dict[str, Any]:
        if self._client is None:
            return {"status": "disconnected"}
        try:
            self._client.get_projects()
            return {"status": "connected"}
        except Exception as exc:
            logger.warning("todoist.health_check_failed", error=str(exc))
            return {"status": "error", "error": str(exc)}

    async def disconnect(self) -> None:
        self._client = None

    async def get_tasks(
        self,
        project_name: str | None = None,
        due_today: bool = False,
    ) -> list[dict[str, Any]]:
        if self._client is None:
            return []

        kwargs: dict[str, Any] = {}
        if project_name:
            mapped_project = self.map_advisor_to_project(project_name)
            project_id = self.get_or_create_project(mapped_project)
            kwargs["project_id"] = project_id

        tasks = [self._to_dict(task) for task in self._client.get_tasks(**kwargs)]
        if not due_today:
            return tasks

        today = datetime.now(UTC).date().isoformat()
        return [task for task in tasks if self._extract_due_date(task) == today]

    async def create_task(
        self,
        content: str,
        project_name: str | None = None,
        due_string: str | None = None,
        labels: list[str] | None = None,
    ) -> str:
        if self._client is None:
            msg = "Todoist client is not connected"
            logger.error("todoist.create_task_failed", reason=msg)
            raise RuntimeError(msg)

        payload: dict[str, Any] = {"content": content}
        if project_name:
            mapped_project = self.map_advisor_to_project(project_name)
            payload["project_id"] = self.get_or_create_project(mapped_project)
        if due_string:
            payload["due_string"] = due_string
        if labels:
            payload["labels"] = labels

        task = self._client.add_task(**payload)
        return str(self._item_get(task, "id", ""))

    async def complete_task(self, task_id: str) -> bool:
        if self._client is None:
            return False

        try:
            self._client.close_task(task_id)
            return True
        except Exception as exc:
            logger.warning("todoist.complete_task_failed", task_id=task_id, error=str(exc))
            return False

    def get_or_create_project(self, name: str) -> str:
        if self._client is None:
            msg = "Todoist client is not connected"
            logger.error("todoist.project_failed", reason=msg, project=name)
            raise RuntimeError(msg)

        for project in self._client.get_projects():
            if self._item_get(project, "name") == name:
                return str(self._item_get(project, "id"))

        project = self._client.add_project(name=name)
        return str(self._item_get(project, "id"))

    @staticmethod
    def map_advisor_to_project(advisor_name: str) -> str:
        return f"NextMe: {advisor_name.title()}"

    @staticmethod
    def _item_get(item: Any, key: str, default: Any = None) -> Any:
        if isinstance(item, dict):
            return item.get(key, default)
        return getattr(item, key, default)

    def _to_dict(self, item: Any) -> dict[str, Any]:
        if isinstance(item, dict):
            return item
        if hasattr(item, "to_dict"):
            return item.to_dict()
        if hasattr(item, "__dict__"):
            return dict(item.__dict__)
        return {}

    @staticmethod
    def _extract_due_date(task: dict[str, Any]) -> str | None:
        due = task.get("due")
        if isinstance(due, dict):
            return due.get("date")
        return None
