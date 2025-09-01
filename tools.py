import os
import subprocess

WORKSPACE = "workspace_project"

# Whitelist of allowed commands
ALLOWED_COMMANDS = {
    "npm": ["create", "install", "run", "start", "build", "test"],
    "yarn": ["create", "install", "start", "build", "test"],
    "npx": ["create-react-app"],
    "python": ["-m", "venv", "manage.py", "main.py"],
    "pip": ["install"],
    "ls": [],
    "pwd": [],
    "echo": []
}

def create_file(filepath: str, content: str):
    """Create a file inside the workspace with given content."""
    if not os.path.isdir(WORKSPACE):
        os.makedirs(WORKSPACE, exist_ok=True)

    full_path = os.path.join(WORKSPACE, filepath)

    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE)):
        return {
            "status": "error",
            "action": "create_file",
            "path": full_path,
            "error": "File path must be inside the workspace."
        }

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {
            "status": "success",
            "action": "create_file",
            "path": full_path,
            "output": f"File created successfully."
        }
    except OSError as e:
        return {
            "status": "error",
            "action": "create_file",
            "path": full_path,
            "error": str(e)
        }

def delete_file(filepath: str):
    """Delete a file inside the workspace."""
    if not os.path.isdir(WORKSPACE):
        return {
            "status": "error",
            "action": "delete_file",
            "error": "Workspace does not exist."
        }

    full_path = os.path.join(WORKSPACE, filepath)

    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE)):
        return {
            "status": "error",
            "action": "delete_file",
            "path": full_path,
            "error": "File path must be inside the workspace."
        }
    
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
            return {
                "status": "success",
                "action": "delete_file",
                "path": full_path,
                "output": "File deleted successfully."
            }
        else:
            return {
                "status": "error",
                "action": "delete_file",
                "path": full_path,
                "error": "File does not exist."
            }
    except OSError as e:
        return {
            "status": "error",
            "action": "delete_file",
            "path": full_path,
            "error": str(e)
        }

def run_command(command: list):
    """Run a whitelisted shell command inside the workspace."""
    if not os.path.isdir(WORKSPACE):
        os.makedirs(WORKSPACE, exist_ok=True)

    if not command:
        return {
            "status": "error",
            "action": "run_command",
            "error": "Command cannot be empty."
        }

    base_cmd = command[0]
    args = command[1:]

    if base_cmd not in ALLOWED_COMMANDS:
        return {
            "status": "error",
            "action": "run_command",
            "error": f"Command '{base_cmd}' is not allowed."
        }

    allowed_args = ALLOWED_COMMANDS[base_cmd]
    if allowed_args and not any(arg in allowed_args for arg in args):
        return {
            "status": "error",
            "action": "run_command",
            "error": f"Arguments '{args}' not allowed for '{base_cmd}'."
        }

    try:
        result = subprocess.run(
            command,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success",
            "action": "run_command",
            "command": " ".join(command),
            "output": result.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "action": "run_command",
            "command": " ".join(command),
            "error": e.stderr.strip()
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "action": "run_command",
            "command": " ".join(command),
            "error": "Command not found."
        }
