from fastapi import FastAPI

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
def health_check():
    return {
        "status": "healthy",
        "database": "disconnected",
    }

