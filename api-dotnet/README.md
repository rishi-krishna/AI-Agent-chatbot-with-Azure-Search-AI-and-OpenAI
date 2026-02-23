# COO Chat .NET Backend (ASP.NET Core)

This folder contains a .NET Core backend with the same API contract and behavior as the Python backend in `../api`.

## Endpoints

- `GET /health` -> `{ "status": "ok" }`
- `POST /chat` -> returns:
  - `reply`
  - `citations[]` with `source_file`, `source_title`, `content_snippet`, `relevance_score`

Request body:

```json
{ "message": "How do I approve requests?" }
```

## Functional Parity with Python Backend

- Query embedding via Azure OpenAI embeddings deployment.
- Vector retrieval from Azure AI Search (`content_vector`).
- Prompt + chat completion via Azure OpenAI chat deployment.
- Same fallback behavior when no context is found.
- Same response shape expected by existing Angular frontend (no frontend changes required).

## Configuration

Primary config is in `appsettings.json` under `CooChat`.
The app also auto-loads `../.env` (same root `.env` used by your Python services) and uses those values when present.

You can override with environment variables:

- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_INDEX_NAME`
- `AZURE_SEARCH_API_KEY`
- `AZURE_SEARCH_API_VERSION`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`
- `AZURE_OPENAI_CHAT_DEPLOYMENT`
- `AZURE_SEARCH_TOP_K`
- `CITATION_SNIPPET_LENGTH`
- `CORS_ORIGINS` (comma-separated)

## Run (after installing .NET SDK)

```bash
cd api-dotnet
dotnet restore
dotnet run
```

Default local URL is usually `http://localhost:5000` or `https://localhost:5001`.

## Notes

- This machine currently does not have `dotnet` installed, so this backend was created but not compiled/tested locally here.
- Install .NET 8 SDK before running build tests.
