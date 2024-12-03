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
    # Remove _2 suffix if present
    base_number = problem_number.split('_')[0]
    
    # Read the system prompt template
    with open('system_prompt_part2.md', 'r') as file:
        system_prompt = file.read()
    
    # Read the problem file
    with open(f'{base_number}_2/problem.md', 'r') as file:
        problem_content = file.read()
    
    # Read the input file
    with open(f'{base_number}_2/in.txt', 'r') as file:
        input_content = file.read()
    
    # If input is too long, truncate it
    if len(input_content) > 500:
        start = input_content[:200]
        end = input_content[-200:]
        input_content = f"""
{start}

[... truncated due to length ...]

{end}"""
    
    # Remove authentication, completed, and sharing sections
    sections_to_remove = [
        "To play, please identify yourself via",
        "Both parts of this puzzle are complete!",
        "You can also [Share"
    ]
    
    for section in sections_to_remove:
        if section in problem_content:
            problem_description = problem_content.split(section)[0].strip()
        else:
            problem_description = problem_content.strip()
    
    # Escape any literal curly braces in the system prompt by doubling them
    system_prompt = system_prompt.replace('{', '{{').replace('}', '}}')
    
    # Restore our named placeholders
    system_prompt = system_prompt.replace('{{problem}}', '{problem}').replace('{{input}}', '{input}')
    
    # Format the system prompt with problem and input using named placeholders
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
    folder = f"{problem_number.split('_')[0]}_2"
    os.makedirs(folder, exist_ok=True)
    
    # Save the cleaned code to exec.py
    with open(f'{folder}/exec.py', 'w') as file:
        file.write(cleaned_code)

def process_problem(problem_number):
    prompt = get_formatted_prompt(problem_number)
    
    # Save prompt to file
    folder = f"{problem_number.split('_')[0]}_2"
    with open(f'{folder}/to_claude.txt', 'w') as file:
        file.write(prompt)
        
    response = get_claude_response(prompt)
    save_response(problem_number, response)

def get_claude_response(prompt, max_tokens=8000):
    response = client.messages.create(
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        model="claude-3-5-sonnet-v2@20241022",
    )
    return response.content[0].text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python claude_part2.py <problem_number>")
        print("Example: python claude_part2.py 1_2")
        sys.exit(1)
    
    try:
        problem_number = sys.argv[1]
        process_problem(problem_number)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)