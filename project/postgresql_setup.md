# PostgreSQL Setup Guide for Beginners (Windows)

This is a complete, step-by-step guide to installing and configuring PostgreSQL for the **Prescription Extractor System**.

---

## 1. Install PostgreSQL on Windows

### Download Link
Go to the official PostgreSQL website:
[https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
Click on "Download the installer" and select the latest version for Windows x86-64.

### Installation Steps
1. Run the downloaded `.exe` installer.
2. **Installation Directory**: Keep the default (`C:\Program Files\PostgreSQL\16`).
3. **Components**: Ensure all boxes are checked (PostgreSQL Server, pgAdmin 4, Stack Builder, Command Line Tools).
4. **Data Directory**: Keep the default.
5. **Password**: You will be asked to set a password for the default `postgres` superuser. 
   - **Important**: Set this password to `admin` or something memorable. You will need it later.
6. **Port**: Keep the default port `5432`.
7. **Advanced Options / Locale**: Keep the default ("Default locale").
8. Finish the installation (you can uncheck Stack Builder at the end).

### What are pgAdmin and psql?
- **pgAdmin 4**: A graphical user interface (GUI) that allows you to manage databases, run queries, and view tables visually using your mouse.
- **SQL Shell (psql)**: A command-line interface (CLI) where you type commands to interact with the database. It is faster and often preferred by developers.

---

## 2. Verify PostgreSQL Installation

### Step 1: Open SQL Shell (psql)
1. Press the Windows Key and search for **SQL Shell (psql)**. Open it.
2. It will ask for several prompts (Server, Database, Port, Username). Just press **Enter** for all of them to accept the defaults (`localhost`, `postgres`, `5432`, `postgres`).
3. When it asks for **Password**, type the password you created during installation (e.g., `admin`) and press Enter. (Note: The password will not show on the screen as you type).

### Step 2: Check Version
Once inside the `postgres=#` prompt, type:
```sql
SELECT version();
```
It should return the installed PostgreSQL version.

---

## 3. Fix Common Errors

> [!WARNING]
> **Error: "psql is not recognized as an internal or external command"**
> **Fix (PATH Issue)**: Windows doesn't know where `psql.exe` is.
> 1. Search for "Environment Variables" in Windows and click "Edit the system environment variables".
> 2. Click "Environment Variables..."
> 3. Under "System variables", find `Path`, select it, and click "Edit".
> 4. Click "New" and paste the path to your PostgreSQL bin folder: `C:\Program Files\PostgreSQL\16\bin`
> 5. Click OK on all windows, restart your terminal, and try again.

> [!WARNING]
> **Error: "password authentication failed for user"**
> **Fix**: You typed the wrong password, or you are trying to connect with a user that doesn't exist. Double-check your spelling.

> [!WARNING]
> **Error: "server not running" or "connection refused"**
> **Fix**: The PostgreSQL service is stopped.
> 1. Press Windows Key + R, type `services.msc`, and press Enter.
> 2. Scroll down to find `postgresql-x64-16`.
> 3. Right-click it and select "Start" or "Restart".

---

## 4 & 5. Create Database and User

Open your **SQL Shell (psql)** and log in as the default `postgres` user. Run the following commands one by one:

**Create the User:**
```sql
CREATE USER prescription_user WITH PASSWORD 'prescription123';
```

**Create the Database:**
```sql
CREATE DATABASE prescription_db;
```

**Grant Privileges:**
```sql
GRANT ALL PRIVILEGES ON DATABASE prescription_db TO prescription_user;
```

**Connect to the new database:**
```sql
\c prescription_db
```
*(You are now connected to database "prescription_db" as user "postgres")*

**Grant Schema Privileges (Required in newer Postgres versions):**
```sql
GRANT ALL ON SCHEMA public TO prescription_user;
```

---

## 6. Create Tables

While still connected to `prescription_db`, run this command to create the schema:

```sql
CREATE TABLE prescriptions (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(255),
    doctor_name VARCHAR(255),
    hospital_name VARCHAR(255),
    medicine TEXT,
    dosage TEXT,
    date VARCHAR(50),
    extracted_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
*Note: We use `SERIAL` so the ID auto-increments, and `VARCHAR`/`TEXT` for string data.*

---

## 7. Insert Sample Data

Run this query to add some dummy records for testing:

```sql
INSERT INTO prescriptions (patient_name, doctor_name, hospital_name, medicine, dosage, date, extracted_text)
VALUES
('John Doe', 'Dr. Smith', 'City General Hospital', 'Amoxicillin, Ibuprofen', '500mg, 200mg', '2023-10-25', 'Raw OCR text here...'),
('Jane Smith', 'Dr. Adams', 'Valley Medical Center', 'Lisinopril', '10mg', '2023-10-26', 'Raw OCR text here...'),
('Robert Jones', 'Dr. Lee', 'Oakwood Clinic', 'Metformin', '500mg', '2023-10-27', 'Raw OCR text here...'),
('Emily Davis', 'Dr. Patel', 'Sunrise Hospital', 'Atorvastatin', '20mg', '2023-10-28', 'Raw OCR text here...'),
('Michael Brown', 'Dr. Wilson', 'Northside Health', 'Levothyroxine', '50mcg', '2023-10-29', 'Raw OCR text here...');
```

---

## 8. Basic SQL Queries (Cheat Sheet)

You can run these in `psql` or `pgAdmin` to test your data:

**View all data:**
```sql
SELECT * FROM prescriptions;
```

**Search by patient name:**
```sql
SELECT * FROM prescriptions WHERE patient_name ILIKE '%Jane%';
```

**Update a prescription:**
```sql
UPDATE prescriptions SET dosage = '20mg' WHERE id = 2;
```

**Count total prescriptions:**
```sql
SELECT COUNT(*) FROM prescriptions;
```

*(You can type `\q` to quit psql).*

---

## 9 & 10. FastAPI & Environment Configuration

The backend code has already been updated to use this new database. Here is how it works:

**Your `.env` file (`c:\Users\ASUS\OneDrive\Desktop\cyber\project\.env`):**
```env
DB_USER=prescription_user
DB_PASSWORD=prescription123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=prescription_db
```

**Your `backend/database.py`:**
FastAPI uses SQLAlchemy and `psycopg2-binary` to connect. It reads the `.env` file and creates the engine.
```python
DATABASE_URL = "postgresql://prescription_user:prescription123@localhost:5432/prescription_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

## 11. Testing the Setup

1. Open a new terminal (Command Prompt or PowerShell) inside your project folder.
2. Run the FastAPI backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Open your browser and go to `http://localhost:8000/prescriptions`.
4. If you see the 5 sample records we inserted earlier formatted as JSON, **your database connection is working perfectly!**

---

## 12. Using pgAdmin (GUI)

If you prefer clicking instead of typing commands:
1. Open **pgAdmin 4** from your Windows start menu.
2. It will ask for a master password. Enter the one you set during installation (e.g., `admin`).
3. On the left sidebar, expand **Servers** -> **PostgreSQL 16**. (Enter password again if prompted).
4. **To view your tables:** Expand **Databases** -> **prescription_db** -> **Schemas** -> **public** -> **Tables** -> **prescriptions**.
5. **To view data:** Right-click the `prescriptions` table, select **View/Edit Data** -> **All Rows**.
6. **To run custom queries:** Click on `prescription_db`, then click the "Query Tool" icon (looks like a cylinder with a play button) in the top menu bar.

---

## 13. Backend Folder Structure Integration

Here is how the project utilizes PostgreSQL:

*   **`database.py`**: Connects to PostgreSQL using credentials.
*   **`models.py`**: Maps Python classes to PostgreSQL tables (e.g., `class Prescription(Base)` -> `prescriptions` table).
*   **`schemas.py`**: Validates the data going in and out of the API.
*   **`crud.py`**: Writes the actual database logic using SQLAlchemy (e.g., `db.query(models.Prescription).all()`).
*   **`main.py`**: Exposes the CRUD functions as web endpoints.
