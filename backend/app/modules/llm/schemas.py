from pydantic import BaseModel


class LLMRequest(BaseModel):
    question: str
    context: str
    conversation_history: str = ""

class LLMResponse(BaseModel):
    answer: str