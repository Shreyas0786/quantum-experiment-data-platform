import numpy as np
import json
import uuid
from datetime import datetime
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_experiment(num_qubits: int = 4, shots: int = 1024) -> dict:
    # Create a quantum circuit
    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Apply gates to all qubits
    for qubit in range(num_qubits):
        circuit.h(qubit)  # Hadamard gate - puts qubit in superposition

    # Entangle qubits
    for qubit in range(num_qubits - 1):
        circuit.cx(qubit, qubit + 1)  # CNOT gate

    # Measure all qubits
    circuit.measure(range(num_qubits), range(num_qubits))

    # Run on local simulator
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Build experiment result
    experiment = {
        "experiment_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "num_qubits": num_qubits,
        "shots": shots,
        "gate_sequence": ["H"] * num_qubits + ["CNOT"] * (num_qubits - 1),
        "error_rate": round(np.random.uniform(0.001, 0.05), 4),
        "measurement_results": counts
    }

    return experiment

def save_experiment(experiment: dict) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    short_id = experiment['experiment_id'][:8]
    filename = f"storage/experiments/exp_{timestamp}_{short_id}.json"
    with open(filename, "w") as f:
        json.dump(experiment, f, indent=2)
    return filename

if __name__ == "__main__":
    experiment = generate_experiment(num_qubits=4, shots=1024)
    filepath = save_experiment(experiment)
    print(f"Experiment saved to: {filepath}")
    print(json.dumps(experiment, indent=2))