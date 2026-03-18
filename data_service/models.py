from sqlalchemy import Column, String, Float, Integer, DateTime, Text
from datetime import datetime
from data_service.database import Base

class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    num_qubits = Column(Integer, nullable=False)
    shots = Column(Integer, nullable=False)
    gate_sequence = Column(Text, nullable=False)
    error_rate = Column(Float, nullable=False)
    file_path = Column(String, nullable=False)