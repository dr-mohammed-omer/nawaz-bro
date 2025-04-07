#!/usr/bin/env python3
import cgi
import json
import sqlite3
import hashlib
import os
import sys

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'db', 'property_deals.db')

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Print necessary headers
print("Content-Type: application/json")
print()  # Empty line to indicate end of headers

try:
    # Get form data
    form = cgi.FieldStorage()
    
    # Extract form values
    username = form.getvalue('username')
    password = form.getvalue('password')
    email = form.getvalue('email')
    first_name = form.getvalue('firstName')
    last_name = form.getvalue('lastName')
    phone = form.getvalue('phone')
    
    # Validate required fields
    if not username or not password or not email or not first_name or not last_name:
        print(json.dumps({"success": False, "message": "All required fields must be filled"}))
        sys.exit()
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print(json.dumps({"success": False, "message": "Username already exists"}))
        conn.close()
        sys.exit()
    
    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        print(json.dumps({"success": False, "message": "Email already exists"}))
        conn.close()
        sys.exit()
    
    # Insert new user
    hashed_password = hash_password(password)
    cursor.execute('''
    INSERT INTO users (username, password, email, first_name, last_name, phone)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, hashed_password, email, first_name, last_name, phone))
    
    # Commit the transaction
    conn.commit()
    
    # Get the new user's ID
    user_id = cursor.lastrowid
    
    # Close the database connection
    conn.close()
    
    # Return success response
    print(json.dumps({"success": True, "message": "Registration successful", "user_id": user_id}))

except sqlite3.IntegrityError as e:
    # Handle database integrity errors
    print(json.dumps({"success": False, "message": "Database error: " + str(e)}))
except Exception as e:
    # Handle any other errors
    print(json.dumps({"success": False, "message": "An error occurred: " + str(e)}))