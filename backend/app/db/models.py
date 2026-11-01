
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    source_ip: Mapped[str] = mapped_column(String(45), index=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str | None] = mapped_column(String(100))
    service: Mapped[str] = mapped_column(String(50))
