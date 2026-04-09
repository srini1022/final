from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
import io
import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from flask_bcrypt import Bcrypt
from database import query_db
from functools import wraps

main_blueprint = Blueprint('main', __name__)
bcrypt = Bcrypt()

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('role') != role:
                flash("Unauthorized access. Please log in with the appropriate role.", "danger")
                return redirect(url_for('main.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        existing_user = query_db("SELECT * FROM users WHERE username=%s OR email=%s", (username, email), fetchone=True)
        if existing_user:
            flash("Username or Email already exists.", "danger")
            return redirect(url_for('main.register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        try:
            user_id = query_db("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                               (username, email, hashed_password, role), commit=True)
            
            if role == 'student':
                name = request.form.get('name')
                usn = request.form.get('usn')
                department = request.form.get('department')
                semester = request.form.get('semester')
                fee_status = request.form.get('fee_status')
                query_db("INSERT INTO students (user_id, name, usn, department, semester, email, fee_status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                         (user_id, name, usn, department, semester, email, fee_status), commit=True)
                
            flash("Registration successful. Please login.", "success")
            return redirect(url_for('main.login'))
        except Exception as e:
            flash(f"Error during registration: {str(e)}", "danger")
            return redirect(url_for('main.register'))

    return render_template('register.html')

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = query_db("SELECT * FROM users WHERE email=%s", (email,), fetchone=True)
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            if user['role'] == 'student':
                return redirect(url_for('main.student_dashboard'))
            elif user['role'] == 'manager':
                return redirect(url_for('main.manager_dashboard'))
            elif user['role'] == 'hod':
                return redirect(url_for('main.hod_dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@main_blueprint.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

@main_blueprint.route('/student_dashboard')
@role_required('student')
def student_dashboard():
    student_details = query_db("SELECT * FROM students WHERE user_id=%s", (session['user_id'],), fetchone=True)
    requests = []
    if student_details:
        requests = query_db("SELECT * FROM requests WHERE student_id=%s ORDER BY created_at DESC", (student_details['student_id'],))
    return render_template('student_dashboard.html', student=student_details, requests=requests)

def verify_signature(public_pem, signature_b64, payload_string):
    if not public_pem or not signature_b64:
        return False
    try:
        public_key = serialization.load_pem_public_key(public_pem.encode('utf-8'))
        signature = base64.b64decode(signature_b64)
        public_key.verify(
            signature,
            payload_string.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

@main_blueprint.route('/generate_keys', methods=['POST'])
@role_required('student')
def generate_keys():
    # 1. Generate RSA Key Pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # 2. Serialize strings
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 3. Save public key
    try:
        query_db("UPDATE students SET public_key = %s WHERE user_id = %s", (public_pem, session['user_id']), commit=True)
        flash("Your new Digital Identity has been generated.", "success")
    except Exception as e:
        flash("Error saving public key.", "danger")
        return redirect(url_for('main.student_dashboard'))

    return send_file(
        io.BytesIO(private_pem),
        as_attachment=True,
        download_name='private_key.pem',
        mimetype='application/x-pem-file'
    )

@main_blueprint.route('/submit_request', methods=['POST'])
@role_required('student')
def submit_request():
    student = query_db("SELECT * FROM students WHERE user_id=%s", (session['user_id'],), fetchone=True)
    if not student:
        flash("Student profile not found. Cannot submit request.", "danger")
        return redirect(url_for('main.student_dashboard'))
        
    if not student.get('public_key'):
        flash("You need to generate a Digital Identity underneath your profile before submitting formal requests.", "danger")
        return redirect(url_for('main.student_dashboard'))

    request_type = request.form.get('request_type')
    reason = request.form.get('reason', '').strip()
    
    # New Exhaustive Fields
    mobile_number = request.form.get('mobile_number')
    pin_code = request.form.get('pin_code')
    telephone = request.form.get('telephone')
    form_email = request.form.get('form_email')
    register_number = request.form.get('register_number')
    course = request.form.get('course')
    faculty = request.form.get('faculty')
    batch = request.form.get('batch')
    study_mode = request.form.get('study_mode')

    if not request_type or not reason:
        flash("Please provide all required fields.", "danger")
        return redirect(url_for('main.student_dashboard'))

    private_key_file = request.files.get('private_key')
    if not private_key_file or private_key_file.filename == '':
        flash("Please upload your downloaded private_key.pem file to cryptographically sign the document.", "danger")
        return redirect(url_for('main.student_dashboard'))
    
    try:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None
        )
    except ValueError:
        flash("Invalid private key file uploaded. Must be a valid unencrypted PEM file.", "danger")
        return redirect(url_for('main.student_dashboard'))

    # Build the payload to sign precisely
    payload = f"{mobile_number}|{pin_code}|{telephone}|{form_email}|{register_number}|{course}|{faculty}|{batch}|{study_mode}|{request_type}|{reason}"
    
    # Cryptographically sign the SHA256 Hash of the payload
    try:
        signature = private_key.sign(
            payload.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        digital_signature_b64 = base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        flash("Cryptography generation failed.", "danger")
        return redirect(url_for('main.student_dashboard'))

    try:
        query_db(
            """INSERT INTO requests (
                student_id, request_type, reason, status, mobile_number, pin_code, telephone, 
                form_email, register_number, course, faculty, batch, study_mode, digital_signature
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (student['student_id'], request_type, reason, 'PENDING_MANAGER', 
             mobile_number, pin_code, telephone, form_email, register_number, 
             course, faculty, batch, study_mode, digital_signature_b64),
            commit=True
        )
        flash(f"Your request for '{request_type}' has been submitted successfully and is pending review.", "success")
    except Exception as e:
        flash(f"Error submitting request: {str(e)}", "danger")

    return redirect(url_for('main.student_dashboard'))

@main_blueprint.route('/manager_dashboard')
@role_required('manager')
def manager_dashboard():
    pending_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department, s.public_key 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        WHERE r.status = 'PENDING_MANAGER'
        ORDER BY r.created_at DESC
    """)
    for req in (pending_requests or []):
        payload = f"{req.get('mobile_number')}|{req.get('pin_code')}|{req.get('telephone')}|{req.get('form_email')}|{req.get('register_number')}|{req.get('course')}|{req.get('faculty')}|{req.get('batch')}|{req.get('study_mode')}|{req.get('request_type')}|{req.get('reason')}"
        req['is_valid_signature'] = verify_signature(req.get('public_key'), req.get('digital_signature'), payload)
    all_students = query_db("SELECT * FROM students")
    return render_template('manager_dashboard.html', pending_requests=pending_requests, students=all_students)

@main_blueprint.route('/manager/update_request/<int:request_id>', methods=['POST'])
@role_required('manager')
def manager_update_request(request_id):
    action = request.form.get('action')
    rejection_reason = request.form.get('rejection_reason', '').strip()
    
    if action == 'forward':
        new_status = 'PENDING_HOD'
    elif action == 'reject':
        if not rejection_reason:
            flash("You must provide a justification when rejecting a request.", "danger")
            return redirect(url_for('main.manager_dashboard'))
        new_status = 'REJECTED'
    else:
        flash("Invalid action.", "danger")
        return redirect(url_for('main.manager_dashboard'))

    try:
        if new_status == 'REJECTED':
            query_db("UPDATE requests SET status = %s, rejection_reason = %s WHERE request_id = %s AND status = 'PENDING_MANAGER'", (new_status, rejection_reason, request_id), commit=True)
        else:
            query_db("UPDATE requests SET status = %s WHERE request_id = %s AND status = 'PENDING_MANAGER'", (new_status, request_id), commit=True)
        action_text = "forwarded to HOD" if new_status == 'PENDING_HOD' else "rejected"
        flash(f"Request {request_id} has been {action_text}.", "success")
    except Exception as e:
        flash(f"Error updating request: {str(e)}", "danger")

    return redirect(url_for('main.manager_dashboard'))

@main_blueprint.route('/hod_dashboard')
@role_required('hod')
def hod_dashboard():
    pending_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department, s.public_key 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        WHERE r.status = 'PENDING_HOD'
        ORDER BY r.created_at DESC
    """)
    for req in (pending_requests or []):
        payload = f"{req.get('mobile_number')}|{req.get('pin_code')}|{req.get('telephone')}|{req.get('form_email')}|{req.get('register_number')}|{req.get('course')}|{req.get('faculty')}|{req.get('batch')}|{req.get('study_mode')}|{req.get('request_type')}|{req.get('reason')}"
        req['is_valid_signature'] = verify_signature(req.get('public_key'), req.get('digital_signature'), payload)

    all_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department, s.public_key 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        ORDER BY r.created_at DESC
    """)
    for req in (all_requests or []):
        payload = f"{req.get('mobile_number')}|{req.get('pin_code')}|{req.get('telephone')}|{req.get('form_email')}|{req.get('register_number')}|{req.get('course')}|{req.get('faculty')}|{req.get('batch')}|{req.get('study_mode')}|{req.get('request_type')}|{req.get('reason')}"
        req['is_valid_signature'] = verify_signature(req.get('public_key'), req.get('digital_signature'), payload)
    return render_template('hod_dashboard.html', pending_requests=pending_requests, all_requests=all_requests)

@main_blueprint.route('/hod/update_request/<int:request_id>', methods=['POST'])
@role_required('hod')
def hod_update_request(request_id):
    action = request.form.get('action')
    rejection_reason = request.form.get('rejection_reason', '').strip()
    
    if action == 'approve':
        new_status = 'APPROVED'
    elif action == 'reject':
        if not rejection_reason:
            flash("You must provide a justification when rejecting a request.", "danger")
            return redirect(url_for('main.hod_dashboard'))
        new_status = 'REJECTED'
    elif action == 'return_to_manager':
        new_status = 'PENDING_MANAGER'
    else:
        flash("Invalid action.", "danger")
        return redirect(url_for('main.hod_dashboard'))

    try:
        if new_status == 'REJECTED':
            query_db("UPDATE requests SET status = %s, rejection_reason = %s WHERE request_id = %s AND status = 'PENDING_HOD'", (new_status, rejection_reason, request_id), commit=True)
        else:
            query_db("UPDATE requests SET status = %s WHERE request_id = %s AND status = 'PENDING_HOD'", (new_status, request_id), commit=True)
        
        if new_status == 'APPROVED':
            action_text = "approved"
        elif new_status == 'REJECTED':
            action_text = "rejected"
        else:
            action_text = "returned to manager for review"
        flash(f"Request {request_id} has been {action_text}.", "success")
    except Exception as e:
        flash(f"Error updating request: {str(e)}", "danger")

    return redirect(url_for('main.hod_dashboard'))
