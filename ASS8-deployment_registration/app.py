from flask import Flask, render_template, request, flash, redirect, send_from_directory, session
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

# Get secret key from environment variable or use a placeholder for development
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# MySQL Database Configuration
# Get database credentials from environment variables
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
# Read MYSQL_PORT safely: if env var is missing or empty, default to 3306 (as a string) so int() never receives None
MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or '3306')

# Function to get database connection
def get_db_connection():
    """Create and return a MySQL database connection."""
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT
    )
    return connection

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        role = request.form['role']
        password = request.form['password']
        
        # Insert into database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = """
                INSERT INTO registrations (name, email, mobile, role, password, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (name, email, mobile, role, password, datetime.utcnow())
            
            cursor.execute(query, values)
            connection.commit()
            
            # Get the inserted ID
            user_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            
            # Store user info in session
            session['user_id'] = user_id
            session['user_name'] = name
            
            # Redirect to dashboard after successful registration
            return redirect('/dashboard')
            
        except mysql.connector.Error as err:
            flash(f"Database error: {err}")
            return render_template('registration.html')
    
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/registration')
    
    # Fetch user data from database
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, name, email, mobile, role, created_at FROM registrations WHERE id = %s"
        cursor.execute(query, (session['user_id'],))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not user:
            return redirect('/registration')
        
        return render_template('dashboard.html', user=user)
        
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
        return redirect('/registration')

if __name__ == '__main__':
    app.run(debug=True)





# CREATE DATABASE b3cpokk0w9aeafea5fiw;

# USE b3cpokk0w9aeafea5fiw;

# DROP TABLE IF EXISTS registrations;

# CREATE TABLE registrations (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   name VARCHAR(255) NOT NULL,
#   email VARCHAR(255) NOT NULL,
#   mobile VARCHAR(20) NOT NULL,
#   role VARCHAR(50) NOT NULL,
#   password VARCHAR(255) NOT NULL,
#   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#   INDEX idx_email (email),
#   INDEX idx_created_at (created_at),
#   INDEX idx_role (role)
# );


# -- Sample data for development / testing
# INSERT INTO registrations (name, email, mobile, role, password, created_at) VALUES
#   ('Ram Kumar', 'ram.kumar@example.com', '9123456789', 'helpseeker', 'password123', '2025-11-01 10:00:00'),
#   ('Sita Patil', 'sita.patil@example.com', '9012345678', 'volunteer', 'volunteerpass', '2025-11-02 11:30:00'),
#   ('Mira Joshi', 'mira.joshi@example.com', '9988776655', 'helpseeker', 'securepwd', '2025-11-03 09:00:00');

# -- Verify table contents
# SELECT * FROM registrations LIMIT 10;


# .env

# # Flask Secret Key
# SECRET_KEY=your-secret-key-here

# # MySQL Database Configuration - Clever Cloud
# MYSQL_HOST=b3cpokk0w9aeafea5fiw-mysql.services.clever-cloud.com
# MYSQL_USER=ukqhcfctcttvaxqq
# MYSQL_PASSWORD=28xRu1dL8QxMrp3bibOb
# MYSQL_DATABASE=b3cpokk0w9aeafea5fiw
# MYSQL_PORT=3306

# # Local MySQL Configuration (Commented)
# #MYSQL_HOST=localhost
# #MYSQL_USER=root
# #MYSQL_PASSWORD=root
# #MYSQL_DATABASE=event_db1
# #MYSQL_PORT=3306



# .gitignore

# __pycache__/
# *.py[cod]
# *$py.class
# *.so
# .Python
# env/
# venv/
# ENV/
# .venv
# *.db
# *.sqlite
# *.sqlite3
# .DS_Store
# .env
# .vscode/
# instance/
