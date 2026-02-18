# COO Chat – Setup and Run (Step-by-Step)

Follow these steps in order. You need **Azure** (AI Search + OpenAI) and **your machine** (Python, Node, terminal).

---

## Part A: What You Need

### 1. On your PC
- **Python 3.10+** – [python.org](https://www.python.org/downloads/)
- **Node.js 18+** – [nodejs.org](https://nodejs.org/)
- **Terminal** – PowerShell or Command Prompt

### 2. In Azure (Portal: [portal.azure.com](https://portal.azure.com))

You will create **two** resources and collect **URLs and keys** for the `.env` file.

| Resource | What to create | What to note |
|----------|----------------|--------------|
| **Azure AI Search** | Create resource → “AI + Machine Learning” → “Azure AI Search”. Pick name, region, tier. | **Endpoint** (e.g. `https://myservice.search.windows.net`) and **Keys** → “Admin key” |
| **Azure OpenAI** | Create resource → “AI + Machine Learning” → “Azure OpenAI”. Same subscription/region. | **Endpoint** (e.g. `https://myopenai.openai.azure.com/`) and **Keys** → “Key 1” |

Then in your **Azure OpenAI** resource:

- Go to **Model deployments** (or “Azure OpenAI Studio” → Deployments).
- **Create two deployments** (if you don’t have them):
  - **Embedding**: Model `text-embedding-ada-002` (or `text-embedding-3-small`). Note the **deployment name** (e.g. `text-embedding-ada-002`).
  - **Chat**: Model `gpt-4o` (recommended) or `gpt-4o-mini`. Note the **deployment name** (e.g. `gpt-4o`).

You’ll need: **Search endpoint**, **Search API key**, **OpenAI endpoint**, **OpenAI API key**, **embedding deployment name**, **chat deployment name**.

---

## Part B: One `.env` File (Project Root)

All commands assume the project root is:

`c:\Users\rishi\Desktop\work and study\AI_Project\Coochat_curser`

1. In that folder, copy the example env file and open it:
   - Copy `.env.example` → `.env`
   - Edit `.env` in a text editor.

2. Fill in **your** values (no quotes, no spaces around `=`):

```env
# Azure AI Search – from Azure Portal → your Search resource → Overview + Keys
AZURE_SEARCH_ENDPOINT=https://YOUR-SEARCH-NAME.search.windows.net
AZURE_SEARCH_INDEX_NAME=coo-help-chunks
AZURE_SEARCH_API_KEY=paste-your-search-admin-key-here

# Azure OpenAI – from Azure Portal → your OpenAI resource → Overview + Keys
AZURE_OPENAI_ENDPOINT=https://YOUR-OPENAI-NAME.openai.azure.com/
AZURE_OPENAI_API_KEY=paste-your-openai-key-here
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
```

- Replace `YOUR-SEARCH-NAME` and `YOUR-OPENAI-NAME` with your actual resource names.
- If your embedding or chat deployment has a **different name**, change `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` and `AZURE_OPENAI_CHAT_DEPLOYMENT` to match.

3. Save `.env`. **Do not commit this file** (it’s secrets).

---

## Part C: Run Everything (In This Order)

Open a terminal. All paths are from the **project root** above.

---

### Step 1: Create the search index (once per environment)

This creates the vector index in Azure AI Search. Run it **once** before the first indexing.

```powershell
cd "c:\Users\rishi\Desktop\work and study\AI_Project\Coochat_curser\indexing"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\create_search_index.py
```

**Expected:** Message like `Index 'coo-help-chunks' created or updated.`

**If it fails:** Check that `.env` is in the **project root** (parent of `indexing`), and that `AZURE_SEARCH_*` and `AZURE_OPENAI_*` are correct.

---

### Step 2: Index the help content (run after changing help-pack)

This chunks the Markdown in `help-pack/`, embeds it, and uploads to Azure AI Search.

```powershell
# Same folder as Step 1; venv still active
python run_indexing.py
```

**Expected:** Lines like:
- `Chunked N chunks from ...\help-pack`
- `Generated N embeddings`
- `Uploaded N chunks to Azure AI Search.`
- `Indexing complete.`

**If it fails:** Check `.env` again, and that your OpenAI embedding deployment name is correct.

---

### Step 3: Start the AI Gateway API

This is the backend that does retrieval + LLM and returns the answer with citations.

**New terminal** (or deactivate the previous venv and reuse):

```powershell
cd "c:\Users\rishi\Desktop\work and study\AI_Project\Coochat_curser\api"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Note:** You must run `python -m venv .venv` first (creates the venv). Only then does `.\.venv\Scripts\Activate.ps1` work. If you see "Activate.ps1 not recognized", the `api` folder has no `.venv` yet—create it with the first line above.

**Expected:**  
`Uvicorn running on http://0.0.0.0:8000`

- Leave this running.
- Test: open in browser **http://localhost:8000/health** → you should see `{"status":"ok"}`.
- API docs: **http://localhost:8000/docs**.

The API reads the **same `.env`** from the project root (via current directory when you start uvicorn from `api/` – if not, copy `.env` into `api/` or set env vars).

---

### Step 4: Start the Angular chat UI

This is the frontend that sends questions to the API and shows answers + citations.

**Another new terminal**:

```powershell
cd "c:\Users\rishi\Desktop\work and study\AI_Project\Coochat_curser\frontend"
npm install
npm start
```

**Expected:**  
`Application bundle generation complete` and something like `localhost:4200`.

- Open in browser: **http://localhost:4200**
- The app is already configured to call **http://localhost:8000** (the API) in development.

---

## Part D: Use the Chat

1. In the browser at **http://localhost:4200**, you should see the COO Help chat.
2. Type a question, e.g. **“How do I approve requests?”** or **“Where do I run reports?”**
3. Click **Send** (or press Enter).
4. You should get an answer and **Sources** (citations from the help-pack).

If you see “assistant is unavailable” or errors, check:
- API is still running on port 8000.
- **http://localhost:8000/health** returns `{"status":"ok"}`.
- Browser console (F12) for CORS or network errors.

---

## Quick Reference: What Runs Where

| What | Command | URL |
|------|---------|-----|
| Index (once) | `python scripts\create_search_index.py` from `indexing/` | – |
| Index content | `python run_indexing.py` from `indexing/` | – |
| API | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` from `api/` | http://localhost:8000 |
| Chat UI | `npm start` from `frontend/` | http://localhost:4200 |

---

## After Changing Help Content

When you add or edit files in `help-pack/`:

1. From `indexing/` (with venv active): run **`python run_indexing.py`** again.
2. No need to restart the API or the Angular app; the next chat request will use the updated index.

---

## Troubleshooting

- **“Retrieval failed” / “LLM failed”**  
  Check `.env` (Search + OpenAI URLs and keys, deployment names). Ensure the index was created and indexing has been run at least once.

- **“I couldn’t find relevant help content”**  
  Run indexing again; try rephrasing the question.

- **CORS errors in browser**  
  The API is set to allow all origins in development. If you still see CORS errors, confirm the request goes to `http://localhost:8000` and the API is running.

- **API can’t find .env**  
  Put `.env` in the project root and run uvicorn from the `api/` folder; or copy `.env` into `api/` and run from there.
