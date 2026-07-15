import json
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

def load_json_file(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

blood_groups_data = load_json_file("blood_groups.json").get("blood_groups", [])

def get_all_blood_groups():
    return blood_groups_data
