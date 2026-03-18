# Quantum Experiment Data Platform

A backend data platform that simulates the infrastructure used to store and analyze experimental data from quantum computing experiments — similar to workflows used by research teams like Google Quantum AI.

---

## Architecture
```
Qiskit Quantum Circuit Simulator
            |
            v
Experiment JSON Files (storage/experiments/)
            |
            v
FastAPI Data Ingestion API
            |
            v
SQLite Metadata Database
            |
            v
Statistical Analysis Pipeline (NumPy + Pandas)
```

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLite + SQLAlchemy
- Qiskit + Qiskit-Aer (local quantum simulator)
- NumPy + Pandas
- Docker
- Pytest

---

## Project Structure
```
quantum-experiment-data-platform/
├── experiment_simulator/
│   └── generate_experiment.py   # Generates real quantum circuit results
├── data_service/
│   ├── main.py                  # FastAPI entry point
│   ├── database.py              # SQLite connection setup
│   ├── models.py                # Experiment metadata model
│   └── routes.py                # API endpoints
├── analysis/
│   └── analyze_results.py       # Statistical analysis pipeline
├── storage/
│   └── experiments/             # Experiment JSON files
├── infra/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   └── test_api.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/quantum-experiment-data-platform.git
cd quantum-experiment-data-platform
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your values.

### 4. Run the experiment simulator
```bash
python3 experiment_simulator/generate_experiment.py
```

### 5. Start the API server
```bash
uvicorn data_service.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to explore the API.

### 6. Run the analysis pipeline
```bash
python3 analysis/analyze_results.py
```

### 7. Run with Docker
```bash
docker compose -f infra/docker-compose.yml up --build
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/experiment` | Store a new experiment |
| GET | `/experiment/{id}` | Retrieve an experiment by ID |
| GET | `/experiments` | List all experiments |
| GET | `/health` | Health check |

---

## Example Experiment Data
```json
{
  "experiment_id": "exp_20260317_223413_6e3265e0",
  "timestamp": "2026-03-17T22:34:13.155769",
  "num_qubits": 4,
  "shots": 1024,
  "gate_sequence": ["H", "H", "H", "H", "CNOT", "CNOT", "CNOT"],
  "error_rate": 0.0155,
  "measurement_results": {
    "0000": 59,
    "0001": 85,
    "0010": 66
  }
}
```

---

## Running Tests
```bash
pytest tests/test_api.py -v
```

---

## Future Improvements

- Add gRPC ingestion service
- Deploy to Kubernetes
- Integrate object storage (S3)
- Add experiment visualization dashboard
- Connect to real IBM Quantum hardware