# Role-Based Access Control (RBAC) Web Application

This is the repository for the final year project: A Role-Based Access Control web application using Flask, MySQL, HTML, CSS, and JS. 
It supports `Student`, `Manager`, and `HOD` roles with unique dashboards and sign-up flows.

---

## 🚀 How to Run the Project

1. **Activate the Virtual Environment:**
   Depending on your terminal in Windows:
   - Command Prompt (cmd): `venv\Scripts\activate.bat`
   - PowerShell: `.\venv\Scripts\Activate.ps1`
   - _You will see `(venv)` prefix your terminal when activated._

2. **Start the Flask Server:**
   Run the following command:
   ```bash
   python app.py
   ```

3. **Open the Application:**
   Open your browser and navigate to: **[http://127.0.0.1:5001](http://127.0.0.1:5001)**

> **Note:** We are using Port `5001` instead of `5000` to avoid conflicts with your system's background services!

---

## 📌 Current Status: What We've Built (Where We Stopped)

### COMPLETED:
- **Database Architecture**: `finalproject` database fully integrated with `.env` configurations. Advanced schema handles expanded attributes.
- **Backend Setup**: `app.py` acts as the factory, `routes.py` manages all business and status logic securely. Password hashing works via `bcrypt`.
- **Frontend & Aesthetics**: Modern UI with a glassmorphism/gradient style is fully integrated (`style.css`).
- **Authentication**: Dynamic Registration and Dashboard Redirection enforcing `@role_required`.
- **Exhaustive Student Form**: A massive request form capturing contact, academic records, and radio metrics.
- **PKI Cryptographic Digital Signatures**: Upgraded from simple canvas drawing to mathematical RSA Cryptography. Students click a generate button to download their `private_key.pem` identity, and their public key saves to the DB dynamically. They then 'Sign' the document by uploading the `.pem` file to generate an encrypted SHA-256 Hash of their request data.
- **Hierarchical Approval Workflow**:
  - **Student**: Generates a request carrying status `PENDING_MANAGER`. Tracks historical tickets.
  - **Manager / HOD Verification**: Dashboard allows admins to expand "View Full Form Details" directly in the table. The server dynamically checks the signature hash against the student's public key to verify mathematically that no data was tampered with, rendering a `✅ VALID` or `❌ FORGED` state before the Managers acts (`Forward to HOD` or `Reject` or `Approve`).

---

## ⏭️ Where to Start Next Time (Next Steps)

Now that the core document request pipeline is functioning flawlessly—including digital tracking and hierarchical authority actions—here is what should be focused on next:

1. **PDF Generation (Automated Certificate Dispatch):**
   - Automatically compile a custom PDF containing the student's details, Date, and the stored **Digital Signature** when the HOD clicks "Approve".
   - Serve the PDF back to the student dashboard so they can download it.

2. **Email Server Notifications:**
   - Integrate `Flask-Mail` so that students receive a live Email Notification when their application status is altered.

3. **HOD Advanced Analytics & Charts:**
   - Integrate `Chart.js` into the HOD dashboard so they can view graphical trends representing the volume of Document Requests.
