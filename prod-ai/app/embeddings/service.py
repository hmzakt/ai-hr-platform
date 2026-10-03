from __future__ import annotations

from .base import EmbeddingProvider
from .models import EmbeddingDocument


class EmbeddingService:

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:

        self.provider = provider

    def embed_documents(
        self,
        documents: list[EmbeddingDocument],
    ) -> list[list[float]]:

        if not documents:
            return []

        texts = [
            document.text
            for document in documents
        ]

        return self.provider.embed_documents(
            texts
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        return self.provider.embed_query(
            query
        )