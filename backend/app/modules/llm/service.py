from app.modules.llm.schemas import (
    LLMRequest,
    LLMResponse,
)


class LLMService:

    def generate_answer(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        raise NotImplementedError