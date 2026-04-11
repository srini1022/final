# QR Code Verification Setup

## Overview
The certificate QR code now points to a running Flask server that can be scanned from any device on the same WiFi network using Google Lens.

## Configuration

### Server Setup
- **Host**: `0.0.0.0` (all network interfaces)
- **Port**: `5001`
- **Local IP**: `192.168.1.15` (automatically detected)

### QR Code URL Format
```
http://{LOCAL_IP}:5001/verify/{CERTIFICATE_ID}
```

Example:
```
http://192.168.1.15:5001/verify/CERT-1775761945
```

## How It Works

### 1. Certificate Generation Flow
```
HOD enters name → Selects signature style → Generates certificate
    ↓
PDF created with signature and QR code
    ↓
QR code contains: http://192.168.1.15:5001/verify/CERT-{timestamp}
    ↓
Certificate saved to database
```

### 2. QR Code Scanning
```
User opens Google Lens on same WiFi network
    ↓
Scans QR code from certificate
    ↓
Browser opens: http://192.168.1.15:5001/verify/CERT-{timestamp}
    ↓
Verification page displays certificate details
```

### 3. Verification Endpoint
- **Route**: `/verify/<certificate_id>`
- **Method**: GET (public, no authentication required)
- **Response**: HTML page showing certificate details
- **Database Query**: Fetches certificate from `certificates` table

## Running the Server

### Start the Flask Application
```bash
python app.py
```

Expected output:
```
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5001
* Running on http://192.168.1.15:5001
Press CTRL+C to quit
```

### Access Points
- **Local machine**: http://127.0.0.1:5001
- **Same WiFi network**: http://192.168.1.15:5001
- **QR code scanning**: Automatically opens http://192.168.1.15:5001/verify/{CERT_ID}

## Testing QR Code

### Prerequisites
- Flask server running: `python app.py`
- Certificate generated with HOD signature
- Device on same WiFi network as server

### Steps
1. Generate a certificate through HOD dashboard
2. Student downloads the certificate PDF
3. Open PDF and locate QR code
4. Use Google Lens to scan QR code
5. Browser automatically opens verification page
6. Certificate details displayed

## Files Modified

### app.py
- Changed from `app.run(debug=..., port=5001)` 
- To: `app.run(host="0.0.0.0", debug=..., port=5001)`
- This enables network access on all interfaces

### routes.py
- `/verify/<certificate_id>` endpoint (already implemented)
- Generates QR code with local IP: `http://{host_ip}:5001/verify/{certificate_id}`
- Public route (no authentication required)

### utils/pdf_generator.py
- Added `hod_name` parameter to `create_certificate()` function
- HOD name now displayed in PDF below signature

### templates/hod_dashboard.html
- Removed HOD download button from "All Requests History"
- Only students can download certificates

## Database Schema

### Certificates Table
```sql
CREATE TABLE certificates (
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
    FOREIGN KEY (request_id) REFERENCES requests(request_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

## Security Notes

- Verification endpoint is public (no authentication)
- Certificate ID is unique and timestamp-based
- Document hash stored for integrity verification
- QR code contains only the certificate ID (not sensitive data)

## Troubleshooting

### QR Code Not Scanning
- Ensure Flask server is running: `python app.py`
- Check that both devices are on same WiFi network
- Verify local IP is correct: `ipconfig` (Windows) or `ifconfig` (Linux/Mac)

### Verification Page Not Loading
- Check server is running on port 5001
- Verify certificate exists in database
- Check certificate ID in QR code matches database

### Wrong IP in QR Code
- The IP is automatically detected using `socket.gethostbyname(socket.gethostname())`
- If incorrect, manually set in environment or code
- Current IP: 192.168.1.15

## Complete Feature Summary

✅ **HOD Signature**: Font-based signature styles (6 options)
✅ **Certificate Generation**: PDF with student details, HOD signature, and QR code
✅ **QR Code**: Points to running Flask server on local network
✅ **Verification**: Public endpoint to view certificate details
✅ **Student Download**: Only students can download certificates
✅ **Database**: All certificates stored with metadata and hashes
✅ **Network Access**: Server accessible on all network interfaces
