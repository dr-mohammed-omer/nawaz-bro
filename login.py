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
    
    # Extract username and password
    username = form.getvalue('username')
    password = form.getvalue('password')
    
    # Validate input
    if not username or not password:
        print(json.dumps({"success": False, "message": "Username and password are required"}))
        sys.exit()
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query the database for the user
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    # Check if user exists and password is correct
    if user and user[2] == hash_password(password):
        # Authentication successful
        print(json.dumps({"success": True, "message": "Login successful", "user_id": user[0]}))
    else:
        # Authentication failed
        print(json.dumps({"success": False, "message": "Invalid username or password"}))
    
    # Close the database connection
    conn.close()

except Exception as e:
    # Handle any errors
    print(json.dumps({"success": False, "message": f"An error occurred: {str(e)}"}))