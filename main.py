from ai_client import ask_ai
from utils import copy_to_clipboard
from chromaUtil import add_message, get_history, reset_session, print_collection

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

if __name__ == "__main__":
    main()
