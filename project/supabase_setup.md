# Supabase Setup Guide for Prescription Extractor

This guide helps you set up a **free Supabase PostgreSQL database** for the project.

---

## Step 1: Create a Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"Start your project"** (sign up with GitHub or email)
3. It's **free** — no credit card required

---

## Step 2: Create a New Project

1. Click **"New Project"**
2. Fill in:
   - **Name**: `prescription-extractor`
   - **Database Password**: Choose a strong password (save it!)
   - **Region**: Choose the closest region to you
3. Click **"Create new project"**
4. Wait ~2 minutes for it to be ready

---

## Step 3: Get Your Database Connection String

1. In your Supabase dashboard, go to **Settings** → **Database**
2. Scroll to **"Connection string"** section
3. Select **"URI"** tab
4. Copy the connection string. It looks like:

```
postgresql://postgres.[YOUR-PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

> **Important**: Replace `[YOUR-PASSWORD]` with the database password you set in Step 2.

---

## Step 4: Update Your .env File

Open the `.env` file in the project root and paste your connection string:

```env
DATABASE_URL=postgresql://postgres.abcdef123456:MySecretPassword@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require
```

> Make sure to add `?sslmode=require` at the end if it's not already there.

---

## Step 5: Create the Table

1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New query"**
3. Paste the contents of `schema.sql` (from the project folder)
4. Click **"Run"**
5. You should see the `prescriptions` table appear in **Table Editor**

---

## Step 6: Verify Connection

Run this command from the project folder:

```bash
py -c "from backend.database import engine; conn = engine.connect(); print('Connected to Supabase!'); conn.close()"
```

If you see `Connected to Supabase!`, you're all set!

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `connection refused` | Check if the DATABASE_URL is correct |
| `password authentication failed` | Double-check your database password |
| `SSL required` | Add `?sslmode=require` to the end of DATABASE_URL |
| `relation "prescriptions" does not exist` | Run `schema.sql` in the SQL Editor |

---

## Running the Project

After Supabase is configured:

```powershell
# Terminal 1 — Start Backend
cd backend
py -m uvicorn main:app --reload --port 8000

# Terminal 2 — Start Frontend
cd frontend
py -m streamlit run app.py --server.port 8501
```

Then open: http://localhost:8501
