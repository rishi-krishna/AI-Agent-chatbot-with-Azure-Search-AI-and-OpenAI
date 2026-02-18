# COO Chat – RAG-Powered FAQ & Navigation Assistant

End-to-end flow:

```
User → Angular Chat → AI Gateway → Retrieval (Azure AI Search) → searchable chunks → LLM → answer with citations → UI
```

## Objectives

- Answer COO FAQs using approved help content.
- Guide users to the right screens in the COO application.
- Provide answers with **citations** from the help pack.

## Project Structure

```
Coochat_curser/
├── help-pack/              # Story 1: COO help documents (source for RAG)
├── indexing/               # Story 2: RAG indexing pipeline
├── api/                    # Story 3: AI Gateway API
├── frontend/               # Story 4: Angular chat UI
└── docs/                   # Architecture & runbooks
```

## Stories

| Story | Description |
|-------|-------------|
| **1. Build Help Pack** | Initial set of COO help documents used for RAG. |
| **2. RAG Indexing Pipeline** | Ingest docs → chunk → embed → load into Azure AI Search. |
| **3. AI Gateway API** | Backend: retrieval + LLM completion, returns answer + citations. |
| **4. Angular Chat UI** | Chat experience in the COO UI. |

## Quick Start

1. **Help content**: Add or edit markdown in `help-pack/`.
2. **Index**: Run the indexing pipeline (see `indexing/README.md`).
3. **API**: Configure env and run the AI Gateway (see `api/README.md`).
4. **UI**: Serve the Angular app and point it at the API (see `frontend/README.md`).

## Environment

- **Azure AI Search**: Vector index for chunks.
- **Azure OpenAI**: Embeddings and chat completion.
- **Backend**: Python 3.10+, FastAPI.
- **Frontend**: Angular 17+, Node 18+.

See `docs/setup.md` for Azure and local setup.
