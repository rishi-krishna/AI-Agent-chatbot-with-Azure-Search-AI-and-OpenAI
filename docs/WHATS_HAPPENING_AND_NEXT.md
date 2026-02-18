# What’s Happening (Theory + Technical) and What to Do Next

This doc explains **why** each step exists, **what** happens technically, and **what to run** next.

---

## Big picture: RAG (Retrieval-Augmented Generation)

**The goal:** Answer user questions using **only** your approved COO help content, and show **where** each part of the answer came from (citations).

**The idea:**  
Instead of the LLM relying only on its training data (which doesn’t know your COO app), we:

1. **Store** your help docs in a searchable form (chunks + vectors).
2. **At question time:** find the most relevant chunks → send them to the LLM as context → the LLM answers **from that context** and we attach **citations** (which chunk/source it came from).

So: **Retrieval** (get the right chunks) + **Augmented** (add them to the prompt) + **Generation** (LLM writes the answer). That’s RAG.

---

## End-to-end flow (theory → technical)

### When a user asks a question in the chat

| Step | What happens in theory | What happens technically |
|------|------------------------|---------------------------|
| 1. User types | User asks e.g. “How do I approve requests?” | Angular app sends `POST /chat` with `{ "message": "..." }` to your API. |
| 2. Embed the question | Turn the question into a “meaning vector” so we can compare it to stored chunks. | API calls **Azure OpenAI** (embedding model) with the question text → gets a list of 1536 numbers (the vector). |
| 3. Search the index | Find the help chunks whose “meaning” is closest to the question. | API sends that vector to **Azure AI Search** (vector search). Search returns the top‑k chunks (e.g. 5) with metadata (source_file, content, etc.). |
| 4. Build the prompt | Give the LLM the question plus the retrieved chunks so it can answer from them. | API concatenates the chunks into a string (context), then builds a system + user message: “Answer using this context: …” + “User asked: …”. |
| 5. Generate the answer | LLM produces a short, on-topic answer and (ideally) sticks to the context. | API calls **Azure OpenAI** (chat model, e.g. gpt-4o) with that prompt → gets back the reply text. |
| 6. Return answer + citations | User sees the answer and which help doc/section it came from. | API returns `{ "reply": "...", "citations": [ { "source_file", "source_title", "content_snippet" }, ... ] }`. Angular displays the reply and the citation list. |

So: **Angular → API → (embed query → Azure AI Search) + (context + query → Azure OpenAI chat) → API → Angular** with citations.

---

## What each “setup” step does (theory + technical)

You run these **once** (or when you change help content or index).

---

### Step 1: Create the search index

**Theory:**  
Azure AI Search doesn’t know what “fields” your documents have. We have to define an **index**: a schema (which fields exist and whether they’re text, numbers, or vectors). The index is empty at first; we’ll fill it in the next step.

**Technical:**  
- Script: `indexing/scripts/create_search_index.py`.  
- It reads `.env` (Azure Search endpoint + API key).  
- It calls the **Azure AI Search REST API** (via `SearchIndexClient`) to create or update an index named e.g. `coo-help-chunks` with:
  - `id` (key), `content` (searchable text), `source_file`, `source_title`, `start_line`, `end_line`, and **`content_vector`** (a vector of 1536 floats for semantic search).  
- No data is uploaded yet; only the “table structure” is created.

**What to run:**  
From `indexing/` (with venv active):

```powershell
python scripts\create_search_index.py
```

---

### Step 2: Index the help content (chunk → embed → upload)

**Theory:**  
We need to turn your Markdown help files into **searchable chunks** and store them in Azure AI Search.  
- **Chunking:** Long docs are split into smaller pieces (by headings and size) so that each chunk is a coherent unit and fits model limits.  
- **Embedding:** Each chunk is converted into a **vector** (numbers that represent meaning). Similar text → similar vectors, so we can later find “chunks similar to the user’s question.”  
- **Upload:** Those chunks (text + metadata + vector) are sent to Azure AI Search and stored in the index we created.

**Technical:**  
- Script: `indexing/run_indexing.py`.  
- **Chunker:** Reads all `.md` files from `help-pack/` (except README), splits by headers and by size (~800 chars, 100 overlap), outputs `Chunk` objects (content, source_file, source_title, line range).  
- **Embedder:** Sends each batch of chunk texts to **Azure OpenAI** (embedding deployment, e.g. `text-embedding-ada-002`) → gets back one vector per chunk (length 1536).  
- **Upload:** Uses `SearchClient.upload_documents()` to push to Azure AI Search. Each document has `id`, `content`, `source_file`, `source_title`, `start_line`, `end_line`, `content_vector`.  
- After this, the index is **filled**; the API can run vector search on it.

**What to run:**  
Same terminal, same venv:

```powershell
python run_indexing.py
```

---

### Step 3: Start the AI Gateway API

**Theory:**  
The API is the **backend** that: (1) takes the user message, (2) retrieves relevant chunks (RAG retrieval), (3) calls the LLM with that context (augmented generation), (4) returns the answer and citations. The Angular app only talks to this API; it never talks to Azure directly.

**Technical:**  
- App: FastAPI in `api/app/main.py`.  
- **POST /chat:** Receives `{ "message": "..." }`.  
- **Retrieval:** `retrieval.py` gets embedding for the message (Azure OpenAI), then calls Azure AI Search **vector search** with that embedding, gets top‑k chunks.  
- **Chat:** `chat.py` builds a prompt with system instructions (“answer only from this context…”) + the retrieved chunks + the user message, then calls Azure OpenAI **chat** (e.g. gpt-4o).  
- Response: `{ "reply": "...", "citations": [ ... ] }`.  
- CORS is enabled so the Angular app (different port) can call the API.

**What to run:**  
New terminal, from project:

```powershell
cd api
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Keep it running. Check: open **http://localhost:8000/health** → `{"status":"ok"}`.

---

### Step 4: Start the Angular chat UI

**Theory:**  
The UI is the **frontend** the user sees. It sends the user’s message to the API and displays the reply and citations. It doesn’t do RAG or LLM itself; it’s a client to your API.

**Technical:**  
- App: Angular in `frontend/`.  
- **CoochatService:** Calls `POST {apiBaseUrl}/chat` with the message. `apiBaseUrl` is in `environment.ts` (e.g. `http://localhost:8000` for dev).  
- **ChatComponent:** Input box and “Send” → calls the service → shows user message, then assistant message + list of citations (source title, file, snippet).  
- **Build/serve:** `npm start` runs the dev server and serves the app at **http://localhost:4200**.

**What to run:**  
Another terminal:

```powershell
cd frontend
npm install
npm start
```

Then open **http://localhost:4200** and use the chat.

---

## Order of operations (what to do next)

Do these in order:

1. **Create index** (once):  
   `python scripts\create_search_index.py` from `indexing/` with venv active and `.env` in project root.

2. **Index help content** (once, and again when you change `help-pack/`):  
   `python run_indexing.py` from `indexing/`.

3. **Start API** (leave running):  
   From `api/`: activate venv, `pip install -r requirements.txt`, `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

4. **Start UI** (leave running):  
   From `frontend/`: `npm install`, `npm start`, then open http://localhost:4200.

After that, when you type in the chat: **Browser → API → (embed + vector search + LLM) → API → Browser** with citations, as in the table at the top.

---

## Summary table

| Step | Theory | Technical |
|------|--------|-----------|
| Create index | Define the “shape” of stored documents (fields + vector). | `create_search_index.py` → Azure AI Search API → empty index created. |
| Run indexing | Turn help docs into searchable chunks + vectors and put them in the index. | Chunk Markdown → embed via Azure OpenAI → upload to Azure AI Search. |
| Start API | Backend that does retrieval + LLM and returns answer + citations. | FastAPI: embed query → vector search → build prompt → chat completion → return JSON. |
| Start UI | Let the user type and see answers + sources. | Angular calls API; displays messages and citations. |

This is the full picture of what’s happening theoretically and technically, and what to do next.
