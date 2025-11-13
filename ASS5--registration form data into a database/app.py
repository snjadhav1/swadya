from flask import Flask, render_template, request, flash, redirect, send_from_directory
import mysql.connector
import mysql.connector.errors

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

def get_db():
    return mysql.connector.connect(host='localhost', user='root', password='root', database='event_db1')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return redirect('/registration')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO registrations (name, email, mobile, role, password) VALUES (%s, %s, %s, %s, %s)",
                           (request.form['name'], request.form['email'], request.form['mobile'], request.form.get('role', ''), request.form['password']))
            db.commit()
        except mysql.connector.errors.ProgrammingError as e:
            # Likely the `role` column is missing in the DB schema. Inform the developer and avoid a 500.
            db.rollback()
            cursor.close()
            db.close()
            # Provide a helpful flash message pointing to the migration script
            flash('Database schema error: missing column "role". Please run the migration at migrations/add_role_to_registrations.sql or run create_table_all_apps.sql (note: that will DROP and recreate the table).')
            return redirect('/registration')
        except Exception as e:
            db.rollback()
            cursor.close()
            db.close()
            flash('An unexpected database error occurred. See server logs for details.')
            raise
        else:
            cursor.close()
            db.close()
            flash('Registration Done!')
            return redirect('/registration')
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)





# CREATE DATABASE event_db1;

# USE event_db1;

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
# SELECT * FROM registrations ;