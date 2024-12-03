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

def get_formatted_prompt(problem_number):
    # Read the system prompt template
    with open('system_prompt.md', 'r') as file:
        system_prompt = file.read()
    
    # Read the specific problem file
    with open(f'{problem_number}/problem.md', 'r') as file:
        problem_content = file.read()
    
    # Read the input file
    with open(f'{problem_number}/in.txt', 'r') as file:
        input_content = file.read()
    
    # If input is too long, truncate it
    if len(input_content) > 500:
        start = input_content[:200]
        end = input_content[-200:]
        input_content = f"""
{start}

[... truncated due to length ...]

{end}"""
    
    # Remove authentication section
    auth_section = "To play, please identify yourself via"
    problem_description = problem_content.split(auth_section)[0].strip()
    
    # Format the system prompt with both problem and input
    formatted_prompt = system_prompt.format(
        problem=problem_description,
        input=input_content
    )
    
    return formatted_prompt

def save_response(problem_number, code):
    # Clean up code if it's wrapped in ```python blocks
    cleaned_code = code
    if code.startswith('```python\n') and code.endswith('```'):
        cleaned_code = code[len('```python\n'):-3].strip()
    
    # Ensure directory exists
    os.makedirs(str(problem_number), exist_ok=True)
    
    # Save the cleaned code to exec.py
    with open(f'{problem_number}/exec.py', 'w') as file:
        file.write(cleaned_code)

def process_problem(problem_number):
    prompt = get_formatted_prompt(problem_number)
    
    # Save prompt to file
    os.makedirs(str(problem_number), exist_ok=True)
    with open(f'{problem_number}/to_claude.txt', 'w') as file:
        file.write(prompt)
        
    response = get_claude_response(prompt)
    save_response(problem_number, response)

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

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python claude.py <problem_number>")
        sys.exit(1)
    
    try:
        problem_number = int(sys.argv[1])
        process_problem(problem_number)
    except ValueError:
        print("Error: Problem number must be an integer")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)