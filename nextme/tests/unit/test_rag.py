# nextme/tests/unit/test_rag.py
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
