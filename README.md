# 🌍 Multilingual RAG System

A powerful Retrieval-Augmented Generation system supporting **100+ languages** using Cohere's multilingual models.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Cohere](https://img.shields.io/badge/Cohere-Multilingual-green)
![Languages](https://img.shields.io/badge/Languages-100+-orange)

## ✨ Features

- **🌐 100+ Languages** - Query and retrieve in any supported language
- **🔄 Cross-lingual Search** - Ask in English, find documents in Chinese
- **📊 Semantic Reranking** - Cohere Rerank for precise relevance
- **💾 Persistent Storage** - ChromaDB vector database
- **🎯 Source Citations** - Know where answers come from
- **📈 Confidence Scores** - Understand answer reliability
- **🖥️ Beautiful Web UI** - Easy-to-use interface

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Cohere API key ([Get one free](https://dashboard.cohere.com/api-keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cohere-multilingual-rag.git
cd cohere-multilingual-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your COHERE_API_KEY
```

### Run Demo

```bash
python rag.py
```

### Run Web Server

```bash
python server.py
# Open http://localhost:8000
```

## 📖 How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                    User Query (Any Language)                  │
│                    "什么是机器学习？"                          │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│            Cohere Embed Multilingual v3.0                     │
│            (Convert query to 1024-dim vector)                 │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                   ChromaDB Vector Search                      │
│            (Find top 10 similar documents)                    │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│            Cohere Rerank Multilingual v3.0                    │
│            (Reorder by semantic relevance → top 5)            │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  Cohere Command R+                            │
│            (Generate answer from context)                     │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              Answer (In Query Language)                       │
│              "机器学习是人工智能的一个分支..."                  │
└──────────────────────────────────────────────────────────────┘
```

## 🌐 Supported Languages

The system supports **100+ languages** including:

| Region | Languages |
|--------|-----------|
| **European** | English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Ukrainian, Greek, Turkish |
| **Asian** | Chinese (Simplified & Traditional), Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Hindi, Bengali, Tamil |
| **Middle Eastern** | Arabic, Hebrew, Persian (Farsi), Urdu |
| **African** | Swahili, Amharic, Yoruba, Hausa |

## 🔧 API Endpoints

### Add Documents
```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Document text in any language..."],
    "metadatas": [{"source": "wikipedia"}]
  }'
```

### Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "n_results": 5,
    "language_filter": null
  }'
```

### Get Stats
```bash
curl http://localhost:8000/stats
```

## 📊 Example Queries

### English → English
```
Q: "What are the benefits of renewable energy?"
A: "Renewable energy offers numerous benefits including reduced greenhouse gas emissions..."
```

### Spanish → Mixed Sources
```
Q: "¿Cuáles son los beneficios de la energía renovable?"
A: "La energía renovable ofrece numerosos beneficios, incluyendo..."
```

### Chinese → Cross-lingual
```
Q: "可再生能源有什么好处？"
A: "可再生能源的好处包括减少温室气体排放..."
```

## 🏗️ Architecture

```
cohere-multilingual-rag/
├── embeddings.py      # Cohere Embed & Rerank wrappers
├── vectorstore.py     # ChromaDB integration
├── rag.py             # Main RAG pipeline
├── server.py          # FastAPI server & web UI
├── requirements.txt
└── README.md
```

## 🎯 Use Cases

1. **Multilingual Customer Support** - Answer questions in customer's language
2. **Global Knowledge Base** - Index documents in multiple languages
3. **Cross-border Research** - Find relevant papers regardless of language
4. **International E-commerce** - Product search across languages
5. **Legal/Compliance** - Search regulations in original language

## 🚢 Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

### Railway / Render

Set environment variable `COHERE_API_KEY` and deploy!

## 🎯 Why This Project?

This demonstrates:
- **Multilingual AI** - Core to Cohere's Aya initiative
- **RAG Architecture** - Production-ready retrieval system
- **Cohere API Mastery** - Embed, Rerank, and Command integration
- **Full-stack Implementation** - From vectors to web UI

Perfect for roles like:
- Member of Technical Staff, Search
- Applied AI Engineer – Agentic Workflows
- Forward Deployed Engineer

## 📄 License

MIT License

## 🙏 Acknowledgments

- [Cohere](https://cohere.com) for multilingual models
- [ChromaDB](https://www.trychroma.com) for vector storage
- [FastAPI](https://fastapi.tiangolo.com) for the API framework

---

Built with ❤️ for the Cohere team
