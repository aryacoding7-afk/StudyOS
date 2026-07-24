from app.modules.chat.schemas import ChatSource
from app.modules.search.schemas import SearchResponse


def build_sources(
    search_response: SearchResponse,
) -> list[ChatSource]:

    return [
        ChatSource(
            page_number=result.page_number,
            similarity=round(result.similarity, 3),
            excerpt=result.content[:250],
        )
        for result in search_response.results
    ]