from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"


@dataclass
class RAGConfig:
    vector_store: str = "chroma"
    persist_dir: str = "data/chroma/"
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 512
    chunk_overlap: int = 50
    watch_dirs: list[str] = field(default_factory=lambda: ["knowledge/"])
    ignore_patterns: list[str] = field(default_factory=lambda: ["*.tmp", ".obsidian/"])
    incremental: bool = True


@dataclass
class LLMConfig:
    provider: str = "openai"
    model: str = "gpt-4o"


@dataclass
class AdvisorConfig:
    name: str
    display_name: str
    description: str
    prompt_file: str
    tools: list[str] = field(default_factory=list)
    knowledge_dirs: list[str] = field(default_factory=list)
    llm: LLMConfig = field(default_factory=LLMConfig)
    tags: list[str] = field(default_factory=list)


@dataclass
class GoogleCalendarConfig:
    enabled: bool = False
    calendar_id: str = "primary"
    sync_interval_minutes: int = 15
    oauth_client_secrets_path: str = ""
    token_path: str = "data/google_token.json"


@dataclass
class TodoistConfig:
    enabled: bool = False
    project_prefix: str = "NextMe"
    sync_interval_minutes: int = 10
    auto_create_tasks: bool = True


@dataclass
class ObsidianConfig:
    enabled: bool = True
    vault_path: str = "knowledge/"
    watch_mode: str = "polling"
    poll_interval_seconds: int = 30


@dataclass
class IntegrationsConfig:
    google_calendar: GoogleCalendarConfig = field(default_factory=GoogleCalendarConfig)
    todoist: TodoistConfig = field(default_factory=TodoistConfig)
    obsidian: ObsidianConfig = field(default_factory=ObsidianConfig)


@dataclass
class SecretsConfig:
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    telegram_bot_token: str = ""
    telegram_owner_chat_id: str = ""
    todoist_api_token: str = ""
    google_calendar_client_secrets_path: str = ""
    api_key: str = ""


def load_yaml(filename: str) -> dict[str, Any]:
    """Load a YAML config file from the config directory."""
    path = CONFIG_DIR / filename
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_advisors() -> dict[str, AdvisorConfig]:
    """Load all advisor configurations."""
    data = load_yaml("advisors.yaml")
    advisors = {}
    for name, cfg in data.get("advisors", {}).items():
        llm_data = cfg.get("llm", {})
        advisors[name] = AdvisorConfig(
            name=name,
            display_name=cfg["display_name"],
            description=cfg["description"],
            prompt_file=cfg["prompt_file"],
            tools=cfg.get("tools", []),
            knowledge_dirs=cfg.get("knowledge_dirs", []),
            llm=LLMConfig(
                provider=llm_data.get("provider", "openai"),
                model=llm_data.get("model", "gpt-4o"),
            ),
            tags=cfg.get("tags", []),
        )
    return advisors


def load_rag_config() -> RAGConfig:
    """Load RAG pipeline configuration."""
    data = load_yaml("rag.yaml")
    rag = data.get("rag", {})
    embedding = rag.get("embedding", {})
    chunking = rag.get("chunking", {})
    indexing = rag.get("indexing", {})
    return RAGConfig(
        vector_store=rag.get("vector_store", "chroma"),
        persist_dir=rag.get("persist_dir", "data/chroma/"),
        embedding_provider=embedding.get("provider", "openai"),
        embedding_model=embedding.get("model", "text-embedding-3-small"),
        chunk_size=chunking.get("chunk_size", 512),
        chunk_overlap=chunking.get("chunk_overlap", 50),
        watch_dirs=indexing.get("watch_dirs", ["knowledge/"]),
        ignore_patterns=indexing.get("ignore_patterns", []),
        incremental=indexing.get("incremental", True),
    )


def load_integrations_config() -> IntegrationsConfig:
    data = load_yaml("integrations.yaml")
    integrations = data.get("integrations", {})

    google_calendar = integrations.get("google_calendar", {})
    todoist = integrations.get("todoist", {})
    obsidian = integrations.get("obsidian", {})

    return IntegrationsConfig(
        google_calendar=GoogleCalendarConfig(
            enabled=google_calendar.get("enabled", False),
            calendar_id=google_calendar.get("calendar_id", "primary"),
            sync_interval_minutes=google_calendar.get("sync_interval_minutes", 15),
            oauth_client_secrets_path=google_calendar.get("oauth_client_secrets_path", ""),
            token_path=google_calendar.get("token_path", "data/google_token.json"),
        ),
        todoist=TodoistConfig(
            enabled=todoist.get("enabled", False),
            project_prefix=todoist.get("project_prefix", "NextMe"),
            sync_interval_minutes=todoist.get("sync_interval_minutes", 10),
            auto_create_tasks=todoist.get("auto_create_tasks", True),
        ),
        obsidian=ObsidianConfig(
            enabled=obsidian.get("enabled", True),
            vault_path=obsidian.get("vault_path", "knowledge/"),
            watch_mode=obsidian.get("watch_mode", "polling"),
            poll_interval_seconds=obsidian.get("poll_interval_seconds", 30),
        ),
    )


def load_secrets() -> SecretsConfig:
    """Load secrets from secrets.yaml."""
    data = load_yaml("secrets.yaml")
    secrets = data.get("secrets", {})
    return SecretsConfig(
        openai_api_key=secrets.get("openai_api_key", ""),
        anthropic_api_key=secrets.get("anthropic_api_key", ""),
        telegram_bot_token=secrets.get("telegram_bot_token", ""),
        telegram_owner_chat_id=secrets.get("telegram_owner_chat_id", ""),
        todoist_api_token=secrets.get("todoist_api_token", ""),
        google_calendar_client_secrets_path=secrets.get("google_calendar_client_secrets_path", ""),
        api_key=secrets.get("api_key", ""),
    )
