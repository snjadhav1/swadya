from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def db():
    return mysql.connector.connect(host='localhost', user='root', password='root', database='ass7')

@app.route('/')
def index():
    event_id = request.args.get('event', 'ALL')
    
    conn = db()
    c = conn.cursor(dictionary=True)
    
    # Get all events for dropdown
    c.execute('SELECT id, title FROM events ORDER BY date DESC')
    events = c.fetchall()
    
    # Get participants filtered by event
    if event_id == 'ALL':
        c.execute('SELECT p.*, e.title as event_title FROM participants p JOIN events e ON p.event_id=e.id ORDER BY p.created_at DESC')
    else:
        c.execute('SELECT p.*, e.title as event_title FROM participants p JOIN events e ON p.event_id=e.id WHERE p.event_id=%s ORDER BY p.created_at DESC', (event_id,))
    
    data = c.fetchall()
    c.close()
    conn.close()

    return render_template('index.html', data=data, events=events, selected=event_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)





# -- Create database and tables for ASS7
# CREATE DATABASE IF NOT EXISTS ass7;
# USE ass7;

# DROP TABLE IF EXISTS participants;
# DROP TABLE IF EXISTS events;

# CREATE TABLE events (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   title VARCHAR(255) NOT NULL,
#   date DATE NOT NULL,
#   location VARCHAR(255),
#   created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE participants (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   event_id INT NOT NULL,
#   name VARCHAR(255) NOT NULL,
#   email VARCHAR(255) NOT NULL,
#   mobile VARCHAR(20) NOT NULL,
#   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#   FOREIGN KEY (event_id) REFERENCES events(id),
#   INDEX idx_event (event_id)
# );

# INSERT INTO events (title, date, location) VALUES
#   ('Computer Basics Workshop', '2025-11-20', 'Community Center'),
#   ('Internet Safety Session', '2025-11-25', 'Library Hall'),
#   ('Smartphone Training', '2025-12-01', 'Senior Center');

# INSERT INTO participants (event_id, name, email, mobile) VALUES
#   (1, 'Ram Kumar', 'ram@example.com', '9123456789'),
#   (1, 'Sita Patil', 'sita@example.com', '9012345678'),
#   (2, 'Mira Joshi', 'mira@example.com', '9988776655'),
#   (2, 'Amit Shah', 'amit@example.com', '9876543210'),
#   (3, 'Priya Desai', 'priya@example.com', '9765432109');
