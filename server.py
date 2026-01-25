"""
FastAPI server for Multilingual RAG System
Provides REST API for document ingestion and Q&A
"""

import os
import tempfile
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from rag import MultilingualRAG

load_dotenv()

# Global RAG instance
rag_system: Optional[MultilingualRAG] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize RAG system on startup."""
    global rag_system
    print("🚀 Starting Multilingual RAG Server...")
    try:
        rag_system = MultilingualRAG()
        print("✅ RAG system initialized")
    except Exception as e:
        print(f"⚠️ RAG initialization failed: {e}")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="Multilingual RAG API",
    description="100+ language RAG system powered by Cohere",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DocumentInput(BaseModel):
    texts: list[str]
    metadatas: Optional[list[dict]] = None


class QueryInput(BaseModel):
    question: str
    n_results: int = 5
    language_filter: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    query_language: str
    confidence: float
    sources: Optional[list[dict]] = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve web UI."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multilingual RAG System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .fade-in { animation: fadeIn 0.3s ease-in; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body class="bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 min-h-screen text-white">
    <div class="container mx-auto max-w-4xl p-6">
        <header class="text-center py-8">
            <h1 class="text-4xl font-bold mb-2">🌍 Multilingual RAG System</h1>
            <p class="text-blue-300">Ask questions in any of 100+ languages</p>
            <div class="flex justify-center gap-2 mt-4 flex-wrap">
                <span class="px-2 py-1 bg-blue-600/50 rounded text-xs">English</span>
                <span class="px-2 py-1 bg-green-600/50 rounded text-xs">Español</span>
                <span class="px-2 py-1 bg-red-600/50 rounded text-xs">中文</span>
                <span class="px-2 py-1 bg-yellow-600/50 rounded text-xs">العربية</span>
                <span class="px-2 py-1 bg-purple-600/50 rounded text-xs">日本語</span>
                <span class="px-2 py-1 bg-pink-600/50 rounded text-xs">हिंदी</span>
                <span class="px-2 py-1 bg-indigo-600/50 rounded text-xs">+94 more</span>
            </div>
        </header>

        <!-- Upload Section -->
        <div class="bg-gray-800/50 rounded-xl p-6 mb-6 backdrop-blur">
            <h2 class="text-xl font-semibold mb-4">📄 Add Documents</h2>
            <div class="space-y-4">
                <textarea
                    id="docInput"
                    placeholder="Paste text documents here (one per line or paragraph)..."
                    class="w-full h-32 bg-gray-700 rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
                <button
                    onclick="addDocuments()"
                    class="bg-green-600 hover:bg-green-700 px-6 py-2 rounded-lg font-semibold transition"
                >
                    Add Documents
                </button>
                <span id="docStatus" class="ml-4 text-sm"></span>
            </div>
        </div>

        <!-- Query Section -->
        <div class="bg-gray-800/50 rounded-xl p-6 backdrop-blur">
            <h2 class="text-xl font-semibold mb-4">❓ Ask a Question</h2>
            <div class="space-y-4">
                <input
                    type="text"
                    id="queryInput"
                    placeholder="Ask anything in any language..."
                    class="w-full bg-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                <div class="flex gap-2">
                    <button
                        onclick="askQuestion()"
                        class="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-semibold transition"
                    >
                        Search & Answer
                    </button>
                    <select id="langFilter" class="bg-gray-700 rounded-lg px-4">
                        <option value="">All Languages</option>
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="zh-cn">Chinese</option>
                        <option value="ja">Japanese</option>
                        <option value="ar">Arabic</option>
                    </select>
                </div>
            </div>

            <!-- Results -->
            <div id="results" class="mt-6 hidden">
                <div class="border-t border-gray-700 pt-4">
                    <div class="flex items-center gap-2 mb-2">
                        <span id="detectedLang" class="px-2 py-1 bg-blue-600 rounded text-xs"></span>
                        <span id="confidence" class="px-2 py-1 bg-green-600 rounded text-xs"></span>
                    </div>
                    <h3 class="font-semibold mb-2">Answer:</h3>
                    <p id="answer" class="bg-gray-700 rounded-lg p-4"></p>

                    <h3 class="font-semibold mt-4 mb-2">Sources:</h3>
                    <div id="sources" class="space-y-2"></div>
                </div>
            </div>
        </div>

        <!-- Stats -->
        <div class="mt-6 text-center">
            <button onclick="loadStats()" class="text-blue-400 hover:underline text-sm">
                View System Stats
            </button>
            <div id="stats" class="mt-2 text-sm text-gray-400"></div>
        </div>

        <footer class="text-center py-6 text-gray-500 text-sm">
            Powered by Cohere Embed, Rerank & Command R+ |
            <a href="/docs" class="text-blue-400 hover:underline">API Docs</a>
        </footer>
    </div>

    <script>
        async function addDocuments() {
            const text = document.getElementById('docInput').value.trim();
            if (!text) return;

            const status = document.getElementById('docStatus');
            status.textContent = 'Adding...';
            status.className = 'ml-4 text-sm text-yellow-400';

            try {
                const texts = text.split(/\\n\\n+/).filter(t => t.trim());
                const response = await fetch('/documents', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ texts })
                });

                const data = await response.json();
                if (response.ok) {
                    status.textContent = `✓ Added ${data.chunks_created} chunks`;
                    status.className = 'ml-4 text-sm text-green-400';
                    document.getElementById('docInput').value = '';
                } else {
                    throw new Error(data.detail);
                }
            } catch (error) {
                status.textContent = '✗ ' + error.message;
                status.className = 'ml-4 text-sm text-red-400';
            }
        }

        async function askQuestion() {
            const question = document.getElementById('queryInput').value.trim();
            if (!question) return;

            const langFilter = document.getElementById('langFilter').value;
            const results = document.getElementById('results');

            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question,
                        language_filter: langFilter || null
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('detectedLang').textContent = 'Language: ' + data.query_language;
                    document.getElementById('confidence').textContent = 'Confidence: ' + (data.confidence * 100).toFixed(1) + '%';
                    document.getElementById('answer').textContent = data.answer;

                    const sourcesDiv = document.getElementById('sources');
                    sourcesDiv.innerHTML = '';
                    if (data.sources) {
                        data.sources.forEach((s, i) => {
                            const div = document.createElement('div');
                            div.className = 'bg-gray-700/50 rounded p-3 text-sm';
                            div.innerHTML = `
                                <div class="flex justify-between text-xs text-gray-400 mb-1">
                                    <span>Source ${i + 1} (${s.language})</span>
                                    <span>Score: ${(s.score * 100).toFixed(1)}%</span>
                                </div>
                                <p>${s.text}</p>
                            `;
                            sourcesDiv.appendChild(div);
                        });
                    }

                    results.classList.remove('hidden');
                    results.classList.add('fade-in');
                } else {
                    throw new Error(data.detail);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                document.getElementById('stats').textContent =
                    `Documents: ${data.document_count} | Model: ${data.generation_model}`;
            } catch (error) {
                console.error(error);
            }
        }

        // Enter key support
        document.getElementById('queryInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') askQuestion();
        });
    </script>
</body>
</html>
"""


@app.post("/documents")
async def add_documents(input: DocumentInput):
    """Add documents to the knowledge base."""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    try:
        result = rag_system.add_documents(
            texts=input.texts,
            metadatas=input.metadatas
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query(input: QueryInput):
    """Query the RAG system."""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    try:
        result = rag_system.query(
            question=input.question,
            n_rerank=input.n_results,
            language_filter=input.language_filter
        )
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    return rag_system.get_stats()


@app.post("/clear")
async def clear_documents():
    """Clear all documents."""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    rag_system.clear()
    return {"status": "cleared"}


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "healthy" if rag_system else "initializing",
        "rag_ready": rag_system is not None
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
