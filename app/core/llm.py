from openai import AsyncOpenAI
from app.core.settings import get_settings

settings = get_settings()

def get_openai_client() -> AsyncOpenAI:
    api_key = settings.OPENAI_API_KEY
    if api_key.startswith("gsk_"):
        # Groq Configuration
        return AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
    return AsyncOpenAI(api_key=api_key)

def get_model_name() -> str:
    """Returns the appropriate model based on the API Key provider."""
    if settings.OPENAI_API_KEY.startswith("gsk_"):
        return "llama-3.3-70b-versatile" # Groq current flagship (Dec 2025)
    return "gpt-4o"
