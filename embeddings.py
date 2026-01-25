"""
Multilingual Embeddings using Cohere's Embed API
Supports 100+ languages via Cohere's multilingual models
"""

import os
import cohere
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class MultilingualEmbedder:
    """
    Generates multilingual embeddings using Cohere's embed-multilingual-v3.0 model.

    Supports 100+ languages including:
    - European: English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, etc.
    - Asian: Chinese, Japanese, Korean, Hindi, Thai, Vietnamese, Indonesian, etc.
    - Middle Eastern: Arabic, Hebrew, Turkish, Persian, etc.
    - African: Swahili, Amharic, etc.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "embed-multilingual-v3.0"
    ):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required")

        self.client = cohere.Client(self.api_key)
        self.model = model
        self.embedding_dimension = 1024  # embed-multilingual-v3.0 dimension

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of documents.

        Args:
            texts: List of text documents to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        # Cohere API has a limit of 96 texts per request
        batch_size = 96
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embed(
                texts=batch,
                model=self.model,
                input_type="search_document"
            )
            all_embeddings.extend(response.embeddings)

        return all_embeddings

    def embed_query(self, query: str) -> list[float]:
        """
        Generate embedding for a search query.

        Args:
            query: Search query text

        Returns:
            Embedding vector
        """
        response = self.client.embed(
            texts=[query],
            model=self.model,
            input_type="search_query"
        )
        return response.embeddings[0]

    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text.

        Args:
            text: Text to analyze

        Returns:
            ISO language code (e.g., 'en', 'es', 'zh')
        """
        try:
            from langdetect import detect
            return detect(text)
        except:
            return "unknown"


class CohereReranker:
    """
    Reranks search results using Cohere's Rerank API for better relevance.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "rerank-multilingual-v3.0"
    ):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required")

        self.client = cohere.Client(self.api_key)
        self.model = model

    def rerank(
        self,
        query: str,
        documents: list[str],
        top_n: int = 5
    ) -> list[dict]:
        """
        Rerank documents by relevance to query.

        Args:
            query: Search query
            documents: List of document texts
            top_n: Number of top results to return

        Returns:
            List of dicts with 'index', 'text', and 'relevance_score'
        """
        if not documents:
            return []

        response = self.client.rerank(
            query=query,
            documents=documents,
            model=self.model,
            top_n=min(top_n, len(documents))
        )

        results = []
        for r in response.results:
            results.append({
                "index": r.index,
                "text": documents[r.index],
                "relevance_score": r.relevance_score
            })

        return results
