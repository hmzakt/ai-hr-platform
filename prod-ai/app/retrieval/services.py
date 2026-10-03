from __future__ import annotations

from typing import Any

from .model import CandidateSearchResult, SemanticSearchResult


class SemanticSearchService:

    def __init__(self, vector_store) -> None:
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        *,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[SemanticSearchResult]:
        query = query.strip()

        if not query:
            return []

        return self.vector_store.similarity_search(
            query=query,
            k=top_k,
            filters=filters,
        )

    def search_candidates(
        self,
        query: str,
        *,
        top_k: int = 10,
        chunks_per_candidate: int = 3,
        filters: dict[str, Any] | None = None,
    ) -> list[CandidateSearchResult]:
        chunk_results = self.search(
            query=query,
            top_k=top_k * chunks_per_candidate,
            filters=filters,
        )

        if not chunk_results:
            return []

        grouped: dict[str, list[SemanticSearchResult]] = {}

        for result in chunk_results:
            grouped.setdefault(result.candidate_id, []).append(result)

        candidates: list[CandidateSearchResult] = []

        for candidate_id, documents in grouped.items():
            documents.sort(key=lambda item: item.distance)
            selected_documents = documents[:chunks_per_candidate]

            if not selected_documents:
                continue

            candidates.append(
                CandidateSearchResult(
                    candidate_id=candidate_id,
                    best_distance=selected_documents[0].distance,
                    matched_documents=selected_documents,
                )
            )

        candidates.sort(key=lambda item: item.best_distance)
        return candidates[:top_k]
