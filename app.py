from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'db', 'property_deals.db')

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to get database connection
def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required"})
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, password, is_admin FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user and user['password'] == hash_password(password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = bool(user['is_admin'])
        
        # Log user login activity
        cursor.execute("""
            INSERT INTO user_activities (user_id, activity_type, activity_data)
            VALUES (?, 'login', ?)
        """, (user['id'], f"User logged in from {request.remote_addr}"))
        conn.commit()
        
        return jsonify({"success": True, "message": "Login successful", "user_id": user['id'], "is_admin": bool(user['is_admin'])})
    
    return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    phone = data.get('phone')
    
    if not all([username, password, email, first_name, last_name]):
        return jsonify({"success": False, "message": "All required fields must be filled"})
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({"success": False, "message": "Username already exists"})
    
    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return jsonify({"success": False, "message": "Email already exists"})
    
    # Insert new user
    cursor.execute("""
        INSERT INTO users (username, password, email, first_name, last_name, phone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, hash_password(password), email, first_name, last_name, phone))
    
    conn.commit()
    return jsonify({"success": True, "message": "Registration successful"})

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    return render_template('dashboard.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get recent user activities
    cursor.execute("""
        SELECT ua.*, u.username 
        FROM user_activities ua 
        JOIN users u ON ua.user_id = u.id 
        ORDER BY ua.created_at DESC LIMIT 50
    """)
    activities = cursor.fetchall()
    
    # Get recent inquiries
    cursor.execute("""
        SELECT i.*, p.title as property_title 
        FROM inquiries i 
        JOIN properties p ON i.property_id = p.id 
        ORDER BY i.created_at DESC LIMIT 10
    """)
    inquiries = cursor.fetchall()
    
    # Get user statistics
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 0")
    user_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM inquiries")
    inquiry_count = cursor.fetchone()['count']
    
    return render_template('admin_dashboard.html', 
                           activities=activities,
                           inquiries=inquiries,
                           user_count=user_count,
                           inquiry_count=inquiry_count)

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
    property_data = cursor.fetchone()
    
    if property_data:
        return render_template('property_detail.html', property=property_data)
    return "Property not found", 404

@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Please login to submit inquiry"})
    
    data = request.form
    property_id = data.get('property_id')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    
    if not all([property_id, name, email, message]):
        return jsonify({"success": False, "message": "All required fields must be filled"})
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO inquiries (property_id, name, email, phone, message)
            VALUES (?, ?, ?, ?, ?)
        """, (property_id, name, email, phone, message))
        conn.commit()
        return jsonify({"success": True, "message": "Inquiry submitted successfully"})
    except sqlite3.Error as e:
        return jsonify({"success": False, "message": "An error occurred while submitting inquiry"})

if __name__ == '__main__':
    app.run(debug=True)