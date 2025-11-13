from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import mysql.connector
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.permanent_session_lifetime = timedelta(hours=2)
CORS(app)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Change this to your MySQL password
    'database': 'lp23'
}

def get_db():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin:
            session.permanent = True
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sessions ORDER BY date DESC")
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(sessions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['POST'])
def create_session():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (title, category, date, venue, description) VALUES (%s, %s, %s, %s, %s)",
            (data['title'], data['category'], data['date'], data['venue'], data.get('description', ''))
        )
        conn.commit()
        session_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'id': session_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<int:id>', methods=['PUT'])
def update_session(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sessions SET title=%s, category=%s, date=%s, venue=%s, description=%s WHERE id=%s",
            (data['title'], data['category'], data['date'], data['venue'], data.get('description', ''), id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<int:id>', methods=['DELETE'])
def delete_session(id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)



# -- Create database
# CREATE DATABASE IF NOT EXISTS lp23;
# USE lp23;

# -- Create admins table
# CREATE TABLE IF NOT EXISTS admins (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Create sessions table
# CREATE TABLE IF NOT EXISTS sessions (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     category VARCHAR(100) NOT NULL,
#     date DATE NOT NULL,
#     venue VARCHAR(255) NOT NULL,
#     description TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Insert default admin (username: admin, password: admin123)
# INSERT INTO admins (username, password) VALUES 
# ('admin', 'admin123');

# -- Insert sample sessions
# INSERT INTO sessions (title, category, date, venue, description) VALUES
# ('Computer Basics for Beginners', 'Computer Basics', '2025-11-20', 'Community Center', 'Learn the fundamentals of using a computer'),
# ('Smartphone Essentials', 'Smartphone Help', '2025-11-22', 'Public Library', 'Master your smartphone basics'),
# ('Internet Safety Workshop', 'Internet Safety', '2025-11-25', 'Computer Lab', 'Stay safe online');
