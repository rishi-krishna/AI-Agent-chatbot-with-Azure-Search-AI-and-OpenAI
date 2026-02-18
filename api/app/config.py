from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure AI Search
    azure_search_endpoint: str = ""
    azure_search_index_name: str = "coo-help-chunks"
    azure_search_api_key: str = ""

    # Azure OpenAI
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_embedding_deployment: str = "text-embedding-ada-002"
    azure_openai_chat_deployment: str = "gpt-4o"

    # RAG
    top_k: int = 5
    citation_snippet_length: int = 200

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()
