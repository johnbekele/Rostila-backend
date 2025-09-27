from google import genai
import os
import time
from google.genai.errors import ClientError
from app.core.config import settings

# Initialize the client with API key from config
api_key = settings.GOOGLE_API_KEY
if not api_key:
    print("Error: Google_AI_API environment variable not set")
    print("Please set your Google API key:")
    print("export Google_AI_API='your_actual_api_key_here'")
    exit(1)

client = genai.Client(api_key=api_key)

def chat(prompt: str):
    try:
        # You can pass the prompt directly as a string
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text  # <-- return the text
    except ClientError as e:
        if e.status_code == 429:
            print("❌ Rate limit exceeded. Please wait a moment and try again.")
            print("💡 You may need to upgrade your Google AI plan or wait for quota reset.")
            return None
        elif e.status_code == 400:
            print("❌ Invalid API key or request.")
            return None
        else:
            print(f"❌ API Error: {e}")
            return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    print("🤖 GenAI Chat Test")
    print("💡 Type 'exit' to quit")
    print("⚠️  Note: You may hit rate limits with the free tier")
    print("-" * 50)
    
    while True:
        prompt = input("Enter your prompt: ")
        if prompt.lower() == "exit":
            print("Exiting...")
            break
        
        result = chat(prompt)
        if result:
            print(f"🤖 Response: {result}")
        else:
            print("❌ No response received. Please try again later.")
        print("-" * 50)

if __name__ == "__main__":
    main()
