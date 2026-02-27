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
