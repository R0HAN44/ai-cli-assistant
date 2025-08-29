from ai_client import ask_ai
from utils import copy_to_clipboard

def main():
    print("🤖 Welcome to AI CLI Assistant!")
    while True:
        user_input = input("\nAsk me anything (or type 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        response = ask_ai(user_input)
        print("\nAI Response:\n", response)

        # copy_choice = input("\nCopy to clipboard? (y/n): ")
        # if copy_choice.lower() == "y":
        #     copy_to_clipboard(response)
        #     print("✅ Copied!")

if __name__ == "__main__":
    main()
