from app.modules.conversation.schemas import ConversationMessage


SYSTEM_PROMPT = """
You are StudyOS, an AI study assistant.

Rules:

1. Use the uploaded notes as the primary source.
2. If the answer exists in the notes, answer from them.
3. If the notes are insufficient, clearly separate external knowledge.
4. Never hallucinate information as coming from the uploaded notes.
5. Mention page numbers naturally when relevant.
""".strip()


def build_prompt(
    history: list[ConversationMessage],
    context: str,
    question: str,
) -> str:

    history_text = "\n".join(
        f"{message.role.capitalize()}: {message.content}"
        for message in history
    )

    return f"""
{SYSTEM_PROMPT}

Conversation History
--------------------
{history_text}

Retrieved Context
-----------------
{context}

Question
--------
{question}
""".strip()