from backend.app.retriever import retriever
from backend.app.context import build_context
from backend.app.prompt import build_prompt
from backend.app.llm import llm
from backend.app.retriever import retrieve_relevant_documents


def ask_question(question, chat_history=None):

    if chat_history is None:
        chat_history = []

    try:
        # Retrieve relevant documents
        documents = retrieve_relevant_documents(
            question=question,
            threshold=1.3,
            k=5
        )

        if not documents:
            return {
                "answer": "I don't know based on the provided documents.",
                "sources": []
            }

        # Build context from documents
        context = build_context(documents)

        # Build conversation history
        history = ""

        for message in chat_history:
            history += f"User: {message['question']}\n"
            history += f"Assistant: {message['answer']}\n"

        # Build prompt
        prompt = build_prompt(context, question  , history)

        # Ask LLM
        response = llm.invoke(prompt)

        answer = response.content

        # Handle structured Gemini response
        if isinstance(answer, list):
            answer = "\n".join(
                item.get("text", "")
                for item in answer
                if isinstance(item, dict)
            )

        return {
            "answer": answer,
            "sources": documents
        }

    except Exception as e:
        raise RuntimeError(
            f"RAG pipeline failed: {str(e)}"
        )