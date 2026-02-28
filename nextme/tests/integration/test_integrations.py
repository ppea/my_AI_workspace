# nextme/tests/integration/test_integrations.py
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest


@pytest.mark.integration
class TestGoogleCalendarIntegration:
    def test_google_calendar_get_events_mocked(self):
        """Test Google Calendar get_events with mocked build."""
        from src.integrations.google_calendar.integration import GoogleCalendarIntegration

        with patch("src.integrations.google_calendar.integration.build") as mock_build:
            # Mock the service
            service = Mock()
            events_api = Mock()
            list_call = Mock()
            execute_result = {
                "items": [
                    {"id": "evt_1", "summary": "Team Standup"},
                    {"id": "evt_2", "summary": "1:1 with Manager"},
                ]
            }
            
            list_call.execute.return_value = execute_result
            events_api.list.return_value = list_call
            service.events.return_value = events_api
            mock_build.return_value = service

            integration = GoogleCalendarIntegration()
            integration._service = service

            # Call get_events
            import asyncio
            result = asyncio.run(
                integration.get_events(
                    datetime(2026, 2, 28, 9, 0, tzinfo=timezone.utc),
                    datetime(2026, 2, 28, 18, 0, tzinfo=timezone.utc),
                )
            )

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["summary"] == "Team Standup"

    def test_google_calendar_create_event_mocked(self):
        """Test Google Calendar create_event with mocked build."""
        from src.integrations.google_calendar.integration import GoogleCalendarIntegration

        with patch("src.integrations.google_calendar.integration.build") as mock_build:
            # Mock the service
            service = Mock()
            events_api = Mock()
            insert_call = Mock()
            insert_call.execute.return_value = {"id": "new_evt_123"}
            
            events_api.insert.return_value = insert_call
            service.events.return_value = events_api
            mock_build.return_value = service

            integration = GoogleCalendarIntegration()
            integration._service = service

            # Call create_event
            import asyncio
            event_id = asyncio.run(
                integration.create_event(
                    title="Team Meeting",
                    start=datetime(2026, 3, 1, 14, 0, tzinfo=timezone.utc),
                    end=datetime(2026, 3, 1, 15, 0, tzinfo=timezone.utc),
                    description="Quarterly planning",
                )
            )

            assert event_id == "new_evt_123"
            events_api.insert.assert_called_once()

    def test_google_calendar_check_availability_mocked(self):
        """Test Google Calendar check_availability returns bool."""
        from src.integrations.google_calendar.integration import GoogleCalendarIntegration

        with patch("src.integrations.google_calendar.integration.build") as mock_build:
            # Mock the service
            service = Mock()
            events_api = Mock()
            list_call = Mock()
            list_call.execute.return_value = {"items": []}  # No events = available
            
            events_api.list.return_value = list_call
            service.events.return_value = events_api
            mock_build.return_value = service

            integration = GoogleCalendarIntegration()
            integration._service = service

            # Call check_availability
            import asyncio
            is_available = asyncio.run(
                integration.check_availability(
                    start=datetime(2026, 3, 1, 9, 0, tzinfo=timezone.utc),
                    end=datetime(2026, 3, 1, 10, 0, tzinfo=timezone.utc),
                )
            )

            assert isinstance(is_available, bool)
            assert is_available is True


@pytest.mark.integration
class TestTodoistIntegration:
    def test_todoist_get_tasks_mocked(self):
        """Test Todoist get_tasks with mocked TodoistAPI."""
        from src.integrations.todoist.integration import TodoistIntegration

        with patch("src.integrations.todoist.integration.TodoistAPI") as mock_api_cls:
            # Mock the API client
            client = Mock()
            client.get_tasks.return_value = [
                Mock(id="task_1", content="Buy groceries", project_id="proj_1"),
                Mock(id="task_2", content="Pay bills", project_id="proj_1"),
            ]
            
            # Mock to_dict for conversion
            for task in client.get_tasks.return_value:
                task.to_dict.return_value = {
                    "id": task.id,
                    "content": task.content,
                    "project_id": task.project_id,
                }
            
            mock_api_cls.return_value = client

            integration = TodoistIntegration(api_token="test_token")
            integration._client = client

            # Call get_tasks
            import asyncio
            tasks = asyncio.run(integration.get_tasks())

            assert isinstance(tasks, list)
            assert len(tasks) == 2
            assert tasks[0]["content"] == "Buy groceries"

    def test_todoist_create_task_mocked(self):
        """Test Todoist create_task with mocked TodoistAPI."""
        from src.integrations.todoist.integration import TodoistIntegration

        with patch("src.integrations.todoist.integration.TodoistAPI") as mock_api_cls:
            # Mock the API client
            client = Mock()
            task_obj = Mock(id="task_new_123", content="Buy groceries")
            task_obj.to_dict.return_value = {"id": "task_new_123", "content": "Buy groceries"}
            client.add_task.return_value = task_obj
            
            mock_api_cls.return_value = client

            integration = TodoistIntegration(api_token="test_token")
            integration._client = client

            # Call create_task
            import asyncio
            task_id = asyncio.run(integration.create_task("Buy groceries"))

            assert task_id == "task_new_123"
            client.add_task.assert_called_once()

    def test_todoist_complete_task_mocked(self):
        """Test Todoist complete_task with mocked TodoistAPI."""
        from src.integrations.todoist.integration import TodoistIntegration

        with patch("src.integrations.todoist.integration.TodoistAPI") as mock_api_cls:
            # Mock the API client
            client = Mock()
            client.close_task.return_value = None  # close_task doesn't return anything
            
            mock_api_cls.return_value = client

            integration = TodoistIntegration(api_token="test_token")
            integration._client = client

            # Call complete_task
            import asyncio
            success = asyncio.run(integration.complete_task("task_123"))

            assert success is True
            client.close_task.assert_called_once_with("task_123")

    def test_todoist_complete_task_failure(self):
        """Test Todoist complete_task handles exceptions."""
        from src.integrations.todoist.integration import TodoistIntegration

        with patch("src.integrations.todoist.integration.TodoistAPI") as mock_api_cls:
            # Mock the API client to raise exception
            client = Mock()
            client.close_task.side_effect = Exception("Network error")
            
            mock_api_cls.return_value = client

            integration = TodoistIntegration(api_token="test_token")
            integration._client = client

            # Call complete_task
            import asyncio
            success = asyncio.run(integration.complete_task("task_123"))

            assert success is False


@pytest.mark.integration
class TestObsidianWatcherIntegration:
    def test_obsidian_watcher_start_stop(self):
        """Test ObsidianWatcher can start and stop without errors."""
        from src.integrations.obsidian.watcher import ObsidianWatcher

        with patch("src.integrations.obsidian.watcher.PollingObserver") as mock_observer_cls:
            observer = Mock()
            mock_observer_cls.return_value = observer

            watcher = ObsidianWatcher(poll_interval_seconds=30)
            callback = Mock()

            # Start the watcher
            watcher.start("knowledge", callback)
            
            # Verify observer was set up correctly
            observer.schedule.assert_called_once()
            observer.start.assert_called_once()

            # Stop the watcher
            watcher.stop()
            
            observer.stop.assert_called_once()
            observer.join.assert_called_once()

    def test_obsidian_watcher_change_callback(self):
        """Test ObsidianWatcher callback is called on file change."""
        from src.integrations.obsidian.watcher import ObsidianWatcher
        from pathlib import Path

        watcher = ObsidianWatcher(poll_interval_seconds=30)
        callback = Mock()
        
        # Build the handler
        handler = watcher._build_handler(callback)
        
        # Simulate a markdown file change event
        event = Mock()
        event.is_directory = False
        event.src_path = str(Path("knowledge") / "daily-note.md")
        
        handler.on_modified(event)
        
        # Verify callback was called with the file path
        callback.assert_called_once_with(str(Path("knowledge") / "daily-note.md"))

    def test_obsidian_watcher_ignores_tmp_files(self):
        """Test ObsidianWatcher ignores .tmp files."""
        from src.integrations.obsidian.watcher import ObsidianWatcher
        from pathlib import Path

        watcher = ObsidianWatcher(poll_interval_seconds=30)
        callback = Mock()
        
        handler = watcher._build_handler(callback)
        
        # Simulate a .tmp file change
        event = Mock()
        event.is_directory = False
        event.src_path = str(Path("knowledge") / "temp.tmp")
        
        handler.on_modified(event)
        
        # Callback should NOT be called
        callback.assert_not_called()

    def test_obsidian_watcher_ignores_obsidian_folder(self):
        """Test ObsidianWatcher ignores .obsidian folder."""
        from src.integrations.obsidian.watcher import ObsidianWatcher
        from pathlib import Path

        watcher = ObsidianWatcher(poll_interval_seconds=30)
        callback = Mock()
        
        handler = watcher._build_handler(callback)
        
        # Simulate a file change in .obsidian folder
        event = Mock()
        event.is_directory = False
        event.src_path = str(Path("knowledge") / ".obsidian" / "workspace.json")
        
        handler.on_modified(event)
        
        # Callback should NOT be called
        callback.assert_not_called()
