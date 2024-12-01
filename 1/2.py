import os
from dotenv import load_dotenv
from anthropic import AnthropicVertex

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get configuration from .env
LOCATION = os.getenv('LOCATION')
PROJECT_ID = os.getenv('PROJECT_ID')

client = AnthropicVertex(region=LOCATION, project_id=PROJECT_ID)

def get_claude_response(prompt, max_tokens=1024):
    response = client.messages.create(
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-5-sonnet-v2@20241022",
    )
    return response.content[0].text

# Example usage
if __name__ == "__main__":
    prompt = "Send me a recipe for banana bread."
    response = get_claude_response(prompt)
    print(response)