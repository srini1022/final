-- Add certificates table to aifinal database
-- Run this SQL to create the certificates table

CREATE TABLE IF NOT EXISTS certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    certificate_id VARCHAR(50) UNIQUE NOT NULL,
    request_id INT NOT NULL,
    student_id INT NOT NULL,
    student_name VARCHAR(100),
    department VARCHAR(50),
    request_type VARCHAR(50),
    signature_path TEXT,
    pdf_path TEXT,
    qr_path TEXT,
    document_hash TEXT,
    verification_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES requests(request_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Add certificate_id column to requests table if not exists
ALTER TABLE requests ADD COLUMN IF NOT EXISTS certificate_id VARCHAR(50);