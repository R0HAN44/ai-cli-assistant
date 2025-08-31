from config import get_api_key
from google import genai
from google.genai import types

client = genai.Client(api_key=get_api_key())

def build_prompt(chat_history, retrieved_docs, user_query):
    """
    chat_history: list of {"role": "user"|"assistant", "content": str}
    retrieved_docs: list of strings (chunks fetched from ChromaDB or any DB)
    user_query: str
    """
    # Convert chat history into text
    history_text = "\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in chat_history[-20:]  # take last 20 messages
    ])

    # Format retrieved documents
    context_text = "\n".join([f"- {doc}" for doc in retrieved_docs])

    # Build the final prompt
    prompt = f"""
        You are an AI assistant. Use the following conversation history and context to answer.

        Conversation history:
        {history_text}

        Relevant context from knowledge base:
        {context_text}

        User question:
        {user_query}

        Answer clearly and concisely.
        """
    return prompt


def ask_ai(user_query: str, history: list, retrieved_docs: list = None) -> str:
    if retrieved_docs is None:
        retrieved_docs = []

    # Build a single prompt with history + retrieved docs + user query
    full_prompt = build_prompt(history, retrieved_docs, user_query)

    # Wrap the prompt in Gemini's message format
    formatted_history = [{
        "role": "user",
        "parts": [{"text": full_prompt}]
    }]

    # Send the constructed prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=formatted_history
    )

    return response.text
