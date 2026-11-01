from app.detection.engine import detect_brute_force
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import SecurityEvent
from app.schemas.events import EventCreate, EventResponse

router = APIRouter(prefix="/events", tags=["Security Events"])



@router.post(
    "/",
    response_model=EventResponse,
    status_code=201
)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    try:
        db_event = SecurityEvent(**event.model_dump())

        db.add(db_event)
        db.flush()

        # Ensure the timestamp is available.
        db.refresh(db_event)

        # Run the detection engine.
        detect_brute_force(db, db_event)

        # Save the event and any generated alert together.
        db.commit()
        db.refresh(db_event)

        return db_event

    except Exception:
        db.rollback()
        raise



@router.get("/", response_model=list[EventResponse])
def list_events(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    statement = (
        select(SecurityEvent)
        .order_by(SecurityEvent.timestamp.desc(), SecurityEvent.id.desc())
        .limit(limit)
    )

    return db.scalars(statement).all()
