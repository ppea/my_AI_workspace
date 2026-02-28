# nextme/tests/unit/test_advisors.py
from src.advisors.health.advisor import HealthAdvisor
from src.advisors.schedule.advisor import ScheduleAdvisor
from src.advisors.finance.advisor import FinanceAdvisor
from src.advisors.career.advisor import CareerAdvisor
from src.advisors.legal.advisor import LegalAdvisor
from src.advisors.family.advisor import FamilyAdvisor
from src.advisors.mental_health.advisor import MentalHealthAdvisor
from src.advisors.learning.advisor import LearningAdvisor
from src.advisors.entrepreneurship.advisor import EntrepreneurshipAdvisor
from src.advisors.health.prompts import SYSTEM_PROMPT as HEALTH_PROMPT
from src.advisors.schedule.prompts import SYSTEM_PROMPT as SCHEDULE_PROMPT
from src.advisors.finance.prompts import SYSTEM_PROMPT as FINANCE_PROMPT
from src.advisors.career.prompts import SYSTEM_PROMPT as CAREER_PROMPT
from src.advisors.legal.prompts import SYSTEM_PROMPT as LEGAL_PROMPT
from src.advisors.family.prompts import SYSTEM_PROMPT as FAMILY_PROMPT
from src.advisors.mental_health.prompts import SYSTEM_PROMPT as MENTAL_HEALTH_PROMPT
from src.advisors.learning.prompts import SYSTEM_PROMPT as LEARNING_PROMPT
from src.advisors.entrepreneurship.prompts import SYSTEM_PROMPT as ENTREPRENEURSHIP_PROMPT


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


class TestFinanceAdvisor:
    def test_creation(self):
        advisor = FinanceAdvisor()
        assert advisor.name == "finance"
        assert advisor.display_name == "Finance & Investment Advisor"
        assert "finance" in advisor.tags

    def test_prompt_content(self):
        assert "NEVER give specific investment advice" in FINANCE_PROMPT
        assert "NEVER guarantee returns" in FINANCE_PROMPT
        assert "financial professional" in FINANCE_PROMPT

    def test_get_info(self):
        advisor = FinanceAdvisor()
        info = advisor.get_info()
        assert info["name"] == "finance"
        assert "tags" in info


class TestCareerAdvisor:
    def test_creation(self):
        advisor = CareerAdvisor()
        assert advisor.name == "career"
        assert advisor.display_name == "Career Development Advisor"
        assert "career" in advisor.tags

    def test_prompt_content(self):
        assert "resume and interview coaching" in CAREER_PROMPT
        assert "salary negotiation" in CAREER_PROMPT
        assert "networking" in CAREER_PROMPT

    def test_get_info(self):
        advisor = CareerAdvisor()
        info = advisor.get_info()
        assert info["name"] == "career"
        assert "tags" in info


class TestLegalAdvisor:
    def test_creation(self):
        advisor = LegalAdvisor()
        assert advisor.name == "legal"
        assert advisor.display_name == "Legal Affairs Advisor"
        assert "legal" in advisor.tags

    def test_prompt_content(self):
        assert "NEVER give specific legal advice" in LEGAL_PROMPT
        assert "ALWAYS recommend consulting a qualified lawyer" in LEGAL_PROMPT
        assert "contract" in LEGAL_PROMPT.lower()

    def test_get_info(self):
        advisor = LegalAdvisor()
        info = advisor.get_info()
        assert info["name"] == "legal"
        assert "tags" in info


class TestFamilyAdvisor:
    def test_creation(self):
        advisor = FamilyAdvisor()
        assert advisor.name == "family"
        assert advisor.display_name == "Family & Relationships Advisor"
        assert "family" in advisor.tags

    def test_prompt_content(self):
        assert "family relationships" in FAMILY_PROMPT
        assert "empathetic and non-judgmental" in FAMILY_PROMPT
        assert "important dates" in FAMILY_PROMPT

    def test_get_info(self):
        advisor = FamilyAdvisor()
        info = advisor.get_info()
        assert info["name"] == "family"
        assert "tags" in info


class TestMentalHealthAdvisor:
    def test_creation(self):
        advisor = MentalHealthAdvisor()
        assert advisor.name == "mental_health"
        assert advisor.display_name == "Mental Wellness Advisor"
        assert "mental_health" in advisor.tags

    def test_prompt_content(self):
        assert "NEVER diagnose mental health conditions" in MENTAL_HEALTH_PROMPT
        assert "NEVER replace professional therapy" in MENTAL_HEALTH_PROMPT
        assert "compassionate ear" in MENTAL_HEALTH_PROMPT

    def test_get_info(self):
        advisor = MentalHealthAdvisor()
        info = advisor.get_info()
        assert info["name"] == "mental_health"
        assert "tags" in info


class TestLearningAdvisor:
    def test_creation(self):
        advisor = LearningAdvisor()
        assert advisor.name == "learning"
        assert advisor.display_name == "Learning & Education Advisor"
        assert "learning" in advisor.tags

    def test_prompt_content(self):
        assert "personalized learning plans" in LEARNING_PROMPT
        assert "spaced repetition" in LEARNING_PROMPT
        assert "learning style" in LEARNING_PROMPT

    def test_get_info(self):
        advisor = LearningAdvisor()
        info = advisor.get_info()
        assert info["name"] == "learning"
        assert "tags" in info


class TestEntrepreneurshipAdvisor:
    def test_creation(self):
        advisor = EntrepreneurshipAdvisor()
        assert advisor.name == "entrepreneurship"
        assert advisor.display_name == "Entrepreneurship & Startup Advisor"
        assert "entrepreneurship" in advisor.tags

    def test_prompt_content(self):
        assert "business ideas" in ENTREPRENEURSHIP_PROMPT
        assert "market research" in ENTREPRENEURSHIP_PROMPT
        assert "data-driven" in ENTREPRENEURSHIP_PROMPT

    def test_get_info(self):
        advisor = EntrepreneurshipAdvisor()
        info = advisor.get_info()
        assert info["name"] == "entrepreneurship"
        assert "tags" in info
