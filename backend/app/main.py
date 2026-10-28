
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine

app = FastAPI(
    title="ThreatLens API",
    description="Cybersecurity Threat Detection Platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "ThreatLens",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )
