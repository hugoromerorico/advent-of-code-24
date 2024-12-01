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
    # Extract base problem number and determine if it's part 2
    is_part2 = False
    base_number = problem_number
    if str(problem_number).endswith('_2'):
        is_part2 = True
        base_number = problem_number.split('_')[0]
    
    # Read the appropriate system prompt template
    system_prompt_file = 'system_prompt_part2.md' if is_part2 else 'system_prompt.md'
    with open(system_prompt_file, 'r') as file:
        system_prompt = file.read()
    
    # Read the specific problem file
    problem_path = f'{base_number}/problem.md' if not is_part2 else f'{base_number}_2/problem.md'
    with open(problem_path, 'r') as file:
        problem_content = file.read()
    
    # Remove authentication section and completed message
    auth_section = "To play, please identify yourself via"
    complete_section = "Both parts of this puzzle are complete!"
    
    problem_description = problem_content.split(auth_section)[0].strip()
    if complete_section in problem_description:
        # Find the start of the line containing the complete_section
        lines = problem_description.split('\n')
        for i, line in enumerate(lines):
            if complete_section in line:
                problem_description = '\n'.join(lines[:i]).strip()
                break
    
    # Format the system prompt with the problem
    formatted_prompt = system_prompt.replace("{problem}", problem_description)
    
    return formatted_prompt

def save_response(problem_number, code):
    # Clean up code if it's wrapped in ```python blocks
    cleaned_code = code
    if code.startswith('```python\n') and code.endswith('```'):
        cleaned_code = code[len('```python\n'):-3].strip()
    
    # Ensure directory exists
    folder = str(problem_number)
    os.makedirs(folder, exist_ok=True)
    
    # Save the cleaned code to exec.py
    with open(f'{folder}/exec.py', 'w') as file:
        file.write(cleaned_code)

def process_problem(problem_number):
    prompt = get_formatted_prompt(problem_number)
    
    # Save prompt to file
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
        print("Usage: python claude.py <problem_number> or <problem_number_2>")
        print("Example: python claude.py 1    # for part 1")
        print("Example: python claude.py 1_2  # for part 2")
        sys.exit(1)
    
    try:
        problem_number = sys.argv[1]
        process_problem(problem_number)
    except ValueError:
        print("Error: Invalid problem number format")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)