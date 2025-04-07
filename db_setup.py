#!/usr/bin/env python3
import sqlite3
import hashlib
import os

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, 'db')

# Create database directory if it doesn't exist
os.makedirs(db_dir, exist_ok=True)

# Define the absolute path to the database
db_path = os.path.join(db_dir, 'property_deals.db')

# Connect to SQLite database (will create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create properties table
cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    price REAL NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    area REAL NOT NULL,
    description TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create inquiries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties (id)
)
''')

# Create user_activities table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL,
    activity_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Create newsletter_subscribers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insert sample users
sample_users = [
    ('admin', 'admin123', 'admin@hyderabadpropertydeals.com', 'Admin', 'User', '+91 9876543210', 1),
    ('nawaz', 'pass123', 'nawaz@gmail.com', 'nawaz', 'saab', '+91 9876543211'),
    ('zaheer', 'pass456', 'zaheerhussain4@gmail.com', 'zah', 'huss', '+91 9966352220')
]

for user in sample_users:
    try:
        cursor.execute('''
        INSERT INTO users (username, password, email, first_name, last_name, phone, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user[0], hash_password(user[1]), user[2], user[3], user[4], user[5], user[6] if len(user) > 6 else 0))
    except sqlite3.IntegrityError:
        # Skip if user already exists
        pass

# Insert sample properties
sample_properties = [
    ('Luxury Villa in Banjara Hills', 'Banjara Hills, Hyderabad', 25000000, 4, 3, 3500, 
     'This luxury villa in Banjara Hills offers premium living with modern amenities.', 
     'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80'),
    
    ('Modern Apartment in Gachibowli', 'Gachibowli, Hyderabad', 12000000, 3, 2, 1800, 
     'This modern apartment in Gachibowli offers contemporary living in one of Hyderabad\'s most sought-after IT hubs.', 
     'https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80'),
    
    ('Spacious Villa in Jubilee Hills', 'Jubilee Hills, Hyderabad', 38000000, 5, 4, 4200, 
     'This magnificent villa in the prestigious Jubilee Hills area offers unparalleled luxury and space.', 
     'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80'),
    
    ('Penthouse in Hitech City', 'Hitech City, Hyderabad', 18000000, 3, 3, 2200, 
     'Experience luxury living at its finest in this stunning penthouse located in the heart of Hitech City.', 
     'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80')
]

for prop in sample_properties:
    try:
        cursor.execute('''
        INSERT INTO properties (title, location, price, bedrooms, bathrooms, area, description, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', prop)
    except sqlite3.IntegrityError:
        # Skip if property already exists
        pass

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup completed successfully!")