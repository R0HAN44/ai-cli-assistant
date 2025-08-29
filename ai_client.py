from config import get_api_key
from google import genai
from google.genai import types

client = genai.Client(api_key=get_api_key())

def ask_ai(prompt : str) -> str:
  response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=prompt
  )
  return response.text