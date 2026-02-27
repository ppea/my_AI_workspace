# LifeOS Phase 1: Core Foundation — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a working LifeOS system with RAG over personal knowledge base, Mem0 memory, Chief of Staff router, 2 advisors (Schedule + Health), OpenCode MCP server, CLI admin tools, and Telegram bot.

**Architecture:** Composable stack — LlamaIndex RAG + ChromaDB for document search, Mem0 for conversational memory, PydanticAI for agent framework. OpenCode is the primary zero-cost channel via MCP server + skill. Telegram for mobile + proactive notifications. CLI for admin commands.

**Tech Stack:** Python 3.12+, uv, PydanticAI, LlamaIndex, ChromaDB, Mem0, FastAPI, Typer, python-telegram-bot, APScheduler, structlog, pytest, mypy, ruff

**Design Doc:** `docs/plans/2026-02-27-lifeos-design.md`

---

## Task 1: Project Scaffold

**Files:**
- Create: `lifeos/pyproject.toml`
- Create: `lifeos/.gitignore`
- Create: `lifeos/src/__init__.py`
- Create: `lifeos/src/core/__init__.py`
- Create: `lifeos/src/agents/__init__.py`
- Create: `lifeos/src/advisors/__init__.py`
- Create: `lifeos/src/integrations/__init__.py`
- Create: `lifeos/src/mcp/__init__.py`
- Create: `lifeos/src/api/__init__.py`
- Create: `lifeos/src/cli/__init__.py`
- Create: `lifeos/config/advisors.yaml`
- Create: `lifeos/config/rag.yaml`
- Create: `lifeos/config/llm.yaml`
- Create: `lifeos/config/integrations.yaml`
- Create: `lifeos/config/schedules.yaml`
- Create: `lifeos/config/secrets.yaml.example`
- Create: `lifeos/tests/__init__.py`
- Create: `lifeos/tests/conftest.py`
- Create: `lifeos/README.md`

**Step 1: Create project directory and pyproject.toml**

```toml
# lifeos/pyproject.toml
[project]
name = "lifeos"
version = "0.1.0"
description = "Personal AI Life Management System"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
    "pydantic-ai>=0.1",
    "llama-index>=0.11",
    "llama-index-vector-stores-chroma>=0.3",
    "chromadb>=0.5",
    "mem0ai>=0.1",
    "fastapi>=0.115",
    "uvicorn>=0.32",
    "typer>=0.12",
    "rich>=13.0",
    "python-telegram-bot>=21.0",
    "apscheduler>=3.10",
    "structlog>=24.0",
    "pyyaml>=6.0",
    "aiosqlite>=0.20",
    "mcp>=1.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "mypy>=1.11",
    "ruff>=0.6",
    "types-pyyaml",
]

[project.scripts]
lifeos = "src.cli.main:app"

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "integration: integration tests with real local components",
    "external: tests requiring external API credentials",
    "llm: tests making real LLM API calls",
    "slow: slow-running tests",
]

[tool.mypy]
strict = true
python_version = "3.12"

[tool.ruff]
target-version = "py312"
line-length = 100

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Step 2: Create .gitignore**

```gitignore
# lifeos/.gitignore
# Runtime data
data/
config/secrets.yaml

# Obsidian
knowledge/.obsidian/

# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

**Step 3: Create all `__init__.py` files and package structure**

All `__init__.py` files are empty initially.

**Step 4: Create config files**

```yaml
# lifeos/config/advisors.yaml
advisors:
  health:
    display_name: "Health Management Advisor"
    description: "Medical records, fitness tracking, nutrition, medication reminders"
    prompt_file: src/advisors/health/prompts.py
    tools: [search_medical_records, log_health_metric, schedule_reminder]
    knowledge_dirs: [knowledge/areas/health/]
    llm: {provider: openai, model: gpt-4o}
    tags: [health, medical, fitness, nutrition]

  schedule:
    display_name: "Schedule & Productivity Advisor"
    description: "Calendar management, task prioritization, time blocking, reminders"
    prompt_file: src/advisors/schedule/prompts.py
    tools: [google_calendar_read, google_calendar_write, todoist_read, todoist_write]
    knowledge_dirs: [knowledge/areas/schedule/]
    llm: {provider: openai, model: gpt-4o-mini}
    tags: [schedule, calendar, productivity, tasks]
```

```yaml
# lifeos/config/rag.yaml
rag:
  vector_store: chroma
  persist_dir: data/chroma/
  embedding:
    provider: openai
    model: text-embedding-3-small
  chunking:
    parser: markdown
    chunk_size: 512
    chunk_overlap: 50
  indexing:
    watch_dirs:
      - knowledge/
    ignore_patterns:
      - "*.tmp"
      - ".obsidian/"
    incremental: true
```

```yaml
# lifeos/config/llm.yaml
llm:
  primary:
    provider: openai
    model: gpt-4o
  fallback:
    provider: anthropic
    model: claude-sonnet-4-20250514
  emergency:
    provider: openai
    model: gpt-4o-mini
  routing_model:
    provider: openai
    model: gpt-4o-mini
  memory_model:
    provider: openai
    model: gpt-4o-mini
```

```yaml
# lifeos/config/integrations.yaml
integrations:
  google_calendar:
    enabled: false
    calendar_id: primary
    sync_interval_minutes: 15
  todoist:
    enabled: false
    project_prefix: "LifeOS"
    sync_interval_minutes: 10
    auto_create_tasks: true
  obsidian:
    enabled: true
    vault_path: knowledge/
    watch_mode: polling
    poll_interval_seconds: 30
```

```yaml
# lifeos/config/schedules.yaml
scheduler:
  timezone: "Asia/Shanghai"
  store: sqlite
  store_path: data/reminders.db
  defaults:
    birthday: [7, 1, 0]
    deadline: [30, 14, 7, 3, 1]
    appointment: [1, 0]
    general: [3, 1]
  notification:
    primary: telegram
    fallback: cli
    quiet_hours:
      start: "22:00"
      end: "07:00"
      exceptions: ["urgent"]
```

```yaml
# lifeos/config/secrets.yaml.example
secrets:
  openai_api_key: "sk-..."
  anthropic_api_key: "sk-ant-..."
  telegram_bot_token: "123456:ABC..."
  telegram_owner_chat_id: "987654321"
  todoist_api_token: ""
  google_oauth:
    client_id: ""
    client_secret: ""
    refresh_token: ""
```

**Step 5: Create config loader**

```python
# lifeos/src/core/config.py
from pathlib import Path
from dataclasses import dataclass, field
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
class SecretsConfig:
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    telegram_bot_token: str = ""
    telegram_owner_chat_id: str = ""
    todoist_api_token: str = ""


def load_yaml(filename: str) -> dict:
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
    )
```

**Step 6: Create test conftest**

```python
# lifeos/tests/conftest.py
import pytest
from pathlib import Path


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def config_dir(project_root: Path) -> Path:
    """Return the config directory."""
    return project_root / "config"


@pytest.fixture
def tmp_knowledge(tmp_path: Path) -> Path:
    """Create a temporary knowledge base directory."""
    kb = tmp_path / "knowledge"
    for area in ["health", "finance", "schedule", "career", "legal",
                 "family", "mental-health", "learning", "entrepreneurship"]:
        (kb / "areas" / area).mkdir(parents=True)
    (kb / "projects").mkdir(parents=True)
    (kb / "resources").mkdir(parents=True)
    (kb / "archive").mkdir(parents=True)
    (kb / "journal").mkdir(parents=True)
    (kb / "inbox").mkdir(parents=True)
    return kb
```

**Step 7: Initialize project with uv**

Run: `cd lifeos && uv sync`
Expected: All dependencies installed, `.venv` created

**Step 8: Run initial checks**

Run: `cd lifeos && uv run ruff check src/ && uv run mypy src/core/config.py`
Expected: No errors

**Step 9: Commit**

```bash
git add lifeos/
git commit -m "feat: scaffold LifeOS project with config loader and test fixtures"
```

---

## Task 2: Knowledge Base Structure

**Files:**
- Create: `lifeos/knowledge/areas/health/.gitkeep`
- Create: `lifeos/knowledge/areas/finance/.gitkeep`
- Create: `lifeos/knowledge/areas/schedule/.gitkeep`
- Create: `lifeos/knowledge/areas/career/.gitkeep`
- Create: `lifeos/knowledge/areas/legal/.gitkeep`
- Create: `lifeos/knowledge/areas/family/.gitkeep`
- Create: `lifeos/knowledge/areas/mental-health/.gitkeep`
- Create: `lifeos/knowledge/areas/learning/.gitkeep`
- Create: `lifeos/knowledge/areas/entrepreneurship/.gitkeep`
- Create: `lifeos/knowledge/projects/.gitkeep`
- Create: `lifeos/knowledge/resources/.gitkeep`
- Create: `lifeos/knowledge/archive/.gitkeep`
- Create: `lifeos/knowledge/journal/.gitkeep`
- Create: `lifeos/knowledge/inbox/.gitkeep`
- Create: `lifeos/knowledge/templates/note.md`
- Create: `lifeos/knowledge/templates/journal.md`

**Step 1: Create PARA directory structure**

Create all directories with `.gitkeep` files.

**Step 2: Create note template**

```markdown
---
type: note
date: YYYY-MM-DD
tags: []
advisor:
confidentiality: normal
---

# Title

Content here.
```

**Step 3: Create journal template**

```markdown
---
type: journal
date: YYYY-MM-DD
tags: [journal, daily]
advisor:
confidentiality: normal
---

# Journal — YYYY-MM-DD

## Morning Intention


## Notes


## Evening Reflection

```

**Step 4: Add sample notes for testing**

Create `lifeos/knowledge/areas/health/blood-pressure-log.md`:

```markdown
---
type: log
date: 2026-02-27
tags: [health, blood-pressure, checkup]
advisor: health
confidentiality: normal
---

# Blood Pressure Log

## 2026-02-27
- Reading: 120/80 mmHg
- Notes: Normal range. Doctor says continue current routine.
- Next checkup: 2026-06-01
```

Create `lifeos/knowledge/areas/schedule/weekly-routine.md`:

```markdown
---
type: note
date: 2026-02-27
tags: [schedule, routine, weekly]
advisor: schedule
confidentiality: normal
---

# Weekly Routine

## Weekdays
- 07:00 Wake up
- 07:30 Exercise
- 09:00 Deep work block
- 12:00 Lunch
- 14:00 Meetings / collaboration
- 18:00 End work
- 22:00 Wind down

## Weekend
- Flexible schedule
- Family time priority
```

**Step 5: Commit**

```bash
git add lifeos/knowledge/
git commit -m "feat: create PARA knowledge base structure with templates and sample notes"
```

---

## Task 3: RAG Pipeline

**Files:**
- Create: `lifeos/src/core/rag.py`
- Create: `lifeos/tests/unit/test_rag.py`
- Create: `lifeos/tests/integration/test_rag_pipeline.py`

**Step 1: Write unit tests for frontmatter parsing and filter building**

```python
# lifeos/tests/unit/test_rag.py
from src.core.rag import parse_frontmatter, build_metadata_filter


class TestFrontmatterParsing:
    def test_extracts_advisor_field(self):
        content = "---\nadvisor: health\ntags: [bp]\n---\n# Note\nContent"
        metadata = parse_frontmatter(content)
        assert metadata["advisor"] == "health"
        assert metadata["tags"] == ["bp"]

    def test_handles_missing_frontmatter(self):
        content = "# Note\nNo frontmatter here"
        metadata = parse_frontmatter(content)
        assert metadata == {}

    def test_handles_empty_frontmatter(self):
        content = "---\n---\n# Note"
        metadata = parse_frontmatter(content)
        assert metadata == {}


class TestMetadataFilter:
    def test_builds_advisor_filter(self):
        filters = build_metadata_filter(advisor="health")
        assert filters["advisor"] == "health"

    def test_builds_empty_filter(self):
        filters = build_metadata_filter()
        assert filters == {}

    def test_builds_multi_filter(self):
        filters = build_metadata_filter(advisor="health", tags=["bp"])
        assert filters["advisor"] == "health"
        assert filters["tags"] == ["bp"]
```

**Step 2: Run tests to verify they fail**

Run: `cd lifeos && uv run pytest tests/unit/test_rag.py -v`
Expected: FAIL — `parse_frontmatter` not defined

**Step 3: Implement RAG pipeline**

```python
# lifeos/src/core/rag.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
import structlog

logger = structlog.get_logger()


@dataclass
class RAGResponse:
    """Response from a RAG query."""
    chunks: list[RAGChunk] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n\n---\n\n".join(c.text for c in self.chunks)

    @property
    def sources(self) -> list[str]:
        return [c.source for c in self.chunks]


@dataclass
class RAGChunk:
    """A single retrieved chunk."""
    text: str
    source: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


def parse_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from Markdown content."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def build_metadata_filter(**kwargs: Any) -> dict[str, Any]:
    """Build a metadata filter dict from keyword arguments."""
    return {k: v for k, v in kwargs.items() if v is not None}


class RAGPipeline:
    """Document retrieval over the knowledge/ directory using LlamaIndex + ChromaDB."""

    def __init__(self, persist_dir: str = "data/chroma/",
                 embedding_model: str = "text-embedding-3-small",
                 chunk_size: int = 512,
                 chunk_overlap: int = 50):
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._index = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization of LlamaIndex components."""
        if self._initialized:
            return

        import chromadb
        from llama_index.core import VectorStoreIndex, StorageContext
        from llama_index.vector_stores.chroma import ChromaVectorStore

        self._chroma_client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._collection = self._chroma_client.get_or_create_collection("lifeos")
        self._vector_store = ChromaVectorStore(chroma_collection=self._collection)
        self._storage_context = StorageContext.from_defaults(
            vector_store=self._vector_store
        )

        # Try to load existing index, or create empty one
        try:
            self._index = VectorStoreIndex.from_vector_store(
                self._vector_store,
            )
        except Exception:
            self._index = VectorStoreIndex.from_documents(
                [],
                storage_context=self._storage_context,
            )

        self._initialized = True
        logger.info("rag.initialized", persist_dir=str(self.persist_dir))

    def index_documents(self, paths: list[Path]) -> int:
        """Index markdown files into the vector store. Returns count of indexed docs."""
        self._ensure_initialized()

        from llama_index.core import Document
        from llama_index.core.node_parser import MarkdownNodeParser

        documents = []
        for path in paths:
            if not path.exists() or not path.suffix == ".md":
                continue
            content = path.read_text(encoding="utf-8")
            metadata = parse_frontmatter(content)
            metadata["source"] = str(path)
            documents.append(Document(text=content, metadata=metadata))

        if not documents:
            return 0

        parser = MarkdownNodeParser()
        nodes = parser.get_nodes_from_documents(documents)

        self._index.insert_nodes(nodes)

        logger.info("rag.indexed", count=len(documents), nodes=len(nodes))
        return len(documents)

    def index_directory(self, directory: Path, recursive: bool = True) -> int:
        """Index all markdown files in a directory."""
        if recursive:
            paths = list(directory.rglob("*.md"))
        else:
            paths = list(directory.glob("*.md"))
        return self.index_documents(paths)

    def query(self, question: str, top_k: int = 5,
              filters: dict[str, Any] | None = None) -> RAGResponse:
        """Query the knowledge base."""
        self._ensure_initialized()

        query_engine = self._index.as_query_engine(similarity_top_k=top_k)
        response = query_engine.query(question)

        chunks = []
        for node in response.source_nodes:
            chunks.append(RAGChunk(
                text=node.text,
                source=node.metadata.get("source", "unknown"),
                score=node.score or 0.0,
                metadata=node.metadata,
            ))

        return RAGResponse(chunks=chunks)

    def query_for_advisor(self, question: str, advisor: str,
                          top_k: int = 5) -> RAGResponse:
        """Scoped query filtered by advisor domain."""
        # For now, prepend advisor context to query for better relevance
        # TODO: implement proper metadata filtering when ChromaDB supports it in LlamaIndex
        scoped_question = f"[{advisor} domain] {question}"
        return self.query(scoped_question, top_k=top_k)

    def get_stats(self) -> dict[str, Any]:
        """Get index statistics."""
        self._ensure_initialized()
        count = self._collection.count()
        return {
            "document_count": count,
            "persist_dir": str(self.persist_dir),
            "embedding_model": self.embedding_model,
        }
```

**Step 4: Run unit tests**

Run: `cd lifeos && uv run pytest tests/unit/test_rag.py -v`
Expected: PASS

**Step 5: Write integration test**

```python
# lifeos/tests/integration/test_rag_pipeline.py
import pytest
from pathlib import Path
from src.core.rag import RAGPipeline


@pytest.mark.integration
class TestRAGPipelineIntegration:
    @pytest.fixture
    def rag(self, tmp_path: Path) -> RAGPipeline:
        return RAGPipeline(persist_dir=str(tmp_path / "chroma"))

    @pytest.fixture
    def sample_note(self, tmp_path: Path) -> Path:
        note = tmp_path / "test-note.md"
        note.write_text(
            "---\n"
            "advisor: health\n"
            "tags: [blood-pressure]\n"
            "---\n"
            "# Blood Pressure\n\n"
            "My blood pressure reading was 120/80 on Feb 27.\n"
            "Doctor says this is normal.\n"
        )
        return note

    def test_index_and_query(self, rag: RAGPipeline, sample_note: Path):
        count = rag.index_documents([sample_note])
        assert count == 1

        results = rag.query("blood pressure reading")
        assert len(results.chunks) > 0
        assert "120/80" in results.text

    def test_get_stats(self, rag: RAGPipeline, sample_note: Path):
        rag.index_documents([sample_note])
        stats = rag.get_stats()
        assert stats["document_count"] > 0

    def test_empty_query(self, rag: RAGPipeline):
        results = rag.query("something random")
        assert isinstance(results.chunks, list)
```

**Step 6: Run integration test**

Run: `cd lifeos && uv run pytest tests/integration/test_rag_pipeline.py -v -m integration`
Expected: PASS (requires OpenAI API key for embeddings)

**Step 7: Commit**

```bash
git add lifeos/src/core/rag.py lifeos/tests/
git commit -m "feat: implement RAG pipeline with LlamaIndex + ChromaDB"
```

---

## Task 4: Memory Layer (Mem0)

**Files:**
- Create: `lifeos/src/core/memory.py`
- Create: `lifeos/tests/unit/test_memory.py`
- Create: `lifeos/tests/integration/test_mem0.py`

**Step 1: Write unit tests**

```python
# lifeos/tests/unit/test_memory.py
from src.core.memory import MemoryItem, format_memories_for_prompt


class TestMemoryFormatting:
    def test_format_empty_memories(self):
        result = format_memories_for_prompt([])
        assert result == "No relevant memories found."

    def test_format_single_memory(self):
        items = [MemoryItem(id="1", text="User prefers index funds", metadata={})]
        result = format_memories_for_prompt(items)
        assert "index funds" in result

    def test_format_multiple_memories(self):
        items = [
            MemoryItem(id="1", text="Prefers index funds", metadata={}),
            MemoryItem(id="2", text="Risk tolerance: moderate", metadata={}),
        ]
        result = format_memories_for_prompt(items)
        assert "index funds" in result
        assert "moderate" in result
```

**Step 2: Run tests to verify they fail**

Run: `cd lifeos && uv run pytest tests/unit/test_memory.py -v`
Expected: FAIL

**Step 3: Implement memory manager**

```python
# lifeos/src/core/memory.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

logger = structlog.get_logger()


@dataclass
class MemoryItem:
    """A single memory entry."""
    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def format_memories_for_prompt(memories: list[MemoryItem]) -> str:
    """Format memories for injection into advisor prompts."""
    if not memories:
        return "No relevant memories found."
    lines = []
    for i, mem in enumerate(memories, 1):
        lines.append(f"- {mem.text}")
    return "Relevant memories:\n" + "\n".join(lines)


class MemoryManager:
    """Cross-session memory powered by Mem0."""

    def __init__(self, persist_dir: str = "data/mem0/",
                 llm_model: str = "gpt-4o-mini",
                 user_id: str = "owner"):
        self.persist_dir = persist_dir
        self.llm_model = llm_model
        self.user_id = user_id
        self._mem0 = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization of Mem0."""
        if self._initialized:
            return

        from mem0 import Memory

        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "lifeos_memory",
                    "path": self.persist_dir,
                },
            },
        }

        self._mem0 = Memory.from_config(config)
        self._initialized = True
        logger.info("memory.initialized", persist_dir=self.persist_dir)

    def add(self, content: str, metadata: dict[str, Any] | None = None) -> str:
        """Store a memory. Returns memory ID."""
        self._ensure_initialized()
        assert self._mem0 is not None

        result = self._mem0.add(
            content,
            user_id=self.user_id,
            metadata=metadata or {},
        )
        memory_id = result.get("id", "") if isinstance(result, dict) else ""
        logger.info("memory.added", content_preview=content[:50], id=memory_id)
        return memory_id

    def search(self, query: str, limit: int = 10) -> list[MemoryItem]:
        """Search memories by semantic similarity."""
        self._ensure_initialized()
        assert self._mem0 is not None

        results = self._mem0.search(query, user_id=self.user_id, limit=limit)

        items = []
        for r in results:
            if isinstance(r, dict):
                items.append(MemoryItem(
                    id=r.get("id", ""),
                    text=r.get("memory", r.get("text", "")),
                    metadata=r.get("metadata", {}),
                ))
        return items

    def get_advisor_context(self, advisor: str, query: str,
                            limit: int = 5) -> str:
        """Get formatted memories relevant to a specific advisor + query."""
        scoped_query = f"[{advisor}] {query}"
        memories = self.search(scoped_query, limit=limit)
        return format_memories_for_prompt(memories)

    def delete(self, memory_id: str) -> bool:
        """Delete a specific memory."""
        self._ensure_initialized()
        assert self._mem0 is not None

        try:
            self._mem0.delete(memory_id)
            logger.info("memory.deleted", id=memory_id)
            return True
        except Exception as e:
            logger.error("memory.delete_failed", id=memory_id, error=str(e))
            return False

    def list_all(self, limit: int = 100) -> list[MemoryItem]:
        """List all stored memories."""
        self._ensure_initialized()
        assert self._mem0 is not None

        results = self._mem0.get_all(user_id=self.user_id)

        items = []
        for r in (results if isinstance(results, list) else []):
            if isinstance(r, dict):
                items.append(MemoryItem(
                    id=r.get("id", ""),
                    text=r.get("memory", r.get("text", "")),
                    metadata=r.get("metadata", {}),
                ))
        return items[:limit]

    def get_stats(self) -> dict[str, Any]:
        """Get memory statistics."""
        all_memories = self.list_all()
        return {
            "total_memories": len(all_memories),
            "persist_dir": self.persist_dir,
        }
```

**Step 4: Run unit tests**

Run: `cd lifeos && uv run pytest tests/unit/test_memory.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add lifeos/src/core/memory.py lifeos/tests/unit/test_memory.py
git commit -m "feat: implement Mem0 memory manager with search and advisor context"
```

---

## Task 5: Message Types & Conversation Context

**Files:**
- Create: `lifeos/src/core/context.py`
- Create: `lifeos/src/core/message.py`
- Create: `lifeos/tests/unit/test_message.py`

**Step 1: Write unit tests**

```python
# lifeos/tests/unit/test_message.py
from src.core.message import OutgoingResponse, ActionItem


class TestResponseRendering:
    def test_render_basic_text(self):
        response = OutgoingResponse(text="Hello world", advisor="health")
        assert response.text == "Hello world"
        assert response.advisor == "health"

    def test_render_with_action_items(self):
        response = OutgoingResponse(
            text="You should exercise more.",
            advisor="health",
            action_items=[ActionItem(title="Go for a walk", advisor="health")],
        )
        assert len(response.action_items) == 1
        assert response.action_items[0].title == "Go for a walk"

    def test_render_for_telegram(self):
        response = OutgoingResponse(text="**Bold** text", advisor="health")
        rendered = response.render_for("telegram")
        assert isinstance(rendered, str)
        assert "Bold" in rendered

    def test_render_for_cli(self):
        response = OutgoingResponse(text="# Header\nContent", advisor=None)
        rendered = response.render_for("cli")
        assert "Header" in rendered
```

**Step 2: Run tests to verify they fail**

Run: `cd lifeos && uv run pytest tests/unit/test_message.py -v`
Expected: FAIL

**Step 3: Implement message types**

```python
# lifeos/src/core/context.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


@dataclass
class Message:
    """A single message in conversation history."""
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ConversationContext:
    """Passed through the entire request lifecycle."""
    session_id: str
    channel: Literal["opencode", "cli", "telegram", "api"]
    history: list[Message] = field(default_factory=list)
    active_advisor: str | None = None
    metadata: dict = field(default_factory=dict)
```

```python
# lifeos/src/core/message.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


@dataclass
class Attachment:
    """File attachment (photo, document, etc.)."""
    filename: str
    content_type: str
    data: bytes = b""


@dataclass
class IncomingMessage:
    """Channel-agnostic incoming message."""
    text: str
    channel: Literal["opencode", "cli", "telegram", "api"]
    session_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionItem:
    """An action item extracted from advisor response."""
    title: str
    advisor: str
    due_date: str | None = None
    priority: str = "medium"


@dataclass
class FollowUp:
    """A suggested follow-up question."""
    question: str
    advisor: str


@dataclass
class Reminder:
    """A reminder to be scheduled."""
    message: str
    date: str
    advance_days: list[int] = field(default_factory=lambda: [3, 1, 0])
    advisor: str = ""


@dataclass
class OutgoingResponse:
    """Channel-agnostic response."""
    text: str
    advisor: str | None = None
    action_items: list[ActionItem] = field(default_factory=list)
    follow_ups: list[FollowUp] = field(default_factory=list)
    reminders: list[Reminder] = field(default_factory=list)
    caveat: str | None = None
    error: bool = False

    def render_for(self, channel: str) -> str:
        """Format response for specific channel."""
        match channel:
            case "cli" | "opencode":
                return self._render_markdown()
            case "telegram":
                return self._render_telegram()
            case "api":
                return self.text
            case _:
                return self.text

    def _render_markdown(self) -> str:
        """Full Markdown rendering for CLI/OpenCode."""
        parts = []
        if self.advisor:
            parts.append(f"**{self.advisor.replace('_', ' ').title()} Advisor**\n")
        parts.append(self.text)
        if self.caveat:
            parts.append(f"\n> ⚠️ {self.caveat}")
        if self.action_items:
            parts.append("\n**Action Items:**")
            for item in self.action_items:
                parts.append(f"- [ ] {item.title}")
        if self.follow_ups:
            parts.append("\n**You might also ask:**")
            for fu in self.follow_ups:
                parts.append(f"- {fu.question}")
        return "\n".join(parts)

    def _render_telegram(self) -> str:
        """Telegram-compatible Markdown rendering."""
        parts = []
        if self.advisor:
            parts.append(
                f"*{self.advisor.replace('_', ' ').title()} Advisor*\n"
            )
        # Convert **bold** to *bold* for Telegram
        text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", self.text)
        parts.append(text)
        if self.caveat:
            parts.append(f"\n⚠️ {self.caveat}")
        if self.action_items:
            parts.append("\n*Action Items:*")
            for item in self.action_items:
                parts.append(f"• {item.title}")
        return "\n".join(parts)
```

**Step 4: Run tests**

Run: `cd lifeos && uv run pytest tests/unit/test_message.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add lifeos/src/core/context.py lifeos/src/core/message.py lifeos/tests/unit/test_message.py
git commit -m "feat: add message types, conversation context, and response rendering"
```

---

## Task 6: Base Advisor

**Files:**
- Create: `lifeos/src/agents/base_advisor.py`
- Create: `lifeos/tests/unit/test_base_advisor.py`

**Step 1: Write tests**

```python
# lifeos/tests/unit/test_base_advisor.py
import pytest
from src.agents.base_advisor import BaseAdvisor, AdvisorResponse


class TestAdvisorResponse:
    def test_create_response(self):
        response = AdvisorResponse(
            text="Drink more water.",
            advisor="health",
        )
        assert response.text == "Drink more water."
        assert response.advisor == "health"
        assert response.action_items == []

    def test_response_with_action_items(self):
        response = AdvisorResponse(
            text="Adjust your budget.",
            advisor="finance",
            action_items=["Review expenses", "Set savings goal"],
        )
        assert len(response.action_items) == 2
```

**Step 2: Run tests to verify fail**

Run: `cd lifeos && uv run pytest tests/unit/test_base_advisor.py -v`
Expected: FAIL

**Step 3: Implement base advisor**

```python
# lifeos/src/agents/base_advisor.py
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import structlog

from src.core.context import ConversationContext
from src.core.memory import MemoryManager, format_memories_for_prompt
from src.core.rag import RAGPipeline

logger = structlog.get_logger()


@dataclass
class AdvisorResponse:
    """Structured response from an advisor."""
    text: str
    advisor: str
    action_items: list[str] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    reminders: list[dict[str, Any]] = field(default_factory=list)


class BaseAdvisor(ABC):
    """Base class for all domain advisors."""

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        system_prompt: str,
        rag: RAGPipeline | None = None,
        memory: MemoryManager | None = None,
        tags: list[str] | None = None,
    ):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.system_prompt = system_prompt
        self.rag = rag
        self.memory = memory
        self.tags = tags or []

    async def handle(self, query: str, context: ConversationContext) -> AdvisorResponse:
        """Main entry point — called by Chief of Staff."""
        logger.info("advisor.handling", advisor=self.name, query=query[:80])

        # 1. Gather context
        rag_context = ""
        if self.rag:
            rag_result = self.rag.query_for_advisor(query, self.name)
            rag_context = rag_result.text

        memories = ""
        if self.memory:
            memories = self.memory.get_advisor_context(self.name, query)

        # 2. Build prompt
        full_prompt = self._build_prompt(query, rag_context, memories, context)

        # 3. Call LLM
        response = await self._call_llm(full_prompt)

        # 4. Post-process
        await self._post_process(query, response)

        return response

    def _build_prompt(
        self,
        query: str,
        rag_context: str,
        memories: str,
        context: ConversationContext,
    ) -> str:
        """Build the full prompt with all context injected."""
        parts = [
            f"# System\n{self.system_prompt}",
            f"\n# User's Personal Context\n{memories}",
        ]
        if rag_context:
            parts.append(f"\n# Relevant Knowledge Base Documents\n{rag_context}")
        if context.history:
            history_text = "\n".join(
                f"{m.role}: {m.content}" for m in context.history[-5:]
            )
            parts.append(f"\n# Recent Conversation\n{history_text}")
        parts.append(f"\n# User's Question\n{query}")
        return "\n".join(parts)

    @abstractmethod
    async def _call_llm(self, prompt: str) -> AdvisorResponse:
        """Call the LLM with the built prompt. Implemented by subclasses."""
        ...

    async def _post_process(self, query: str, response: AdvisorResponse) -> None:
        """Store memories and handle follow-ups after response."""
        if self.memory:
            try:
                self.memory.add(
                    f"Q: {query}\nA: {response.text[:200]}",
                    metadata={"advisor": self.name},
                )
            except Exception as e:
                logger.warning("advisor.memory_save_failed", error=str(e))

    def get_info(self) -> dict[str, Any]:
        """Return advisor info for registry."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "tags": self.tags,
        }
```

**Step 4: Run tests**

Run: `cd lifeos && uv run pytest tests/unit/test_base_advisor.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add lifeos/src/agents/base_advisor.py lifeos/tests/unit/test_base_advisor.py
git commit -m "feat: implement BaseAdvisor with RAG and memory context injection"
```

---

## Task 7: Health & Schedule Advisors

**Files:**
- Create: `lifeos/src/advisors/health/__init__.py`
- Create: `lifeos/src/advisors/health/prompts.py`
- Create: `lifeos/src/advisors/health/advisor.py`
- Create: `lifeos/src/advisors/schedule/__init__.py`
- Create: `lifeos/src/advisors/schedule/prompts.py`
- Create: `lifeos/src/advisors/schedule/advisor.py`
- Create: `lifeos/tests/unit/test_advisors.py`

**Step 1: Create health advisor prompts and implementation**

```python
# lifeos/src/advisors/health/prompts.py

SYSTEM_PROMPT = """You are a Health Management Advisor in the LifeOS personal AI system.

Your responsibilities:
- Help track and analyze health metrics (blood pressure, weight, exercise, sleep)
- Provide general wellness guidance (NOT medical diagnosis)
- Remind about medical appointments and medication schedules
- Suggest healthy habits based on the user's goals and history

Important rules:
- NEVER diagnose medical conditions
- NEVER prescribe or recommend specific medications
- ALWAYS recommend consulting a healthcare professional for medical concerns
- Reference the user's personal health data when available
- Be encouraging and supportive

You have access to the user's health notes and memory. Use them to personalize your advice."""
```

```python
# lifeos/src/advisors/health/advisor.py
from __future__ import annotations

from src.agents.base_advisor import BaseAdvisor, AdvisorResponse
from src.advisors.health.prompts import SYSTEM_PROMPT
from src.core.rag import RAGPipeline
from src.core.memory import MemoryManager


class HealthAdvisor(BaseAdvisor):
    """Health Management Advisor."""

    def __init__(self, rag: RAGPipeline | None = None,
                 memory: MemoryManager | None = None):
        super().__init__(
            name="health",
            display_name="Health Management Advisor",
            description="Medical records, fitness tracking, nutrition, medication reminders",
            system_prompt=SYSTEM_PROMPT,
            rag=rag,
            memory=memory,
            tags=["health", "medical", "fitness", "nutrition"],
        )

    async def _call_llm(self, prompt: str) -> AdvisorResponse:
        """Call LLM for health advice."""
        # TODO: Replace with PydanticAI agent call
        # For now, use direct OpenAI call
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI()
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt.split("# User's Question")[0]},
                    {"role": "user", "content": prompt.split("# User's Question")[-1]},
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            text = response.choices[0].message.content or "I couldn't generate a response."
            return AdvisorResponse(text=text, advisor=self.name)
        except Exception as e:
            return AdvisorResponse(
                text=f"I'm having trouble processing your health query. Error: {e}",
                advisor=self.name,
            )
```

**Step 2: Create schedule advisor**

```python
# lifeos/src/advisors/schedule/prompts.py

SYSTEM_PROMPT = """You are a Schedule & Productivity Advisor in the LifeOS personal AI system.

Your responsibilities:
- Help manage daily/weekly schedules and time blocking
- Prioritize tasks based on urgency, importance, and energy levels
- Suggest optimal meeting times and break schedules
- Track productivity patterns and suggest improvements
- Manage reminders and deadlines

Important rules:
- Always consider the user's existing commitments before suggesting changes
- Respect work-life balance — don't over-schedule
- Suggest buffer time between meetings
- Consider time zones when relevant
- Reference the user's calendar and task data when available

You have access to the user's schedule notes and memory. Use them to personalize your advice."""
```

```python
# lifeos/src/advisors/schedule/advisor.py
from __future__ import annotations

from src.agents.base_advisor import BaseAdvisor, AdvisorResponse
from src.advisors.schedule.prompts import SYSTEM_PROMPT
from src.core.rag import RAGPipeline
from src.core.memory import MemoryManager


class ScheduleAdvisor(BaseAdvisor):
    """Schedule & Productivity Advisor."""

    def __init__(self, rag: RAGPipeline | None = None,
                 memory: MemoryManager | None = None):
        super().__init__(
            name="schedule",
            display_name="Schedule & Productivity Advisor",
            description="Calendar management, task prioritization, time blocking, reminders",
            system_prompt=SYSTEM_PROMPT,
            rag=rag,
            memory=memory,
            tags=["schedule", "calendar", "productivity", "tasks"],
        )

    async def _call_llm(self, prompt: str) -> AdvisorResponse:
        """Call LLM for schedule advice."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI()
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt.split("# User's Question")[0]},
                    {"role": "user", "content": prompt.split("# User's Question")[-1]},
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            text = response.choices[0].message.content or "I couldn't generate a response."
            return AdvisorResponse(text=text, advisor=self.name)
        except Exception as e:
            return AdvisorResponse(
                text=f"I'm having trouble with your schedule query. Error: {e}",
                advisor=self.name,
            )
```

**Step 3: Write tests**

```python
# lifeos/tests/unit/test_advisors.py
from src.advisors.health.advisor import HealthAdvisor
from src.advisors.schedule.advisor import ScheduleAdvisor
from src.advisors.health.prompts import SYSTEM_PROMPT as HEALTH_PROMPT
from src.advisors.schedule.prompts import SYSTEM_PROMPT as SCHEDULE_PROMPT


class TestHealthAdvisor:
    def test_creation(self):
        advisor = HealthAdvisor()
        assert advisor.name == "health"
        assert advisor.display_name == "Health Management Advisor"
        assert "health" in advisor.tags

    def test_prompt_safety(self):
        assert "NEVER diagnose" in HEALTH_PROMPT
        assert "NEVER prescribe" in HEALTH_PROMPT
        assert "healthcare professional" in HEALTH_PROMPT

    def test_get_info(self):
        advisor = HealthAdvisor()
        info = advisor.get_info()
        assert info["name"] == "health"
        assert "tags" in info


class TestScheduleAdvisor:
    def test_creation(self):
        advisor = ScheduleAdvisor()
        assert advisor.name == "schedule"
        assert "calendar" in advisor.tags

    def test_prompt_content(self):
        assert "time blocking" in SCHEDULE_PROMPT
        assert "work-life balance" in SCHEDULE_PROMPT

    def test_get_info(self):
        advisor = ScheduleAdvisor()
        info = advisor.get_info()
        assert info["name"] == "schedule"
```

**Step 4: Run tests**

Run: `cd lifeos && uv run pytest tests/unit/test_advisors.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add lifeos/src/advisors/ lifeos/tests/unit/test_advisors.py
git commit -m "feat: implement Health and Schedule advisors with safety-guarded prompts"
```

---

## Task 8: Chief of Staff (Router Agent)

**Files:**
- Create: `lifeos/src/agents/chief_of_staff.py`
- Create: `lifeos/tests/unit/test_routing.py`

**Step 1: Write routing tests**

```python
# lifeos/tests/unit/test_routing.py
from src.agents.chief_of_staff import classify_intent, RoutingDecision


class TestIntentClassification:
    def test_health_query(self):
        routing = classify_intent("What's a good blood pressure range?")
        assert routing.action == "single_advisor"
        assert routing.advisor == "health"

    def test_schedule_query(self):
        routing = classify_intent("What's on my calendar tomorrow?")
        assert routing.action == "single_advisor"
        assert routing.advisor == "schedule"

    def test_greeting_is_direct(self):
        routing = classify_intent("Hello")
        assert routing.action == "direct"

    def test_simple_question_is_direct(self):
        routing = classify_intent("What time is it?")
        assert routing.action == "direct"

    def test_cross_domain_is_multi(self):
        routing = classify_intent(
            "I'm stressed about money and it's affecting my sleep"
        )
        assert routing.action in ("single_advisor", "multi_advisor")

    def test_finance_keywords(self):
        routing = classify_intent("Should I invest in index funds?")
        assert routing.advisor in ("finance", None)
        # finance advisor not yet registered, falls to direct or unknown
```

**Step 2: Run tests to verify fail**

Run: `cd lifeos && uv run pytest tests/unit/test_routing.py -v`
Expected: FAIL

**Step 3: Implement Chief of Staff**

```python
# lifeos/src/agents/chief_of_staff.py
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import structlog

from src.agents.base_advisor import BaseAdvisor, AdvisorResponse
from src.core.context import ConversationContext
from src.core.message import OutgoingResponse, ActionItem, FollowUp, Reminder
from src.core.memory import MemoryManager

logger = structlog.get_logger()


# Keyword-based routing (fast, no LLM call needed)
ADVISOR_KEYWORDS: dict[str, list[str]] = {
    "health": [
        "health", "medical", "doctor", "blood pressure", "exercise", "fitness",
        "nutrition", "diet", "sleep", "medication", "symptom", "pain", "weight",
        "checkup", "hospital", "clinic", "vaccine", "allergy",
    ],
    "finance": [
        "money", "finance", "invest", "budget", "tax", "expense", "salary",
        "portfolio", "stock", "fund", "savings", "debt", "mortgage", "insurance",
        "retirement", "dividend",
    ],
    "schedule": [
        "schedule", "calendar", "meeting", "appointment", "deadline", "task",
        "productivity", "time", "plan", "agenda", "reminder", "todo",
    ],
    "career": [
        "career", "job", "resume", "interview", "promotion", "skill",
        "networking", "professional", "workplace", "salary negotiation",
    ],
    "legal": [
        "legal", "law", "contract", "lease", "rights", "court", "lawyer",
        "attorney", "dispute", "compliance", "regulation",
    ],
    "family": [
        "family", "parent", "child", "marriage", "relationship", "birthday",
        "anniversary", "spouse", "wife", "husband", "kids", "parenting",
    ],
    "mental_health": [
        "stress", "anxiety", "depression", "mental", "therapy", "meditation",
        "mindfulness", "mood", "emotional", "wellbeing", "burnout", "overwhelm",
    ],
    "learning": [
        "learn", "study", "course", "book", "education", "skill", "tutorial",
        "certification", "training", "knowledge",
    ],
    "entrepreneurship": [
        "startup", "business", "entrepreneur", "venture", "pitch", "market",
        "product", "customer", "revenue", "funding", "investor",
    ],
}

DIRECT_PATTERNS = [
    r"^(hi|hello|hey|good morning|good evening|thanks|thank you)",
    r"^what time",
    r"^who are you",
    r"^help$",
]


@dataclass
class RoutingDecision:
    """Result of intent classification."""
    action: str  # "direct" | "single_advisor" | "multi_advisor"
    advisor: str | None = None
    advisors: list[str] = field(default_factory=list)
    confidence: float = 0.0


def classify_intent(query: str) -> RoutingDecision:
    """Classify user intent using keyword matching.

    Fast, no LLM call. For ambiguous queries, defaults to direct answer.
    """
    query_lower = query.lower().strip()

    # Check for direct-answer patterns
    for pattern in DIRECT_PATTERNS:
        if re.match(pattern, query_lower):
            return RoutingDecision(action="direct", confidence=1.0)

    # Score each advisor by keyword matches
    scores: dict[str, int] = {}
    for advisor, keywords in ADVISOR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[advisor] = score

    if not scores:
        return RoutingDecision(action="direct", confidence=0.5)

    # Sort by score descending
    sorted_advisors = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # If top advisor has significantly higher score, route to single
    if len(sorted_advisors) == 1 or sorted_advisors[0][1] > sorted_advisors[1][1]:
        return RoutingDecision(
            action="single_advisor",
            advisor=sorted_advisors[0][0],
            confidence=min(sorted_advisors[0][1] / 3, 1.0),
        )

    # Multiple advisors with similar scores → multi-advisor
    top_score = sorted_advisors[0][1]
    multi = [name for name, score in sorted_advisors if score >= top_score * 0.5]
    if len(multi) > 1:
        return RoutingDecision(
            action="multi_advisor",
            advisors=multi[:3],  # max 3 advisors
            confidence=0.7,
        )

    return RoutingDecision(
        action="single_advisor",
        advisor=sorted_advisors[0][0],
        confidence=0.6,
    )


class ChiefOfStaff:
    """Router agent — the user's primary interface."""

    def __init__(
        self,
        advisors: dict[str, BaseAdvisor] | None = None,
        memory: MemoryManager | None = None,
    ):
        self.advisors = advisors or {}
        self.memory = memory

    def register_advisor(self, advisor: BaseAdvisor) -> None:
        """Register an advisor for routing."""
        self.advisors[advisor.name] = advisor
        logger.info("chief.advisor_registered", advisor=advisor.name)

    async def process(
        self, query: str, context: ConversationContext
    ) -> OutgoingResponse:
        """Main entry point for all user queries."""
        logger.info("chief.processing", query=query[:80], channel=context.channel)

        # If user is mid-conversation with an advisor, keep routing there
        if context.active_advisor and context.active_advisor in self.advisors:
            return await self._route_to_advisor(
                context.active_advisor, query, context
            )

        # Classify intent
        routing = classify_intent(query)
        logger.info(
            "chief.routing",
            action=routing.action,
            advisor=routing.advisor,
            advisors=routing.advisors,
            confidence=routing.confidence,
        )

        match routing.action:
            case "direct":
                return await self._direct_answer(query, context)
            case "single_advisor":
                if routing.advisor and routing.advisor in self.advisors:
                    return await self._route_to_advisor(
                        routing.advisor, query, context
                    )
                return await self._direct_answer(query, context)
            case "multi_advisor":
                available = [
                    a for a in routing.advisors if a in self.advisors
                ]
                if available:
                    return await self._multi_advisor(available, query, context)
                return await self._direct_answer(query, context)
            case _:
                return await self._direct_answer(query, context)

    async def _direct_answer(
        self, query: str, context: ConversationContext
    ) -> OutgoingResponse:
        """Answer directly without an advisor."""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI()

            memory_context = ""
            if self.memory:
                memory_context = self.memory.get_advisor_context("general", query)

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the Chief of Staff for LifeOS, a personal AI "
                            "life management system. Answer the user's question "
                            "helpfully and concisely.\n\n"
                            f"User context:\n{memory_context}"
                        ),
                    },
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            text = response.choices[0].message.content or "How can I help you?"
            return OutgoingResponse(text=text)
        except Exception as e:
            logger.error("chief.direct_answer_failed", error=str(e))
            return OutgoingResponse(
                text="I'm having trouble processing your request. Please try again.",
                error=True,
            )

    async def _route_to_advisor(
        self, advisor_name: str, query: str, context: ConversationContext
    ) -> OutgoingResponse:
        """Route to a single advisor."""
        advisor = self.advisors[advisor_name]
        try:
            result = await advisor.handle(query, context)
            return OutgoingResponse(
                text=result.text,
                advisor=result.advisor,
                action_items=[
                    ActionItem(title=item, advisor=advisor_name)
                    for item in result.action_items
                ],
                follow_ups=[
                    FollowUp(question=q, advisor=advisor_name)
                    for q in result.follow_ups
                ],
            )
        except Exception as e:
            logger.error("chief.advisor_failed", advisor=advisor_name, error=str(e))
            return OutgoingResponse(
                text=(
                    f"I'm having trouble reaching the {advisor.display_name}. "
                    "Let me try to help directly."
                ),
                caveat=f"{advisor.display_name} temporarily unavailable",
            )

    async def _multi_advisor(
        self,
        advisor_names: list[str],
        query: str,
        context: ConversationContext,
    ) -> OutgoingResponse:
        """Consult multiple advisors and synthesize."""
        import asyncio

        results: list[tuple[str, AdvisorResponse | Exception]] = []

        async def call_advisor(name: str) -> tuple[str, AdvisorResponse | Exception]:
            try:
                result = await self.advisors[name].handle(query, context)
                return (name, result)
            except Exception as e:
                return (name, e)

        gathered = await asyncio.gather(
            *[call_advisor(name) for name in advisor_names]
        )
        results = list(gathered)

        successful = [
            (name, r) for name, r in results if isinstance(r, AdvisorResponse)
        ]
        failed = [
            (name, r) for name, r in results if isinstance(r, Exception)
        ]

        if not successful:
            return await self._direct_answer(query, context)

        # Combine responses
        parts = []
        all_action_items: list[ActionItem] = []
        for name, resp in successful:
            advisor = self.advisors[name]
            parts.append(f"**{advisor.display_name}:**\n{resp.text}")
            all_action_items.extend(
                ActionItem(title=item, advisor=name)
                for item in resp.action_items
            )

        combined_text = "\n\n---\n\n".join(parts)

        caveat = None
        if failed:
            names = [n for n, _ in failed]
            caveat = f"Could not reach: {', '.join(names)}"

        return OutgoingResponse(
            text=combined_text,
            action_items=all_action_items,
            caveat=caveat,
        )

    def get_advisor_list(self) -> list[dict[str, Any]]:
        """List all registered advisors."""
        return [a.get_info() for a in self.advisors.values()]

    def get_stats(self) -> dict[str, Any]:
        """Get system statistics."""
        return {
            "advisors_loaded": len(self.advisors),
            "advisor_names": list(self.advisors.keys()),
        }
```

**Step 4: Run tests**

Run: `cd lifeos && uv run pytest tests/unit/test_routing.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add lifeos/src/agents/chief_of_staff.py lifeos/tests/unit/test_routing.py
git commit -m "feat: implement Chief of Staff router with keyword-based intent classification"
```

---

## Task 9: CLI (Admin Commands)

**Files:**
- Create: `lifeos/src/cli/main.py`

**Step 1: Implement CLI**

```python
# lifeos/src/cli/main.py
from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(name="lifeos", help="Personal AI Life Management System")
console = Console()


@app.command()
def status() -> None:
    """Show system health status."""
    from src.core.rag import RAGPipeline
    from src.core.memory import MemoryManager

    console.print("\n[bold]LifeOS System Status[/bold]")
    console.print("=" * 40)

    try:
        rag = RAGPipeline()
        stats = rag.get_stats()
        console.print(f"RAG Index:     ✅ {stats['document_count']} documents indexed")
    except Exception as e:
        console.print(f"RAG Index:     ❌ Error: {e}")

    try:
        memory = MemoryManager()
        stats = memory.get_stats()
        console.print(f"Memory (Mem0): ✅ {stats['total_memories']} memories stored")
    except Exception as e:
        console.print(f"Memory (Mem0): ❌ Error: {e}")

    console.print()


@app.command()
def reindex(
    full: bool = typer.Option(False, "--full", help="Full reindex (not incremental)"),
    directory: str = typer.Option("knowledge/", "--dir", help="Directory to index"),
) -> None:
    """Rebuild RAG index."""
    from src.core.rag import RAGPipeline

    console.print(f"[bold]Indexing {directory}...[/bold]")
    rag = RAGPipeline()
    count = rag.index_directory(Path(directory))
    console.print(f"✅ Indexed {count} documents")


@app.command()
def note(
    text: str = typer.Argument(..., help="Note content"),
    area: str = typer.Option("inbox", "--area", "-a", help="Knowledge area"),
    tags: str = typer.Option("", "--tags", "-t", help="Comma-separated tags"),
) -> None:
    """Add a quick note to the knowledge base."""
    from datetime import date

    area_dir = Path(f"knowledge/areas/{area}" if area != "inbox" else "knowledge/inbox")
    if not area_dir.exists():
        area_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # Create note file
    filename = f"{today}-note.md"
    filepath = area_dir / filename

    # If file exists, append; otherwise create
    if filepath.exists():
        with open(filepath, "a") as f:
            f.write(f"\n\n## {today}\n{text}\n")
        console.print(f"📝 Appended to {filepath}")
    else:
        frontmatter = (
            f"---\ntype: note\ndate: {today}\n"
            f"tags: {tag_list}\nadvisor: {area}\n"
            f"confidentiality: normal\n---\n\n"
            f"# Note — {today}\n\n{text}\n"
        )
        filepath.write_text(frontmatter)
        console.print(f"📝 Created {filepath}")


@app.command()
def chat(
    advisor: str | None = typer.Option(None, "--advisor", "-a", help="Direct advisor"),
) -> None:
    """Interactive chat with Chief of Staff or specific advisor."""
    from src.agents.chief_of_staff import ChiefOfStaff
    from src.advisors.health.advisor import HealthAdvisor
    from src.advisors.schedule.advisor import ScheduleAdvisor
    from src.core.context import ConversationContext

    chief = ChiefOfStaff()
    chief.register_advisor(HealthAdvisor())
    chief.register_advisor(ScheduleAdvisor())

    context = ConversationContext(session_id="cli-session", channel="cli")

    console.print("[bold]🤖 LifeOS Chief of Staff ready. Type 'exit' to quit.[/bold]\n")

    while True:
        try:
            query = console.input("[bold green]> [/bold green]")
        except (KeyboardInterrupt, EOFError):
            break

        if query.strip().lower() in ("exit", "quit", "q"):
            break

        if not query.strip():
            continue

        if advisor:
            context.active_advisor = advisor

        response = asyncio.run(chief.process(query, context))
        rendered = response.render_for("cli")
        console.print(f"\n{rendered}\n")


@app.command()
def memory(
    action: str = typer.Argument("list", help="Action: list, search, forget"),
    query: str = typer.Argument("", help="Search query or memory to forget"),
) -> None:
    """Manage long-term memory."""
    from src.core.memory import MemoryManager

    mem = MemoryManager()

    match action:
        case "list":
            memories = mem.list_all(limit=20)
            if not memories:
                console.print("No memories stored yet.")
                return
            table = Table(title="Stored Memories")
            table.add_column("ID", style="dim")
            table.add_column("Memory")
            for m in memories:
                table.add_row(m.id[:8], m.text[:80])
            console.print(table)

        case "search":
            if not query:
                console.print("Please provide a search query.")
                return
            results = mem.search(query)
            for r in results:
                console.print(f"  • {r.text}")

        case "forget":
            if not query:
                console.print("Please provide the memory ID to forget.")
                return
            success = mem.delete(query)
            if success:
                console.print(f"✅ Memory {query} deleted.")
            else:
                console.print(f"❌ Could not delete memory {query}.")

        case _:
            console.print(f"Unknown action: {action}. Use list, search, or forget.")


if __name__ == "__main__":
    app()
```

**Step 2: Test CLI runs**

Run: `cd lifeos && uv run python -m src.cli.main --help`
Expected: Help text displayed

**Step 3: Commit**

```bash
git add lifeos/src/cli/main.py
git commit -m "feat: implement CLI with status, reindex, note, chat, and memory commands"
```

---

## Task 10: MCP Server for OpenCode

**Files:**
- Create: `lifeos/src/mcp/server.py`

**Step 1: Implement MCP server**

```python
# lifeos/src/mcp/server.py
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

import structlog

logger = structlog.get_logger()

server = Server("lifeos")

# Lazy-loaded shared instances
_rag = None
_memory = None


def _get_rag():
    global _rag
    if _rag is None:
        from src.core.rag import RAGPipeline
        _rag = RAGPipeline()
    return _rag


def _get_memory():
    global _memory
    if _memory is None:
        from src.core.memory import MemoryManager
        _memory = MemoryManager()
    return _memory


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="rag_search",
            description="Search the personal knowledge base via RAG. Returns relevant document chunks.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "advisor": {"type": "string", "description": "Optional: scope to advisor domain (health, finance, schedule, etc.)"},
                    "top_k": {"type": "integer", "description": "Number of results (default 5)", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="memory_recall",
            description="Search long-term memory for relevant personal context (preferences, decisions, facts).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to recall"},
                    "limit": {"type": "integer", "description": "Max results (default 10)", "default": 10},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="memory_save",
            description="Save an important fact, preference, or decision to long-term memory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Memory to save"},
                    "advisor": {"type": "string", "description": "Related advisor domain"},
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="note_add",
            description="Add a note to the personal knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Note content"},
                    "area": {"type": "string", "description": "Knowledge area (health, finance, schedule, etc.)", "default": "inbox"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for the note"},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="note_search",
            description="Search notes in the knowledge base by keyword.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "area": {"type": "string", "description": "Optional: limit to specific area"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_advisor_prompt",
            description="Load a domain advisor's system prompt. The LLM should adopt this persona when responding.",
            inputSchema={
                "type": "object",
                "properties": {
                    "advisor": {
                        "type": "string",
                        "description": "Advisor name: health, finance, schedule, career, legal, family, mental_health, learning, entrepreneurship",
                    },
                },
                "required": ["advisor"],
            },
        ),
        Tool(
            name="system_status",
            description="Get LifeOS system health status (RAG index, memory count, advisors).",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    match name:
        case "rag_search":
            rag = _get_rag()
            advisor = arguments.get("advisor")
            top_k = arguments.get("top_k", 5)
            if advisor:
                result = rag.query_for_advisor(arguments["query"], advisor, top_k=top_k)
            else:
                result = rag.query(arguments["query"], top_k=top_k)

            if not result.chunks:
                return [TextContent(type="text", text="No relevant documents found.")]

            parts = []
            for chunk in result.chunks:
                source = chunk.source
                parts.append(f"**Source:** {source}\n{chunk.text}")
            return [TextContent(type="text", text="\n\n---\n\n".join(parts))]

        case "memory_recall":
            memory = _get_memory()
            results = memory.search(arguments["query"], limit=arguments.get("limit", 10))
            if not results:
                return [TextContent(type="text", text="No relevant memories found.")]
            lines = [f"- {m.text}" for m in results]
            return [TextContent(type="text", text="Relevant memories:\n" + "\n".join(lines))]

        case "memory_save":
            memory = _get_memory()
            metadata = {}
            if "advisor" in arguments:
                metadata["advisor"] = arguments["advisor"]
            memory_id = memory.add(arguments["content"], metadata=metadata)
            return [TextContent(type="text", text=f"✅ Memory saved (ID: {memory_id})")]

        case "note_add":
            text = arguments["text"]
            area = arguments.get("area", "inbox")
            tags = arguments.get("tags", [])
            today = date.today().isoformat()

            area_dir = Path(f"knowledge/areas/{area}" if area != "inbox" else "knowledge/inbox")
            area_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{today}-note.md"
            filepath = area_dir / filename

            if filepath.exists():
                with open(filepath, "a") as f:
                    f.write(f"\n\n## {today}\n{text}\n")
            else:
                frontmatter = (
                    f"---\ntype: note\ndate: {today}\ntags: {tags}\n"
                    f"advisor: {area}\nconfidentiality: normal\n---\n\n"
                    f"# Note — {today}\n\n{text}\n"
                )
                filepath.write_text(frontmatter)

            return [TextContent(type="text", text=f"📝 Note saved to {filepath}")]

        case "note_search":
            rag = _get_rag()
            query = arguments["query"]
            area = arguments.get("area")
            if area:
                result = rag.query_for_advisor(query, area)
            else:
                result = rag.query(query)
            if not result.chunks:
                return [TextContent(type="text", text="No matching notes found.")]
            parts = [f"**{c.source}**\n{c.text[:200]}..." for c in result.chunks]
            return [TextContent(type="text", text="\n\n".join(parts))]

        case "get_advisor_prompt":
            advisor_name = arguments["advisor"]
            prompts = _load_advisor_prompts()
            if advisor_name not in prompts:
                return [TextContent(type="text", text=f"Unknown advisor: {advisor_name}. Available: {', '.join(prompts.keys())}")]
            return [TextContent(type="text", text=prompts[advisor_name])]

        case "system_status":
            parts = ["**LifeOS System Status**\n"]
            try:
                rag = _get_rag()
                stats = rag.get_stats()
                parts.append(f"RAG Index: ✅ {stats['document_count']} documents")
            except Exception as e:
                parts.append(f"RAG Index: ❌ {e}")
            try:
                memory = _get_memory()
                stats = memory.get_stats()
                parts.append(f"Memory: ✅ {stats['total_memories']} memories")
            except Exception as e:
                parts.append(f"Memory: ❌ {e}")
            return [TextContent(type="text", text="\n".join(parts))]

        case _:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]


def _load_advisor_prompts() -> dict[str, str]:
    """Load all advisor prompts."""
    prompts = {}
    try:
        from src.advisors.health.prompts import SYSTEM_PROMPT as health_prompt
        prompts["health"] = f"## You are now: Health Management Advisor\n\n{health_prompt}"
    except ImportError:
        pass
    try:
        from src.advisors.schedule.prompts import SYSTEM_PROMPT as schedule_prompt
        prompts["schedule"] = f"## You are now: Schedule & Productivity Advisor\n\n{schedule_prompt}"
    except ImportError:
        pass
    return prompts


async def main() -> None:
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Step 2: Test MCP server starts**

Run: `cd lifeos && uv run python -c "from src.mcp.server import server; print('MCP server loaded OK')"`
Expected: "MCP server loaded OK"

**Step 3: Commit**

```bash
git add lifeos/src/mcp/server.py
git commit -m "feat: implement LifeOS MCP server with RAG, memory, notes, and advisor tools"
```

---

## Task 11: OpenCode Skill

**Files:**
- Create: `skills/custom/lifeos.md`

**Step 1: Create the LifeOS skill for OpenCode**

```markdown
---
name: lifeos
description: "Personal AI Life Management — Chief of Staff with 9 domain advisors. Use when the user asks about health, finance, schedule, career, legal, family, mental health, learning, or entrepreneurship topics in a personal context."
---

You are the **Chief of Staff** for LifeOS, a personal AI life management system.

## Your Role

You are a personal assistant that routes queries to domain-specific advisors and uses the user's personal knowledge base and long-term memory to give personalized answers.

## Workflow

For every user query:

1. **CLASSIFY** the query into one or more domains
2. **GATHER CONTEXT** using MCP tools:
   - `rag_search(query, advisor?)` — search the personal knowledge base
   - `memory_recall(query)` — recall relevant personal memories/preferences
3. **LOAD ADVISOR** if domain-specific:
   - `get_advisor_prompt(advisor)` — load the advisor's persona and expertise
   - Adopt that advisor's persona for your response
4. **ANSWER** using all gathered context — personalized, actionable advice
5. **FOLLOW UP**:
   - `memory_save(content)` — save important new facts/decisions
   - `note_add(text, area, tags)` — save detailed notes to knowledge base

## Routing Rules

| Domain | Triggers | Advisor |
|--------|----------|---------|
| Health | medical, fitness, nutrition, sleep, medication | `health` |
| Finance | money, investment, budget, tax, expenses | `finance` |
| Schedule | calendar, meetings, tasks, productivity | `schedule` |
| Career | job, promotion, skills, networking | `career` |
| Legal | contract, rights, law, lease, dispute | `legal` |
| Family | relationship, parenting, birthday, family | `family` |
| Mental Health | stress, anxiety, mood, meditation | `mental_health` |
| Learning | study, courses, books, skill acquisition | `learning` |
| Entrepreneurship | startup, business, market, pitch | `entrepreneurship` |

## Cross-Domain Queries

For queries spanning multiple domains (e.g., "I'm stressed about money and can't sleep"):
1. Gather context from ALL relevant domains via `rag_search` and `memory_recall`
2. Load the primary advisor's prompt
3. Synthesize advice that addresses all domains

## Important Rules

- Always check `rag_search` and `memory_recall` BEFORE answering
- Never diagnose medical conditions or prescribe medication
- Never give specific investment advice (suggest consulting a professional)
- Always reference the user's personal data when available
- Save new important facts via `memory_save`
- Be concise and actionable
```

**Step 2: Commit**

```bash
git add skills/custom/lifeos.md
git commit -m "feat: create LifeOS OpenCode skill with Chief of Staff routing"
```

---

## Task 12: Telegram Bot

**Files:**
- Create: `lifeos/src/integrations/telegram/bot.py`
- Create: `lifeos/src/integrations/telegram/__init__.py`

**Step 1: Implement Telegram bot**

```python
# lifeos/src/integrations/telegram/bot.py
from __future__ import annotations

import structlog
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.agents.chief_of_staff import ChiefOfStaff
from src.core.context import ConversationContext

logger = structlog.get_logger()


class LifeOSTelegramBot:
    """Telegram interface for LifeOS."""

    def __init__(self, token: str, owner_chat_id: str, chief: ChiefOfStaff):
        self.token = token
        self.owner_chat_id = int(owner_chat_id)
        self.chief = chief

        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("note", self.cmd_note))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    def _is_owner(self, update: Update) -> bool:
        """Only respond to the configured owner."""
        return update.effective_chat is not None and update.effective_chat.id == self.owner_chat_id

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return
        await update.message.reply_text(  # type: ignore
            "🤖 LifeOS Chief of Staff ready.\n\n"
            "Just send me a message and I'll route it to the right advisor.\n\n"
            "Commands:\n"
            "/status — System status\n"
            "/note <text> — Quick note to inbox"
        )

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return
        stats = self.chief.get_stats()
        text = (
            "📊 *LifeOS Status*\n\n"
            f"Advisors: {stats['advisors_loaded']}\n"
            f"Loaded: {', '.join(stats['advisor_names'])}"
        )
        await update.message.reply_text(text, parse_mode="Markdown")  # type: ignore

    async def cmd_note(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return
        text = " ".join(context.args) if context.args else ""
        if not text:
            await update.message.reply_text("Usage: /note <your note text>")  # type: ignore
            return

        from datetime import date
        from pathlib import Path

        today = date.today().isoformat()
        inbox = Path("knowledge/inbox")
        inbox.mkdir(parents=True, exist_ok=True)
        filepath = inbox / f"{today}-telegram.md"

        if filepath.exists():
            with open(filepath, "a") as f:
                f.write(f"\n\n- {text}")
        else:
            filepath.write_text(
                f"---\ntype: note\ndate: {today}\ntags: [telegram, inbox]\n"
                f"advisor:\nconfidentiality: normal\n---\n\n"
                f"# Telegram Notes — {today}\n\n- {text}\n"
            )
        await update.message.reply_text(f"📝 Saved to inbox")  # type: ignore

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return

        query = update.message.text  # type: ignore
        if not query:
            return

        conv_context = ConversationContext(
            session_id=f"telegram-{update.effective_chat.id}",  # type: ignore
            channel="telegram",
        )

        response = await self.chief.process(query, conv_context)
        rendered = response.render_for("telegram")

        # Telegram has a 4096 char limit
        if len(rendered) > 4000:
            rendered = rendered[:4000] + "\n\n_(truncated)_"

        await update.message.reply_text(rendered, parse_mode="Markdown")  # type: ignore

    async def send_notification(self, message: str) -> None:
        """Send a proactive notification to the owner."""
        bot = self.app.bot
        await bot.send_message(
            chat_id=self.owner_chat_id,
            text=message,
            parse_mode="Markdown",
        )

    def run(self) -> None:
        """Start the bot (blocking)."""
        logger.info("telegram.starting")
        self.app.run_polling()
```

**Step 2: Commit**

```bash
git add lifeos/src/integrations/telegram/
git commit -m "feat: implement Telegram bot with Chief of Staff routing and note capture"
```

---

## Task 13: Logging Setup

**Files:**
- Create: `lifeos/src/core/logging.py`

**Step 1: Implement structured logging**

```python
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
```

**Step 2: Commit**

```bash
git add lifeos/src/core/logging.py
git commit -m "feat: add structured logging with structlog"
```

---

## Final Verification

**Step 1: Run full test suite**

```bash
cd lifeos && uv run pytest tests/unit/ -v
```
Expected: All unit tests pass

**Step 2: Type check**

```bash
cd lifeos && uv run mypy src/core/config.py src/core/message.py src/core/context.py --strict
```
Expected: No errors (may have some on files with lazy imports)

**Step 3: Lint**

```bash
cd lifeos && uv run ruff check src/
```
Expected: Clean or minimal warnings

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat: complete LifeOS Phase 1 core foundation"
```
