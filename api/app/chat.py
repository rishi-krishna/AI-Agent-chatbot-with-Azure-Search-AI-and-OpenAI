"""
Build prompt from retrieved chunks and call Azure OpenAI chat; return reply text.
"""
from openai import AzureOpenAI

from app.config import Settings


SYSTEM_PROMPT = """You are a helpful assistant for the COO (Chief Operating Office) application. Answer only using the provided help content. If the answer is not in the context, say so and suggest using the in-app navigation or contacting support. When guiding users to a screen, mention the exact menu path (e.g. "Go to Approvals in the main menu" or "Reports → Report Library"). Keep answers concise and cite the source document when relevant."""


def build_messages(context: str, user_message: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\nRelevant help content:\n\n" + context},
        {"role": "user", "content": user_message},
    ]


def chat_with_context(settings: Settings, context: str, user_message: str) -> str:
    client = AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=settings.azure_openai_endpoint,
    )
    messages = build_messages(context, user_message)
    resp = client.chat.completions.create(
        model=settings.azure_openai_chat_deployment,
        messages=messages,
        max_tokens=1024,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""
