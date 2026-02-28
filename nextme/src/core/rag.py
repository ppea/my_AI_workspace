# nextme/src/core/rag.py
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
        self._index: Any = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization of LlamaIndex components."""
        if self._initialized:
            return

        import chromadb
        from llama_index.core import VectorStoreIndex, StorageContext
        from llama_index.vector_stores.chroma import ChromaVectorStore

        self._chroma_client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._collection = self._chroma_client.get_or_create_collection("nextme")
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
