from __future__ import annotations

import pytest

from internship_copilot.planning import create_preparation_plan
from internship_copilot.schemas import Priority, SkillGap


def test_create_preparation_plan_prioritizes_gaps_and_fits_time_window() -> None:
    gaps = [
        SkillGap(
            skill="Docker",
            priority=Priority.LOW,
            reason="No container experience is listed.",
        ),
        SkillGap(
            skill="PyTorch",
            priority=Priority.HIGH,
            reason="The role requires PyTorch, but the resume does not mention it.",
        ),
        SkillGap(
            skill="Testing",
            priority=Priority.MEDIUM,
            reason="The resume does not show automated testing.",
        ),
    ]

    plan = create_preparation_plan(gaps, duration_weeks=2)

    assert [action.title for action in plan] == [
        "Build evidence for PyTorch",
        "Build evidence for Testing",
        "Build evidence for Docker",
    ]
    assert [action.week for action in plan] == [1, 2, 2]
    assert all(action.completion_evidence for action in plan)


def test_create_preparation_plan_rejects_invalid_duration() -> None:
    with pytest.raises(ValueError, match="duration_weeks must be at least 1"):
        create_preparation_plan([], duration_weeks=0)
