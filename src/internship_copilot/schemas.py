from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MatchLabel(str, Enum):
    SUPPORTED = "supported"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"
    UNCERTAIN = "uncertain"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnalysisRequest(StrictModel):
    job_description: str
    resume: str

    @field_validator("job_description", "resume")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("input text must not be empty")
        return cleaned


class JobRequirement(StrictModel):
    id: str = Field(min_length=1)
    skill: str = Field(min_length=1)
    description: str = Field(min_length=1)
    priority: Priority


class EvidencePassage(StrictModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1)


class MatchResult(StrictModel):
    requirement_id: str = Field(min_length=1)
    label: MatchLabel
    evidence_ids: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def supported_matches_require_evidence(self) -> "MatchResult":
        if self.label in {MatchLabel.SUPPORTED, MatchLabel.PARTIAL} and not self.evidence_ids:
            raise ValueError(f"{self.label.value} matches require evidence")
        return self


class SkillGap(StrictModel):
    skill: str = Field(min_length=1)
    priority: Priority
    reason: str = Field(min_length=1)


class PreparationAction(StrictModel):
    week: int = Field(ge=1)
    title: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    completion_evidence: str = Field(min_length=1)


class AnalysisReport(StrictModel):
    summary: str = Field(min_length=1)
    requirements: list[JobRequirement]
    evidence: list[EvidencePassage]
    matches: list[MatchResult]
    gaps: list[SkillGap]
    preparation_plan: list[PreparationAction]
    limitations: list[str]

    @model_validator(mode="after")
    def validate_references(self) -> "AnalysisReport":
        requirement_ids = {requirement.id for requirement in self.requirements}
        evidence_ids = {passage.id for passage in self.evidence}

        for match in self.matches:
            if match.requirement_id not in requirement_ids:
                raise ValueError(
                    f"match references unknown requirement ID: {match.requirement_id}"
                )

            unknown_evidence_ids = set(match.evidence_ids) - evidence_ids
            if unknown_evidence_ids:
                unknown = ", ".join(sorted(unknown_evidence_ids))
                raise ValueError(f"match references unknown evidence ID: {unknown}")

        return self
