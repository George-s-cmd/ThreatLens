
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import SecurityAlert

router = APIRouter(
    prefix="/alerts",
    tags=["Security Alerts"]
)


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_ip: str
    alert_type: str
    severity: str
    description: str
    created_at: datetime


@router.get("/", response_model=list[AlertResponse])
def list_alerts(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    statement = (
        select(SecurityAlert)
        .order_by(
            SecurityAlert.created_at.desc(),
            SecurityAlert.id.desc()
        )
        .limit(limit)
    )

    return db.scalars(statement).all()
