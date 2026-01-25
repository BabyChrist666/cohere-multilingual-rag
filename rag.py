"""
Multilingual RAG (Retrieval-Augmented Generation) System
Combines Cohere's Embed, Rerank, and Command models for powerful Q&A
"""

import os
import cohere
from typing import Optional
from dotenv import load_dotenv
from embeddings import MultilingualEmbedder, CohereReranker
from vectorstore import VectorStore

load_dotenv()


class MultilingualRAG:
    """
    Complete RAG system supporting 100+ languages.

    Pipeline:
    1. Query in any language
    2. Embed query with multilingual model
    3. Retrieve relevant documents
    4. Rerank for better relevance
    5. Generate answer with Command model

    Features:
    - Cross-lingual retrieval (query in one language, retrieve in another)
    - Automatic language detection
    - Source citation
    - Confidence scoring
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        collection_name: str = "multilingual_rag",
        persist_directory: str = "./chroma_db",
        generation_model: str = "command-r-08-2024"
    ):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required")

        # Initialize components
        self.embedder = MultilingualEmbedder(api_key=self.api_key)
        self.reranker = CohereReranker(api_key=self.api_key)
        self.vectorstore = VectorStore(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedder=self.embedder
        )
        self.cohere_client = cohere.Client(self.api_key)
        self.generation_model = generation_model

    def add_documents(
        self,
        texts: list[str],
        metadatas: Optional[list[dict]] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> dict:
        """
        Add documents to the knowledge base with automatic chunking.

        Args:
            texts: List of document texts
            metadatas: Optional metadata for each document
            chunk_size: Maximum chunk size in characters
            chunk_overlap: Overlap between chunks

        Returns:
            Statistics about added documents
        """
        all_chunks = []
        all_metadatas = []

        for i, text in enumerate(texts):
            # Chunk the document
            chunks = self._chunk_text(text, chunk_size, chunk_overlap)
            all_chunks.extend(chunks)

            # Create metadata for each chunk
            base_metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            for j, chunk in enumerate(chunks):
                chunk_metadata = {
                    **base_metadata,
                    "doc_index": i,
                    "chunk_index": j,
                    "language": self.embedder.detect_language(chunk[:200])
                }
                all_metadatas.append(chunk_metadata)

        # Add to vector store
        ids = self.vectorstore.add_documents(all_chunks, all_metadatas)

        return {
            "documents_processed": len(texts),
            "chunks_created": len(all_chunks),
            "chunk_ids": ids
        }

    def _chunk_text(
        self,
        text: str,
        chunk_size: int,
        overlap: int
    ) -> list[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                for punct in ['. ', '! ', '? ', '\n\n', '\n']:
                    last_punct = text[start:end].rfind(punct)
                    if last_punct != -1:
                        end = start + last_punct + len(punct)
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - overlap

        return chunks

    def query(
        self,
        question: str,
        n_retrieve: int = 10,
        n_rerank: int = 5,
        language_filter: Optional[str] = None,
        include_sources: bool = True
    ) -> dict:
        """
        Query the RAG system.

        Args:
            question: User's question (any language)
            n_retrieve: Number of documents to retrieve initially
            n_rerank: Number of documents after reranking
            language_filter: Optional language filter (ISO code)
            include_sources: Whether to include source documents

        Returns:
            Dict with 'answer', 'sources', 'query_language', 'confidence'
        """
        # Detect query language
        query_language = self.embedder.detect_language(question)

        # Build filter
        where_filter = None
        if language_filter:
            where_filter = {"language": language_filter}

        # Step 1: Retrieve relevant documents
        retrieved = self.vectorstore.search(
            query=question,
            n_results=n_retrieve,
            where=where_filter
        )

        if not retrieved:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": [],
                "query_language": query_language,
                "confidence": 0.0
            }

        # Step 2: Rerank for better relevance
        doc_texts = [r["text"] for r in retrieved]
        reranked = self.reranker.rerank(
            query=question,
            documents=doc_texts,
            top_n=n_rerank
        )

        # Prepare context for generation
        context_docs = []
        for r in reranked:
            context_docs.append({
                "text": r["text"],
                "score": r["relevance_score"],
                "metadata": retrieved[r["index"]]["metadata"]
            })

        context_text = "\n\n---\n\n".join([d["text"] for d in context_docs])

        # Step 3: Generate answer
        preamble = """You are a helpful multilingual assistant.
Answer questions based ONLY on the provided context.
If the context doesn't contain enough information, say so.
Always respond in the same language as the question.
Be concise but thorough."""

        user_message = f"""Context:
{context_text}

Question: {question}

Answer based on the context above:"""

        response = self.cohere_client.chat(
            model=self.generation_model,
            message=user_message,
            preamble=preamble
        )

        answer = response.text

        # Calculate confidence based on rerank scores
        avg_score = sum(r["relevance_score"] for r in reranked) / len(reranked)

        result = {
            "answer": answer,
            "query_language": query_language,
            "confidence": round(avg_score, 3)
        }

        if include_sources:
            result["sources"] = [
                {
                    "text": d["text"][:200] + "..." if len(d["text"]) > 200 else d["text"],
                    "score": round(d["score"], 3),
                    "language": d["metadata"].get("language", "unknown")
                }
                for d in context_docs
            ]

        return result

    def get_stats(self) -> dict:
        """Get system statistics."""
        vs_stats = self.vectorstore.get_stats()
        return {
            **vs_stats,
            "generation_model": self.generation_model,
            "embedding_model": self.embedder.model,
            "rerank_model": self.reranker.model
        }

    def clear(self) -> None:
        """Clear all documents."""
        self.vectorstore.clear()


def main():
    """Demo the RAG system."""
    print("=" * 60)
    print("🌍 Multilingual RAG System Demo")
    print("=" * 60)

    try:
        rag = MultilingualRAG()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("Please set COHERE_API_KEY in your .env file")
        return

    # Add sample multilingual documents
    sample_docs = [
        # English
        "Artificial intelligence (AI) is intelligence demonstrated by machines. AI research has been defined as the field of study of intelligent agents.",

        # Spanish
        "La inteligencia artificial (IA) es la inteligencia demostrada por máquinas. Es un campo de la informática que busca crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana.",

        # French
        "L'intelligence artificielle (IA) est l'intelligence démontrée par les machines. Elle englobe la création de programmes informatiques capables de simuler certains aspects de l'intelligence humaine.",

        # German
        "Künstliche Intelligenz (KI) ist Intelligenz, die von Maschinen demonstriert wird. Sie ist ein Teilgebiet der Informatik, das sich mit der Automatisierung intelligenten Verhaltens befasst.",

        # Chinese
        "人工智能（AI）是由机器展示的智能。人工智能研究被定义为对智能代理的研究领域，包括任何能够感知环境并采取行动以实现目标的系统。",
    ]

    print("\n📚 Adding sample documents in 5 languages...")
    stats = rag.add_documents(sample_docs)
    print(f"   Added {stats['chunks_created']} chunks from {stats['documents_processed']} documents")

    # Test queries in different languages
    test_queries = [
        "What is artificial intelligence?",  # English
        "¿Qué es la inteligencia artificial?",  # Spanish
        "什么是人工智能？",  # Chinese
    ]

    print("\n" + "=" * 60)
    print("Testing cross-lingual queries:")
    print("=" * 60)

    for query in test_queries:
        print(f"\n❓ Query: {query}")
        result = rag.query(query)
        print(f"🌐 Detected language: {result['query_language']}")
        print(f"💬 Answer: {result['answer'][:300]}...")
        print(f"📊 Confidence: {result['confidence']}")


if __name__ == "__main__":
    main()
