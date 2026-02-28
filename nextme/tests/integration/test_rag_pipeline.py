# nextme/tests/integration/test_rag_pipeline.py
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
