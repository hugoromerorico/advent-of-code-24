from pathlib import Path
from prefect import task

@task(name="Create Solution Directories")
def create_solution_directories(year: int, day: int) -> Path:
    base_path = Path(f"solutions/year_{year}/day_{day}")
    part1_path = base_path / "part_1"
    part2_path = base_path / "part_2"
    
    for path in [base_path, part1_path, part2_path]:
        path.mkdir(parents=True, exist_ok=True)
    
    return base_path

@task(name="Save Text to File")
def save_text_to_file(text: str, filepath: Path) -> Path:
    filepath.write_text(text)
    return filepath
