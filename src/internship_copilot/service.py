from __future__ import annotations

from internship_copilot.schemas import (
    AnalysisReport,
    AnalysisRequest,
    EvidencePassage,
    JobRequirement,
    MatchLabel,
    MatchResult,
    PreparationAction,
    Priority,
    SkillGap,
)


def create_fixture_analysis(request: AnalysisRequest) -> AnalysisReport:
    """Return deterministic fixture output for the Milestone 1A prototype."""
    skill = "Python"
    requirement = JobRequirement(
        id="req-python",
        skill=skill,
        description="Demonstrate Python experience relevant to the role.",
        priority=Priority.HIGH,
    )

    resume_mentions_skill = skill.casefold() in request.resume.casefold()
    evidence = (
        [EvidencePassage(id="ev-python", text=request.resume)]
        if resume_mentions_skill
        else []
    )
    label = MatchLabel.SUPPORTED if resume_mentions_skill else MatchLabel.UNSUPPORTED
    evidence_ids = ["ev-python"] if resume_mentions_skill else []

    match = MatchResult(
        requirement_id=requirement.id,
        label=label,
        evidence_ids=evidence_ids,
        rationale=(
            "The resume explicitly mentions Python."
            if resume_mentions_skill
            else "The resume does not provide explicit Python evidence."
        ),
    )

    gaps = (
        []
        if resume_mentions_skill
        else [
            SkillGap(
                skill=skill,
                priority=Priority.HIGH,
                reason="The fixture found no explicit Python evidence in the resume.",
            )
        ]
    )

    return AnalysisReport(
        summary=(
            "Fixture analysis found explicit Python evidence."
            if resume_mentions_skill
            else "Fixture analysis found no explicit Python evidence."
        ),
        requirements=[requirement],
        evidence=evidence,
        matches=[match],
        gaps=gaps,
        preparation_plan=[
            PreparationAction(
                week=1,
                title="Review the fixture report",
                purpose="Verify the Milestone 1A schema and CLI flow.",
                completion_evidence="Save one schema-valid JSON report.",
            )
        ],
        limitations=[
            "Deterministic fixture output only; no LLM or retrieval analysis was used.",
            "Only explicit Python mentions are checked in Milestone 1A.",
        ],
    )
