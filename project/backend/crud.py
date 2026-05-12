"""
CRUD (Create, Read, Update, Delete) operations for prescriptions.
All database logic is centralized here.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
import models
import schemas


# ─── READ ────────────────────────────────────────────────────────────────

def get_prescriptions(db: Session, skip: int = 0, limit: int = 100):
    """Return a paginated list of all prescriptions."""
    return (
        db.query(models.Prescription)
        .order_by(models.Prescription.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_prescription(db: Session, prescription_id: int):
    """Return a single prescription by ID, or None if not found."""
    return (
        db.query(models.Prescription)
        .filter(models.Prescription.id == prescription_id)
        .first()
    )


# ─── CREATE ──────────────────────────────────────────────────────────────

def create_prescription(db: Session, prescription: schemas.PrescriptionCreate):
    """Create a new prescription record and return it."""
    db_prescription = models.Prescription(
        patient_name=prescription.patient_name,
        doctor_name=prescription.doctor_name,
        hospital_name=prescription.hospital_name,
        medicine=prescription.medicine,
        dosage=prescription.dosage,
        date=prescription.date,
        extracted_text=prescription.extracted_text,
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription


# ─── DELETE ──────────────────────────────────────────────────────────────

def delete_prescription(db: Session, prescription_id: int):
    """Delete a prescription by ID. Returns True if deleted, False if not found."""
    db_prescription = (
        db.query(models.Prescription)
        .filter(models.Prescription.id == prescription_id)
        .first()
    )
    if db_prescription:
        db.delete(db_prescription)
        db.commit()
        return True
    return False


# ─── ANALYTICS ───────────────────────────────────────────────────────────

def get_analytics(db: Session):
    """
    Return analytics data:
    - total prescription count
    - top 10 most frequent medicines
    - doctor frequency
    """
    total_prescriptions = db.query(models.Prescription).count()

    # ── Medicine frequency ──
    prescriptions = db.query(models.Prescription.medicine).all()
    medicine_counts = {}
    for p in prescriptions:
        if p.medicine:
            meds = [m.strip() for m in p.medicine.split(",")]
            for med in meds:
                if med:
                    medicine_counts[med] = medicine_counts.get(med, 0) + 1

    sorted_medicines = sorted(medicine_counts.items(), key=lambda x: x[1], reverse=True)
    top_medicines = [{"name": k, "count": v} for k, v in sorted_medicines[:10]]

    # ── Doctor frequency ──
    doctor_records = db.query(models.Prescription.doctor_name).all()
    doctor_counts = {}
    for d in doctor_records:
        if d.doctor_name:
            name = d.doctor_name.strip()
            if name:
                doctor_counts[name] = doctor_counts.get(name, 0) + 1

    sorted_doctors = sorted(doctor_counts.items(), key=lambda x: x[1], reverse=True)
    top_doctors = [{"name": k, "count": v} for k, v in sorted_doctors[:10]]

    return {
        "total_prescriptions": total_prescriptions,
        "top_medicines": top_medicines,
        "top_doctors": top_doctors,
    }
