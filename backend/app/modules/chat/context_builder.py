from app.modules.search.schemas import SearchResponse


def build_context(
    search_response: SearchResponse,
) -> str:
    return "\n\n---\n\n".join(
        f"Page {result.page_number}\n{result.content}"
        for result in search_response.results
    )