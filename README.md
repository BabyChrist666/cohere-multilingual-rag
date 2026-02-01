<div align="center">

```
██████╗ ██╗      ██████╗  ██████╗ ██████╗     ████████╗ ██████╗ ███╗   ██╗ ██████╗ ██╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗████╗  ██║██╔════╝ ██║   ██║██╔════╝
██████╔╝██║     ██║   ██║██║   ██║██║  ██║       ██║   ██║   ██║██╔██╗ ██║██║  ███╗██║   ██║█████╗
██╔══██╗██║     ██║   ██║██║   ██║██║  ██║       ██║   ██║   ██║██║╚██╗██║██║   ██║██║   ██║██╔══╝
██████╔╝███████╗╚██████╔╝╚██████╔╝██████╔╝       ██║   ╚██████╔╝██║ ╚████║╚██████╔╝╚██████╔╝███████╗
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝        ╚═╝    ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚══════╝
```

# ⛧ MULTILINGUAL RAG SYSTEM ⛧

<img src="https://img.shields.io/badge/LANGUAGES-100+-ff0033?style=for-the-badge&labelColor=1a0000" />
<img src="https://img.shields.io/badge/COHERE-EMBED%20v3-cc0000?style=for-the-badge&labelColor=1a0000" />
<img src="https://img.shields.io/badge/PYTHON-3.10+-8b0000?style=for-the-badge&labelColor=1a0000" />
<img src="https://img.shields.io/badge/STATUS-OPERATIONAL-ff1a1a?style=for-the-badge&labelColor=1a0000" />

<br/>

**`[ CROSS-LINGUAL KNOWLEDGE EXTRACTION // POWERED BY COHERE ]`**

*Query in any language. Retrieve with precision.*

---

</div>

---

## ▼ SYSTEM OVERVIEW

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ║
║   ▓                                                                      ▓   ║
║   ▓   A retrieval-augmented generation system that speaks ALL tongues   ▓   ║
║   ▓   Leveraging Cohere's multilingual models to pierce language        ▓   ║
║   ▓   barriers and extract knowledge from the depths of any corpus      ▓   ║
║   ▓                                                                      ▓   ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## ◈ CAPABILITIES

<table>
<tr>
<td width="50%">

### ⛧ RETRIEVAL ENGINE

```
┌─────────────────────────────────┐
│  ◉ 100+ Languages Supported    │
│  ◉ Cross-Lingual Search        │
│  ◉ Semantic Vector Matching    │
│  ◉ ChromaDB Persistence        │
└─────────────────────────────────┘
```

</td>
<td width="50%">

### ⛧ GENERATION CORE

```
┌─────────────────────────────────┐
│  ◉ Cohere Command R+           │
│  ◉ Source Citations            │
│  ◉ Confidence Scoring          │
│  ◉ Context-Aware Responses     │
└─────────────────────────────────┘
```

</td>
</tr>
</table>

---

## ◈ FEATURE MATRIX

| FEATURE | DESCRIPTION | STATUS |
|:--------|:------------|:------:|
| **`MULTILINGUAL EMBED`** | Query and retrieve in 100+ languages | `◉ ACTIVE` |
| **`CROSS-LINGUAL`** | Ask in English → Find documents in Chinese | `◉ ACTIVE` |
| **`SEMANTIC RERANK`** | Cohere Rerank v3 for precision retrieval | `◉ ACTIVE` |
| **`PERSISTENT STORAGE`** | ChromaDB vector database with HNSW | `◉ ACTIVE` |
| **`SOURCE TRACKING`** | Full citation chain for every response | `◉ ACTIVE` |
| **`CONFIDENCE METRICS`** | Reliability scores for all outputs | `◉ ACTIVE` |
| **`WEB INTERFACE`** | Dark-themed UI for human interaction | `◉ ACTIVE` |

---

## ⛧ SYSTEM ARCHITECTURE

```
                              ╔═══════════════════════════════════════╗
                              ║     USER QUERY [ANY LANGUAGE]         ║
                              ║         "什么是机器学习？"              ║
                              ╚═══════════════════╤═══════════════════╝
                                                  │
                                                  ▼
                    ┌─────────────────────────────────────────────────────┐
                    │            ⛧ COHERE EMBED MULTILINGUAL v3.0 ⛧       │
                    │           [ Convert query → 1024-dim vector ]       │
                    └─────────────────────────┬───────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────────┐
                    │              ⛧ CHROMADB VECTOR SEARCH ⛧             │
                    │            [ Retrieve top 10 similar docs ]         │
                    └─────────────────────────┬───────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────────┐
                    │           ⛧ COHERE RERANK MULTILINGUAL v3.0 ⛧       │
                    │          [ Reorder by semantic relevance → 5 ]      │
                    └─────────────────────────┬───────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────────┐
                    │                 ⛧ COHERE COMMAND R+ ⛧               │
                    │              [ Generate grounded answer ]           │
                    └─────────────────────────┬───────────────────────────┘
                                              │
                                              ▼
                              ╔═══════════════════════════════════════╗
                              ║      RESPONSE [QUERY LANGUAGE]        ║
                              ║   "机器学习是人工智能的一个分支..."     ║
                              ╚═══════════════════════════════════════╝
```

---

## ◈ SUPPORTED LANGUAGES

<table>
<tr>
<td>

### EUROPEAN
```
◉ English    ◉ Spanish
◉ French     ◉ German
◉ Italian    ◉ Portuguese
◉ Dutch      ◉ Polish
◉ Russian    ◉ Ukrainian
◉ Greek      ◉ Turkish
```

</td>
<td>

### ASIAN
```
◉ Chinese (Simplified)
◉ Chinese (Traditional)
◉ Japanese   ◉ Korean
◉ Vietnamese ◉ Thai
◉ Indonesian ◉ Malay
◉ Hindi      ◉ Bengali
```

</td>
<td>

### MIDDLE EASTERN
```
◉ Arabic
◉ Hebrew
◉ Persian (Farsi)
◉ Urdu
```

### AFRICAN
```
◉ Swahili    ◉ Amharic
◉ Yoruba     ◉ Hausa
```

</td>
</tr>
</table>

---

## ⛧ QUICK START

### PREREQUISITES

```
╔════════════════════════════════════════════════╗
║  ◉ Python 3.10+                                ║
║  ◉ Cohere API Key (https://cohere.com)         ║
╚════════════════════════════════════════════════╝
```

### INSTALLATION

```bash
# Clone the repository
git clone https://github.com/BabyChrist666/cohere-multilingual-rag.git
cd cohere-multilingual-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env → Add your COHERE_API_KEY
```

### EXECUTE

```bash
# Run CLI Demo
python rag.py

# Launch Web Server
python server.py
# Access: http://localhost:8000
```

---

## ◈ API ENDPOINTS

### `POST` /documents — *Ingest Knowledge*

```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Document content in any language..."],
    "metadatas": [{"source": "origin"}]
  }'
```

### `POST` /query — *Extract Knowledge*

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "n_results": 5
  }'
```

### `GET` /stats — *System Status*

```bash
curl http://localhost:8000/stats
```

---

## ◈ DIRECTORY STRUCTURE

```
cohere-multilingual-rag/
├── embeddings.py      # Cohere Embed & Rerank integration
├── vectorstore.py     # ChromaDB vector operations
├── rag.py             # Core RAG pipeline
├── server.py          # FastAPI server & web UI
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

---

## ⛧ USE CASES

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│   ◉ MULTILINGUAL CUSTOMER SUPPORT                                     │
│     Answer queries in the customer's native language                   │
│                                                                        │
│   ◉ GLOBAL KNOWLEDGE BASE                                             │
│     Index and retrieve documents across language barriers              │
│                                                                        │
│   ◉ CROSS-BORDER RESEARCH                                             │
│     Find relevant papers regardless of publication language            │
│                                                                        │
│   ◉ INTERNATIONAL E-COMMERCE                                          │
│     Product search that transcends linguistic boundaries               │
│                                                                        │
│   ◉ LEGAL/COMPLIANCE                                                  │
│     Search regulations in their original jurisdictional language       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ◈ DEPLOYMENT

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

### Cloud Platforms

```
◉ Railway    → Set COHERE_API_KEY → Deploy
◉ Render     → Set COHERE_API_KEY → Deploy
◉ Fly.io     → Set COHERE_API_KEY → Deploy
```

---

## ◈ TECH STACK

<table>
<tr>
<td align="center"><strong>Cohere</strong><br/>Multilingual LLMs</td>
<td align="center"><strong>ChromaDB</strong><br/>Vector Storage</td>
<td align="center"><strong>FastAPI</strong><br/>API Framework</td>
<td align="center"><strong>Python</strong><br/>Runtime</td>
</tr>
</table>

---

<div align="center">

```
═══════════════════════════════════════════════════════════════════════════════
                         ⛧ BUILT FOR THE COHERE ECOSYSTEM ⛧
═══════════════════════════════════════════════════════════════════════════════
```

**MIT License**

*Language is no barrier. Knowledge flows through all tongues.*

</div>
