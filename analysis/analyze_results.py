import json
import os
import numpy as np
import pandas as pd
from pathlib import Path

EXPERIMENTS_DIR = Path("storage/experiments")

def load_experiments() -> list:
    experiments = []
    for file in EXPERIMENTS_DIR.glob("*.json"):
        with open(file, "r") as f:
            experiments.append(json.load(f))
    return experiments

def analyze_measurement_distribution(measurement_results: dict) -> dict:
    counts = list(measurement_results.values())
    total_shots = sum(counts)
    probabilities = {state: count / total_shots for state, count in measurement_results.items()}
    return {
        "total_shots": total_shots,
        "unique_states": len(measurement_results),
        "most_frequent_state": max(measurement_results, key=measurement_results.get),
        "least_frequent_state": min(measurement_results, key=measurement_results.get),
        "probabilities": probabilities
    }

def analyze_experiments() -> dict:
    experiments = load_experiments()

    if not experiments:
        print("No experiments found in storage/experiments/")
        return {}

    df = pd.DataFrame([{
        "experiment_id": e["experiment_id"],
        "num_qubits": e["num_qubits"],
        "shots": e["shots"],
        "error_rate": e["error_rate"],
        "timestamp": e["timestamp"]
    } for e in experiments])

    stats = {
        "total_experiments": len(experiments),
        "mean_error_rate": round(float(df["error_rate"].mean()), 4),
        "variance_error_rate": round(float(df["error_rate"].var()), 6),
        "min_error_rate": round(float(df["error_rate"].min()), 4),
        "max_error_rate": round(float(df["error_rate"].max()), 4),
        "mean_qubits": round(float(df["num_qubits"].mean()), 2),
    }

    print("\n=== Experiment Analysis Report ===")
    print(f"Total Experiments Analyzed: {stats['total_experiments']}")
    print(f"Mean Error Rate:            {stats['mean_error_rate']}")
    print(f"Error Rate Variance:        {stats['variance_error_rate']}")
    print(f"Min Error Rate:             {stats['min_error_rate']}")
    print(f"Max Error Rate:             {stats['max_error_rate']}")
    print(f"Mean Qubits:                {stats['mean_qubits']}")

    print("\n=== Per Experiment Breakdown ===")
    for e in experiments:
        dist = analyze_measurement_distribution(e["measurement_results"])
        print(f"\nExperiment: {e['experiment_id']}")
        print(f"  Qubits: {e['num_qubits']} | Shots: {e['shots']} | Error Rate: {e['error_rate']}")
        print(f"  Unique States: {dist['unique_states']}")
        print(f"  Most Frequent State: {dist['most_frequent_state']}")
        print(f"  Least Frequent State: {dist['least_frequent_state']}")

    return stats

if __name__ == "__main__":
    analyze_experiments()