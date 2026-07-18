import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def _load_json_file(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


BLOOD_GROUPS = _load_json_file("blood_groups.json").get("blood_groups", [])
DIVISIONS = _load_json_file("bd-divisions.json").get("divisions", [])
DISTRICTS = _load_json_file("bd-districts.json").get("districts", [])
UPAZILAS = _load_json_file("bd-upazilas.json").get("upazilas", [])

BLOOD_GROUP_IDS = {int(b["id"]) for b in BLOOD_GROUPS}
DIVISION_IDS = {int(d["id"]) for d in DIVISIONS}
DISTRICT_BY_ID = {int(d["id"]): d for d in DISTRICTS}
UPAZILA_BY_ID = {int(u["id"]): u for u in UPAZILAS}


def validate_blood_group_id(blood_group_id: int) -> None:
    if blood_group_id not in BLOOD_GROUP_IDS:
        raise ValueError(f"Unknown blood_group_id: {blood_group_id}")


def validate_location_ids(*, division_id: int, district_id: int, upazila_id: int) -> None:
    """Checks the division/district/upazila ids exist and are properly nested
    (a district under a different division, or an upazila under a different
    district, is rejected rather than silently accepted)."""
    if division_id not in DIVISION_IDS:
        raise ValueError(f"Unknown division_id: {division_id}")

    district = DISTRICT_BY_ID.get(district_id)
    if district is None:
        raise ValueError(f"Unknown district_id: {district_id}")
    if int(district["division_id"]) != division_id:
        raise ValueError(f"district_id {district_id} does not belong to division_id {division_id}")

    upazila = UPAZILA_BY_ID.get(upazila_id)
    if upazila is None:
        raise ValueError(f"Unknown upazila_id: {upazila_id}")
    if int(upazila["district_id"]) != district_id:
        raise ValueError(f"upazila_id {upazila_id} does not belong to district_id {district_id}")
