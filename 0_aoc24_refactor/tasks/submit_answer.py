from prefect import task
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SESSION_COOKIE = os.getenv('COOKIE')
BASE_URL = "https://adventofcode.com"

@task(name="Submit Answer")
def submit_answer(year: int, day: int, part: int, answer: int) -> str:
    url = f"{BASE_URL}/{year}/day/{day}/answer"
    headers = {
        'Cookie': f'session={SESSION_COOKIE}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'level': part,
        'answer': answer
    }
    response = requests.post(url, headers=headers, data=data)
    return response.text
