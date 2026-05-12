"""
FastAPI Backend for Prescription Extractor System.
Entry point — run with: py -m uvicorn main:app --reload
"""

import os
import sys
from pathlib import Path

# ── Windows encoding fix (MUST be before any easyocr imports) ────────────
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure backend directory is on sys.path for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
import ocr
import extract
import utils
from database import engine, get_db

# ── Create database tables if they don't exist ──────────────────────────
models.Base.metadata.create_all(bind=engine)

# ── FastAPI app ──────────────────────────────────────────────────────────
app = FastAPI(
    title="Prescription Extractor API",
    description="Upload prescription images, extract text via OCR, and store structured data.",
    version="1.0.0",
)

# ── CORS (allow Streamlit frontend to call the API) ─────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════════════════════════════════


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "API is running", "database": "Supabase PostgreSQL"}


@app.post("/upload_prescription")
async def upload_prescription(file: UploadFile = File(...)):
    """
    Upload a prescription image → run OCR → extract fields → return parsed data.
    The image is deleted after processing.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: JPG, PNG, WEBP",
        )

    # 1. Save uploaded file
    file_path = utils.save_upload_file(file)

    try:
        # 2. Run OCR
        extracted_text = ocr.extract_text_from_image(file_path)

        # 3. Parse fields from raw text
        parsed_data = extract.parse_extracted_text(extracted_text)

        # Include raw text for manual correction
        parsed_data["extracted_text"] = extracted_text

        # 4. Clean up uploaded file
        utils.delete_file(file_path)

        return {"status": "success", "data": parsed_data}

    except Exception as e:
        utils.delete_file(file_path)
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.post("/save_prescription", response_model=schemas.PrescriptionResponse)
def save_prescription(
    prescription: schemas.PrescriptionCreate,
    db: Session = Depends(get_db),
):
    """Save a validated prescription to the database."""
    return crud.create_prescription(db=db, prescription=prescription)


@app.get("/prescriptions", response_model=List[schemas.PrescriptionResponse])
def read_prescriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Return all prescriptions (paginated, newest first)."""
    return crud.get_prescriptions(db, skip=skip, limit=limit)


@app.get("/prescription/{id}", response_model=schemas.PrescriptionResponse)
def read_prescription(id: int, db: Session = Depends(get_db)):
    """Return a single prescription by ID."""
    db_prescription = crud.get_prescription(db, prescription_id=id)
    if db_prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return db_prescription


@app.delete("/prescription/{id}")
def delete_prescription(id: int, db: Session = Depends(get_db)):
    """Delete a prescription by ID."""
    success = crud.delete_prescription(db, prescription_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return {"status": "deleted", "id": id}


@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    """Return analytics data (counts, top medicines, top doctors)."""
    return crud.get_analytics(db)
