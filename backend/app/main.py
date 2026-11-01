
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.events import router as events_router
from app.db.database import engine
from app.db.models import Base
from app.api.alerts import router as alerts_router

app = FastAPI(
    title="ThreatLens API",
    description="Cybersecurity Threat Detection Platform",
    version="0.2.0"
)

# Temporary MVP table creation.
# We'll use Alembic migrations in a later stage.
Base.metadata.create_all(bind=engine)

app.include_router(events_router)
app.include_router(alerts_router)


@app.get("/")
def root():
    return {
        "project": "ThreatLens",
        "status": "running",
        "version": "0.2.0"
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
