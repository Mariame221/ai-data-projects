# Back/main.py
# ============================================
# API principale de mar‑IA‑me
# Pointage + messages + synthèse vocale
# ============================================

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

from model import Base, Employee, Punch
from events import get_upcoming_events
from messages import welcome_message, goodbye_message
from voice import speak


# ============================================
# Base de données
# ============================================

DATABASE_URL = "sqlite:///./maria_me.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Création des tables si elles n'existent pas
Base.metadata.create_all(bind=engine)


# ============================================
# Application FastAPI
# ============================================

app = FastAPI(
    title="mar‑IA‑me API",
    version="1.0",
    description="Gardienne intelligente de votre entreprise"
)


# ============================================
# Session DB par requête
# ============================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# Détection de retard
# ============================================

def is_late(employee: Employee, now: datetime) -> bool:
    """
    Retourne True si l'employé est en retard.
    """
    expected = datetime.combine(now.date(), employee.expected_start_time)
    return now > expected


# ============================================
# Endpoint principal : scan QR code
# ============================================

@app.post("/scan")
def scan(qr_code: str, punch_type: str = "in", db: Session = Depends(get_db)):
    """
    Pointage d'un employé via QR code.
    Retourne :
    - message personnalisé
    - fichier audio généré
    - timestamp
    """

    now = datetime.utcnow()

    # Vérification employé
    employee = (
        db.query(Employee)
        .filter(Employee.qr_code == qr_code)
        .first()
    )

    if not employee:
        raise HTTPException(404, "Employé introuvable.")

    # Détermination du message
    if punch_type == "in":
        late = is_late(employee, now)
        events = get_upcoming_events(db, now)
        msg = welcome_message(employee, now, late, events)

    elif punch_type == "out":
        msg = goodbye_message(employee)

    else:
        raise HTTPException(400, "Type de pointage invalide.")

    # Enregistrement du pointage
    punch = Punch(
        employee_id=employee.id,
        type=punch_type
    )
    db.add(punch)
    db.commit()

    # Génération de la voix
    audio_file = speak(msg)

    # Réponse API
    return {
        "message": msg,
        "audio": audio_file,
        "timestamp": now.isoformat()
    }
