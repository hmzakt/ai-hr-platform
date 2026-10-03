from __future__ import annotations

import os

import voyageai

from .base import EmbeddingProvider


class VoyageEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        model: str | None = None,
    ) -> None:

        self.model = model or os.getenv(
            "voyage-2",
        )

        self.client = voyageai.Client(
            api_key=os.getenv("VOYAGE_API_KEY")
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="document",
        )

        return response.embeddings

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        if not text.strip():
            raise ValueError(
                "Query text cannot be empty."
            )

        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="query",
        )

        return response.embeddings[0]