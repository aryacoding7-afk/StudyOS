from app.modules.llm.schemas import LLMRequest
from app.modules.llm.service import LLMService


def main():
    service = LLMService()

    response = service.generate_answer(
        LLMRequest(
            question="What is Python?",
            context="Python is a programming language."
        )
    )

    print(response.answer)


if __name__ == "__main__":
    main()