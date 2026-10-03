from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @abstractmethod
    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for stored documents.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a search query.
        """
        raise NotImplementedError