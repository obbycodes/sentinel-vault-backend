from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine) ## Create all tables in the database

app = FastAPI(
    title="SentinelVault",
    description="Enterprise Asset & Secure Telemetry Platform",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {
        "system": "SentinelVault Telemetry Engine",
        "status": "operational",
        "version": "0.1.0",
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "database": "connected"
    }

