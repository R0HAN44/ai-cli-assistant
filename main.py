from ai_client import ask_ai
from utils import copy_to_clipboard
from chromaUtil import add_message, get_history, reset_session, print_collection
from tools import create_file, run_command, delete_file, read_file

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
    testFunc()
