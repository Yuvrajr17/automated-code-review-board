import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv()


def create_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Please check your backend/.env file."
        )

    return OpenAIChatCompletionClient(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        model=model,
    )