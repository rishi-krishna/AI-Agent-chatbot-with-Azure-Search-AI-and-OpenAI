# COO Chat - RAG FAQ and Navigation Assistant

COO Chat is a Retrieval-Augmented Generation (RAG) system that answers COO app questions using approved internal help content and returns citations for traceability.

## Goals

- Answer COO FAQs from internal documentation.
- Guide users to the right UI screen and menu path.
- Return source citations with each response.

## High-Level Architecture

```text
User (Angular UI)
  -> POST /chat (FastAPI)
    -> Embed query (Azure OpenAI embeddings)
    -> Vector search (Azure AI Search index)
    -> Build prompt with retrieved chunks
    -> Generate response (Azure OpenAI chat model)
  -> Return reply + citations
  -> Render in chat widget
```

## Repository Structure

```text
Coochat_curser/
  README.md
  .env
  help-pack/
    00-overview.md
    approvals.md
    navigation-and-settings.md
    reports-dashboard.md
  indexing/
    chunker.py
    embedder.py
    run_indexing.py
    scripts/create_search_index.py
  api/
    app/
      main.py
      config.py
      retrieval.py
      chat.py
    requirements.txt
  frontend/
    src/
      app/
        app.component.ts
        app.component.html
        app.component.css
        chat/
          chat.component.ts
          chat.component.html
          chat.component.css
          coochat.service.ts
          models.ts
      environments/
        environment.ts
        environment.prod.ts
  docs/
    setup and troubleshooting guides
```

## What Each Folder Does

### `help-pack/`
Business-owned source content used by the assistant.  
This is the source of truth for retrieval.

### `indexing/`
Offline data pipeline that transforms help docs into vector-searchable records.

- `scripts/create_search_index.py`: creates/updates Azure AI Search schema, including `content_vector`.
- `chunker.py`: splits markdown into manageable chunks with metadata.
- `embedder.py`: calls Azure OpenAI embeddings endpoint.
- `run_indexing.py`: orchestrates chunk -> embed -> upload.

### `api/`
Online runtime service (FastAPI) that powers chat.

- `main.py`: HTTP layer (`/chat`, `/health`) + response shaping.
- `retrieval.py`: query embedding + vector retrieval from Azure AI Search.
- `chat.py`: prompt construction + chat completion call.
- `config.py`: runtime settings used by API services.

### `frontend/`
Angular web app with a company-style page and bottom-right floating chatbot widget.

- `app.component.*`: company landing shell.
- `chat/chat.component.*`: chat widget UI/state management.
- `chat/coochat.service.ts`: HTTP client for backend `/chat`.
- `environments/*`: API base URL by environment.

### `docs/`
Setup guides, Azure setup docs, and troubleshooting notes.

## End-to-End Data Flow

### 1) Indexing Flow (offline, run when docs change)

1. Read markdown files from `help-pack/`.
2. Split into chunks with metadata (file, title, line ranges).
3. Generate embeddings for each chunk via Azure OpenAI.
4. Upload chunk records + vectors to Azure AI Search.

### 2) Chat Flow (online, per user request)

1. User sends a message from Angular widget.
2. Frontend calls `POST /chat`.
3. API embeds user query.
4. API performs vector KNN search in Azure AI Search.
5. API builds context from top chunks.
6. API calls chat model with system prompt + context + user question.
7. API returns `reply` and `citations`.
8. Frontend renders response and sources.

## API Contract

### `POST /chat`

Request:

```json
{ "message": "How do I approve requests?" }
```

Response:

```json
{
  "reply": "To approve requests, go to Approvals -> Pending ...",
  "citations": [
    {
      "source_file": "approvals.md",
      "source_title": "Approvals",
      "content_snippet": "...",
      "relevance_score": 0.89
    }
  ]
}
```

### `GET /health`

```json
{ "status": "ok" }
```

## Local Run Order

1. Configure Azure values (`.env` and/or runtime config as currently used).
2. Create index (first time only):

```bash
cd indexing
python scripts/create_search_index.py
```

3. Index content:

```bash
python run_indexing.py
```

4. Start API:

```bash
cd ../api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Start frontend:

```bash
cd ../frontend
npm install
npm start
```

6. Open `http://localhost:4200`.

## Updating Content

When files in `help-pack/` are changed:

1. Re-run `indexing/run_indexing.py`.
2. No code changes needed for API/UI.

## Tech Stack

- Frontend: Angular 17
- Backend: FastAPI (Python)
- Retrieval: Azure AI Search (vector index)
- Models: Azure OpenAI (embeddings + chat)

## Tools and Frameworks Used

### Languages

- Python
- TypeScript
- HTML/CSS
- Markdown

### Frontend

- Angular 17 (`@angular/core`, `@angular/common`, `@angular/forms`, `@angular/animations`)
- RxJS
- Zone.js
- Angular CLI and Angular DevKit
- TypeScript (`~5.4`)

### Backend API

- FastAPI
- Uvicorn (`uvicorn[standard]`)
- Pydantic
- Pydantic Settings
- python-dotenv

### RAG, AI, and Search

- Azure OpenAI (embeddings + chat completions)
- Azure AI Search (vector search)
- OpenAI Python SDK (`openai`)
- Azure Search SDK (`azure-search-documents`)
- Azure Identity SDK (`azure-identity`)

### Indexing Pipeline

- `indexing/chunker.py` for chunking
- `indexing/embedder.py` for embeddings
- `indexing/run_indexing.py` for orchestration
- `indexing/scripts/create_search_index.py` for index schema creation

### Infra and Runtime

- Python virtual environments (`.venv`)
- Node.js + npm
- Azure OpenAI resource
- Azure AI Search resource

## Notes

- Current local setup may use hardcoded values in `api/app/config.py` for convenience.
- For production, use secret-managed environment variables and key rotation.
