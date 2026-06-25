from __future__ import annotations

from internship_copilot.schemas import PreparationAction, Priority, SkillGap


_PRIORITY_ORDER = {
    Priority.HIGH: 0,
    Priority.MEDIUM: 1,
    Priority.LOW: 2,
}


def create_preparation_plan(
    gaps: list[SkillGap],
    duration_weeks: int = 2,
) -> list[PreparationAction]:
    """Create one deterministic preparation action for each prioritized gap."""
    if duration_weeks < 1:
        raise ValueError("duration_weeks must be at least 1")

    ordered_gaps = sorted(gaps, key=lambda gap: _PRIORITY_ORDER[gap.priority])

    return [
        PreparationAction(
            week=min(index, duration_weeks),
            title=f"Build evidence for {gap.skill}",
            purpose=gap.reason,
            completion_evidence=(
                f"Create one reviewable artifact demonstrating {gap.skill}."
            ),
        )
        for index, gap in enumerate(ordered_gaps, start=1)
    ]
