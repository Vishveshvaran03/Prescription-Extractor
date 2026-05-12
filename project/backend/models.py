"""
SQLAlchemy ORM models for the Prescription Extractor System.
Maps Python classes to PostgreSQL tables.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Prescription(Base):
    """Represents a single prescription record in the database."""

    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), index=True, nullable=True)
    doctor_name = Column(String(255), index=True, nullable=True)
    hospital_name = Column(String(255), nullable=True)
    medicine = Column(Text, nullable=True)       # Comma-separated list
    dosage = Column(Text, nullable=True)         # Comma-separated list
    date = Column(String(50), nullable=True)
    extracted_text = Column(Text, nullable=True)  # Raw OCR output
    created_at = Column(DateTime(timezone=True), server_default=func.now())
