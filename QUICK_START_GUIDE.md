# Quick Start Guide - Certificate Feature

## 🚀 Start the Server

```bash
python app.py
```

You'll see:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5001
* Running on http://192.168.1.15:5001
```

## 📋 Complete Workflow

### Step 1: Student Submits Request
- Login as Student
- Fill request form
- Submit

### Step 2: Manager Reviews
- Login as Manager
- View pending requests
- Click "Forward to HOD"

### Step 3: HOD Signs Certificate
- Login as HOD
- Click "Sign & Approve"
- **Enter your name** (e.g., "Dr. John Smith")
- **Select signature style** from 6 font previews
- Click "Generate Certificate"
- ✅ Certificate generated!

### Step 4: Student Downloads
- Login as Student
- Go to Dashboard
- Click "Download Certificate"
- PDF downloads with QR code

### Step 5: Verify Certificate
- Open PDF on same WiFi network
- Use **Google Lens** to scan QR code
- Browser opens verification page
- ✅ Certificate verified!

## 🔑 Key Features

| Feature | Status |
|---------|--------|
| HOD Name Input | ✅ Keyboard input |
| Signature Styles | ✅ 6 font-based options |
| Certificate PDF | ✅ Professional layout |
| QR Code | ✅ Network-scannable |
| Student Download | ✅ Role-protected |
| Verification | ✅ Public endpoint |
| Database | ✅ Full metadata storage |

## 📱 QR Code Details

- **Format**: `http://192.168.1.15:5001/verify/CERT-{timestamp}`
- **Scannable**: Yes, with Google Lens
- **Network**: Same WiFi required
- **Public**: No authentication needed

## 🗂️ File Locations

```
outputs/
├── certificates/     # PDF files
├── signatures/       # HOD signature images
└── qrcodes/         # QR code images
```

## 🔧 Configuration

- **Port**: 5001
- **Host**: 0.0.0.0 (all interfaces)
- **Database**: aifinal
- **Local IP**: 192.168.1.15 (auto-detected)

## ✅ Verification Checklist

- [ ] Server running on 0.0.0.0:5001
- [ ] HOD can enter name
- [ ] 6 signature styles visible
- [ ] Certificate PDF generated
- [ ] QR code created
- [ ] Student can download
- [ ] QR code scans with Google Lens
- [ ] Verification page loads

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| QR won't scan | Ensure server running, same WiFi |
| Wrong IP in QR | Check local IP: `ipconfig` |
| Certificate not found | Verify certificate ID in database |
| Download fails | Check student role and request status |

## 📊 Test Results

```
✓ HOD name input working
✓ Font-based signature selection working
✓ Certificate PDF generation working
✓ QR code generation working
✓ Database storage working
✓ Student download working
✓ Verification endpoint working
✓ All 9 test scenarios passed
```

## 🎯 What's New

1. **Network-Accessible Server**: Changed from localhost to 0.0.0.0
2. **HOD Name in PDF**: Added hod_name parameter to certificate generation
3. **Font-Based Signatures**: 6 signature style options
4. **QR Code Verification**: Public endpoint for scanning
5. **Removed HOD Download**: Only students can download

## 📝 Notes

- All changes are backward compatible
- No database migration needed (certificates table already exists)
- Server runs in debug mode (development only)
- Local IP automatically detected

---

**Status**: ✅ READY TO USE

For detailed information, see:
- `CERTIFICATE_FEATURE_COMPLETE.md` - Full documentation
- `QR_CODE_SETUP.md` - QR code technical details
