from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime, timedelta
import uuid
import json
from difflib import get_close_matches
import smtplib
from email.mime.text import MIMEText
from interactive_module import *
from interactive_phishing import *
from interactive_gamification import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in a production environment

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'cosymwas254@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'blfa psei kxtt fues'  # Replace with your Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = 'SAT PLATFORM <your_email@gmail.com>'
mail = Mail(app)

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your database password
    database="login"
)

cursor = db_connection.cursor(named_tuple=True)

# Create users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL
    )
''')
db_connection.commit()

# Create password_resets table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS password_resets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        token VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (email) REFERENCES users (email)
    )
''')
db_connection.commit()




# Routes for serving the pages

@app.route('/home')
def home_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return home(user=user)
        else:
            # Handle the case when user_data is None
            return home(user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))


@app.route('/quiz',  methods=['GET', 'POST'])
def quiz_route():
        # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return quiz(user=user)
        else:
            # Handle the case when user_data is None
            return quiz(user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
    

@app.route('/quiz_summary', methods=['GET'])
def quiz_summary_route():
    quiz_summary()
    return quiz_summary()


@app.route('/simulation', methods=['GET'])
def simulation_route():
    simulation()
    return simulation()

@app.route('/simulation_response', methods=['POST'])
def simulation_response_route():
    simulation_response()
    return simulation_response()

@app.route('/simulation_result', methods=['GET'])
def simulation_result_route():
    simulation_result()
    return simulation_result()



@app.route('/real_life_situation', methods=['GET'])
def real_life_situation_route():
    real_life_situation()
    return real_life_situation()


@app.route('/phishing')
def phishing_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data[0], 'username': user_data[1]}  # Access tuple elements by index
            return phishing(user=user)
        else:
            # Handle the case when user_data is None
            return phishing(user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))

    
@app.route('/send_email_route', methods=['POST'])    
def send_phishing_email_route():
     # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data[0], 'username': user_data[1]}  # Access tuple elements by index
            return send_phishing_email(user=user)
        else:
            # Handle the case when user_data is None
            return send_phishing_email(user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))

    
   
@app.route('/success')
def success_route():
    email = request.args.get('email')

    if email is None and 'email' in session:
        email = session['email']

    if email:
        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data[0], 'username': user_data[1]}
        else:
            user = None
    else:
        # Handle the case when 'email' is not provided
        return redirect(url_for('index'))

    return success(email, user)

@app.route('/Phishing training content')
def provide_training_content_route():
    email = request.args.get('email')

    if email is None and 'email' in session:
        email = session['email']

    if email:
        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data[0], 'username': user_data[1]}
        else:
            user = None
    else:
        # Handle the case when 'email' is not provided
        return redirect(url_for('index'))

    return provide_training_content(email, user)



# gamification app route
@app.route('/game_index', methods=['GET', 'POST'])
def game_index_route():
   # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return game_index(user=user)
        else:
            # Handle the case when user_data is None
            return game_index(user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
    
@app.route('/phishing_scenario', methods=['GET', 'POST'])
def phishing_scenario_route():
   # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return phishing_scenario(user=user)
        else:
            # Handle the case when user_data is None
            return phishing_scenario(user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
@app.route('/malware_scenario', methods=['GET', 'POST'])
def malware_scenario_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return malware_scenario(user=user)
        else:
            # Handle the case when user_data is None
            return redirect(url_for('index'))
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))

@app.route('/password_scenario_route', methods=['GET', 'POST'])
def password_scenario_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return password_scenario(user=user)
        else:
            # Handle the case when user_data is None
            return redirect(url_for('index'))
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))

@app.route('/show_leaderboard_route')
def show_leaderboard_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additionaluser information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return show_leaderboard(user=user)
        else:
            # Handle the case when user_data is None
            return redirect(url_for('index'))
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))

@app.route('/game_summary_route', methods=['GET', 'POST'])
def game_summary_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return game_summary(username=user_data.username, user=user)
        else:
            # Handle the case when user_data is None
            return redirect(url_for('index'))
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
@app.route('/game_over_route', methods=['GET', 'POST'])
def game_over_route():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return game_over(user=user)
        else:
            # Handle the case when user_data is None
            return redirect(url_for('index'))
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))


@app.route('/education')
def education():
      # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return render_template('education.html', user=user)
        else:
            # Handle the case when user_data is None
            return render_template('education.html', user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
   


@app.route('/password')
def password():
    # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return render_template('password.html', user=user)
        else:
            # Handle the case when user_data is None
            return render_template('password.html', user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
   
@app.route('/Social_engineering')
def Social_engineering():
     # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return render_template('social_engineering.html', user=user)
        else:
            # Handle the case when user_data is None
            return render_template('social_engineering.html', user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
   
      
@app.route('/phishing_education')
def phishing_education():
     # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return render_template('phishing_education.html', user=user)
        else:
            # Handle the case when user_data is None
            return render_template('phishing_education.html', user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
   

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        return redirect(url_for('result', email=email))
    return render_template('index.html')


@app.route('/result/<email>')
def result(email):
    return render_template('result.html', email=email)


# Show registration form route
@app.route('/register')
def show_registration_form():
    return render_template('register.html')


# Registration route
@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')

    # Check if the user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        flash('User already exists. Please choose another email.', 'danger')
        return redirect(url_for('show_registration_form'))

    # Hash the password before storing
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the new user
    cursor.execute("INSERT INTO users (email, password, username) VALUES (%s, %s, %s)",
                   (email, hashed_password, username))
    db_connection.commit()

    flash('Registration successful. Please log in.', 'success')
    return redirect(url_for('index'))


# Forgot password route
# Forgot password route
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Check if the email exists in the users table
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                # Generate a random token
                token = str(uuid.uuid4())

                # Insert the token and email into the password_resets table
                cursor.execute("INSERT INTO password_resets (email, token) VALUES (%s, %s)", (email, token))
                db_connection.commit()

                # Send the password reset email to the user
                send_password_reset_email(email, token, user)
                flash('An email has been sent to you with instructions to reset your password.', 'info')

                return render_template('password_reset.html', token=token, email=email)
            else:
                flash('There is no user with this email address.', 'danger')

    return render_template('forgot_password.html')

# Reset password route
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')

        # Check if the token is valid and not expired
        if check_token(email, token):
            # Update the user's password
            hashed_password = generate_password_hash(new_password, method='sha256')
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            db_connection.commit()

            # Delete the reset token
            cursor.execute("DELETE FROM password_resets WHERE email = %s", (email,))
            db_connection.commit()

            flash('Password reset successful. Please log in with your new password.', 'success')
            return redirect(url_for('index'))

    return render_template('forgot_password_success.html', token=token)



# Function to check token validity and expiration
def check_token(email, token):
    cursor.execute("SELECT * FROM password_resets WHERE email = %s AND token = %s", (email, token))
    reset = cursor.fetchone()

    if reset:
        # Check if the token is not expired
        now = datetime.utcnow()
        token_created_at = reset.created_at
        time_diff = now - token_created_at

        expiration_period = timedelta(hours=1)

        return time_diff < expiration_period

    return False



# send email route
@app.route('/send_forgot_password_email', methods=['GET', 'POST'])
def send_password_reset_email(email, token, user):
    email = request.form.get('email')

    if request.method == 'POST':
        receiver_email = email

        # Set up sender information (better to use environment variables)
        sender_email = "cosymwas254@gmail.com"  # Replace with your email
        sender_password = "blfa psei kxtt fues"  # Avoid storing password in code
        smtp_server = "smtp.gmail.com"

        # Load email template
        html = render_template('password_reset.html', user=user, token=token)
        subject = 'Password Reset Request'
        recipients = [email]

        # Use Flask-Mail to send the email
        message = Message(subject, recipients=recipients, html=html)
        message.sender = sender_email
        message.password = sender_password

        try:
            server = smtplib.SMTP(smtp_server)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send(message)
            server.quit()
            flash('A password reset email has been sent to your email address.', 'success')
            return redirect(url_for('forgot_password'))
        except Exception as e:
            flash('An error occurred while sending the password reset email. Please try again later.', 'danger')
            return str(e)

    return render_template('forgot_password_email.html', email=email)


# Login route
@app.route('/login', methods=['POST'])
def login():
    login_email = request.form.get('login_email')
    login_password = request.form.get('login_password')

    # Check if the user exists and provided correct credentials
    cursor.execute("SELECT * FROM users WHERE email = %s", (login_email,))
    user = cursor.fetchone()

    if user and check_password_hash(user.password, login_password):
        session['email'] = login_email
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', message='Invalid email or password')


# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return render_template('dashboard.html', user=user)
        else:
            return render_template('dashboard.html', user=None)
    else:
        return redirect(url_for('index'))


# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


# Load the knowledge base
def load_knowledge_base(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Save the knowledge base
def save_knowledge_base(file_path, data):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    else:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        if existing_data != data:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
# Find the best match
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def search_keyword(keyword, knowledge_base):
    for q in knowledge_base["questions"]:
        if keyword in q["question"].lower():
            return q["answer"]
    return None

# Get the answer for a question
def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

   # Try to find a direct match
    direct_match = get_answer_for_question(question, knowledge_base)
    if direct_match:
        return direct_match

    # If no direct match, perform a keyword-based search
    tokens = question.lower().split()
    for token in tokens:
        response = search_keyword(token, knowledge_base)
        if response:
            return response

    return None

# Load the knowledge base
knowledge_base = load_knowledge_base('knowledge_base.json')


# Render the initial page
@app.route('/chatbot')
def chatbot():
     # Check if 'email' is in session
    if 'email' in session:
        user_email = session['email']

        # Fetch additional user information including username
        cursor.execute("SELECT email, username FROM users WHERE email = %s", (user_email,))
        user_data = cursor.fetchone()

        if user_data:
            user = {'email': user_data.email, 'username': user_data.username}
            return render_template('chatbot.html', bot_response='', user=user)
        else:
            # Handle the case when user_data is None
            return render_template('chatbot.html', bot_response='', user=None)
    else:
        # Handle the case when 'email' is not in session
        return redirect(url_for('index'))
   
    


# Handle the form submission
@app.route('/ask', methods=['POST'])
def ask():
    # Get the user's input from the form
    user_input = request.form['user_input']

    # Find the best match for the user's input
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    # If a match is found, get the answer and return it
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({"bot_response": answer})

    # If no match is found, update the conversation and ask the user to teach the bot
    else:
        return jsonify({"bot_response": "I don't know the answer. Can you teach me?"})


# Handle the form submission for teaching the bot a new response
@app.route('/teach', methods=['POST'])
def teach():
    # Get the new answer from the form
    new_answer = request.form['new_answer']

    # If the user doesn't want to teach, skip the process
    if new_answer.lower() == 'skip':
        return jsonify({"status": "skipped"})

    # Add the new question and answer to the knowledge base
    knowledge_base["questions"].append({"question": request.form['user_input'], "answer": new_answer})
    save_knowledge_base('knowledge_base.json', knowledge_base)

    return jsonify({"status": "success"})


# Handle the form submission for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')

    # Find the best match for the user's input
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    # If a match is found, get the answer and return it
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return render_template('chatbot.html', user_input=user_input, bot_response=answer)

    # If no match is found, update the conversation and ask the user to teach the bot
    else:
        return render_template('chatbot.html', user_input=user_input, bot_response="I don't know the answer. Can you teach me?")


if __name__ == '__main__':
    app.run(debug=True)


