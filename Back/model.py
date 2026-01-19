from datetime import datetime, time
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Employee(Base):
    """Employé de l'entreprise."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, default="employee")  # employee / manager / boss
    qr_code = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    birthday = Column(DateTime, nullable=True)
    expected_start_time = Column(Time, default=time(9, 0))

    punches = relationship("Punch", back_populates="employee")

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} ({self.role})>"


class Punch(Base):
    """Historique des pointages."""
    __tablename__ = "punches"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String, default="in")  # in / out

    employee = relationship("Employee", back_populates="punches")
