import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBh8PBHh-MgQd5i7vzq6hUdLzcik_ulvsY")  # Replace with your actual API key

generation_config = {
    "temperature": 0.25,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",  # Or another suitable model
    generation_config=generation_config,
    system_instruction="You are an English improvement chatbot that engages in conversations on any topic the user wants to discuss, helping them refine their language skills along the way.",
)

def talk():
    try:
        with open("curr.txt", "r") as f:
            user_input = f.read().strip()

        if not user_input:
            print("curr.txt is empty. Please provide input.")
            return

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        print(response.text)

        with open("inputs.txt", "a") as outfile:
            outfile.write("## START ##\n")  # Mark the beginning of a new conversation
            outfile.write(user_input + "\n")
            outfile.write("## END ##\n")  # Mark the end of the conversation

        open("curr.txt", "w").close()  # Clear curr.txt

    except FileNotFoundError:
        print("curr.txt not found. Please create the file and add your input.")
    except Exception as e:
        print(f"An error occurred during talk(): {e}")


def evaluate():
    try:
        with open("inputs.txt", "r") as f:
            all_inputs = f.read()  # Read the entire content as a single string

        if not all_inputs:
            print("inputs.txt is empty. No input to evaluate.")
            return

        conversations = all_inputs.split("## START ##")  # Split into conversations

        with open("mistakes.txt", "w") as mistake_file:
            for i in range(1, len(conversations)):  # Skip the initial empty string
                conversation_block = conversations[i].split("## END ##")[0].strip()  # Extract and clean conversation
                if not conversation_block:  # Handle empty conversations
                    continue

                evaluation_prompt = f"""
                Please evaluate the following text for English language quality, providing feedback on 4 sections distinctly:
                1. How I could have said it better - More formally and More concisely (only 1 response)
                2. Words that should be in my vocabulary (suggest 2 words)
                3. Grammar mistakes (list them clearly)
                4. Spelling mistakes (list them clearly)
                Be specific and no need to give a summary.

                ```
                {conversation_block}
                ```
                """

                eval_chat_session = model.start_chat(history=[])
                evaluation_response = eval_chat_session.send_message(evaluation_prompt)

                # Write full response to mistakes.txt
                mistake_file.write(f"--- Evaluation of Conversation {i} ---\n")
                mistake_file.write(evaluation_response.text + "\n\n")

    except FileNotFoundError:
        print("inputs.txt not found. Please create the file.")
    except Exception as e:
        print(f"An error occurred during evaluate(): {e}")


# Main program loop
while True:
    choice = input("Enter 'talk' to converse, 'eval' to get feedback, or 'exit' to quit: ").lower()

    if choice == "talk":
        talk()
    elif choice == "eval":
        evaluate()
    elif choice == "exit":
        break
    else:
        print("Invalid choice. Please enter 'talk', 'eval', or 'exit'.")