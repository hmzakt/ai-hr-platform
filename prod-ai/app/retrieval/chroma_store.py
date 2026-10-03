from __future__ import annotations

from typing import Any

from langchain_chroma import Chroma

from app.retrieval.model import SemanticSearchResult


class ChromaVectorStore:

    def __init__(
        self,
        vectorstore: Chroma,
    ) -> None:

        self.vectorstore = vectorstore

    def similarity_search(
        self,
        query: str,
        k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[SemanticSearchResult]:

        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
            filter=filters,
        )

        return [
            self._to_search_result(
                document=document,
                score=score,
            )
            for document, score in results
        ]

    @staticmethod
    def _to_search_result(
        document,
        score: float,
    ) -> SemanticSearchResult:

        metadata = document.metadata

        return SemanticSearchResult(
            document_id=metadata.get(
                "document_id",
                "",
            ),
            candidate_id=metadata.get(
              "candidate_id",
              "",
            ),
            text=document.page_content,
            source_type=metadata["source_type"],
            source_id=metadata.get("source_id"),
            distance=score,
            metadata=metadata,
        )