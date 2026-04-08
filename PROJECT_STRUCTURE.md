# Project Architecture & File Documentation

Welcome to the **Role-Based Access Control (RBAC) Student Document Request System** codebase. This document outlines the physical architecture of the application, ensuring that any developer (or evaluator) can understand exactly what each file contributes to the broader ecosystem.

## Root Directory

### 📄 `app.py`
**The Factory Engine & Application Core**
This is the main execution script that boots up the Flask server (`python app.py`). 
- **What it does:** Initializes the Flask application, manages session timeouts, configures secret keys from `.env`, initializes raw extensions (like Database/Bcrypt), registers our application blueprints (found in `routes.py`), and handles global error capturing.

### 📄 `routes.py`
**The Security & Business Logic Router**
This is the heart of the application's processing. 
- **What it does:** It explicitly listens to every URL endpoint (like `/login`, `/submit_request`, `/hod_dashboard`). It holds the `@role_required` decorators preventing students from accessing Manager portals. Critically, **this file handles all Cryptographic Digital Signatures (PKI)** logic—generating RSA `.pem` keys, assembling SHA-256 Hashes, and mathematically verifying forgery statuses when Managers open requests.

### 📄 `database.py`
**The Database Interceptor**
A utility library specifically for standardizing SQL actions cleanly.
- **What it does:** Standardizes connection setups to MySQL using PyMySQL, converting raw SQL rows gracefully into readable Python Dictionaries that `routes.py` can pass directly to HTML templates.

### 📄 `schema.sql`
**The Absolute Database Blueprint**
A raw, automatable MySQL structured dump.
- **What it does:** Contains the DDL (Data Definition Language) to reconstruct the `finalproject` database instantly from scratch. It contains all relationships across `users`, `students`, and `requests`. **Note:** This was recently updated to allocate the `public_key` repository on the `students` table to facilitate cryptography.

### 📄 `README.md`
**The Project Marketing & Setup Guide**
- **What it does:** Provides the high-level onboarding commands to boot the virtual environment, start the server, and lists what is currently completed vs what is upcoming.

### 📄 `update_db.py` & `update_db2.py`
**Temporary Migration Pipelines**
- **What they do:** These are backend scripts we executed out-of-band to dynamically perform "ALTER TABLE" adjustments (like adding `register_number` or `public_key`) without having to manually drop/reset the whole table through `schema.sql`.

---

## 📁 `static/` Directory
Contains all client-side non-template assets.

### 📄 `static/css/style.css`
**The Theme System**
- **What it does:** Implements the custom modern 'glassmorphism' aesthetic, managing all spacing, gradient colors (`var(--primary)` tokens), typography bindings, and table hover effects. It builds the immersive visual experience that sits over the static HTML.

---

## 📁 `templates/` Directory
The client-facing physical Views. Flask securely injects dynamic python variables into these HTML structures utilizing the Jinja2 (`{% ... %}`) templating engine.

### 📄 `templates/base.html`
**The Global Scaffold**
Contains the `<!DOCTYPE html>` layout, imports the main `style.css`, and anchors the dynamic Navbar logic (It displays "Logout" dynamically if `session['user_id']` exists, etc). All other pages physically inject themselves into this file's `{% block content %}`.

### 📄 `templates/login.html` & `templates/register.html`
**The Authentication Gates**
Houses the visual forms enabling students/managers/HODs to register credentials or establish their secure session tokens. 

### 📄 `templates/student_dashboard.html`
**The Origin Point**
- Contains exactly three zones: 
  1. The auto-rendered, read-only applicant identity card.
  2. The actual **Digital Interface** for generating RSA `.pem` files.
  3. The massive Request document form which now requires `.pem` cryptography to physically sign the submission. Also houses the data-table history at the bottom.

### 📄 `templates/manager_dashboard.html`
**The Tier 1 Escalation Console**
Provides a robust data-table for Managers to review `PENDING_MANAGER` tickets. Features `<details>` expansion blocks allowing Managers to view the entire exhaustive form side-by-side with an auto-rendered cryptographic check flag (`VALID` vs `FORGED`). Allows forwarding decisions.

### 📄 `templates/hod_dashboard.html`
**The Tier 2 Executive Console**
The absolute final approval state. Looks similar to the manager dashboard but targets `PENDING_HOD` tickets and includes an ultimate "All Requests" history compendium. Handles Final Signature auditing dynamically.
