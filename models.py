from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

DBModelBase = declarative_base()


class Patient(DBModelBase):
    __tablename__ = "patients"

    id = Column(String, primary_key=True)
    age = Column(Integer, nullable=False)
    primary_issue = Column(String, nullable=False)
    no_show_probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan"
    )



class Appointment(DBModelBase):
    __tablename__ = "appointments"

    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)

    patient_age = Column(Integer, nullable=False)
    appointment_type = Column(String, nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    day_of_week = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)

    scheduled_duration = Column(Integer, nullable=False)
    actual_duration = Column(Integer, nullable=False)
    duration_difference = Column(Integer, nullable=False)

    show_up = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="appointments")