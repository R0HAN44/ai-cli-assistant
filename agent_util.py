import json
from config import get_api_key
from google import genai
from google.genai import types
import re

client = genai.Client(api_key=get_api_key())

# Example tools config (define it somewhere in your project)
TOOLS = [
    {
        "name": "create_file",
        "description": "Create a file inside the workspace with given content",
        "args": {
            "filepath": "Path of the file relative to workspace",
            "content": "Content to write in the file"
        }
    },
    {
        "name": "read_file",
        "description": "Read a file inside the workspace from specific line range",
        "args": {
            "filepath": "Path of the file relative to workspace",
            "start_line": "Line number to start reading (1-indexed)",
            "end_line": "Line number to end reading (inclusive)"
        }
    },
    {
        "name": "delete_file",
        "description": "Delete a file inside the workspace",
        "args": {
            "filepath": "Path of the file relative to workspace"
        }
    },
    {
        "name": "run_command",
        "description": "Run a whitelisted shell command inside the workspace",
        "args": {
            "command": "List of command and args, e.g. ['npm','install']"
        }
    }
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

    Respond in JSON format with a list of steps. Each step can either be a tool call or a plain answer. 
    Example:
    {{
      "steps": [
        {{
          "action": "use_tool",
          "tool_name": "create_file",
          "args": {{ "filepath": "path/to/file.txt", "content": "Hello, world!" }},
          "response": "Creating a new file with the specified content"
        }},
        {{
          "action": "use_tool",
          "tool_name": "run_command",
          "args": {{ "command": ["npm", "install"] }},
          "response": "Running npm install to install dependencies"
        }},
        {{
          "action": "answer",
          "response": "Final explanation or result for the user"
        }}
      ]
    }}

    Always output a pure JSON string without any Markdown formatting, backticks, or explanations.
    """

def clean_json_output(output: str):
    # Remove code fences if present
    cleaned = re.sub(r"^```(?:json)?\n?", "", output.strip())
    cleaned = re.sub(r"\n?```$", "", cleaned)
    return cleaned

def interact_with_llm(user_query: str, history: list) -> str:

    # Build the full prompt
    full_prompt = build_prompt(history, user_query)

    # Send the constructed prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[{"role": "user", "parts": [{"text": full_prompt}]}]
    )

    raw_output = response.text.strip()
    # print("Raw output:", raw_output)
    cleaned_output = clean_json_output(raw_output)
    try:
        parsed_output = json.loads(cleaned_output)
        # print("Parsed output:", parsed_output)
    except json.JSONDecodeError:
        return {
            "steps": [
                {"action": "answer", "response": cleaned_output}
            ]
        }
    print("returned output:", parsed_output)
    return parsed_output
