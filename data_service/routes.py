from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data_service.database import get_db
from data_service.models import Experiment
from pydantic import BaseModel
from typing import List
import json

router = APIRouter()

class ExperimentCreate(BaseModel):
    experiment_id: str
    num_qubits: int
    shots: int
    gate_sequence: List[str]
    error_rate: float
    file_path: str

class ExperimentResponse(BaseModel):
    experiment_id: str
    num_qubits: int
    shots: int
    gate_sequence: List[str]
    error_rate: float
    file_path: str

    model_config = {"from_attributes": True}

@router.post("/experiment")
def create_experiment(experiment: ExperimentCreate, db: Session = Depends(get_db)):
    existing = db.query(Experiment).filter(
        Experiment.experiment_id == experiment.experiment_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Experiment already exists")

    db_experiment = Experiment(
        experiment_id=experiment.experiment_id,
        num_qubits=experiment.num_qubits,
        shots=experiment.shots,
        gate_sequence=json.dumps(experiment.gate_sequence),
        error_rate=experiment.error_rate,
        file_path=experiment.file_path
    )
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return {"message": "Experiment stored successfully", "experiment_id": experiment.experiment_id}

@router.get("/experiment/{experiment_id}")
def get_experiment(experiment_id: str, db: Session = Depends(get_db)):
    experiment = db.query(Experiment).filter(
        Experiment.experiment_id == experiment_id
    ).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment

@router.get("/experiments")
def list_experiments(db: Session = Depends(get_db)):
    experiments = db.query(Experiment).all()
    return experiments