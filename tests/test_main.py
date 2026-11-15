import json
import pytest
from fastapi.testclient import TestClient
from src.main import app, DATA_FILE

client = TestClient(app)
ORIGINAL = [
    {"name": "Arun", "department": "Sales", "salary": 30000},
    {"name": "Priya", "department": "HR", "salary": 45000},
    {"name": "Rahul", "department": "IT", "salary": 60000},
    {"name": "Divya", "department": "IT", "salary": 75000},
    {"name": "Karthik", "department": "Finance", "salary": 90000},
]

@pytest.fixture(autouse=True)
def reset_data():
    DATA_FILE.write_text(json.dumps(ORIGINAL), encoding="utf-8")
    yield
    DATA_FILE.write_text(json.dumps(ORIGINAL), encoding="utf-8")

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_get_employee_success():
    response = client.get("/employees/Arun")
    assert response.status_code == 200
    assert response.json()["salary"] == 30000

def test_get_employee_404():
    response = client.get("/employees/Ravi")
    assert response.status_code == 404

def test_invalid_salary():
    response = client.post("/employees", json={"name": "Ravi", "salary": -5})
    assert response.status_code == 422

def test_empty_name():
    response = client.post("/employees", json={"name": "", "salary": 1000})
    assert response.status_code == 422

def test_create_employee():
    response = client.post("/employees", json={"name": "Ravi", "salary": 25000})
    assert response.status_code == 201
    assert response.json()["name"] == "Ravi"
