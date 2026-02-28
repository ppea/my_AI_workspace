from __future__ import annotations

from pathlib import Path

import pytest

from src.core.message import OutgoingResponse, ActionItem, FollowUp
from tests.eval.eval_runner import EvalRunner, EvalCase
from tests.eval.rubrics import ADVISOR_RUBRICS

EVAL_CASES_DIR = Path(__file__).parent / "eval_cases"


def build_response_from_mock(mock_data: dict) -> OutgoingResponse:
    """Construct OutgoingResponse from YAML mock_response dict."""
    action_items = [
        ActionItem(title=title, advisor=mock_data["advisor"])
        for title in mock_data.get("action_items", [])
    ]
    follow_ups = [
        FollowUp(question=q, advisor=mock_data["advisor"])
        for q in mock_data.get("follow_ups", [])
    ]

    return OutgoingResponse(
        text=mock_data["text"],
        advisor=mock_data.get("advisor"),
        action_items=action_items,
        follow_ups=follow_ups,
        caveat=mock_data.get("caveat"),
    )


def load_all_cases() -> list[tuple[str, EvalCase]]:
    """Return list of (case_id, case) for parametrize."""
    runner = EvalRunner()
    all_cases = []

    # Load all YAML files from eval_cases directory
    for yaml_file in sorted(EVAL_CASES_DIR.glob("*.yaml")):
        cases = runner.load_cases_from_yaml(yaml_file)
        for case in cases:
            all_cases.append((case.id, case))

    return all_cases


@pytest.mark.parametrize("case_id,case", load_all_cases())
def test_eval_case(case_id: str, case: EvalCase):
    """Run each eval case against its rubric."""
    runner = EvalRunner()
    response = build_response_from_mock(case.mock_response)
    rubric = ADVISOR_RUBRICS[case.advisor]

    result = runner.run_case(case, response, rubric)

    assert result.passed, (
        f"Eval case {case_id} failed:\n" + "\n".join(result.messages)
    )
