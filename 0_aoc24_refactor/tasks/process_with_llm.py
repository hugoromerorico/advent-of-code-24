from prefect import task
import subprocess
import sys
import os

@task(name="Process with LLM (Claude)", retries=3, retry_delay_seconds=5)
def process_with_llm(problem_dir: str) -> str:
    day = problem_dir.split('_')[0]
    script_path = os.path.join("scripts", "claude.py")
    
    result = subprocess.run(
        [sys.executable, script_path, day],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"LLM processing failed: {result.stderr}")
    
    return problem_dir
