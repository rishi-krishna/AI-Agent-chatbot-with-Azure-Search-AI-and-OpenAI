# AI Gateway API (Story 3)

Backend that performs **retrieval** (Azure AI Search) + **LLM completion** (Azure OpenAI) and returns an answer with **citations**.

## Endpoints

- `POST /chat` – Send a user message; receive assistant reply and citations.

## Request / Response

**POST /chat**

```json
// Request
{ "message": "How do I approve requests?" }

// Response
{
  "reply": "To approve requests, go to Approvals...",
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

## Environment

- `AZURE_SEARCH_*` – Same as indexing.
- `AZURE_OPENAI_*` – Plus `AZURE_OPENAI_CHAT_DEPLOYMENT` for the chat model.

## Run

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Default: `http://localhost:8000`. OpenAPI: `http://localhost:8000/docs`.
