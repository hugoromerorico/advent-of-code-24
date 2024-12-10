from prefect import task
import subprocess
import sys
from pathlib import Path

@task(name="Execute Generated Code", retries=3, retry_delay_seconds=5)
def execute_code(solution_path: Path) -> int:
    if not solution_path.exists():
        raise FileNotFoundError(f"{solution_path} does not exist.")
    
    result = subprocess.run(
        [sys.executable, str(solution_path)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Execution failed: {result.stderr}")
    
    try:
        answer = int(result.stdout.strip())
    except ValueError:
        raise ValueError("Executed code did not return an integer answer.")
    
    return answer
