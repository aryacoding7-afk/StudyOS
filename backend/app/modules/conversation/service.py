import json
import logging
from uuid import UUID

from app.modules.conversation.schemas import ConversationMessage
from app.utils.redis import redis_client

logger = logging.getLogger(__name__)


class ConversationService:

    PREFIX = "conversation"
    TTL = 60 * 60 * 24 * 7  # 7 days

    def _get_key(
        self,
        conversation_id: UUID,
    ) -> str:
        return f"{self.PREFIX}:{conversation_id}"

    def get_history(
        self,
        conversation_id: UUID,
    ) -> list[ConversationMessage]:

        try:
            history = redis_client.get(
                self._get_key(conversation_id)
            )

            if history is None:
                return []

            messages = json.loads(history)

            return [
                ConversationMessage(**message)
                for message in messages
            ]

        except Exception:
            logger.exception(
                "Failed to retrieve conversation history for %s",
                conversation_id,
            )
            raise

    def append_message(
        self,
        conversation_id: UUID,
        message: ConversationMessage,
    ) -> None:

        try:
            key = self._get_key(conversation_id)

            history = redis_client.get(key)

            if history is None:
                messages = []
            else:
                messages = json.loads(history)

            messages.append(
                message.model_dump()
            )

            redis_client.set(
                key,
                json.dumps(messages),
                ex=self.TTL,
            )

        except Exception:
            logger.exception(
                "Failed to append message to conversation %s",
                conversation_id,
            )
            raise

    def clear(
        self,
        conversation_id: UUID,
    ) -> None:

        try:
            redis_client.delete(
                self._get_key(conversation_id)
            )

        except Exception:
            logger.exception(
                "Failed to clear conversation %s",
                conversation_id,
            )
            raise