from prefect import task, get_run_logger
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path


BASE_URL = "https://adventofcode.com"
MAX_RETRIES = 10
RETRY_DELAY = 1  # seconds

@task(name="Download Problem Description", 
      retries=MAX_RETRIES, 
      retry_delay_seconds=RETRY_DELAY)
def download_problem_description(year: int, day: int, part: int) -> str:
    load_dotenv('../.env')

    SESSION_COOKIE = os.getenv('COOKIE_SECONDARY')
    logger = get_run_logger()
    logger.info(f"Downloading problem description for Year {year} Day {day} Part {part}")
    
    problem_url = f"{BASE_URL}/{year}/day/{day}"
    cookies = {'session': SESSION_COOKIE}
    logger.info(f"Requesting problem description from {problem_url} with cookies {cookies}")
    response = requests.get(problem_url, cookies=cookies)
    
    if "Internal Server Error" in response.text:
        raise requests.RequestException("Internal Server Error received")
        
    problem_text = extract_main_content(response.text)
    if not problem_text.strip():
        raise ValueError("Empty problem text received")
    if part == 1:
        problem_text = ''.join(problem_text.split("Answer:")[:-1])
    logger.info(f"Successfully downloaded problem description")
    return problem_text

@task(name="Download Input Data", 
      retries=MAX_RETRIES, 
      retry_delay_seconds=RETRY_DELAY)
def download_input_data(year: int, day: int) -> str:
    load_dotenv('../.env')

    SESSION_COOKIE = os.getenv('COOKIE_SECONDARY')
    logger = get_run_logger()
    logger.info(f"Downloading input data for Year {year} Day {day}")
    
    input_url = f"{BASE_URL}/{year}/day/{day}/input"
    cookies = {'session': SESSION_COOKIE}
    response = requests.get(input_url, cookies=cookies)
    
    if "Internal Server Error" in response.text:
        raise requests.RequestException("Internal Server Error received")
        
    input_text = response.text
    if not input_text.strip():
        raise ValueError("Empty input received")
        
    logger.info(f"Successfully downloaded input data")
    return input_text

def extract_main_content(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    
    # Remove all <script> and <style> elements
    for element in main.find_all(['script', 'style']):
        element.decompose()
    
    # Replace <p> and <h2> with double newlines
    for tag in main.find_all(['p', 'h2']):
        tag.insert_before(soup.new_string('\n\n'))
        tag.unwrap()
    
    # Special handling for <pre> blocks to keep them compact
    for pre in main.find_all('pre'):
        # Replace newlines within pre blocks with a special marker
        pre_text = pre.get_text().strip()
        # Keep the pre content compact without extra newlines
        pre.string = '\n' + pre_text + '\n'
    
    # Remove all remaining HTML tags
    text = main.get_text()
    
    # Clean up multiple newlines and spaces
    text = '\n'.join(
        line.strip() for line in text.splitlines() if line.strip()
    )
    
    # Add consistent spacing
    text = '\n\n'.join(text.split('\n'))
    
    return text.strip()
