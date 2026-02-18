"""
Create Azure AI Search index for COO help chunks (vector + keyword).
Run once before first indexing. Requires azure-search-documents.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of indexing/)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

if not os.environ.get("AZURE_SEARCH_ENDPOINT"):
    print("ERROR: AZURE_SEARCH_ENDPOINT not set.")
    print(f"  Create a .env file at: {_env_path}")
    print("  Copy .env.example to .env and add your Azure AI Search endpoint and API key.")
    raise SystemExit(1)

try:
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SimpleField,
        SearchableField,
        SearchFieldDataType,
        SearchField,
        VectorSearch,
        HnswAlgorithmConfiguration,
        VectorSearchProfile,
    )
    from azure.core.credentials import AzureKeyCredential
except ImportError:
    print("Install: pip install azure-search-documents")
    raise

# Embedding dimension for text-embedding-ada-002 is 1536; for text-embedding-3-small often 1536
VECTOR_DIMENSION = 1536


def main():
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    key = os.environ["AZURE_SEARCH_API_KEY"]
    index_name = os.environ.get("AZURE_SEARCH_INDEX_NAME", "coo-help-chunks")

    client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    index = SearchIndex(
        name=index_name,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="source_file", type=SearchFieldDataType.String, filterable=True),
            SearchableField(name="source_title", type=SearchFieldDataType.String, filterable=True),
            SimpleField(name="start_line", type=SearchFieldDataType.Int32),
            SimpleField(name="end_line", type=SearchFieldDataType.Int32),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=VECTOR_DIMENSION,
                vector_search_profile_name="help-vector-profile",
            ),
        ],
        vector_search=VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
            profiles=[VectorSearchProfile(name="help-vector-profile", algorithm_configuration_name="hnsw")],
        ),
    )
    client.create_or_update_index(index)
    print(f"Index '{index_name}' created or updated.")


if __name__ == "__main__":
    main()
