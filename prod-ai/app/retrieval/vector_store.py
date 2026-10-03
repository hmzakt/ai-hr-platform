from __future__ import annotations

from typing import Any

from langchain_chroma import Chroma

from app.embeddings.models import EmbeddingDocument


class CandidateVectorStore:

    COLLECTION_NAME = "candidate_profiles"

    def __init__(
        self,
        vectorstore: Chroma,
    ) -> None:

        self.vectorstore = vectorstore

    def add_documents(
        self,
        documents: list[EmbeddingDocument],
    ) -> list[str]:

        if not documents:
            return []

        ids = [
            document.id
            for document in documents
        ]

        texts = [
            document.text
            for document in documents
        ]

        metadatas = [
            {
                **document.metadata,
                "source_type": document.source_type.value,
            }
            for document in documents
        ]

        return self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
        )

    def search(
        self,
        query: str,
        k: int = 10,
    ):

        return self.vectorstore.similarity_search(
            query,
            k=k,
        )



from abc import ABC, abstractmethod

class VectorStore(ABC):

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        k: int = 10,
        filters: dict[str, Any] | None = None,
    ):
        raise NotImplementedError