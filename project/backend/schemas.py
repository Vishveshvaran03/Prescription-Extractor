"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PrescriptionBase(BaseModel):
    """Base schema with common prescription fields."""
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    hospital_name: Optional[str] = None
    medicine: Optional[str] = None
    dosage: Optional[str] = None
    date: Optional[str] = None
    extracted_text: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    """Schema for creating a new prescription (inherits all base fields)."""
    pass


class PrescriptionResponse(PrescriptionBase):
    """Schema for returning a prescription (includes id and timestamp)."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode (SQLAlchemy -> Pydantic)
