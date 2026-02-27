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
