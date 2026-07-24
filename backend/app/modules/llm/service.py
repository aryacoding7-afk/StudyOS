import logging

from google.genai import types

from app.core.config import settings
from app.core.exceptions import LLMGenerationException
from app.modules.llm.prompts import build_prompt
from app.modules.llm.schemas import (
    LLMRequest,
    LLMResponse,
)
from app.utils.gemini import get_gemini_client

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service responsible for interacting with the Gemini LLM.
    """

    def generate_answer(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        try:
            prompt = build_prompt(
                question=request.question,
                context=request.context,
                conversation_history=request.conversation_history,
            )

            logger.info(
                "Generating AI response using Gemini model '%s'",
                settings.LLM_MODEL,
            )

            # Lazily initialize the Gemini client
            client = get_gemini_client()

            response = client.models.generate_content(
                model=settings.LLM_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=settings.TEMPERATURE,
                    max_output_tokens=settings.MAX_OUTPUT_TOKENS,
                ),
            )

            logger.info(
                "Gemini response generated successfully"
            )

            return LLMResponse(
                answer=response.text,
            )

        except Exception:
            logger.exception(
                "Failed to generate AI response"
            )
            raise LLMGenerationException()