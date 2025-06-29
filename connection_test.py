import openai
import os

# Set your Azure OpenAI credentials
client = openai.AzureOpenAI(
    
deployment_name = "gpt-4o"

def test_connection():
    try:
        print("Sending test request to Azure OpenAI GPT-4o...")
        response = client.chat.completions.create(
            model=deployment_name,  # Deployment name, not model like "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        print("✅ Connection successful!")
        print("Response:", response.choices[0].message.content)

    except Exception as e:
        print("❌ Connection failed!")
        print("Error:", str(e))

if __name__ == "__main__":
    test_connection()
