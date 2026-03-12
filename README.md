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
- **Database Architecture**: `finalproject` database with `users`, `students`, and `requests` tables is populated.
- **Backend Setup**: `app.py` acts as the factory, `routes.py` handles business logic securely, and `database.py` handles PyMySQL connections. Password hashing is actively working via `bcrypt`.
- **Security & Config**: Centralized configuration via `config.py`. All sensitive database credentials and Flask keys are securely stored and loaded from the new `.env` file (see `.env.example`).
- **Frontend & Aesthetics**: Modern UI with a glassmorphism/gradient style is fully integrated (`style.css`).
- **Authentication**: 
  - Dynamic Registration Form: Students see extra inputs (USN, Dept) automatically via JS toggles.
  - Login system checks passwords and session roles.
- **Role-Based Redirection**: Successfully restricting access and mapping `@role_required` decorators.
  - Students go to `/student_dashboard`
  - Managers go to `/manager_dashboard`
  - HODs go to `/hod_dashboard`

---

## ⏭️ Where to Start Next Time (Next Steps)

Right now, the UI for the dashboards exists, but the **internal logic for making and managing requests is not yet implemented.** 

Here is what you should focus on next time you open the project:

1. **Student Dashboard - Submitting Requests:**
   - Create a form in `student_dashboard.html` that allows the student to submit a new request (e.g., Leave, Fee Extension).
   - Write a Flask `POST` route in `app.py` to insert this into the `requests` table in MySQL.

2. **Manager Dashboard - Approving/Rejecting:**
   - The Buttons for "Approve" and "Reject" are currently just triggering a JavaScript `alert()`.
   - Update `app.py` to accept POST requests that update the `status` column in the `requests` table from "Pending" to "Approved" or "Rejected".

3. **HOD Dashboard - Advanced Analytics:**
   - Currently, the HOD just sees all requests in a table. Next, implement data aggregations (e.g., "Total Students", "Total Pending Requests").
