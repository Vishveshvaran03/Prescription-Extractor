"""
Text extraction and parsing module.
Uses regex heuristics to extract structured fields from raw OCR text.
"""

import re


def parse_extracted_text(text: str) -> dict:
    """
    Parse raw OCR text into structured prescription fields using regex heuristics.

    Returns a dict with all fields (empty string if not found).
    """
    parsed_data = {
        "patient_name": "",
        "doctor_name": "",
        "hospital_name": "",
        "medicine": "",
        "dosage": "",
        "date": "",
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return parsed_data

    # ── 1. Hospital Name (usually in first 5 lines) ─────────────────────
    hospital_keywords = r"(hospital|clinic|care|medical|health|centre|center|pharmacy|lab|diagnostic|nursing)"
    for line in lines[:5]:
        if re.search(hospital_keywords, line, re.IGNORECASE):
            parsed_data["hospital_name"] = line
            break

    # ── 2. Doctor Name (Dr., Doctor, Physician, M.D., MBBS) ─────────────
    doctor_patterns = [
        r"(Dr\.?\s+[\w\s\.]+)",                    # Dr. Smith
        r"(Doctor\s+[\w\s\.]+)",                    # Doctor Smith
        r"([\w\s\.]+(?:M\.?D\.?|MBBS|M\.?B\.?B\.?S))", # Name MD / Name MBBS
    ]
    for line in lines:
        for pattern in doctor_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                parsed_data["doctor_name"] = match.group(1).strip()
                break
        if parsed_data["doctor_name"]:
            break

    # ── 3. Patient Name ─────────────────────────────────────────────────
    patient_patterns = [
        r"(?:Patient\s*Name|Patient|Name|Pt\.?\s*Name)\s*[:\-\s]\s*([\w\s\.]+)",
        r"(?:Mr\.|Mrs\.|Ms\.|Miss)\s+([\w\s\.]+)",
    ]
    for line in lines:
        for pattern in patient_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 2:
                    parsed_data["patient_name"] = name
                    break
        if parsed_data["patient_name"]:
            break

    # ── 4. Date (many formats) ──────────────────────────────────────────
    date_patterns = [
        r"(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})",     # DD/MM/YYYY or MM-DD-YY
        r"(\d{4}[/\-\.]\d{1,2}[/\-\.]\d{1,2})",         # YYYY-MM-DD
        r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*[\s,]+\d{2,4})",  # 25 Oct 2023
        r"(?:Date)\s*[:\-]\s*([\w\s/\-\.,]+)",          # Date: anything
    ]
    for line in lines:
        for pattern in date_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                parsed_data["date"] = match.group(1).strip()
                break
        if parsed_data["date"]:
            break

    # ── 5. Medicine & Dosage ────────────────────────────────────────────
    medicines = []
    dosages = []
    rx_found = False

    dosage_pattern = re.compile(
        r"(\d+\s*(?:mg|ml|g|mcg|iu|tablet|tab|cap|capsule|times|/day|daily|bid|tid|qid|od|bd|tds|hs|prn|sos))",
        re.IGNORECASE,
    )

    # Common medicine name patterns (capitalized words that look like drug names)
    common_meds = re.compile(
        r"\b((?:Tab|Cap|Syp|Inj|Cream|Ointment|Drop)[\s\.]+[\w\s\-]+)",
        re.IGNORECASE,
    )

    for line in lines:
        # Check if we've reached the Rx section
        if re.search(r"^R[xX]\b|^℞|^Prescription", line, re.IGNORECASE):
            rx_found = True
            continue

        dosage_match = dosage_pattern.search(line)
        med_match = common_meds.search(line)

        if dosage_match or med_match or rx_found:
            if dosage_match:
                dosage = dosage_match.group(1)
                med_name = line.replace(dosage, "").strip(" -.,:")
                # Clean up extracted medicine name
                med_name = re.sub(r"\s+", " ", med_name).strip()
                if med_name and len(med_name) > 2:
                    medicines.append(med_name)
                dosages.append(dosage)
            elif med_match:
                medicines.append(med_match.group(1).strip())
            elif rx_found and len(line) > 3:
                medicines.append(line)

    parsed_data["medicine"] = ", ".join(medicines) if medicines else ""
    parsed_data["dosage"] = ", ".join(dosages) if dosages else ""

    return parsed_data
