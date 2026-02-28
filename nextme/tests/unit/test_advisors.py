# nextme/tests/unit/test_advisors.py
from src.advisors.health.advisor import HealthAdvisor
from src.advisors.schedule.advisor import ScheduleAdvisor
from src.advisors.health.prompts import SYSTEM_PROMPT as HEALTH_PROMPT
from src.advisors.schedule.prompts import SYSTEM_PROMPT as SCHEDULE_PROMPT


class TestHealthAdvisor:
    def test_creation(self):
        advisor = HealthAdvisor()
        assert advisor.name == "health"
        assert advisor.display_name == "Health Management Advisor"
        assert "health" in advisor.tags

    def test_prompt_safety(self):
        assert "NEVER diagnose" in HEALTH_PROMPT
        assert "NEVER prescribe" in HEALTH_PROMPT
        assert "healthcare professional" in HEALTH_PROMPT

    def test_get_info(self):
        advisor = HealthAdvisor()
        info = advisor.get_info()
        assert info["name"] == "health"
        assert "tags" in info


class TestScheduleAdvisor:
    def test_creation(self):
        advisor = ScheduleAdvisor()
        assert advisor.name == "schedule"
        assert "calendar" in advisor.tags

    def test_prompt_content(self):
        assert "time blocking" in SCHEDULE_PROMPT
        assert "work-life balance" in SCHEDULE_PROMPT

    def test_get_info(self):
        advisor = ScheduleAdvisor()
        info = advisor.get_info()
        assert info["name"] == "schedule"
