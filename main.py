from ai_client import ask_ai
from utils import copy_to_clipboard
from chromaUtil import add_message, get_history, reset_session, print_collection
from tools import create_file, run_command, delete_file, read_file
from historyUtils import add_message_to_history, get_history_from_file
from agent_util import interact_with_llm

session_id = "default_session"

def main():
    print("🤖 Welcome to AI CLI Assistant!")
    print("\nAvailable options:")
    print("  • Type your question and press Enter to chat with AI")
    print("  • Type 'reset' to start a new conversation")
    print("  • Type 'exit' or 'quit' to close the assistant\n")

    while True:
        user_input = input("\nAsk me anything: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        elif user_input.lower() in ["reset", "new chat"]:
            reset_session(session_id)
            print("🔄 Conversation reset! Starting fresh...")
            print_collection()
            continue
        add_message(session_id, "user", user_input)
        history = get_history(user_input, session_id)
        response = ask_ai(user_input, history)
        add_message(session_id, "assistant", response)
        print("\nAI Response:\n", response)

        # print_collection()

        # copy_choice = input("\nCopy to clipboard? (y/n): ")
        # if copy_choice.lower() == "y":
        #     copy_to_clipboard(response)
        #     print("✅ Copied!")

def performActions(aiResponse):
    for step in aiResponse.get("steps", []):
        action = step.get("action")
        tool_name = step.get("tool_name")  # Only exists if action == "use_tool"
        args = step.get("args", {})
        response_reason = step.get("response", "")

        print(f"\nAction: {action}")
        print(f"Reason: {response_reason}")

        if action == "use_tool":
            if tool_name == "create_file":
                filepath = args.get("filepath")
                content = args.get("content", "")
                result = create_file(filepath, content)
                add_message_to_history({
                    "role": "system",
                    "content": f"Created file at {filepath}",
                    "status": result["status"],
                    "tool_name": tool_name,
                    "args": {"filepath": filepath}
                })
                if result["status"] == "success":
                    print(f"✅ File created at: {filepath}")
                else:
                    print(f"❌ Error creating file: {result['error']}")

            elif tool_name == "read_file":
                filepath = args.get("filepath")
                start_line = args.get("start_line", 1)
                end_line = args.get("end_line", 10)
                result = read_file(filepath, start_line, end_line)
                add_message_to_history({
                    "role": "system",
                    "content": f"Read file from {filepath} (lines {start_line}-{end_line})",
                    "status": result["status"],
                    "tool_name": tool_name,
                    "args": {"filepath": filepath, "start_line": start_line, "end_line": end_line}
                })
                if result["status"] == "success":
                    print(f"📄 File content from {start_line}-{end_line}:\n{result['output']}")
                else:
                    print(f"❌ Error reading file: {result['error']}")

            elif tool_name == "delete_file":
                filepath = args.get("filepath")
                result = delete_file(filepath)
                add_message_to_history({
                    "role": "system",
                    "content": f"Deleted file at {filepath}",
                    "status": result["status"],
                    "tool_name": tool_name,
                    "args": {"filepath": filepath}
                })
                if result["status"] == "success":
                    print(f"🗑️ File deleted: {filepath}")
                else:
                    print(f"❌ Error deleting file: {result['error']}")

            elif tool_name == "run_command":
                command = args.get("command", [])
                print("COMMAND _>>>>>>", command)
                result = run_command(command)
                add_message_to_history({
                    "role": "system",
                    "content": f"Ran command: {command}",
                    "status": result["status"],
                    "tool_name": tool_name,
                    "args": {"command": command}
                })
                if result["status"] == "success":
                    print(f"💻 Command output:\n{result['output']}")
                else:
                    print(f"❌ Error running command: {result['error']}")

            else:
                print(f"❌ Unknown tool: {tool_name}")

        elif action == "answer":
            add_message_to_history({
                "role": "assistant",
                "content": response_reason,
                "status": "success",
                "tool_name": "answer",
                "args": {}
            })
            print(f"🤖 Answer: {response_reason}")

        else:
            print(f"❌ Unknown action type: {action}")

def codeAgent():
    print("Welcome to AI Code Agent!")
    print("Provide a prompt to build your app.")
    print("Type 'done' when you are finished.")
    while True:
        user_prompt = input("Enter your prompt: ")
        if user_prompt.lower() == "done":
            print("Building process completed.")
            break
        print(f"Building your app with prompt: {user_prompt}")
        add_message_to_history({
            "role": "user",
            "content": user_prompt
        })
        history = get_history_from_file()
        aiResponse = interact_with_llm(user_prompt, history)
        performActions(aiResponse)

def testFunc():
    print("press 1 for creating file")
    print("press 2 for running command")
    print("press 3 for deleting file")
    print("press 4 for reading file")

    while True:
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == "1":
            file_path = input("Enter the file path: ")
            content = input("Enter the file content: ")
            result = create_file(file_path, content)
            if result["status"] == "success":
                print(f"File created at: {file_path}")
            else:
                print(f"Error creating file: {result['error']}")
        elif choice == "2":
            command = input("Enter the command to run: ")
            result = run_command(command.split())
            if result["status"] == "success":
                print(f"Command output:\n{result['output']}")
            else:
                print(f"Error running command: {result['error']}")
        elif choice == "3":
            file_path = input("Enter the file path to delete: ")
            result = delete_file(file_path)
            if result["status"] == "success":
                print(f"File deleted at: {file_path}")
            else:
                print(f"Error deleting file: {result['error']}")
        elif choice == "4":
            file_path = input("Enter the file path to read: ")
            start_line = int(input("Enter the start line (1-indexed): "))
            end_line = int(input("Enter the end line (1-indexed): "))
            result = read_file(file_path, start_line, end_line)
            if result["status"] == "success":
                print(f"File content from lines {start_line} to {end_line}:\n{result['output']}")
            else:
                print(f"Error reading file: {result['error']}")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    codeAgent()
