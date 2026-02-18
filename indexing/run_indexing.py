"""
Run the RAG indexing pipeline: help-pack → chunk → embed → Azure AI Search.
"""
import os
import uuid
import argparse
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root so one file works for indexing and API
_load_env = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_load_env)

from chunker import chunk_help_pack, Chunk
from embedder import get_embedding_client, embed_chunks

# Azure Search
try:
    from azure.search.documents import SearchClient
    from azure.core.credentials import AzureKeyCredential
except ImportError:
    SearchClient = None
    AzureKeyCredential = None


def get_search_client():
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    key = os.environ["AZURE_SEARCH_API_KEY"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    if not SearchClient:
        raise ImportError("Install azure-search-documents: pip install azure-search-documents")
    return SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))


def upload_chunks(search_client, chunks: list[Chunk], vectors: list[list[float]]):
    """Upload chunk documents with vectors to Azure AI Search."""
    documents = []
    for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
        documents.append({
            "id": str(uuid.uuid4()),
            "content": chunk.content,
            "source_file": chunk.source_file,
            "source_title": chunk.source_title,
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "content_vector": vec,
        })
    # Upload in batches of 100
    batch_size = 100
    for j in range(0, len(documents), batch_size):
        batch = documents[j : j + batch_size]
        result = search_client.upload_documents(documents=batch)
        failed = [r for r in result if not r.succeeded]
        if failed:
            print(f"WARNING: {len(failed)} documents failed to upload")
    print(f"Uploaded {len(documents)} chunks to Azure AI Search.")


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Index help-pack into Azure AI Search")
    parser.add_argument("--help-pack", type=Path, default=Path(__file__).resolve().parent.parent / "help-pack")
    args = parser.parse_args()

    help_pack = args.help_pack
    if not help_pack.is_dir():
        print(f"Help pack path is not a directory: {help_pack}")
        return 1

    chunks = list(chunk_help_pack(help_pack))
    print(f"Chunked {len(chunks)} chunks from {help_pack}")

    deployment = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    client = get_embedding_client()
    vectors = embed_chunks(client, chunks, deployment)
    print(f"Generated {len(vectors)} embeddings")

    search_client = get_search_client()
    upload_chunks(search_client, chunks, vectors)
    print("Indexing complete.")
    return 0


if __name__ == "__main__":
    exit(main())
