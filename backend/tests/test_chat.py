from unittest.mock import patch
from uuid import uuid4
from app.modules.search.schemas import SearchResponse, SearchResult
from app.modules.llm.schemas import LLMResponse

API_PREFIX = "/api/v1"


@patch("app.modules.chat.service.ConversationService")
@patch("app.modules.chat.service.LLMService")
@patch("app.modules.chat.service.SearchService")
def test_chat_success(
    mock_search_cls,
    mock_llm_cls,
    mock_conversation_cls,
    client,
):
    search = mock_search_cls.return_value
    llm = mock_llm_cls.return_value
    conversation = mock_conversation_cls.return_value

    conversation.get_history.return_value = []

    search.search.return_value = SearchResponse(
        results=[
            SearchResult(
                chunk_index=0,
                page_number=1,
                content="StudyOS is an AI platform.",
                similarity=0.98,
            )
        ]
    )

    llm.generate_answer.return_value = LLMResponse(
        answer="StudyOS is an AI-powered learning platform."
    )

    response = client.post(
        f"{API_PREFIX}/chat/",
        json={
            "document_id": str(uuid4()),
            "conversation_id": str(uuid4()),
            "question": "What is StudyOS?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data