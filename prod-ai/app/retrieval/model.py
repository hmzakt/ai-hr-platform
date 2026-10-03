from __future__ import annotations
from pydantic import BaseModel, Field
from app.embeddings.models import EmbeddingSourceType

class SemanticSearchResult(BaseModel):

    document_id: str
    candidate_id: str
    text: str
    source_type: EmbeddingSourceType
    source_id: str | None = None

    distance: float

    metadata: dict[str, str] = Field(
        default_factory=dict
    )

class CandidateSearchResult(BaseModel):

    candidate_id: str
    best_distance: float

    matched_documents: list[
        SemanticSearchResult
    ] = Field(
        default_factory=list
    )