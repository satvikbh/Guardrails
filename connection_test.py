import openai
import os

# Set your Azure OpenAI credentials
client = openai.AzureOpenAI(
    api_key="FZspLxVIufHClmDpUeKn0Cgq0yOEHZugpQ7stmobByi34KYHhcpqJQQJ99BDACHYHv6XJ3w3AAAAACOGiXeP",
    api_version="2025-01-01-preview",
    azure_endpoint="https://dqazureaifound6652576421.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"
)

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
