from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in a production environment

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="login"
)

cursor = db_connection.cursor()

# Create users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')
db_connection.commit()

# Show registration form route
@app.route('/register')
def show_registration_form():
    return render_template('register.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return render_template('register.html', message='User already exists. Please choose another email.')

    # Insert the new user
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    db_connection.commit()

    return redirect(url_for('index'))

# Login route
@app.route('/login', methods=['POST'])
def login():
    login_email = request.form.get('login_email')
    login_password = request.form.get('login_password')

    # Check if the user exists and provided correct credentials
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (login_email, login_password))
    user = cursor.fetchone()

    if user:
        session['email'] = login_email
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', message='Invalid email or password')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f'Welcome, {session["email"]}! This is your dashboard.'
    else:
        return redirect(url_for('index'))

# Index route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
