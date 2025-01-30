#---	Imports		---#
import requests

BASE_URL = "http://localhost:5000/consommation"

def test_get_data_valid():
	response = requests.get(f"{BASE_URL}?start_date=2022-01-01 00:00:00&end_date=2022-01-02 00:00:00")
	assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
	assert "data" in response.json(), "Expected 'data' in response but it was not found."

def test_get_data_invalid_dates():
	response = requests.get(f"{BASE_URL}?start_date=2022-01-01&end_date=invalid-date")
	assert response.status_code == 400, f"Expected status code 400 for invalid date format, got {response.status_code}"
	assert "error" in response.json(), "Expected error message, but it was not returned."

def test_missing_dates():
	response = requests.get(f"{BASE_URL}?start_date=2022-01-01")
	assert response.status_code == 400, f"Expected status code 400 when 'end_date' is missing, got {response.status_code}"
	assert "error" in response.json(), "Expected error message for missing 'end_date'."

	response = requests.get(f"{BASE_URL}?end_date=2022-01-02")
	assert response.status_code == 400, f"Expected status code 400 when 'start_date' is missing, got {response.status_code}"
	assert "error" in response.json(), "Expected error message for missing 'start_date'."

