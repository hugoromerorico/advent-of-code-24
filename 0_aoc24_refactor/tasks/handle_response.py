from prefect import task
from bs4 import BeautifulSoup
import re
import time
from typing import Optional

@task(name="Handle Submission Response")
def handle_response(day: int, part: int, response_text: str) -> Optional[str]:
    soup = BeautifulSoup(response_text, 'html.parser')
    article = soup.find('article')
    if not article:
        raise ValueError("No article tag found in response.")
    
    message = article.get_text().strip()
    print(f"Submission response: {message}")
    
    if "That's not the right answer" in message:
        print("Wrong answer. Preparing to retry with a different solution.")
        return "retry"
    elif "That's the right answer" in message:
        print("Correct answer!")
        if part == 1:
            return "proceed_to_part2"
        else:
            return "completed"
    elif "You gave an answer too recently" in message:
        wait_seconds = extract_wait_time(message)
        print(f"Rate limited. Waiting for {wait_seconds} seconds.")
        time.sleep(wait_seconds)
        return "retry"
    elif "Puzzle input" in message:
        print("Problem not available yet.")
        return "retry_later"
    else:
        print("Unhandled response:", message)
        return "unknown"

def extract_wait_time(message: str) -> int:
    match = re.search(r'you must wait (\d+) seconds', message)
    if match:
        return int(match.group(1))
    return 60  # Default wait time if not specified
