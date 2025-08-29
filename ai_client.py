from config import get_api_key
from google import genai
from google.genai import types

client = genai.Client(api_key=get_api_key())

def ask_ai(prompt: str, history: list) -> str:
    # add the new user message to history
    history.append({"role": "user", "parts": [prompt]})

    # send the full history
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=history
    )
    
    return response.text
