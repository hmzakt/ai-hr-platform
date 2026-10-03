from enum import StrEnum

from pydantic import BaseModel, Field


class EmbeddingSourceType(StrEnum):
    CANDIDATE = "candidate"
    EXPERIENCE = "experience"
    PROJECT = "project"
    SKILL = "skill"
    EDUCATION = "education"
    CERTIFICATION = "certification"
    JOB = "job"


class EmbeddingDocument(BaseModel):

    id: str
    text: str
    source_type: EmbeddingSourceType
    candidate_id: str | None = None
    source_id: str | None = None
    metadata: dict[str, str] = Field(
        default_factory=dict
    )