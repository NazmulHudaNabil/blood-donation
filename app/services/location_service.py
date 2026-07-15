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

divisions_data = load_json_file("bd-divisions.json").get("divisions", [])
districts_data = load_json_file("bd-districts.json").get("districts", [])
upazilas_data = load_json_file("bd-upazilas.json").get("upazilas", [])

def get_divisions():
    return divisions_data

def get_districts_by_division(division_id: int):
    div_id_str = str(division_id)
    return [d for d in districts_data if d.get("division_id") == div_id_str]

def get_upazilas_by_district(district_id: int):
    dist_id_str = str(district_id)
    return [u for u in upazilas_data if u.get("district_id") == dist_id_str]
