import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to a valid model

# Initialize Gemini chat
chat = model.start_chat(history=[])

# Conversational loop
print("🧑 Enter your message (type 'bye' or 'end' to exit): ")
while True:
    user_input = input("🧑 You: ")
    
    # Check for termination
    if user_input.lower() in ["bye", "end"]:
        print("🤖 Bot: Goodbye! Have a great day!")
        break

    # Send input to Guardrails
    response = requests.post("http://localhost:5000/guardrails", json={"user_input": user_input})

    # Handle response
    if response.status_code == 200:
        result = response.json()
        if "response" in result and "is_harmful" in result:
            guardrails_output = result["response"]
            is_harmful = result["is_harmful"]
            print("🛡️ Guardrails Output:", guardrails_output)

            # If guardrails detect harmful content, only show guardrails response
            if is_harmful:
                print("🤖 Bot: Input detected as harmful or toxic. Please try a different query.")
            else:
                # Pass original user input to Gemini for non-harmful content
                try:
                    gemini_reply = chat.send_message(user_input)
                    print("🤖 Bot:", gemini_reply.text)
                except Exception as e:
                    print("❌ Gemini Error:", str(e))
        else:
            print("❌ Guardrails error:", result.get("error", "Unknown error"))
    else:
        # Handle content filter or other errors as toxic input
        print("🛡️ Guardrails Output: Input blocked due to content filtering.")
        print("🤖 Bot: Input detected as harmful or toxic. Please try a different query.")