from google import genai

from app.core.config import settings
from app.utils.gemini import get_gemini_client


def validate_model() -> None:
    """
    Ensure the configured Gemini model exists and
    supports generate_content().
    """

    configured = f"models/{settings.LLM_MODEL}"

    client = get_gemini_client()

    available = {
        model.name
        for model in client.models.list()
    }

    if configured not in available:
        raise RuntimeError(
            f"""
Configured Gemini model '{settings.LLM_MODEL}' is unavailable.

Please update LLM_MODEL in your .env.

Available models include:

{chr(10).join(sorted(list(available))[:15])}
"""
        )