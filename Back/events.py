# Back/events.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime
from model import Base

class Event(Base):
    """Événements (réunions, visites, etc.)."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    room = Column(String, nullable=True)
    audience = Column(String, default="all")


def get_upcoming_events(db: Session, now: datetime, hours: int = 2):
    """Retourne les événements dans les X prochaines heures."""
    window = now + timedelta(hours=hours)
    return (
        db.query(Event)
        .filter(Event.datetime >= now, Event.datetime <= window)
        .all()
    )
def get_upcoming_events(db: Session, now: datetime, hours: int = 2):
    """Retourne les événements dans les X prochaines heures, triés."""
    window = now + timedelta(hours=hours)
    return (
        db.query(Event)
        .filter(Event.datetime >= now, Event.datetime <= window)
        .order_by(Event.datetime.asc())
        .all()
    )
