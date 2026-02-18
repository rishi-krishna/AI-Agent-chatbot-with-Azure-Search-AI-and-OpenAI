"""
Generate embeddings via Azure OpenAI.
"""
import os
from openai import AzureOpenAI
from chunker import Chunk


def get_embedding_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    key = os.environ.get("AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_OPENAI_KEY")
    if not key:
        raise ValueError("Set AZURE_OPENAI_API_KEY or AZURE_OPENAI_KEY")
    return AzureOpenAI(api_key=key, api_version="2024-02-15-preview", azure_endpoint=endpoint)


def embed_chunks(client: AzureOpenAI, chunks: list[Chunk], deployment: str) -> list[list[float]]:
    """Embed a list of chunks; returns list of vectors. deployment = exact name from Azure OpenAI Studio."""
    if not chunks:
        return []
    texts = [c.content for c in chunks]
    try:
        resp = client.embeddings.create(input=texts, model=deployment)
    except Exception as e:
        if "DeploymentNotFound" in str(e) or "404" in str(e):
            raise SystemExit(
                f"Embedding deployment '{deployment}' not found. In Azure OpenAI Studio, open the same resource as AZURE_OPENAI_ENDPOINT → Deployments → copy the exact deployment name for the embedding model into .env as AZURE_OPENAI_EMBEDDING_DEPLOYMENT."
            ) from e
        raise
    return [item.embedding for item in resp.data]
