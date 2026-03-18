from fastapi import FastAPI
from data_service.database import engine, Base
from data_service.routes import router
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quantum Experiment Data Platform",
    description="API for storing and retrieving quantum experiment data",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT")}