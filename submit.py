import requests
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def submit_solution(day, level, answer, session_cookie):
    url = f'https://adventofcode.com/2024/day/{day}/answer'
    
    headers = {
        'Cookie': f'session={session_cookie}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'level': level,  # 1 for part 1, 2 for part 2
        'answer': answer
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.text

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python submit.py <day> <level> <answer>.\nExample: python submit.py 1 1 142")
        sys.exit(1)
    
    try:
        day = int(sys.argv[1])
        level = int(sys.argv[2])
        answer = int(sys.argv[3])
        
        session_cookie = os.getenv('COOKIE')
        if not session_cookie:
            print("Error: COOKIE environment variable not found")
            sys.exit(1)
            
        result = submit_solution(day, level, answer, session_cookie)
        print(result)
    except ValueError:
        print("Error: Day, level and answer must be integers")
        sys.exit(1)