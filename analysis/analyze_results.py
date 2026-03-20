import json
import os
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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

def export_pdf_report(stats: dict, experiments: list):
    filename = f"analysis_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Quantum Experiment Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Summary statistics table
    elements.append(Paragraph("Summary Statistics", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    summary_data = [
        ["Metric", "Value"],
        ["Total Experiments", str(stats["total_experiments"])],
        ["Mean Error Rate", str(stats["mean_error_rate"])],
        ["Error Rate Variance", str(stats["variance_error_rate"])],
        ["Min Error Rate", str(stats["min_error_rate"])],
        ["Max Error Rate", str(stats["max_error_rate"])],
        ["Mean Qubits", str(stats["mean_qubits"])],
    ]

    summary_table = Table(summary_data, colWidths=[300, 150])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # Per experiment breakdown
    elements.append(Paragraph("Per Experiment Breakdown", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    exp_data = [["Experiment ID", "Qubits", "Shots", "Error Rate", "Unique States"]]
    for e in experiments:
        dist = analyze_measurement_distribution(e["measurement_results"])
        exp_data.append([
            e["experiment_id"][:8] + "...",
            str(e["num_qubits"]),
            str(e["shots"]),
            str(e["error_rate"]),
            str(dist["unique_states"])
        ])

    exp_table = Table(exp_data, colWidths=[180, 60, 60, 80, 80])
    exp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(exp_table)

    doc.build(elements)
    print(f"\nPDF report saved to: {filename}")
    return filename

if __name__ == "__main__":
    stats = analyze_experiments()
    if stats:
        experiments = load_experiments()
        export_pdf_report(stats, experiments)