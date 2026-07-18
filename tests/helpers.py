# A real, mutually-consistent set of reference ids (Dhaka district under the
# Dhaka division, Savar upazila under Dhaka district) pulled from the actual
# data/*.json files — used across tests instead of guessed numbers.
VALID_LOCATION = {
    "blood_group_id": 7,  # O+
    "division_id": 3,  # Dhaka
    "district_id": 1,  # Dhaka
    "upazila_id": 149,  # Savar
}


def register_payload(**overrides):
    payload = {
        "name": "Test Donor",
        "email": "donor@example.com",
        "phone": "01700000001",
        "password": "secret123",
        **VALID_LOCATION,
    }
    payload.update(overrides)
    return payload
