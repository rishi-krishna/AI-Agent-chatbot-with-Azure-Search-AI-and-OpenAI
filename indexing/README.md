# RAG Indexing Pipeline (Story 2)

Ingests help-pack documents, chunks them, generates embeddings with Azure OpenAI, and loads vectors into Azure AI Search.

## Flow

```
help-pack/*.md → read & parse → chunk (overlap) → embed (Azure OpenAI) → upload to Azure AI Search
```

## Prerequisites

- Python 3.10+
- Azure AI Search service (with a vector index)
- Azure OpenAI (embedding model, e.g. `text-embedding-ada-002` or `text-embedding-3-small`)

## Environment variables

Create `.env` in project root or set:

- `AZURE_SEARCH_ENDPOINT` – Azure AI Search URL
- `AZURE_SEARCH_INDEX_NAME` – Index name (e.g. `coo-help-chunks`)
- `AZURE_SEARCH_API_KEY` – Search API key
- `AZURE_OPENAI_ENDPOINT` – Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY` – OpenAI API key
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` – Embedding deployment name

## Usage

```bash
cd indexing
pip install -r requirements.txt
python run_indexing.py
```

Optional: `--help-pack ../help-pack` to override the help pack path.

## Index schema

The pipeline expects an index with at least:

- `id` (Edm.String, key)
- `content` (Edm.String) – chunk text
- `source_file` (Edm.String) – e.g. `approvals.md`
- `source_title` (Edm.String) – first H1 from the doc
- `content_vector` (Collection(Edm.Single)) – embedding vector

Use `scripts/create_search_index.py` to create the index if needed.
