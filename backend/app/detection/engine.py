
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import SecurityAlert, SecurityEvent

FAILED_LOGIN_THRESHOLD = 5
DETECTION_WINDOW_SECONDS = 60
ALERT_COOLDOWN_SECONDS = 60


def detect_brute_force(db: Session, event: SecurityEvent):
    if event.event_type != "login_failed":
        return None

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(
        seconds=DETECTION_WINDOW_SECONDS
    )

    # Count recent failures from the same IP and service.
    failed_count = db.scalar(
        select(func.count(SecurityEvent.id)).where(
            SecurityEvent.source_ip == event.source_ip,
            SecurityEvent.service == event.service,
            SecurityEvent.event_type == "login_failed",
            SecurityEvent.timestamp >= window_start,
            SecurityEvent.timestamp <= now,
        )
    )

    if failed_count < FAILED_LOGIN_THRESHOLD:
        return None

    # Avoid duplicate alerts during the cooldown.
    cooldown_start = now - timedelta(
        seconds=ALERT_COOLDOWN_SECONDS
    )

    existing_alert = db.scalar(
        select(SecurityAlert).where(
            SecurityAlert.source_ip == event.source_ip,
            SecurityAlert.alert_type == "brute_force",
            SecurityAlert.created_at >= cooldown_start,
        ).limit(1)
    )

    if existing_alert:
        return None

    alert = SecurityAlert(
        source_ip=event.source_ip,
        alert_type="brute_force",
        severity="HIGH",
        description=(
            f"Possible brute-force attack: "
            f"{failed_count} failed login attempts "
            f"on {event.service} within 60 seconds."
        ),
    )

    db.add(alert)
    db.flush()

    return alert
