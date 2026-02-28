from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from src.integrations.obsidian.watcher import ObsidianWatcher


@pytest.mark.asyncio
class TestGoogleCalendarIntegration:
    async def test_get_events_returns_event_list(self) -> None:
        from src.integrations.google_calendar.integration import GoogleCalendarIntegration

        integration = GoogleCalendarIntegration()
        execute_mock = Mock(return_value={"items": [{"id": "evt_1", "summary": "Standup"}]})
        list_mock = Mock(return_value=Mock(execute=execute_mock))
        events_mock = Mock(return_value=Mock(list=list_mock))
        integration._service = Mock(events=events_mock)

        result = await integration.get_events(
            datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
            datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc),
        )

        assert result == [{"id": "evt_1", "summary": "Standup"}]
        list_mock.assert_called_once()

    async def test_get_events_returns_empty_list_on_transport_error(self) -> None:
        from google.auth.exceptions import TransportError

        from src.integrations.google_calendar.integration import GoogleCalendarIntegration

        integration = GoogleCalendarIntegration()
        execute_mock = Mock(side_effect=TransportError("network down"))
        list_mock = Mock(return_value=Mock(execute=execute_mock))
        events_mock = Mock(return_value=Mock(list=list_mock))
        integration._service = Mock(events=events_mock)

        result = await integration.get_events(
            datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
            datetime(2026, 1, 1, 18, 0, tzinfo=timezone.utc),
        )

        assert result == []


@pytest.mark.asyncio
class TestTodoistIntegration:
    async def test_get_tasks_returns_items(self) -> None:
        from src.integrations.todoist.integration import TodoistIntegration

        integration = TodoistIntegration(api_token="token")
        integration._client = Mock()
        integration._client.get_tasks.return_value = [{"id": "1", "content": "Task"}]

        result = await integration.get_tasks()

        assert result == [{"id": "1", "content": "Task"}]

    async def test_create_task_with_project_mapping(self) -> None:
        from src.integrations.todoist.integration import TodoistIntegration

        integration = TodoistIntegration(api_token="token")
        integration._client = Mock()
        integration.get_or_create_project = Mock(return_value="proj_1")
        integration._client.add_task.return_value = {"id": "task_1"}

        task_id = await integration.create_task(
            content="Do the thing",
            project_name="health",
            due_string="today",
            labels=["nextme"],
        )

        assert task_id == "task_1"
        integration.get_or_create_project.assert_called_once_with("NextMe: Health")

    async def test_get_or_create_project_creates_when_missing(self) -> None:
        from src.integrations.todoist.integration import TodoistIntegration

        integration = TodoistIntegration(api_token="token")
        integration._client = Mock()
        integration._client.get_projects.return_value = [{"id": "p1", "name": "Inbox"}]
        integration._client.add_project.return_value = {"id": "p2", "name": "NextMe: Finance"}

        project_id = integration.get_or_create_project("NextMe: Finance")

        assert project_id == "p2"
        integration._client.add_project.assert_called_once_with(name="NextMe: Finance")


class TestObsidianWatcher:
    def test_start_and_stop(self) -> None:
        callback = Mock()
        watcher = ObsidianWatcher(poll_interval_seconds=30)

        with patch("src.integrations.obsidian.watcher.PollingObserver") as observer_cls:
            observer = MagicMock()
            observer_cls.return_value = observer

            watcher.start("knowledge", callback)
            watcher.stop()

            observer.schedule.assert_called_once()
            observer.start.assert_called_once()
            observer.stop.assert_called_once()
            observer.join.assert_called_once()

    def test_ignores_non_markdown_and_obsidian_paths(self) -> None:
        callback = Mock()
        watcher = ObsidianWatcher(poll_interval_seconds=30)
        handler = watcher._build_handler(callback)

        event_tmp = Mock()
        event_tmp.is_directory = False
        event_tmp.src_path = str(Path("knowledge") / "notes.tmp")

        event_obsidian = Mock()
        event_obsidian.is_directory = False
        event_obsidian.src_path = str(Path("knowledge") / ".obsidian" / "workspace.json")

        event_md = Mock()
        event_md.is_directory = False
        event_md.src_path = str(Path("knowledge") / "daily.md")

        handler.on_modified(event_tmp)
        handler.on_modified(event_obsidian)
        handler.on_modified(event_md)

        callback.assert_called_once_with(str(Path("knowledge") / "daily.md"))
