"""
OCR module using EasyOCR and OpenCV.
Extracts text from prescription images.
"""

import os
import sys

# Fix Windows console encoding for EasyOCR download progress bar
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import easyocr
import cv2

# ── Lazy-initialized EasyOCR reader ─────────────────────────────────────
_reader = None


def _get_reader():
    """Lazy-load EasyOCR reader so model downloads happen on first use, not at import."""
    global _reader
    if _reader is None:
        print("[OCR] Initializing EasyOCR reader (first time may download ~100MB of models)...")
        _reader = easyocr.Reader(["en"], gpu=False)
        print("[OCR] EasyOCR reader ready.")
    return _reader


# ── Image Preprocessing ─────────────────────────────────────────────────

def preprocess_image(image_path: str):
    """
    Preprocess image for better OCR accuracy:
    1. Read with OpenCV
    2. Convert to grayscale
    3. Apply median blur for noise reduction
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image could not be loaded from path: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction with median blur
    denoised = cv2.medianBlur(gray, 3)

    return denoised


# ── Text Extraction ─────────────────────────────────────────────────────

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using EasyOCR.

    Strategy:
    1. Try with preprocessing (grayscale + denoise) for better accuracy
    2. If that fails, fallback to direct image read
    3. If both fail, raise a clear error
    """
    reader = _get_reader()

    # Attempt 1: With preprocessing
    try:
        processed_img = preprocess_image(image_path)
        results = reader.readtext(processed_img, detail=0, paragraph=False)
        extracted_text = "\n".join(results)
        if extracted_text.strip():
            return extracted_text
    except Exception as e:
        print(f"[OCR] Preprocessing path failed: {e}")

    # Attempt 2: Direct read (no preprocessing)
    try:
        results = reader.readtext(image_path, detail=0, paragraph=False)
        extracted_text = "\n".join(results)
        return extracted_text if extracted_text.strip() else "(No text detected)"
    except Exception as e2:
        raise RuntimeError(
            f"OCR failed on both preprocessed and raw image.\n"
            f"Error: {e2}"
        ) from e2
