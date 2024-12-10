from prefect import flow, get_run_logger
from tasks import (
    check_website_availability,
    download_problem_description,
    download_input_data,
    process_with_llm,
    execute_code,
    submit_answer,
    handle_response,
    create_solution_directories,
    save_text_to_file
)
import time
import math

@flow(name="Advent of Code Pipeline")
def advent_of_code_pipeline(year: int, day: int, part: int, max_retries: int = 3):
    logger = get_run_logger()
    logger.info(f"Starting pipeline for Year {year}, Day {day}, Part {part}")
    
    # Step 0: Create solution directories
    solution_dir = create_solution_directories(year, day)
    
    # Step 1: Check website availability
    available = check_website_availability(year, day)
    if not available:
        logger.warning(f"Problem {day} is not available yet. Exiting pipeline.")
        return
    
    # Step 2a: Download problem description
    problem_text = download_problem_description(year, day, part)
    problem_path = solution_dir / f"part_{part}/problem.md"
    save_text_to_file(problem_text, problem_path)
    
    # Step 2b: Download input data (only if it doesn't exist)
    input_path = solution_dir / "input.txt"
    if not input_path.exists():
        input_text = download_input_data(year, day)
        save_text_to_file(input_text, input_path)
    
    # Step 3: Process with LLM
    solution_text = process_with_llm(problem_text)
    solution_path = solution_dir / f"part_{part}/solution.py"
    save_text_to_file(solution_text, solution_path)
    
    # Step 4: Execute generated code
    answer = execute_code(solution_path)
    logger.info(f"Generated answer: {answer}")
    
    # Step 5: Submit answer
    response = submit_answer(year, day, part, answer)
    
    # Step 6: Handle submission response
    action = handle_response(year, day, part, response)
    
    # Conditional Logic
    if action == "retry":
        logger.info("Retrying with a different solution.")
        for attempt in range(max_retries):
            wait_time = math.pow(2, attempt)
            logger.info(f"Retry attempt {attempt + 1} for Day {day}, Part {part} after waiting {wait_time} seconds.")
            time.sleep(wait_time)
            try:
                solution_text = process_with_llm(problem_text)
                retry_path = solution_dir / f"part_{part}/solution_retry_{attempt+1}.py"
                save_text_to_file(solution_text, retry_path)
                answer = execute_code(retry_path)
                logger.info(f"Retry generated answer: {answer}")
                response = submit_answer(year, day, part, answer)
                action = handle_response(year, day, part, response)
                if action in ["proceed_to_part2", "completed"]:
                    break
            except Exception as e:
                logger.error(f"Retry attempt {attempt + 1} failed: {e}")
        else:
            logger.error(f"Failed to submit correct answer after {max_retries} attempts.")
    elif action == "proceed_to_part2":
        logger.info(f"Proceeding to Part 2 for Day {day}.")
        advent_of_code_pipeline(year, day, 2)
    elif action == "retry_later":
        logger.info("Problem not available yet. Will retry later.")
        time.sleep(60)  # Wait for 60 seconds before retrying
        advent_of_code_pipeline(year, day, part)
    elif action == "completed":
        logger.info(f"Completed Day {day}, Part {part}.")
    else:
        logger.warning(f"Unhandled action: {action}. Manual intervention may be required.")

@flow(name="Run All Days")
def run_all_days(year: int):
    for day in range(1, 26):
        for part in [1, 2]:
            advent_of_code_pipeline(year, day, part)

if __name__ == "__main__":
    # Run a single day and part
    advent_of_code_pipeline(year=2024, day=1, part=1)
    
    # Or run all days
    # run_all_days(year=2023)
    # advent_of_code_pipeline.visualize(day=1, part=1)
