# nextme/tests/integration/test_memory.py
from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from src.core.memory import MemoryManager


@pytest.mark.integration
class TestMemoryManagerIntegration:
    @pytest.fixture
    def mock_mem0(self):
        """Mock the Mem0 Memory class."""
        with patch("src.core.memory.importlib.import_module") as import_mock:
            mem0_module = Mock()
            memory_cls = Mock()
            mem0_module.Memory = memory_cls
            
            # Mock Memory.from_config to return a memory instance
            memory_instance = Mock()
            memory_cls.from_config.return_value = memory_instance
            
            import_mock.return_value = mem0_module
            
            yield memory_instance

    def test_memory_manager_init(self, mock_mem0, tmp_path):
        """Test MemoryManager can be instantiated with mocked Memory."""
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        
        # Trigger lazy initialization
        manager._ensure_initialized()
        
        assert manager._initialized is True
        assert manager._mem0 is not None

    def test_store_and_search(self, mock_mem0, tmp_path):
        """Test storing a memory and searching for it."""
        mock_mem0.add.return_value = {"id": "mem_123"}
        mock_mem0.search.return_value = [
            {
                "id": "mem_123",
                "memory": "I prefer dark roast coffee",
                "metadata": {"advisor": "health"},
            }
        ]
        
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        
        # Store a memory
        memory_id = manager.add("I prefer dark roast coffee", {"advisor": "health"})
        assert memory_id == "mem_123"
        
        # Search for it
        results = manager.search("coffee preference")
        assert len(results) == 1
        assert results[0].id == "mem_123"
        assert "coffee" in results[0].text.lower()

    def test_get_stats(self, mock_mem0, tmp_path):
        """Test get_stats returns proper statistics dict."""
        mock_mem0.get_all.return_value = [
            {"id": "mem_1", "memory": "Memory 1"},
            {"id": "mem_2", "memory": "Memory 2"},
            {"id": "mem_3", "memory": "Memory 3"},
        ]
        
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        stats = manager.get_stats()
        
        assert "total_memories" in stats
        assert stats["total_memories"] == 3
        assert "persist_dir" in stats

    def test_delete_memory(self, mock_mem0, tmp_path):
        """Test deleting a memory."""
        mock_mem0.add.return_value = {"id": "mem_456"}
        mock_mem0.delete.return_value = None  # delete doesn't return anything
        
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        
        # Add a memory
        memory_id = manager.add("Test memory")
        assert memory_id == "mem_456"
        
        # Delete it
        success = manager.delete(memory_id)
        assert success is True
        
        # Verify delete was called
        mock_mem0.delete.assert_called_once_with("mem_456")

    def test_search_returns_list(self, mock_mem0, tmp_path):
        """Test search returns a list even when no matches."""
        mock_mem0.search.return_value = []
        
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        results = manager.search("nonexistent query")
        
        assert isinstance(results, list)
        assert len(results) == 0

    def test_get_advisor_context(self, mock_mem0, tmp_path):
        """Test get_advisor_context formats memories correctly."""
        mock_mem0.search.return_value = [
            {"id": "mem_1", "memory": "Patient prefers morning appointments"},
            {"id": "mem_2", "memory": "Allergic to penicillin"},
        ]
        
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        context = manager.get_advisor_context("health", "appointments", limit=5)
        
        assert "Relevant memories:" in context
        assert "morning appointments" in context
        assert "penicillin" in context

    def test_list_all(self, mock_mem0, tmp_path):
        """Test list_all returns all memories."""
        mock_mem0.get_all.return_value = [
            {"id": "mem_1", "memory": "Memory 1"},
            {"id": "mem_2", "text": "Memory 2"},  # Test alternate field
        ]
        
        manager = MemoryManager(persist_dir=str(tmp_path / "mem0"))
        all_memories = manager.list_all()
        
        assert len(all_memories) == 2
        assert all_memories[0].id == "mem_1"
        assert all_memories[0].text == "Memory 1"
        assert all_memories[1].text == "Memory 2"
