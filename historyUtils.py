import json
import os

WORKSPACE = "workspace_project"
HISTORY_FILE = "history.json"

def add_message_to_history(messageObj):
    """Add a message object (role + content) to the history file in JSON format."""
    
    history = []
    
    # Load existing history if file exists
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    
    # Append new message
    history.append(messageObj)
    
    # Write back to file
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_history_from_file():
    """Retrieve the conversation history from the history file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []