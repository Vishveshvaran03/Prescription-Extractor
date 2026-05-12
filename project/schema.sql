-- =====================================================
-- Prescription Extractor — Supabase SQL Schema
-- =====================================================
-- Run this in the Supabase SQL Editor:
-- https://supabase.com/dashboard → Your Project → SQL Editor

-- 1. Create the prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
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

-- 2. Insert sample data for testing
INSERT INTO prescriptions (patient_name, doctor_name, hospital_name, medicine, dosage, date, extracted_text)
VALUES
('John Doe', 'Dr. Smith', 'City General Hospital', 'Amoxicillin, Ibuprofen', '500mg, 200mg', '2023-10-25', 'Sample OCR text for John Doe...'),
('Jane Smith', 'Dr. Adams', 'Valley Medical Center', 'Lisinopril', '10mg', '2023-10-26', 'Sample OCR text for Jane Smith...'),
('Robert Jones', 'Dr. Lee', 'Oakwood Clinic', 'Metformin', '500mg', '2023-10-27', 'Sample OCR text for Robert Jones...'),
('Emily Davis', 'Dr. Patel', 'Sunrise Hospital', 'Atorvastatin', '20mg', '2023-10-28', 'Sample OCR text for Emily Davis...'),
('Michael Brown', 'Dr. Wilson', 'Northside Health', 'Levothyroxine', '50mcg', '2023-10-29', 'Sample OCR text for Michael Brown...');

-- 3. Useful queries for testing
-- View all data:
-- SELECT * FROM prescriptions;

-- Search by patient:
-- SELECT * FROM prescriptions WHERE patient_name ILIKE '%Jane%';

-- Count total:
-- SELECT COUNT(*) FROM prescriptions;

-- Medicine frequency:
-- SELECT medicine, COUNT(*) as frequency FROM prescriptions GROUP BY medicine ORDER BY frequency DESC;
