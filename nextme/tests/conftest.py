# nextme/tests/conftest.py
import pytest
from pathlib import Path


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "live: mark test as requiring live external services")

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
