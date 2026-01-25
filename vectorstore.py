"""
Vector Store using ChromaDB for persistent storage
Handles document storage, retrieval, and similarity search
"""

import os
import uuid
import chromadb
from chromadb.config import Settings
from typing import Optional
from embeddings import MultilingualEmbedder


class VectorStore:
    """
    ChromaDB-based vector store for multilingual document storage and retrieval.

    Features:
    - Persistent storage
    - Multilingual support via Cohere embeddings
    - Metadata filtering
    - Similarity search with scores
    """

    def __init__(
        self,
        collection_name: str = "multilingual_docs",
        persist_directory: str = "./chroma_db",
        embedder: Optional[MultilingualEmbedder] = None
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedder = embedder or MultilingualEmbedder()

        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        texts: list[str],
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None
    ) -> list[str]:
        """
        Add documents to the vector store.

        Args:
            texts: List of document texts
            metadatas: Optional list of metadata dicts
            ids: Optional list of document IDs

        Returns:
            List of document IDs
        """
        if not texts:
            return []

        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]

        # Generate default metadata if not provided
        if metadatas is None:
            metadatas = []
            for text in texts:
                lang = self.embedder.detect_language(text[:500])
                metadatas.append({
                    "language": lang,
                    "char_count": len(text)
                })

        # Generate embeddings
        embeddings = self.embedder.embed_documents(texts)

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

        return ids

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[dict] = None,
        include_scores: bool = True
    ) -> list[dict]:
        """
        Search for similar documents.

        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional metadata filter
            include_scores: Whether to include similarity scores

        Returns:
            List of results with 'id', 'text', 'metadata', and optionally 'score'
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_query(query)

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        formatted = []
        for i in range(len(results["ids"][0])):
            result = {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {}
            }
            if include_scores and results["distances"]:
                # Convert distance to similarity score (cosine)
                result["score"] = 1 - results["distances"][0][i]
            formatted.append(result)

        return formatted

    def delete(self, ids: list[str]) -> None:
        """Delete documents by ID."""
        self.collection.delete(ids=ids)

    def get_stats(self) -> dict:
        """Get collection statistics."""
        return {
            "collection_name": self.collection_name,
            "document_count": self.collection.count(),
            "persist_directory": self.persist_directory
        }

    def clear(self) -> None:
        """Clear all documents from collection."""
        # Delete and recreate collection
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
