# ⚕️ Prescription Extractor System

An AI-powered web application that extracts text from medical prescription images using OCR and stores structured data in a cloud database.

---

## 🚀 Features

- **📤 Upload** — Upload prescription images (JPG, PNG, WEBP)
- **🔍 OCR Extraction** — EasyOCR + OpenCV for text recognition
- **✏️ Manual Correction** — Review and correct extracted fields before saving
- **💾 Cloud Storage** — Data stored securely in Supabase PostgreSQL
- **📋 History** — View, search, export (CSV/JSON), and delete records
- **📈 Analytics** — Interactive charts (Plotly) for medicine and doctor trends

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| OCR | EasyOCR + OpenCV |
| Database | Supabase PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Charts | Plotly |
| Language | Python 3.12 |

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── main.py          # FastAPI entry point + routes
│   ├── database.py      # Supabase connection (SQLAlchemy)
│   ├── models.py        # ORM models
│   ├── schemas.py       # Pydantic validation
│   ├── crud.py          # Database operations
│   ├── ocr.py           # EasyOCR text extraction
│   ├── extract.py       # Regex field parsing
│   └── utils.py         # File upload/delete helpers
├── frontend/
│   ├── app.py           # Streamlit main page
│   └── pages/
│       ├── dashboard.py # Overview + recent records
│       ├── upload.py    # Image upload + OCR
│       ├── history.py   # View/search/export records
│       └── analytics.py # Charts + statistics
├── uploads/             # Temporary image storage
├── sample_prescriptions/
├── .env                 # Database credentials
├── requirements.txt     # Python dependencies
├── schema.sql           # Database table schema
├── supabase_setup.md    # Supabase setup guide
└── README.md
```

---

## ⚡ Quick Start

### 1. Install Dependencies

```powershell
cd project
py -m pip install -r requirements.txt
```

### 2. Set Up Supabase

Follow the detailed guide in [`supabase_setup.md`](supabase_setup.md):
1. Create a free Supabase project
2. Copy the database connection string
3. Paste it into `.env`
4. Run `schema.sql` in the Supabase SQL Editor

### 3. Start the Backend

```powershell
cd backend
py -m uvicorn main:app --reload --port 8000
```

### 4. Start the Frontend (new terminal)

```powershell
cd frontend
py -m streamlit run app.py --server.port 8501
```

### 5. Open the App

Go to: **http://localhost:8501**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload_prescription` | Upload image → OCR → return parsed data |
| POST | `/save_prescription` | Save prescription to database |
| GET | `/prescriptions` | List all prescriptions |
| GET | `/prescription/{id}` | Get single prescription |
| DELETE | `/prescription/{id}` | Delete prescription |
| GET | `/analytics` | Get analytics data |

---

## 📋 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres.YOUR_REF:YOUR_PASSWORD@aws-0-REGION.pooler.supabase.com:6543/postgres?sslmode=require
```

---

## 👥 Team

College Mini-Project — Prescription Extractor System

---
