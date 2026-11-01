
from datetime import datetime
from ipaddress import ip_address
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventCreate(BaseModel):
    source_ip: str
    event_type: Literal[
        "login_failed",
        "login_success",
        "suspicious_request"
    ]
    username: str | None = Field(default=None, max_length=100)
    service: str = Field(min_length=1, max_length=50)

    @field_validator("source_ip")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        return str(ip_address(value))


class EventResponse(EventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
