from functools import lru_cache

from google import genai

from app.core.config import settings


@lru_cache
def get_gemini_client() -> genai.Client:
    """
    Lazily create and cache the Gemini client.

    The client is created only the first time it is needed
    and reused for the lifetime of the application.
    """
    return genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )