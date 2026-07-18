from app.utils.reference_data import DIVISIONS as divisions_data
from app.utils.reference_data import DISTRICTS as districts_data
from app.utils.reference_data import UPAZILAS as upazilas_data


def get_divisions():
    return divisions_data

def get_all_districts():
    return districts_data

def get_districts_by_division(division_id: int):
    div_id_str = str(division_id)
    return [d for d in districts_data if d.get("division_id") == div_id_str]

def get_upazilas_by_district(district_id: int):
    dist_id_str = str(district_id)
    return [u for u in upazilas_data if u.get("district_id") == dist_id_str]
