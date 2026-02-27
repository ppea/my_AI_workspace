# LifeOS — Personal AI Life Management System

## Design Document

**Date**: 2026-02-27
**Status**: Approved
**Author**: AI-assisted design session

---

## Table of Contents

1. [Vision & Goals](#1-vision--goals)
2. [Design Decisions](#2-design-decisions)
3. [Project Structure & Knowledge Base](#3-project-structure--knowledge-base)
4. [Memory & RAG Layer](#4-memory--rag-layer)
5. [Agent Architecture](#5-agent-architecture)
6. [Interaction Layer](#6-interaction-layer)
7. [Proactive Scheduler](#7-proactive-scheduler)
8. [Integrations](#8-integrations)
9. [Data Flow & Error Handling](#9-data-flow--error-handling)
10. [Testing Strategy](#10-testing-strategy)
11. [Phased Implementation Roadmap](#11-phased-implementation-roadmap)
12. [Tech Stack Summary](#12-tech-stack-summary)

---

## 1. Vision & Goals

### Vision

A composable, extensible personal AI system that enhances all areas of life through AI-powered advisory, proactive reminders, and accumulated personal data.

### Goals

- Git-backed Markdown knowledge base (PARA method)
- RAG pipeline over personal data
- Long-term AI memory (cross-session)
- 9 domain-specific advisor agents (health, finance, career, legal, family, mental health, learning, entrepreneurship, schedule)
- A "Chief of Staff" router agent
- OpenCode (primary, zero-cost) + CLI for admin + Telegram bot for mobile notifications/quick Q&A
- Proactive scheduling and reminders
- Integrations with Google Calendar, Todoist, Obsidian
- Framework that continuously accumulates and expands
- Reuse existing best open-source tools — don't reinvent the wheel
- Entire project in English

---

## 2. Design Decisions

| Dimension | Decision |
|---|---|
| **Primary Interaction** | OpenCode + LifeOS MCP Server (zero extra LLM cost, uses existing Copilot/Codex/Claude subscription) |
| **Secondary Interaction** | Telegram for mobile notifications & quick Q&A |
| **Admin Interface** | CLI (`lifeos` commands) for reindex, status, memory management |
| **Hosting** | Local data storage + cloud LLMs for inference |
| **Knowledge Base** | Plain Markdown + Git |
| **Advisors** | All 9 domains — framework is config-driven, adding new advisor is trivial |
| **Tech Stack** | Python 3.12+ |
| **Integrations** | Google Calendar, Todoist, Obsidian |
| **Architecture** | Composable Stack — best-of-breed components assembled by thin orchestration layer |

### Key Open-Source Components

| Layer | Tool | Why |
|---|---|---|
| RAG Pipeline | **LlamaIndex** | Best-in-class document Q&A, Markdown-native |
| Long-term Memory | **Mem0** | Cross-session memory, self-improving, remembers preferences |
| Vector Store | **ChromaDB** | Lightweight, local-first, Python-native |
| Agent Framework | **PydanticAI** | Type-safe, lightweight, structured outputs, multi-model |
| Telegram Bot | **python-telegram-bot** | Mature, async, well-documented |
| Scheduler | **APScheduler** | Cron-based proactive reminders |
| API | **FastAPI** | REST API for webhooks and future web UI |
| CLI | **Typer + Rich** | Terminal interface for admin commands |
| MCP Server | **mcp (Python SDK)** | OpenCode integration, zero-cost LLM channel |

---

## 3. Project Structure & Knowledge Base

### Directory Layout

```
lifeos/
├── knowledge/                    # Git-tracked personal knowledge base (Obsidian vault)
│   ├── areas/                    # Ongoing life domains (PARA: Areas)
│   │   ├── health/
│   │   │   ├── medical-records.md
│   │   │   ├── fitness-log.md
│   │   │   └── nutrition-plan.md
│   │   ├── finance/
│   │   │   ├── portfolio.md
│   │   │   ├── budget-2026.md
│   │   │   └── tax-planning.md
│   │   ├── career/
│   │   ├── legal/
│   │   ├── family/
│   │   ├── mental-health/
│   │   ├── learning/
│   │   ├── entrepreneurship/
│   │   └── schedule/
│   ├── projects/                 # Active projects with deadlines (PARA: Projects)
│   ├── resources/                # Reference material (PARA: Resources)
│   ├── archive/                  # Completed/inactive items (PARA: Archive)
│   ├── journal/                  # Daily journal entries
│   │   └── 2026-02-27.md
│   └── inbox/                    # Quick capture, unprocessed notes
│
├── src/                          # Application source code
│   ├── core/                     # Shared infrastructure
│   │   ├── rag.py                # LlamaIndex RAG pipeline
│   │   ├── memory.py             # Mem0 long-term memory
│   │   ├── scheduler.py          # APScheduler proactive engine
│   │   ├── reminders.py          # SQLite reminder store
│   │   ├── context.py            # ConversationContext dataclass
│   │   ├── message.py            # IncomingMessage / OutgoingResponse
│   │   ├── resilience.py         # Retry, fallback, error handling
│   │   ├── cost_tracker.py       # LLM cost tracking
│   │   └── logging.py            # Structured logging (structlog)
│   ├── agents/                   # Agent framework
│   │   ├── base_advisor.py       # BaseAdvisor ABC
│   │   └── chief_of_staff.py     # Router agent
│   ├── advisors/                 # Domain advisors (one dir per advisor)
│   │   ├── health/
│   │   │   ├── prompts.py
│   │   │   └── tools.py
│   │   ├── finance/
│   │   ├── schedule/
│   │   ├── career/
│   │   ├── legal/
│   │   ├── family/
│   │   ├── mental_health/
│   │   ├── learning/
│   │   └── entrepreneurship/
│   ├── integrations/             # External service adapters
│   │   ├── base.py               # BaseIntegration ABC
│   │   ├── google_calendar.py
│   │   ├── todoist.py
│   │   ├── obsidian.py
│   │   └── telegram/
│   │       └── bot.py
│   ├── mcp/                      # MCP server for OpenCode
│   │   └── server.py
│   ├── api/                      # FastAPI REST API
│   │   └── main.py
│   └── cli/                      # Typer CLI
│       └── main.py
│
├── config/                       # Configuration files
│   ├── advisors.yaml             # Advisor registry
│   ├── integrations.yaml         # Integration settings
│   ├── schedules.yaml            # Cron jobs and reminder defaults
│   ├── rag.yaml                  # RAG pipeline settings
│   ├── llm.yaml                  # LLM model configuration
│   └── secrets.yaml              # API keys (GITIGNORED)
│
├── data/                         # Runtime data (GITIGNORED)
│   ├── chroma/                   # ChromaDB vector store
│   ├── mem0/                     # Mem0 memory store
│   ├── cache/                    # LLM response cache
│   ├── reminders.db              # SQLite reminder database
│   └── logs/                     # Application logs
│
├── skills/                       # OpenCode skills
│   └── custom/
│       └── lifeos.md             # LifeOS Chief of Staff skill
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── eval/
│   └── fixtures/
│
├── pyproject.toml
├── README.md
└── .gitignore
```

### Knowledge Base Conventions

**YAML Frontmatter** for every note:

```yaml
---
type: note | log | record | plan | review
date: 2026-02-27
tags: [health, blood-pressure]
advisor: health
confidentiality: normal | high    # high = never sent to cloud embeddings
---
```

**File naming**: `kebab-case.md` (e.g., `blood-pressure-log.md`)
**Journal**: `YYYY-MM-DD.md` in `knowledge/journal/`

---

## 4. Memory & RAG Layer

### Two Complementary Systems

| System | Purpose | Data | Example |
|--------|---------|------|---------|
| **Mem0** | Conversational memory — remembers *you* | Preferences, decisions, context from past chats | "User prefers index funds over individual stocks" |
| **LlamaIndex RAG** | Document retrieval — searches *your knowledge base* | All Markdown files in `knowledge/` | "What did my doctor say about blood pressure on Jan 15?" |

### LlamaIndex RAG Pipeline

```python
# src/core/rag.py

class RAGPipeline:
    def __init__(self, config: RAGConfig):
        self.vector_store = ChromaVectorStore(
            collection_name="lifeos",
            persist_directory="data/chroma/"
        )
        self.index = VectorStoreIndex.from_vector_store(self.vector_store)
    
    def index_documents(self, paths: list[Path]):
        """Full reindex of specified paths."""
        
    def incremental_update(self):
        """Detect changed files via git diff, reindex only those."""
        
    def query(self, question: str, filters: dict = None) -> RAGResponse:
        """Retrieve relevant chunks with optional metadata filters."""
        
    def query_for_advisor(self, question: str, advisor: str) -> RAGResponse:
        """Scoped query — filters by advisor domain tag."""
```

**Key decisions:**

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Vector store | ChromaDB | Local-first, zero-config, good for personal scale (<100k docs) |
| Embedding model | `text-embedding-3-small` (OpenAI) or local `nomic-embed-text` | Configurable privacy/cost tradeoff |
| Chunk strategy | `MarkdownNodeParser` | Respects Markdown structure |
| Chunk size | 512 tokens, 50-token overlap | Balanced for personal notes |
| Metadata extraction | YAML frontmatter → filter fields | Enables scoped queries |

**Git-aware incremental indexing:**

1. On startup: check `git log` for changed files since last index timestamp
2. Re-chunk and re-embed only changed/new files
3. Remove vectors for deleted files
4. Store last-indexed commit SHA in `data/chroma/.last_indexed`
5. Full reindex: `lifeos reindex --full`

### Mem0 Long-Term Memory

```python
# src/core/memory.py

class MemoryManager:
    def __init__(self, config: MemoryConfig):
        self.mem0 = Memory.from_config({
            "vector_store": {"provider": "chroma", "config": {"path": "data/mem0/"}},
            "llm": {"provider": "openai", "config": {"model": "gpt-4o-mini"}}
        })
    
    def add(self, content: str, metadata: dict = None):
        """Store a memory (auto-deduplicates)."""
        
    def search(self, query: str, limit: int = 10) -> list[MemoryItem]:
        """Retrieve relevant memories."""
        
    def get_advisor_context(self, advisor: str, query: str) -> str:
        """Get memories relevant to a specific advisor + query."""
```

**What Mem0 remembers:**

| Category | Examples |
|----------|----------|
| Preferences | "Prefers passive investing", "Allergic to penicillin" |
| Decisions | "Decided to pursue MBA in 2027" |
| Facts | "Has 2 children, ages 5 and 8" |
| Goals | "Wants to save 500k by 2027" |
| Relationships | "Wife's birthday March 15" |

### Privacy

- All vector data stored locally in `data/` (gitignored)
- `confidentiality: high` frontmatter → only indexed with local model, never sent to cloud
- Memory deletion is permanent and immediate: `lifeos memory forget "..."`

---

## 5. Agent Architecture

### Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        User Input                             │
│         (OpenCode / CLI / Telegram / API)                      │
└──────────────────────────┬───────────────────────────────────┘
                           │
                ┌──────────▼──────────┐
                │   Chief of Staff     │
                │   (Router Agent)     │
                │                      │
                │  • Intent classify   │
                │  • Direct answer     │
                │  • Route to advisor  │
                │  • Multi-advisor     │
                │    orchestration     │
                └──────┬───────────────┘
                       │
        ┌──────────────┼──────────────────────────┐
        │              │              │            │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐  ┌───▼─────┐
   │ Health   │   │ Finance │   │ Career  │  │  ...    │
   │ Advisor  │   │ Advisor │   │ Advisor │  │ (N more)│
   └────┬────┘   └────┬────┘   └────┬────┘  └───┬─────┘
        │              │              │            │
   ┌────▼──────────────▼──────────────▼────────────▼────┐
   │              Shared Services Layer                   │
   │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
   │  │ RAG      │  │ Mem0     │  │ Tool Registry    │  │
   │  │ Pipeline │  │ Memory   │  │ (Calendar, etc.) │  │
   │  └──────────┘  └──────────┘  └──────────────────┘  │
   └──────────────────────────────────────────────────────┘
```

### Base Advisor Class

```python
# src/agents/base_advisor.py

class BaseAdvisor(ABC):
    def __init__(self, config: AdvisorConfig, rag: RAGPipeline, memory: MemoryManager):
        self.name = config.name
        self.display_name = config.display
        self.rag = rag
        self.memory = memory
        self.tools = self._load_tools(config.tools)
        self.system_prompt = self._load_prompt(config.prompt_file)
        self.llm = self._init_llm(config.llm)
    
    async def handle(self, query: str, context: ConversationContext) -> AdvisorResponse:
        rag_context = await self.rag.query_for_advisor(query, self.name)
        memories = await self.memory.get_advisor_context(self.name, query)
        prompt = self._build_prompt(query, rag_context, memories, context)
        response = await self.llm.chat(prompt, tools=self.tools)
        await self._post_process(query, response, context)
        return response
    
    async def _post_process(self, query, response, context):
        await self.memory.add(f"Q: {query}\nA: {response.text}", 
                             metadata={"advisor": self.name})
        if response.action_items:
            await self._create_tasks(response.action_items)
```

### Chief of Staff (Router Agent)

```python
# src/agents/chief_of_staff.py

class ChiefOfStaff:
    async def process(self, query: str, context: ConversationContext) -> Response:
        routing = await self._classify(query, context)
        
        match routing.action:
            case "direct":
                return await self._direct_answer(query, context)
            case "single_advisor":
                return await self.advisors[routing.advisor].handle(query, context)
            case "multi_advisor":
                results = await asyncio.gather(*[
                    self.advisors[name].handle(query, context)
                    for name in routing.advisors
                ])
                return await self._synthesize(query, results, context)
```

### Advisor Registry (Config-Driven)

```yaml
# config/advisors.yaml

advisors:
  health:
    display_name: "Health Management Advisor"
    description: "Medical records, fitness tracking, nutrition, medication reminders"
    prompt_file: src/advisors/health/prompts.py
    tools: [search_medical_records, log_health_metric, schedule_reminder]
    knowledge_dirs: [knowledge/areas/health/]
    llm: {provider: openai, model: gpt-4o}
    tags: [health, medical, fitness, nutrition]

  finance:
    display_name: "Financial Advisor"
    description: "Investment portfolio, budgeting, tax planning, expense tracking"
    prompt_file: src/advisors/finance/prompts.py
    tools: [query_portfolio, log_expense, calculate_compound_interest]
    knowledge_dirs: [knowledge/areas/finance/]
    llm: {provider: openai, model: gpt-4o}
    tags: [finance, investment, budget, tax]

  schedule:
    display_name: "Schedule & Productivity Advisor"
    description: "Calendar management, task prioritization, time blocking, reminders"
    prompt_file: src/advisors/schedule/prompts.py
    tools: [google_calendar_read, google_calendar_write, todoist_read, todoist_write]
    knowledge_dirs: [knowledge/areas/schedule/]
    llm: {provider: openai, model: gpt-4o-mini}
    tags: [schedule, calendar, productivity, tasks]

  career:
    display_name: "Career Planning Advisor"
    description: "Career development, job market analysis, skill gap assessment"
    prompt_file: src/advisors/career/prompts.py
    tools: [search_job_market, analyze_skill_gap]
    knowledge_dirs: [knowledge/areas/career/]
    llm: {provider: openai, model: gpt-4o}
    tags: [career, job, professional, skills]

  legal:
    display_name: "Legal Advisor"
    description: "Contract review, legal rights, regulatory compliance"
    prompt_file: src/advisors/legal/prompts.py
    tools: [search_legal_database]
    knowledge_dirs: [knowledge/areas/legal/]
    llm: {provider: openai, model: gpt-4o}
    tags: [legal, contract, law, compliance]

  family:
    display_name: "Family Relationship Advisor"
    description: "Family dynamics, parenting, relationship communication"
    prompt_file: src/advisors/family/prompts.py
    tools: [search_family_events, schedule_reminder]
    knowledge_dirs: [knowledge/areas/family/]
    llm: {provider: openai, model: gpt-4o}
    tags: [family, relationship, parenting]

  mental_health:
    display_name: "Mental Health & Wellness Advisor"
    description: "Stress management, emotional wellbeing, mindfulness"
    prompt_file: src/advisors/mental_health/prompts.py
    tools: [mood_tracker, journaling_prompt]
    knowledge_dirs: [knowledge/areas/mental-health/]
    llm: {provider: openai, model: gpt-4o}
    tags: [mental, wellness, stress, mindfulness]

  learning:
    display_name: "Learning & Education Advisor"
    description: "Study plans, skill acquisition, course recommendations"
    prompt_file: src/advisors/learning/prompts.py
    tools: [create_study_plan, track_learning_progress]
    knowledge_dirs: [knowledge/areas/learning/]
    llm: {provider: openai, model: gpt-4o}
    tags: [learning, education, study, courses]

  entrepreneurship:
    display_name: "Entrepreneurship Advisor"
    description: "Business ideas, market analysis, startup planning"
    prompt_file: src/advisors/entrepreneurship/prompts.py
    tools: [market_research, business_model_canvas]
    knowledge_dirs: [knowledge/areas/entrepreneurship/]
    llm: {provider: openai, model: gpt-4o}
    tags: [startup, business, entrepreneur, venture]
```

**To add a new advisor:**

1. Add entry to `config/advisors.yaml`
2. Create `src/advisors/<name>/prompts.py` (system prompt)
3. Create `src/advisors/<name>/tools.py` (optional domain tools)
4. Create `knowledge/areas/<name>/` directory
5. Done — Chief of Staff auto-discovers on startup

### Agent Framework: PydanticAI

Chosen for: type-safe structured outputs, dependency injection, tool definitions with Pydantic models, multi-model support, lightweight.

### Advisor Tools

```
Shared Tools (all advisors):
├── search_knowledge_base    → RAG query
├── recall_memory            → Mem0 search
├── save_note                → Write to knowledge/
├── schedule_reminder        → APScheduler
├── create_task              → Todoist integration
└── get_calendar             → Google Calendar read

Domain-Specific Tools (per advisor):
├── Health:  log_health_metric, search_medical_records
├── Finance: query_portfolio, log_expense, calculate_compound_interest
├── Schedule: google_calendar_write, todoist_write, time_block
├── Career:  search_job_market, analyze_skill_gap
└── ...
```

---

## 6. Interaction Layer

### Channel Overview

| Channel | Use Case | Extra LLM Cost | Proactive |
|---------|----------|----------------|-----------|
| **OpenCode + MCP** | Default deep work, complex queries | **$0** (uses existing subscription) | No |
| **CLI (`lifeos`)** | Admin: reindex, status, memory | **$0** (no LLM) | No |
| **Telegram Bot** | Mobile, quick Q&A, notifications | ~$15-30/month | **Yes** |
| **FastAPI** | Webhooks, future web UI | N/A | **Yes** |

### OpenCode Integration (Primary Channel)

**Zero extra LLM cost** — your existing Copilot/Codex/Claude subscription acts as the LLM.

```
┌──────────────────────────────────────────────────────────┐
│  OpenCode (Copilot / Codex / Claude — your subscription) │
│                                                           │
│  ┌─────────────────────────────────────┐                 │
│  │  LifeOS Skill (system prompt)       │                 │
│  │  = Chief of Staff routing logic     │                 │
│  │  = Advisor prompt injection         │                 │
│  │  = All intelligence via YOUR LLM    │                 │
│  └──────────────┬──────────────────────┘                 │
│                 │ calls tools                             │
│  ┌──────────────▼──────────────────────┐                 │
│  │  LifeOS MCP Server (NO LLM calls)  │                 │
│  │                                      │                 │
│  │  Tools (data access only):           │                 │
│  │   • rag_search(query, advisor?)      │  ← local       │
│  │   • memory_recall(query)             │  ← local       │
│  │   • memory_save(content)             │  ← local       │
│  │   • note_add(text, area, tags)       │  ← local       │
│  │   • note_search(query)               │  ← local       │
│  │   • calendar_read(date)              │  ← API call    │
│  │   • calendar_write(event)            │  ← API call    │
│  │   • todoist_tasks(filter?)           │  ← API call    │
│  │   • todoist_create(task)             │  ← API call    │
│  │   • remind_create(msg, date)         │  ← local       │
│  │   • remind_list(days?)               │  ← local       │
│  │   • get_advisor_prompt(advisor)      │  ← local       │
│  │   • system_status()                  │  ← local       │
│  └──────────────────────────────────────┘                 │
└──────────────────────────────────────────────────────────┘
```

**LifeOS OpenCode Skill** — contains Chief of Staff routing logic:

```markdown
# skills/custom/lifeos.md

You are the Chief of Staff for LifeOS.

## Routing Rules
1. CLASSIFY query into domain(s)
2. GATHER context: rag_search, memory_recall, calendar_read, todoist_tasks
3. LOAD advisor prompt: get_advisor_prompt(advisor_name)
4. ANSWER as that advisor with full context
5. FOLLOW UP: memory_save, create tasks/reminders if needed
```

**LifeOS MCP Server** — provides tools only, no LLM calls:

```python
# src/mcp/server.py

@server.tool()
async def rag_search(query: str, advisor: str | None = None) -> str:
    """Search the knowledge base via RAG."""

@server.tool()
async def memory_recall(query: str) -> str:
    """Search long-term memory."""

@server.tool()
async def get_advisor_prompt(advisor: str) -> str:
    """Load advisor persona prompt. LLM adopts this persona."""

# ... (note_add, calendar_read, todoist_tasks, remind_create, etc.)
```

### Telegram Bot

```python
# src/integrations/telegram/bot.py

class LifeOSTelegramBot:
    async def handle_message(self, update, context):
        """Free-text → Chief of Staff."""
        response = await self.chief.process(query, conv_context)
        await self._send_response(update, response)
    
    async def send_reminder(self, message: str):
        """Proactive push notification."""
    
    async def send_daily_briefing(self, briefing: str):
        """Morning briefing."""
```

**Telegram features:**
- Inline keyboard buttons for quick actions
- Voice messages → Whisper transcription (future)
- Photo/document → save to knowledge base
- Single owner — only responds to configured `owner_chat_id`

### CLI (Admin Only)

```bash
lifeos reindex [--full]          # rebuild RAG index
lifeos status [--costs]          # system health check
lifeos memory list [--advisor X] # list memories
lifeos memory forget "..."       # delete memory
lifeos note add "..." --area X   # add note
lifeos remind "..." --date X     # create reminder
```

### Unified Message Bus

All channels produce/consume the same format:

```python
@dataclass
class IncomingMessage:
    text: str
    channel: Literal["opencode", "cli", "telegram", "api"]
    session_id: str
    timestamp: datetime
    attachments: list[Attachment] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

@dataclass  
class OutgoingResponse:
    text: str
    advisor: str | None
    action_items: list[ActionItem]
    follow_ups: list[FollowUp]
    reminders: list[Reminder]
    
    def render_for(self, channel: str) -> str:
        """Format for specific channel."""
```

### Security

| Concern | Solution |
|---------|----------|
| OpenCode | Local — inherits shell access |
| CLI | Local — shell access |
| Telegram | Whitelist `owner_chat_id` |
| API | API key in `secrets.yaml` (gitignored) |

---

## 7. Proactive Scheduler

### Job Types

**1. Recurring (Cron-based)**

```yaml
# config/schedules.yaml

recurring:
  morning_briefing:
    cron: "30 7 * * *"
    action: daily_briefing
    channel: telegram

  weekly_review:
    cron: "0 18 * * 5"
    action: weekly_review
    channel: telegram

  monthly_finance:
    cron: "0 10 1 * *"
    action: monthly_finance_summary
    channel: telegram

  health_checkin:
    cron: "0 21 * * *"
    action: health_checkin
    channel: telegram

  journal_prompt:
    cron: "0 22 * * *"
    action: journal_prompt
    channel: telegram
```

**2. Date-based (One-shot reminders)**

```python
Reminder(
    message="Wife's birthday — gift + dinner reservation",
    trigger_date=date(2026, 3, 15),
    advance_days=[7, 3, 1, 0],
    advisor="family",
    channel="telegram"
)
```

**3. Event-driven (Triggered by conditions)**

```python
EventTrigger(
    name="calendar_prep",
    source="google_calendar",
    condition="new_event_tomorrow",
    action="prepare_briefing",
    advance_minutes=60
)

EventTrigger(
    name="task_overdue",
    source="todoist",
    condition="task_overdue_24h",
    action="nudge_task_completion"
)

EventTrigger(
    name="knowledge_stale",
    source="internal",
    condition="area_not_updated_30d",
    action="prompt_area_review"
)
```

### Briefing Engine

```python
class ProactiveScheduler:
    async def daily_briefing(self) -> str:
        calendar, tasks, reminders, memories = await asyncio.gather(
            self.integrations.google_calendar.get_events(today),
            self.integrations.todoist.get_tasks(due=today),
            self.reminder_store.get_due(today),
            self.memory.search(f"important events around {today}")
        )
        return await self.chief.process(briefing_prompt, context)
    
    async def weekly_review(self) -> str:
        completed_tasks, journal_entries, new_notes = await asyncio.gather(
            self.integrations.todoist.get_completed(week_range),
            self.rag.query(f"journal entries {week_range}"),
            self._get_new_notes_this_week()
        )
        return await self.chief.process(review_prompt, context)
```

### Smart Reminders

Advisors auto-create reminders from conversations:

```
User: "I just signed a new lease, it expires December 2027"
→ Legal Advisor auto-creates:
  - "Review lease renewal options" → Oct 2027
  - "Lease expiration — decide: renew or move" → Nov 2027
  - "Lease expires today" → Dec 2027
```

### Reminder Storage

SQLite (`data/reminders.db`) — structured data with exact dates, not semantic content.

### Configuration

```yaml
scheduler:
  timezone: "Asia/Shanghai"
  store: sqlite
  store_path: data/reminders.db
  defaults:
    birthday: [7, 1, 0]
    deadline: [30, 14, 7, 3, 1]
    appointment: [1, 0]
  notification:
    primary: telegram
    fallback: cli
    quiet_hours:
      start: "22:00"
      end: "07:00"
      exceptions: ["urgent"]
```

---

## 8. Integrations

### Base Interface

```python
class BaseIntegration(ABC):
    async def connect(self) -> bool:
    async def health_check(self) -> IntegrationStatus:
    async def sync(self) -> SyncResult:
    async def disconnect(self):
```

### Google Calendar

- OAuth2 flow, refresh token in `secrets.yaml`
- Read/write events, availability check
- Push notifications via webhook (when deployed)
- Tools: `google_calendar_read`, `google_calendar_write`, `check_availability`

### Todoist

- API token auth
- Task CRUD, completed task history
- Advisor-to-project mapping: `LifeOS: Health`, `LifeOS: Finance`, etc.
- Auto-create projects on first use
- Tools: `todoist_read`, `todoist_write`, `todoist_complete`

### Obsidian

- **Same directory** — `knowledge/` is the Obsidian vault
- No sync needed — Obsidian is the GUI editor, LifeOS is the AI brain
- File watcher (`watchdog`) for real-time reindex on Obsidian edits
- Ensures: wiki-links disabled, YAML frontmatter recognized, `.obsidian/` gitignored

### Future Integrations

| Integration | Purpose | Priority |
|-------------|---------|----------|
| Apple Health / Google Fit | Auto-import health metrics | Medium |
| Bank API / Plaid | Auto-import transactions | Medium |
| Email (IMAP) | Scan for action items, deadlines | Medium |
| WeChat | Alternative to Telegram | Low |
| Whisper (local) | Voice note transcription | Medium |
| Web Clipper | Save web pages to resources/ | Low |

### Configuration

```yaml
# config/integrations.yaml

integrations:
  google_calendar:
    enabled: true
    calendar_id: primary
    sync_interval_minutes: 15

  todoist:
    enabled: true
    project_prefix: "LifeOS"
    sync_interval_minutes: 10
    auto_create_tasks: true

  obsidian:
    enabled: true
    vault_path: knowledge/
    watch_mode: polling
    poll_interval_seconds: 30
```

### Health Dashboard

```bash
$ lifeos status

LifeOS System Status
═══════════════════════════════════════
RAG Index:        ✅ 847 documents indexed
Memory (Mem0):    ✅ 234 memories stored
Reminders:        ✅ 12 active, 3 due today

Integrations:
  Google Calendar: ✅ Connected
  Todoist:         ✅ Connected (23 active tasks)
  Obsidian:        ✅ Vault watched (847 files)
  Telegram Bot:    ✅ Running

Advisors: 9/9 loaded
```

---

## 9. Data Flow & Error Handling

### End-to-End Request Flow

```
1. INTAKE: Channel receives message → IncomingMessage
2. ROUTING: Chief of Staff classifies → direct | single_advisor | multi_advisor
3. CONTEXT: Pre-fetch Mem0 memories + RAG documents (parallel)
4. ADVISOR: Execute advisor(s) with full context → AdvisorResponse
5. SYNTHESIS: Merge multi-advisor responses if needed
6. POST-PROCESS: Auto-extract memories, create tasks/reminders
7. DELIVERY: Format for channel, send response
```

### Three-Layer Error Handling

**Layer 1 — Tool/Integration:**
- API timeout → retry 3x with exponential backoff
- Rate limit → retry with `Retry-After` respect
- Auth failure → disable integration, notify user
- Network down → use cached data, note staleness

**Layer 2 — Advisor:**
- RAG unavailable → answer from memory only + caveat
- LLM error → try fallback model
- Tool failure → answer without that tool + caveat

**Layer 3 — Chief of Staff:**
- Advisor unavailable → best-effort direct answer
- Multi-advisor partial failure → synthesize with available results
- Total failure → honest error message

### LLM Fallback Chain

```yaml
# config/llm.yaml

llm:
  primary: {provider: openai, model: gpt-4o}
  fallback: {provider: anthropic, model: claude-sonnet-4-20250514}
  emergency: {provider: openai, model: gpt-4o-mini}
  routing_model: {provider: openai, model: gpt-4o-mini}
  memory_model: {provider: openai, model: gpt-4o-mini}
```

### Logging

```
data/logs/
├── lifeos.log    # structured JSON log (structlog)
├── error.log     # errors only
└── audit.log     # all LLM calls with token counts
```

### Cost Tracking

Per-advisor, per-day cost tracking. Exposed via `lifeos status --costs`.

---

## 10. Testing Strategy

### Testing Pyramid

```
              ╱╲
             ╱E2E╲           Few: full flow tests
            ╱──────╲
           ╱Integration╲     Medium: real local components
          ╱──────────────╲
         ╱   Unit Tests    ╲  Many: pure logic, mocked deps
        ╱────────────────────╲
       ╱   LLM Eval Suite     ╲  Separate: quality scoring
      ╱────────────────────────╲
```

### Unit Tests

- Routing classification logic
- Message formatting per channel
- Reminder date calculations
- RAG metadata extraction and filter building
- Config parsing and validation
- Cost tracking calculations

### Integration Tests

- RAG pipeline with real ChromaDB (temp collection)
- Mem0 with real memory operations
- Scheduler with real SQLite
- External API tests (Google Calendar, Todoist) — marked `@pytest.mark.external`

### LLM Evaluation Suite

- LLM-as-judge quality scoring (1-10 scale)
- Per-advisor rubrics (e.g., health advisor must not diagnose)
- Hard checks (must contain / must not contain)
- Soft checks (quality score ≥ 7/10)

### Test Structure

```
tests/
├── unit/
├── integration/
│   └── external/          # requires real credentials
├── eval/
│   └── eval_cases/        # YAML test case definitions
├── fixtures/
└── conftest.py
```

### Commands

```bash
pytest tests/unit/ -v                           # fast (seconds)
pytest tests/unit/ tests/integration/ -v        # before commit
pytest tests/ -v -m "not slow"                  # full suite
pytest tests/eval/ -v                           # LLM quality eval
mypy src/ --strict                              # type checking
ruff check src/ tests/                          # linting
```

---

## 11. Phased Implementation Roadmap

### Phase Overview

```
Phase 1 ──────── Phase 2 ──────── Phase 3 ──────── Phase 4
 (Core)         (Advisors)       (Proactive)       (Polish)
 2-3 weeks       2 weeks          1-2 weeks         Ongoing
```

### Phase 1: Core Foundation (Weeks 1-3)

**Goal**: Working system with 2 advisors via OpenCode (zero cost) and Telegram.

| # | Task | Deliverable |
|---|------|-------------|
| 1.1 | Project scaffold | pyproject.toml, deps, config loading |
| 1.2 | Knowledge base | PARA directory structure, templates |
| 1.3 | RAG pipeline | LlamaIndex + ChromaDB, incremental indexing |
| 1.4 | Memory layer | Mem0 integration, advisor-scoped recall |
| 1.5 | Base advisor | BaseAdvisor class, shared tools |
| 1.6 | Chief of Staff | Router, intent classification |
| 1.7 | Schedule Advisor | Prompt, basic tools |
| 1.8 | Health Advisor | Prompt, health metric logging |
| 1.9 | CLI (admin) | `lifeos reindex`, `lifeos status`, `lifeos note` |
| 1.10 | Telegram bot | Free-text chat, `/ask`, `/note` |
| 1.11 | Unit tests | Routing, message formatting, RAG metadata |
| 1.12 | OpenCode Skill | Chief of Staff routing via existing LLM |
| 1.13 | MCP Server | LifeOS tools for OpenCode (rag_search, memory, etc.) |

**Milestone**: Ask "What should I eat given my health goals?" via OpenCode and get a personalized answer from your knowledge base — at zero extra LLM cost.

### Phase 2: Full Advisor Suite + Integrations (Weeks 4-5)

**Goal**: All 9 advisors, multi-advisor collaboration, external integrations.

| # | Task | Deliverable |
|---|------|-------------|
| 2.1 | Remaining 7 advisors | Prompts + tools for all domains |
| 2.2 | Multi-advisor routing | Parallel calls, response synthesis |
| 2.3 | Google Calendar | OAuth, read/write, availability |
| 2.4 | Todoist | Task CRUD, advisor-to-project mapping |
| 2.5 | Obsidian compat | Vault config, file watcher |
| 2.6 | FastAPI | REST endpoints for webhooks |
| 2.7 | Integration tests | RAG, Mem0, external APIs |
| 2.8 | LLM eval suite | Quality rubrics for all 9 advisors |

**Milestone**: "I'm stressed about money and can't sleep" triggers 3 advisors in parallel with synthesized response.

### Phase 3: Proactive Intelligence (Weeks 6-7)

**Goal**: LifeOS reaches out proactively.

| # | Task | Deliverable |
|---|------|-------------|
| 3.1 | Scheduler core | APScheduler, SQLite reminders, cron runner |
| 3.2 | Daily briefing | Morning: calendar + tasks + reminders |
| 3.3 | Weekly review | Friday: accomplishments + next week |
| 3.4 | Smart reminders | Auto-create from conversations |
| 3.5 | Event triggers | Calendar prep, overdue task nudge |
| 3.6 | Quiet hours | Defer non-urgent during sleep |
| 3.7 | Cost tracker | Per-advisor daily/monthly costs |

**Milestone**: 7:30 AM Telegram: "Good morning! 3 meetings today. Wife's birthday in 5 days — shall I suggest gifts?"

### Phase 4: Polish & Expansion (Ongoing)

| Task | Priority |
|------|----------|
| Voice messages (Whisper) | Medium |
| Web UI | Low |
| Apple Health / Google Fit | Medium |
| Bank API / Plaid | Medium |
| Email scanner | Medium |
| Web clipper | Low |
| Monthly PDF reports | Medium |

### Dependency Graph

```
Phase 1:
  1.1 → 1.2, 1.3, 1.4 (scaffold first)
  1.3 + 1.4 → 1.5 (BaseAdvisor needs RAG + Mem0)
  1.5 → 1.6 (Chief needs BaseAdvisor)
  1.5 → 1.7, 1.8 (advisors need BaseAdvisor)
  1.6 → 1.9, 1.10 (CLI + Telegram need Chief)
  1.3 + 1.4 → 1.13 (MCP server needs RAG + Mem0)
  1.6 → 1.12 (Skill needs Chief routing logic)

Phase 2:
  1.5 → 2.1 (new advisors need BaseAdvisor)
  1.6 → 2.2 (multi-advisor needs Chief)

Phase 3:
  1.10 → 3.1 (scheduler sends via Telegram)
  2.3 + 2.4 → 3.5 (event triggers need integrations)
```

---

## 12. Tech Stack Summary

```
Runtime:          Python 3.12+
Package Manager:  uv
Project Config:   pyproject.toml
Agent Framework:  PydanticAI
RAG:              LlamaIndex
Vector Store:     ChromaDB
Memory:           Mem0
Scheduler:        APScheduler
API:              FastAPI + Uvicorn
CLI:              Typer + Rich
Telegram:         python-telegram-bot
MCP:              mcp (Python SDK)
Testing:          pytest + pytest-asyncio
Type Checking:    mypy --strict
Linting:          ruff
Logging:          structlog
Reminder DB:      SQLite (aiosqlite)
```

### Success Metrics

| Metric | Target |
|--------|--------|
| Daily active usage | At least once per day |
| Knowledge base growth | 10+ new notes per week |
| Advisor accuracy | LLM eval ≥ 7/10 |
| Response latency | < 5s single, < 10s multi-advisor |
| System uptime | Telegram + scheduler 24/7 |
| Monthly LLM cost | < $30 (Telegram channel only) |
| New advisor time | < 1 hour to add |

### Daily Workflow

```
☀️ Morning    Telegram → daily briefing (proactive)
💻 Deep work  OpenCode + LifeOS MCP ($0 — uses your subscription)
🚶 On-the-go  Telegram bot (quick notes, questions)
🌙 Evening    OpenCode for journaling/review ($0)
🔧 Admin      CLI: lifeos reindex / status / memory ($0, no LLM)
```
