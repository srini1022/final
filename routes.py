from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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

@main_blueprint.route('/manager_dashboard')
@role_required('manager')
def manager_dashboard():
    pending_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        WHERE r.status = 'Pending'
        ORDER BY r.created_at DESC
    """)
    all_students = query_db("SELECT * FROM students")
    return render_template('manager_dashboard.html', pending_requests=pending_requests, students=all_students)

@main_blueprint.route('/hod_dashboard')
@role_required('hod')
def hod_dashboard():
    all_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        ORDER BY r.created_at DESC
    """)
    return render_template('hod_dashboard.html', all_requests=all_requests)
