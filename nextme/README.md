# NextMe — Personal AI Life Management System

A composable, extensible personal AI system with Git-backed knowledge base, RAG pipeline, long-term memory, and domain-specific advisor agents.

## Quick Start

```bash
uv sync
uv run nextme status
uv run nextme chat
```

## Architecture

- **Knowledge Base**: Git-backed Markdown files (PARA method)
- **RAG Pipeline**: LlamaIndex + ChromaDB for semantic search
- **Memory**: Mem0 for cross-session conversational memory
- **Advisors**: Domain-specific AI agents (health, finance, schedule, etc.)
- **Chief of Staff**: Router that classifies queries and delegates to advisors
- **Channels**: OpenCode (primary), CLI (admin), Telegram (mobile)
