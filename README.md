# Semantic Search RAG

A production-oriented Retrieval-Augmented Generation (RAG) system built with Python, PostgreSQL, FAISS, Sentence Transformers, and Groq LLMs.

The project ingests documents from multiple formats, generates semantic embeddings, stores vectors in FAISS, stores metadata in PostgreSQL, retrieves relevant context using vector similarity search, and generates grounded responses using a Large Language Model.

---

# Features

- Multi-format document ingestion
  - PDF
  - DOCX
  - TXT
  - Markdown
  - CSV
  - Local HTML
  - Remote HTML (URL)

- Semantic chunking

- Sentence Transformer embeddings

- FAISS vector search

- PostgreSQL metadata storage

- Retrieval-Augmented Generation (RAG)

- Groq LLM integration

- CLI interface

- FastAPI support

- Production-ready modular architecture

---

# Architecture

```
                Documents
                     │
     ┌───────────────┼───────────────┐
     │               │               │
   PDF            DOCX            HTML
     │               │               │
     └───────────────┼───────────────┘
                     │
             Document Loader
                     │
             Ingestor Factory
                     │
           Format-specific Ingestors
                     │
             Text Normalization
                     │
              Semantic Chunking
                     │
          SentenceTransformer
                     │
          Embedding Generation
                     │
        ┌────────────┴─────────────┐
        │                          │
     PostgreSQL                 FAISS
  (metadata store)          (vector store)
        │                          │
        └────────────┬─────────────┘
                     │
                 Retriever
                     │
             Prompt Builder
                     │
                 Groq LLM
                     │
                  Response
```

---

# Project Structure

```
project_semantic_search/

├── src/
│   ├── api/
│   ├── chunking/
│   ├── cli/
│   ├── config/
│   ├── database/
│   ├── domain/
│   ├── embeddings/
│   ├── generation/
│   ├── ingestion/
│   ├── retrieval/
│   ├── services/
│   ├── utils/
│   └── vectorstore/
│
├── tests/
│
├── scripts/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── vector_store/
│
├── requirements.txt
├── pyproject.toml
├── README.md
└── .env.example
```

---

# Technologies

| Category     | Technology            |
| ------------ | --------------------- |
| Language     | Python 3.12+          |
| API          | FastAPI               |
| CLI          | Typer                 |
| Database     | PostgreSQL            |
| Vector Store | FAISS                 |
| Embeddings   | Sentence Transformers |
| LLM          | Groq                  |
| ORM          | SQLAlchemy            |
| Migrations   | Alembic               |
| PDF          | PyMuPDF               |
| DOCX         | python-docx           |
| HTML         | lxml                  |
| CSV          | pandas                |

---

# Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/project_semantic_search.git

cd project_semantic_search
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -e .
```

---

# Configuration

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/semantic_search

GROQ_API_KEY=your_api_key

GROQ_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

FAISS_INDEX_PATH=data/vector_store/faiss.index

FAISS_METADATA_PATH=data/vector_store/metadata.json

CHUNK_SIZE=500

CHUNK_OVERLAP=100
```

---

# Ingest Documents

Place your documents inside

```
data/raw/
```

Run

```bash
semantic-search ingest
```

Example output

```
Successfully ingested 10 documents.
```

---

# Query

```bash
semantic-search query "What is gradient descent?"
```

or

```bash
semantic-search query "Explain the SajiloMart architecture."
```

---

# Supported File Types

| Type        | Supported |
| ----------- | --------- |
| PDF         | ✅        |
| DOCX        | ✅        |
| TXT         | ✅        |
| Markdown    | ✅        |
| CSV         | ✅        |
| HTML        | ✅        |
| Remote HTML | ✅        |

---

# Retrieval Pipeline

1. User asks a question.

2. Query embedding is generated.

3. FAISS retrieves top-K semantic matches.

4. Metadata is fetched from PostgreSQL.

5. PromptBuilder creates grounded context.

6. Groq generates the final answer.

---

# Development Roadmap

## Completed

- Multi-format ingestion

- FAISS integration

- PostgreSQL integration

- Semantic chunking

- Embedding generation

- Retriever

- Prompt Builder

- Groq integration

- CLI

- FastAPI support

---

## Planned

- Hybrid Search (BM25 + FAISS)

- Query Expansion

- Query Rewriting

- Cross Encoder Reranking

- Metadata Filtering

- Incremental Index Updates

- Multi-user Collections

- Streaming Responses

- Evaluation Pipeline

- Web Interface

- Docker Deployment

- Kubernetes Deployment

---

# Example Workflow

```
Documents

↓

Ingestion

↓

Chunking

↓

Embeddings

↓

FAISS

↓

Question

↓

Retriever

↓

Prompt Builder

↓

Groq

↓

Answer
```

---

# Testing

Run

```bash
python -m tests.test_ingestion

python -m tests.test_retriever

python -m tests.test_api
```

---

# Future Improvements

- Hybrid Retrieval

- Agentic RAG

- Knowledge Graph Integration

- Parent-Child Retrieval

- Context Compression

- Semantic Caching

- Conversation Memory

- OCR Support

- Image Embeddings

- Multi-modal RAG

---

# License

MIT License

---

# Author

Sanjaya Chaudhary

---

# Acknowledgements

- FastAPI
- FAISS
- PostgreSQL
- Sentence Transformers
- Hugging Face
- Groq
- SQLAlchemy
