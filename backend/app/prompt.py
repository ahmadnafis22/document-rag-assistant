def build_prompt(context, question ,history):
    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using only the provided context.

Use the conversation history to understand references
such as "it", "they", "this", or "the previous topic".

If the answer is not available in the context, say:
"I don't know based on the provided documents."

Conversation History:
{history}

Context:
{context}

Current Question:
{question}

Answer:
"""

    return prompt