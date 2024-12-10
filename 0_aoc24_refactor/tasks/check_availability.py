from prefect import task, get_run_logger
import requests

BASE_URL = "https://adventofcode.com"

@task(retries=5, retry_delay_seconds=10, name="Check Website Availability")
def check_website_availability(year: int, day: int) -> bool:
    logger = get_run_logger()
    url = f"{BASE_URL}/{year}/day/{day}"
    response = requests.get(url)
    
    if "Please don't repeatedly request this endpoint" in response.text:
        logger.warning(f"Website not available for {year} Day {day}")
        return False
    
    logger.info(f"Website available for {year} Day {day}")
    return True
