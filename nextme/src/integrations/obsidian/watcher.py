from __future__ import annotations

from pathlib import Path
from typing import Callable

import structlog
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

logger = structlog.get_logger()


class ObsidianWatcher:
    def __init__(self, poll_interval_seconds: int = 30):
        self.poll_interval_seconds = poll_interval_seconds
        self._observer: PollingObserver | None = None

    def start(self, vault_path: str, callback: Callable[[str], None]) -> None:
        if self._observer is not None:
            logger.warning("obsidian.watcher_already_running")
            return

        handler = self._build_handler(callback)
        self._observer = PollingObserver(timeout=self.poll_interval_seconds)
        self._observer.schedule(handler, vault_path, recursive=True)
        self._observer.start()
        logger.info("obsidian.watcher_started", vault_path=vault_path)

    def stop(self) -> None:
        if self._observer is None:
            return

        self._observer.stop()
        self._observer.join()
        self._observer = None
        logger.info("obsidian.watcher_stopped")

    def _build_handler(self, callback: Callable[[str], None]) -> FileSystemEventHandler:
        class MarkdownEventHandler(FileSystemEventHandler):
            def on_modified(self, event: FileSystemEvent) -> None:
                if event.is_directory:
                    return

                path = Path(event.src_path)
                path_parts = set(path.parts)
                if ".obsidian" in path_parts:
                    return
                if path.suffix == ".tmp":
                    return
                if path.suffix != ".md":
                    return

                logger.info("obsidian.file_changed", file_path=str(path))
                callback(str(path))

        return MarkdownEventHandler()
