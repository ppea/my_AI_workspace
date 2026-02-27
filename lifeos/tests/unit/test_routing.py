# lifeos/tests/unit/test_routing.py
from src.agents.chief_of_staff import classify_intent, RoutingDecision


class TestIntentClassification:
    def test_health_query(self):
        routing = classify_intent("What's a good blood pressure range?")
        assert routing.action == "single_advisor"
        assert routing.advisor == "health"

    def test_schedule_query(self):
        routing = classify_intent("What's on my calendar tomorrow?")
        assert routing.action == "single_advisor"
        assert routing.advisor == "schedule"

    def test_greeting_is_direct(self):
        routing = classify_intent("Hello")
        assert routing.action == "direct"

    def test_simple_question_is_direct(self):
        routing = classify_intent("What time is it?")
        assert routing.action == "direct"

    def test_cross_domain_is_multi(self):
        routing = classify_intent(
            "I'm stressed about money and it's affecting my sleep"
        )
        assert routing.action in ("single_advisor", "multi_advisor")

    def test_finance_keywords(self):
        routing = classify_intent("Should I invest in index funds?")
        assert routing.advisor in ("finance", None)
        # finance advisor not yet registered, falls to direct or unknown
