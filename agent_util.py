import json
from config import get_api_key
from google import genai
from google.genai import types

client = genai.Client(api_key=get_api_key())

# Example tools config (define it somewhere in your project)
TOOLS = [
    {"name": "search", "description": "Search the web"},
    {"name": "database", "description": "Query the database"}
]

def build_prompt(history, user_input):
    return f"""
    You are an AI developer assistant.

    You have access to the following tools:
    {json.dumps(TOOLS, indent=2)}

    Conversation history:
    {json.dumps(history, indent=2)}

    The user asked:
    {user_input}

    Respond in JSON format:
    {{
      "action": "tool_name | answer",
      "args": {{}}  # if tool is required
      "response": "your reasoning/answer"
    }}
    """

def ask_ai(user_query: str, history: list) -> str:
    if retrieved_docs is None:
        retrieved_docs = []

    # Build the full prompt
    full_prompt = build_prompt(history, user_query)

    # Send the constructed prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[{"role": "user", "parts": [{"text": full_prompt}]}]
    )

    # Append to history for next turn
    history.append({"role": "user", "content": user_query})
    history.append({"role": "assistant", "content": response.text})

    return response.text
