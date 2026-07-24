import logging

from sqlalchemy.orm import Session

from app.modules.chat.context_builder import build_context
from app.modules.chat.schemas import (
    ChatRequest,
    ChatResponse,
)
from app.modules.chat.source_builder import build_sources
from app.modules.conversation.schemas import ConversationMessage
from app.modules.conversation.service import ConversationService
from app.modules.llm.schemas import LLMRequest
from app.modules.llm.service import LLMService
from app.modules.search.schemas import SearchRequest
from app.modules.search.service import SearchService

logger = logging.getLogger(__name__)


class ChatService:

    def __init__(self, db: Session):
        self.search_service = SearchService(db)
        self.llm_service = LLMService()
        self.conversation_service = ConversationService()

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        logger.info(
            "Starting chat request for conversation %s and document %s",
            request.conversation_id,
            request.document_id,
        )

        try:
            # Load conversation history
            history = self.conversation_service.get_history(
                request.conversation_id
            )

            logger.info(
                "Loaded %d conversation messages",
                len(history),
            )

            history_text = "\n".join(
                f"{message.role.capitalize()}: {message.content}"
                for message in history
            )

            # Retrieve relevant chunks
            search_response = self.search_service.search(
                SearchRequest(
                    document_id=request.document_id,
                    query=request.question,
                )
            )

            logger.info(
                "Semantic search returned %d chunks",
                len(search_response.results),
            )

            # Build LLM context
            context = build_context(search_response)

            logger.info(
                "Built context (%d characters)",
                len(context),
            )

            # Generate AI response
            llm_response = self.llm_service.generate_answer(
                LLMRequest(
                    question=request.question,
                    context=context,
                    conversation_history=history_text,
                )
            )

            logger.info(
                "LLM response generated successfully",
            )

            # Save user message
            self.conversation_service.append_message(
                request.conversation_id,
                ConversationMessage(
                    role="user",
                    content=request.question,
                ),
            )

            # Save assistant message
            self.conversation_service.append_message(
                request.conversation_id,
                ConversationMessage(
                    role="assistant",
                    content=llm_response.answer,
                ),
            )

            logger.info(
                "Conversation history updated",
            )

            response = ChatResponse(
                answer=llm_response.answer,
                sources=build_sources(search_response),
            )

            logger.info(
                "Chat request completed successfully",
            )

            return response

        except Exception:
            logger.exception(
                "Chat request failed for conversation %s",
                request.conversation_id,
            )
            raise