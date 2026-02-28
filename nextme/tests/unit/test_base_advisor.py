# nextme/tests/unit/test_base_advisor.py
import pytest
from src.agents.base_advisor import BaseAdvisor, AdvisorResponse


class TestAdvisorResponse:
    def test_create_response(self):
        response = AdvisorResponse(
            text="Drink more water.",
            advisor="health",
        )
        assert response.text == "Drink more water."
        assert response.advisor == "health"
        assert response.action_items == []

    def test_response_with_action_items(self):
        response = AdvisorResponse(
            text="Adjust your budget.",
            advisor="finance",
            action_items=["Review expenses", "Set savings goal"],
        )
        assert len(response.action_items) == 2


class TestBaseAdvisor:
    def test_is_abstract(self):
        with pytest.raises(TypeError):
            type("TempAdvisor", (BaseAdvisor,), {})(
                "health", "Health", "desc", "system"
            )
