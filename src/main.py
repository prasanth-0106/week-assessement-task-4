import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Employee Data Service")
DATA_FILE = Path(__file__).resolve().parent.parent / "employees.json"

class EmployeeIn(BaseModel):
    name: str = Field(min_length=1)
    salary: float = Field(gt=0)

def load_employees() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/employees")
def get_employees() -> list[dict]:
    return load_employees()

@app.get("/employees/{name}")
def get_employee(name: str) -> dict:
    employee = next(
        (item for item in load_employees() if item["name"].casefold() == name.casefold()),
        None,
    )
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeIn) -> dict:
    employees = load_employees()
    if any(item["name"].casefold() == employee.name.casefold() for item in employees):
        raise HTTPException(status_code=409, detail="Employee already exists")
    result = employee.model_dump()
    employees.append(result)
    DATA_FILE.write_text(json.dumps(employees, indent=2), encoding="utf-8")
    return result
