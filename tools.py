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
    
def read_file(filepath: str, start_line: int, end_line: int):
    """Read a file inside the workspace from start_line to end_line (1-indexed, inclusive)."""
    if not os.path.isdir(WORKSPACE):
        return {
            "status": "error",
            "action": "read_file",
            "error": "Workspace does not exist."
        }

    full_path = os.path.join(WORKSPACE, filepath)

    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE)):
        return {
            "status": "error",
            "action": "read_file",
            "path": full_path,
            "error": "File path must be inside the workspace."
        }
    
    if not os.path.isfile(full_path):
        return {
            "status": "error",
            "action": "read_file",
            "path": full_path,
            "error": "File does not exist."
        }

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            selected_lines = lines[start_line - 1:end_line]
            content = "".join(selected_lines)
        return {
            "status": "success",
            "action": "read_file",
            "path": full_path,
            "output": content
        }
    except OSError as e:
        return {
            "status": "error",
            "action": "read_file",
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
    print("base command:", base_cmd)
    print("arguments:", args)
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
        print("FINAL COMMAND", command)
        process = subprocess.Popen(
            command,
            cwd=WORKSPACE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        captured_output = []
        for line in process.stdout:
            print(line, end="")   # print live to terminal
            captured_output.append(line)

        process.wait()

        if process.returncode == 0:
            return {
                "status": "success",
                "action": "run_command",
                "command": " ".join(command),
                "output": "".join(captured_output).strip()
            }
        else:
            return {
                "status": "error",
                "action": "run_command",
                "command": " ".join(command),
                "error": "".join(captured_output).strip()
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
