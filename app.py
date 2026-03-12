from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from database import query_db
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_rbac_key_for_flask'
bcrypt = Bcrypt(app)

# Role Required Decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('role') != role:
                flash("Unauthorized access. Please log in with the appropriate role.", "danger")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # Check if user exists
        existing_user = query_db("SELECT * FROM users WHERE username=%s OR email=%s", (username, email), fetchone=True)
        if existing_user:
            flash("Username or Email already exists.", "danger")
            return redirect(url_for('register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert User
        try:
            user_id = query_db("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                               (username, email, hashed_password, role), commit=True)
            
            # If role is student, insert into students table
            if role == 'student':
                name = request.form.get('name')
                usn = request.form.get('usn')
                department = request.form.get('department')
                semester = request.form.get('semester')
                fee_status = request.form.get('fee_status')
                query_db("INSERT INTO students (user_id, name, usn, department, semester, email, fee_status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                         (user_id, name, usn, department, semester, email, fee_status), commit=True)
                
            flash("Registration successful. Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error during registration: {str(e)}", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'manager':
                return redirect(url_for('manager_dashboard'))
            elif user['role'] == 'hod':
                return redirect(url_for('hod_dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/student_dashboard')
@role_required('student')
def student_dashboard():
    student_details = query_db("SELECT * FROM students WHERE user_id=%s", (session['user_id'],), fetchone=True)
    requests = []
    if student_details:
        requests = query_db("SELECT * FROM requests WHERE student_id=%s ORDER BY created_at DESC", (student_details['student_id'],))
    return render_template('student_dashboard.html', student=student_details, requests=requests)

@app.route('/manager_dashboard')
@role_required('manager')
def manager_dashboard():
    # Manager sees all students and requests, maybe pending requests
    pending_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        WHERE r.status = 'Pending'
        ORDER BY r.created_at DESC
    """)
    all_students = query_db("SELECT * FROM students")
    return render_template('manager_dashboard.html', pending_requests=pending_requests, students=all_students)

@app.route('/hod_dashboard')
@role_required('hod')
def hod_dashboard():
    # HOD sees aggregated info or all requests
    all_requests = query_db("""
        SELECT r.*, s.name, s.usn, s.department 
        FROM requests r 
        JOIN students s ON r.student_id = s.student_id 
        ORDER BY r.created_at DESC
    """)
    return render_template('hod_dashboard.html', all_requests=all_requests)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
