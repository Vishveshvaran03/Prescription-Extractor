"""
Utility functions for file handling.
"""

import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile

# Use absolute path for uploads directory (project_root/uploads)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_DIR = str(PROJECT_ROOT / "uploads")


def save_upload_file(upload_file: UploadFile) -> str:
    """Save an uploaded file to disk with a unique name. Returns the file path."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename to avoid overwrites
    file_extension = os.path.splitext(upload_file.filename or ".png")[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


def delete_file(file_path: str):
    """Safely delete a file from disk. No error if file doesn't exist."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError:
        pass  # Silently ignore deletion errors
