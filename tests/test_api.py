import pytest
from fastapi.testclient import TestClient
from data_service.main import app
from data_service.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_experiment():
    payload = {
        "experiment_id": "test-exp-001",
        "num_qubits": 4,
        "shots": 1024,
        "gate_sequence": ["H", "H", "CNOT"],
        "error_rate": 0.012,
        "file_path": "storage/experiments/test-exp-001.json"
    }
    response = client.post("/experiment", json=payload)
    assert response.status_code == 200
    assert response.json()["experiment_id"] == "test-exp-001"

def test_create_duplicate_experiment():
    payload = {
        "experiment_id": "test-exp-002",
        "num_qubits": 4,
        "shots": 1024,
        "gate_sequence": ["H", "CNOT"],
        "error_rate": 0.015,
        "file_path": "storage/experiments/test-exp-002.json"
    }
    client.post("/experiment", json=payload)
    response = client.post("/experiment", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Experiment already exists"

def test_get_experiment():
    payload = {
        "experiment_id": "test-exp-003",
        "num_qubits": 2,
        "shots": 512,
        "gate_sequence": ["H", "CNOT"],
        "error_rate": 0.02,
        "file_path": "storage/experiments/test-exp-003.json"
    }
    client.post("/experiment", json=payload)
    response = client.get("/experiment/test-exp-003")
    assert response.status_code == 200
    assert response.json()["experiment_id"] == "test-exp-003"

def test_get_nonexistent_experiment():
    response = client.get("/experiment/does-not-exist")
    assert response.status_code == 404

def test_list_experiments():
    payload = {
        "experiment_id": "test-exp-004",
        "num_qubits": 4,
        "shots": 1024,
        "gate_sequence": ["H", "CNOT"],
        "error_rate": 0.018,
        "file_path": "storage/experiments/test-exp-004.json"
    }
    client.post("/experiment", json=payload)
    response = client.get("/experiments")
    assert response.status_code == 200
    assert len(response.json()) >= 1