import os
from dotenv import load_dotenv
from anthropic import AnthropicVertex
import sys

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.', '.env'))

# Get configuration from .env
LOCATION = os.getenv('LOCATION')
PROJECT_ID = os.getenv('PROJECT_ID')

client = AnthropicVertex(region=LOCATION, project_id=PROJECT_ID)

def get_retry_prompt(problem_folder, wrong_output):
    # Read the retry prompt template
    with open('retry_prompt.md', 'r') as file:
        retry_prompt = file.read()
    
    # Read the original prompt
    with open(f'{problem_folder}/to_claude.txt', 'r') as file:
        original_prompt = file.read()
    
    # Read the failed solution
    with open(f'{problem_folder}/exec.py', 'r') as file:
        failed_code = file.read()
    
    # Format the retry prompt
    formatted_prompt = retry_prompt.format(
        original_prompt=original_prompt,
        failed_code=failed_code,
        wrong_output=wrong_output
    )
    
    return formatted_prompt

def save_response(problem_folder, code):
    # Clean up code if it's wrapped in ```python blocks
    cleaned_code = code
    if code.startswith('```python\n') and code.endswith('```'):
        cleaned_code = code[len('```python\n'):-3].strip()
    
    # Save the cleaned code to exec.py, overwriting the old solution
    with open(f'{problem_folder}/exec.py', 'w') as file:
        file.write(cleaned_code)

def retry_problem(problem_folder, wrong_output):
    prompt = get_retry_prompt(problem_folder, wrong_output)
    
    # Save retry prompt for reference
    with open(f'{problem_folder}/retry_to_claude.txt', 'w') as file:
        file.write(prompt)
        
    response = get_claude_response(prompt)
    save_response(problem_folder, response)

def get_claude_response(prompt, max_tokens=8000):
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python retry_claude.py <problem_folder> <wrong_output>")
        sys.exit(1)
    
    try:
        problem_folder = sys.argv[1]
        wrong_output = sys.argv[2]
        if not os.path.isdir(problem_folder):
            raise FileNotFoundError(f"Problem folder '{problem_folder}' not found")
        retry_problem(problem_folder, wrong_output)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
