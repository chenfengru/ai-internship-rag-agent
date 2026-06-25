from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

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


def test_valid_report_can_be_constructed_and_serialized() -> None:
    report = AnalysisReport(
        summary="The candidate has evidence for Python and testing experience.",
        requirements=[
            JobRequirement(
                id="req-python",
                skill="Python",
                description="Build Python tools for machine learning workflows.",
                priority=Priority.HIGH,
            )
        ],
        evidence=[
            EvidencePassage(
                id="ev-python",
                text="Built Python data-processing scripts.",
            )
        ],
        matches=[
            MatchResult(
                requirement_id="req-python",
                label=MatchLabel.SUPPORTED,
                evidence_ids=["ev-python"],
                rationale="The resume explicitly describes Python project work.",
            )
        ],
        gaps=[
            SkillGap(
                skill="Deployment",
                priority=Priority.MEDIUM,
                reason="The job values production awareness, but no evidence is provided.",
            )
        ],
        preparation_plan=[
            PreparationAction(
                week=1,
                title="Review model serving basics",
                purpose="Prepare to discuss how a model can be exposed safely.",
                completion_evidence="Write a one-page deployment checklist.",
            )
        ],
        limitations=["Fixture output; no real AI analysis has been performed."],
    )

    payload = json.loads(report.model_dump_json())

    assert payload["matches"][0]["label"] == "supported"
    assert payload["matches"][0]["evidence_ids"] == ["ev-python"]


def test_empty_resume_input_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AnalysisRequest(
            job_description="Python and machine learning experience required.",
            resume="   ",
        )


def test_match_with_nonexistent_evidence_id_fails_validation() -> None:
    with pytest.raises(ValidationError, match="unknown evidence ID"):
        AnalysisReport(
            summary="Invalid report.",
            requirements=[
                JobRequirement(
                    id="req-python",
                    skill="Python",
                    description="Python is required.",
                    priority=Priority.HIGH,
                )
            ],
            evidence=[],
            matches=[
                MatchResult(
                    requirement_id="req-python",
                    label=MatchLabel.SUPPORTED,
                    evidence_ids=["ev-missing"],
                    rationale="This evidence does not exist.",
                )
            ],
            gaps=[],
            preparation_plan=[],
            limitations=[],
        )
