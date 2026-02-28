from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.core.message import ActionItem, FollowUp, OutgoingResponse


@pytest.fixture
def client():
    """Create FastAPI test client."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_chief():
    """Mock ChiefOfStaff for testing."""
    mock = MagicMock()
    mock.process = AsyncMock()
    mock.get_stats = MagicMock(
        return_value={
            "total_advisors": 9,
            "advisor_names": [
                "health",
                "schedule",
                "finance",
                "career",
                "legal",
                "family",
                "mental_health",
                "learning",
                "entrepreneurship",
            ],
        }
    )
    mock._advisors = {}
    return mock


@pytest.fixture
def mock_rag():
    """Mock RAGPipeline for testing."""
    mock = MagicMock()
    mock.get_stats = MagicMock(return_value={"document_count": 42})
    return mock


@pytest.fixture
def mock_memory():
    """Mock MemoryManager for testing."""
    mock = MagicMock()
    mock.get_stats = MagicMock(return_value={"total_memories": 100})
    return mock


@pytest.fixture
def mock_advisors():
    """Mock advisors for get_advisors endpoint."""
    mock_advisors = {}
    for name, display_name, description in [
        ("health", "Health", "Health and wellness advisor"),
        ("schedule", "Schedule", "Calendar and scheduling advisor"),
        ("finance", "Finance", "Personal finance advisor"),
        ("career", "Career", "Career development advisor"),
        ("legal", "Legal", "Legal matters advisor"),
        ("family", "Family", "Family and relationships advisor"),
        ("mental_health", "Mental Health", "Mental health and wellbeing advisor"),
        ("learning", "Learning", "Learning and education advisor"),
        (
            "entrepreneurship",
            "Entrepreneurship",
            "Entrepreneurship and business advisor",
        ),
    ]:
        mock_advisor = MagicMock()
        mock_advisor.name = name
        mock_advisor.display_name = display_name
        mock_advisor.description = description
        mock_advisors[name] = mock_advisor
    return mock_advisors


def test_status_endpoint(client, mock_chief, mock_rag, mock_memory):
    """Test GET /status endpoint."""
    with (
        patch("src.api.app.chief", mock_chief),
        patch("src.api.app.rag", mock_rag),
        patch("src.api.app.memory", mock_memory),
    ):
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["rag_documents"] == 42
        assert data["memory_count"] == 100
        assert data["advisors_loaded"] == 9
        assert len(data["advisor_names"]) == 9


def test_query_endpoint_success(client, mock_chief):
    """Test POST /query with valid payload."""
    mock_response = OutgoingResponse(
        text="Here's your response",
        advisor="health",
        action_items=[ActionItem(title="Exercise 30 minutes", advisor="health")],
        follow_ups=[FollowUp(question="How's your diet?", advisor="health")],
        caveat="Consult a doctor",
    )
    mock_chief.process.return_value = mock_response

    with patch("src.api.app.chief", mock_chief):
        response = client.post(
            "/query",
            json={"text": "How can I improve my health?", "session_id": "test-123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "Here's your response"
        assert data["advisor"] == "health"
        assert len(data["action_items"]) == 1
        assert data["action_items"][0] == "Exercise 30 minutes"
        assert len(data["follow_ups"]) == 1
        assert data["follow_ups"][0] == "How's your diet?"
        assert data["caveat"] == "Consult a doctor"


def test_query_endpoint_missing_text(client):
    """Test POST /query with missing text returns 422."""
    response = client.post("/query", json={"session_id": "test-123"})
    assert response.status_code == 422


def test_query_endpoint_with_advisor(client, mock_chief):
    """Test POST /query with specific advisor."""
    mock_response = OutgoingResponse(text="Finance advice", advisor="finance")
    mock_chief.process.return_value = mock_response

    with patch("src.api.app.chief", mock_chief):
        response = client.post(
            "/query",
            json={
                "text": "Should I invest?",
                "session_id": "test-123",
                "advisor": "finance",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["advisor"] == "finance"


def test_notes_endpoint_create(client, tmp_path):
    """Test POST /notes creates a note."""
    with patch("src.api.app.Path", return_value=tmp_path / "knowledge/inbox"):
        response = client.post(
            "/notes",
            json={"text": "Test note", "area": "inbox", "tags": ["test"]},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "created"
        assert "path" in data


def test_advisors_endpoint(client, mock_chief, mock_advisors):
    """Test GET /advisors returns all 9 advisors."""
    mock_chief._advisors = mock_advisors

    with patch("src.api.app.chief", mock_chief):
        response = client.get("/advisors")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert all("name" in advisor for advisor in data)
        assert all("display_name" in advisor for advisor in data)
        assert all("description" in advisor for advisor in data)


def test_telegram_webhook_success(client, mock_chief):
    """Test POST /webhook/telegram processes updates."""
    mock_response = OutgoingResponse(text="Hello from Telegram!")
    mock_chief.process.return_value = mock_response

    with patch("src.api.app.chief", mock_chief):
        response = client.post(
            "/webhook/telegram",
            json={
                "message": {
                    "chat": {"id": 12345},
                    "text": "Hello",
                }
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "sendMessage"
        assert data["chat_id"] == 12345
        assert "Hello from Telegram!" in data["text"]


def test_telegram_webhook_invalid_format(client):
    """Test POST /webhook/telegram with invalid format."""
    response = client.post("/webhook/telegram", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert "error" in data
