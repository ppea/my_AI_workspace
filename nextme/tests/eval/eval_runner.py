from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from src.core.message import OutgoingResponse
from tests.eval.rubrics import AdvisorRubric, HardCheck


@dataclass
class EvalCase:
    """A single evaluation test case."""
    id: str
    query: str
    expected_advisor_tag: str
    mock_response: dict[str, Any]
    must_pass_hard_checks: bool
    advisor: str

    @classmethod
    def from_dict(cls, data: dict[str, Any], advisor: str) -> EvalCase:
        """Create EvalCase from YAML dict."""
        return cls(
            id=data["id"],
            query=data["query"],
            expected_advisor_tag=data["expected_advisor_tag"],
            mock_response=data["mock_response"],
            must_pass_hard_checks=data.get("must_pass_hard_checks", True),
            advisor=advisor,
        )


@dataclass
class EvalResult:
    """Result of running an eval case."""
    passed: bool
    hard_check_results: dict[str, bool] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)


class EvalRunner:
    """Runs evaluation cases against rubrics."""

    def run_case(
        self, case: EvalCase, response: OutgoingResponse, rubric: AdvisorRubric
    ) -> EvalResult:
        """Run hard checks against the response. Return pass/fail with details."""
        result = EvalResult(passed=True)

        for check in rubric.hard_checks:
            check_passed = self._run_hard_check(check, response)
            result.hard_check_results[check.name] = check_passed

            if not check_passed:
                result.passed = False
                result.messages.append(
                    f"❌ {check.name}: {check.description} (check_fn={check.check_fn})"
                )
            else:
                result.messages.append(
                    f"✅ {check.name}: {check.description}"
                )

        return result

    def _run_hard_check(self, check: HardCheck, response: OutgoingResponse) -> bool:
        """Execute a single hard check."""
        match check.check_fn:
            case "contains":
                return check.value.lower() in response.text.lower()
            case "not_contains":
                return check.value.lower() not in response.text.lower()
            case "has_action_items":
                return len(response.action_items) > 0
            case "has_follow_ups":
                return len(response.follow_ups) > 0
            case "contains_one_of":
                if isinstance(check.value, list):
                    text_lower = response.text.lower()
                    return any(val.lower() in text_lower for val in check.value)
                return False
            case _:
                return False

    def load_cases_from_yaml(self, path: Path) -> list[EvalCase]:
        """Load eval cases from a YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        advisor = data["advisor"]
        cases = []
        for case_data in data["cases"]:
            cases.append(EvalCase.from_dict(case_data, advisor))
        return cases
