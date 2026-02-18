# COO Chat – Setup Guide

## Azure resources

1. **Azure AI Search**
   - Create a search service in Azure Portal.
   - Note: **Endpoint** (e.g. `https://<name>.search.windows.net`) and **Admin key**.
   - Create the index (run `indexing/scripts/create_search_index.py` once) or use the index creation script.

2. **Azure OpenAI**
   - Create an OpenAI resource and deploy:
     - An **embedding** model (e.g. `text-embedding-ada-002` or `text-embedding-3-small`).
     - A **chat** model (e.g. `gpt-4o` or `gpt-4o-mini`).
   - Note: **Endpoint**, **API key**, and **deployment names**.

## Local development

### 1. Help pack (Story 1)

- Edit or add Markdown files in `help-pack/`.
- See `help-pack/README.md` for conventions.

### 2. Indexing (Story 2)

```bash
cd indexing
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create `.env` in project root (or in `indexing/`):

```
AZURE_SEARCH_ENDPOINT=https://<your-search>.search.windows.net
AZURE_SEARCH_INDEX_NAME=coo-help-chunks
AZURE_SEARCH_API_KEY=<key>

AZURE_OPENAI_ENDPOINT=https://<your-openai>.openai.azure.com/
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

Create the index (first time only):

```bash
python scripts/create_search_index.py
```

Run indexing:

```bash
python run_indexing.py
```

### 3. AI Gateway API (Story 3)

```bash
cd api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set the same variables as above, plus:

```
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
```

Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Angular Chat UI (Story 4)

```bash
cd frontend
npm install
npm start
```

Open `http://localhost:4200`. Set `apiBaseUrl` in `src/environments/environment.ts` to `http://localhost:8000` so the UI calls the local API.

## End-to-end flow

1. User types in Angular chat.
2. Frontend sends `POST /chat` with `{ "message": "..." }`.
3. API embeds the query, runs vector search on Azure AI Search, then calls Azure OpenAI with retrieved chunks.
4. API returns `{ "reply": "...", "citations": [...] }`.
5. UI shows the reply and citation sources.

## Production notes

- Use HTTPS and set CORS `allow_origins` in the API to your COO app origin.
- Set `apiBaseUrl` in Angular to the deployed API URL (e.g. `https://api.yourcoo.com`).
- Keep Azure keys in secure config (e.g. Key Vault, app settings); never commit `.env`.
