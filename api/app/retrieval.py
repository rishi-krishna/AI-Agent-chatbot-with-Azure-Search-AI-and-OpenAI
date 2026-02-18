"""
Retrieve relevant help chunks from Azure AI Search using vector search.
"""
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

from app.config import Settings


def get_embedding(settings: Settings, query: str) -> list[float]:
    client = AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=settings.azure_openai_endpoint,
    )
    resp = client.embeddings.create(
        input=query,
        model=settings.azure_openai_embedding_deployment,
    )
    return resp.data[0].embedding


def search_chunks(settings: Settings, query: str) -> list[dict]:
    """
    Vector search; returns list of dicts with keys:
    content, source_file, source_title, start_line, end_line, relevance_score.
    """
    vector = get_embedding(settings, query)
    search_client = SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_api_key),
    )
    vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=settings.top_k, fields="content_vector")
    results = search_client.search(search_text=None, vector_queries=[vector_query], select=["content", "source_file", "source_title", "start_line", "end_line"])
    out = []
    for r in results:
        out.append({
            "content": r["content"],
            "source_file": r.get("source_file", ""),
            "source_title": r.get("source_title", ""),
            "start_line": r.get("start_line", 0),
            "end_line": r.get("end_line", 0),
            "relevance_score": getattr(r, "@search.score", None),
        })
    return out
