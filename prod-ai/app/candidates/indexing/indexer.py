from __future__ import annotations

from app.schemas.candidate.profile import CandidateProfile
from app.embeddings.service import EmbeddingService
from app.retrieval.vector_store import CandidateVectorStore

from .documents import CandidateEmbeddingBuilder


class CandidateIndexer:

    def __init__(
        self,
        document_builder: CandidateEmbeddingBuilder,
        embedding_service: EmbeddingService,
        vector_store: CandidateVectorStore,
    ) -> None:

        self.document_builder = document_builder
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index(
        self,
        candidate: CandidateProfile,
        candidate_id: str,
    ) -> list[str]:

        documents = self.document_builder.build(
            candidate=candidate,
            candidate_id=candidate_id,
        )

        if not documents:
            return []

        return self.vector_store.add_documents(
            documents
        )