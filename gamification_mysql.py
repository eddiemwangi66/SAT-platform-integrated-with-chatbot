from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User class
class User:
    def __init__(self, username, db_conn, default_avatar="default.jpg"):
        self.username = username
        self.points = 0
        self.badges = []
        self.db_conn = db_conn
        self.avatar = default_avatar  # Default avatar
        self.initialize_user()
        self.scenario_results = []  # Initialize scenario results list

    def initialize_user(self):
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, points INT, badges TEXT, avatar VARCHAR(255))")
        cursor.execute("INSERT IGNORE INTO users (username, points, badges, avatar) VALUES (%s, 0, '',  %s)", (self.username, self.avatar))
        self.db_conn.commit()

    def set_avatar(self, avatar_path):
        self.avatar = avatar_path
        self.update_database()
        return f"{self.username}'s avatar has been updated to: {self.avatar}"    

    def earn_points(self, points):
        self.points += points
        self.update_database()
        return f"{self.username} earned {points} points! Total points: {self.points}"

    def update_database(self):
        cursor = self.db_conn.cursor()
        # Check if the user exists in the database
        cursor.execute("SELECT points FROM users WHERE username = %s", (self.username,))
        existing_points = cursor.fetchone()

        if existing_points:
            total_points = existing_points[0] + self.points
            cursor.execute("UPDATE users SET points=%s, badges=%s WHERE username=%s", (total_points, ', '.join(self.badges), self.username))
        else:
            # If user not found in the database, insert a new record
            cursor.execute("INSERT INTO users (username, points, badges, avatar) VALUES (%s, %s, %s, %s)",
                           (self.username, self.points, ', '.join(self.badges), self.avatar))

        self.db_conn.commit()

    def earn_badge(self, badge_name):
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            self.update_database()
            return f"{self.username} earned the {badge_name} badge!"

# Leaderboard class
class Leaderboard:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def display_leaderboard(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT username, points FROM users ORDER BY points DESC")
        result = cursor.fetchall()

        leaderboard_data = []
        for i, (username, points) in enumerate(result, start=1):
            leaderboard_data.append({"rank": i, "username": username, "points": points})
        
        return leaderboard_data

# LevelSystem class
class LevelSystem:
    def __init__(self, levels, db_conn):
        self.levels = levels
        self.db_conn = db_conn

    def get_user_level(self, user):
        for i, level_points in enumerate(self.levels, start=1):
            if user.points < level_points:
                return i
        return len(self.levels) + 1  # User surpassed all levels

    def display_user_level(self, user_points):
        level = self.get_user_level(user_points)
        next_level_points = self.levels[level - 1] if level <= len(self.levels) else None
    
        return {"level": level, "next_level_points": next_level_points}
    
    def update_user_level(self, user):
        new_level = self.get_user_level(user)
        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE users SET level=%s WHERE username=%s", (new_level, user.username))
        self.db_conn.commit()

@app.route('/process_scenario', methods=['POST'])
def process_scenario():
    username = request.form['username']
    avatar = request.form['avatar']
    
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']

    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gamification"
    )

    # Check if the user already exists in the database
    cursor = db_connection.cursor()
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # If user already exists, retrieve the user
        current_user = User(username, db_connection)
    else:
        # If user doesn't exist, create a new user
        current_user = User(username, db_connection)
        current_user.set_avatar(avatar)

    # Store the username in the session
    session['username'] = username

    # Redirect to the first scenario
    return redirect(url_for('phishing_scenario'))

@app.route('/phishing_scenario', methods=['GET', 'POST'])
def phishing_scenario():
    if request.method == 'GET':
        # Handle GET request
        question, choices = simulate_phishing_scenario()
        return render_template('phishing_scenario.html', question=question, choices=choices)
    elif request.method == 'POST':
        # Handle POST request
        user_choice = request.form['choice']
        
        # Retrieve the username from the session
        username = session['username']
        
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        )

        # Update user points based on choice
        current_user = User(username, db_connection)
        if user_choice == 'phishing':
            current_user.earn_points(0)
            current_user.earn_badge("threat")
        elif user_choice == 'ignore':
            current_user.earn_points(10)
            current_user.earn_badge("Phishing Awareness")
        elif user_choice == 'report':
            current_user.earn_points(20)
            current_user.earn_badge("Cyber Hero")

        # Add scenario result
        current_user.add_scenario_result("Phishing Scenario", user_choice, current_user.points)

        # Redirect to the next scenario or game over page
        return redirect(url_for('malware_scenario'))

def simulate_phishing_scenario():
    question = "You receive an email from your bank asking you to reset your password. What do you want to do?"
    choices = [
        ("Click on the link in the email", "phishing"),
        ("Ignore the email", "ignore"),
        ("Report the email as phishing", "report")
    ]
    return question, choices


# Malware scenario
@app.route('/malware_scenario', methods=['GET', 'POST'])
def malware_scenario():
    if request.method == 'GET':
        question, choices = simulate_malware_scenario()
        return render_template('malware_scenario.html', question=question, choices=choices)
    elif request.method == 'POST':
        user_choice = request.form['choice']
        
        # Retrieve the username from the session
        username = session['username']
        
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        )

        # Update user points based on choice
        current_user = User(username, db_connection)
        if user_choice == 'malware':
            current_user.earn_points(0)
            current_user.earn_badge("threat")
        elif user_choice == 'ignore':
            current_user.earn_points(10)
            current_user.earn_badge("Phishing Awareness")
        elif user_choice == 'safe':
            current_user.earn_points(20)
            current_user.earn_badge("Cyber Hero")

        # Add scenario result
        current_user.add_scenario_result("Malware Scenario", user_choice, current_user.points)

        # Redirect to the next scenario or game over page
        return redirect(url_for('password_scenario'))
    


def simulate_malware_scenario():
    question = "You receive a pop-up message claiming your computer is infected. It prompts you to download a file to fix the issue. What do you want to do?"
    choices = [
        ("Download and run the file", "malware"),
        ("Close the pop-up and run a malware scan", "safe"),
        ("Ignore the message", "ignore")
    ]
    return question, choices




# Password scenario
@app.route('/password_scenario', methods=['GET', 'POST'])
def password_scenario():
    if request.method == 'GET':
        question, choices = simulate_password_scenario()
        return render_template('password_scenario.html', question=question, choices=choices)
    elif request.method == 'POST':
        user_choice = request.form['choice']
        
        # Retrieve the username from the session
        username = session['username']
        
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        )

        # Update user points based on choice
        current_user = User(username, db_connection)
        if user_choice == 'insecure':
            current_user.earn_points(0)
            current_user.earn_badge("threat")
        elif user_choice == 'threat':
            current_user.earn_points(10)
            current_user.earn_badge("Phishing Awareness")
        elif user_choice == 'secure':
            current_user.earn_points(20)
            current_user.earn_badge("Cyber Hero")

        # Add scenario result
        current_user.add_scenario_result("Password Scenario", user_choice, current_user.points)

        # Redirect to the next scenario or game over page
        return redirect(url_for('game_over'))
    
      
def simulate_password_scenario():
    question = "You are required to setup a password for your account. This account is used in logging into your work office computer. It therefore requires a strong password. What measures will you implement to ensure it remains secure?"
    choices = [
        ("Use personal information as your password e.g your name and date of birth", "insecure"),
        ("Using the same password in all accounts you use to avoid forgetting", "threat"),
        ("Use a passsword of 10 characters and above, using alphabets, numbers and symbols.", "secure")
    ]
    return question, choices



# Leaderboard route
@app.route('/leaderboard')
def show_leaderboard():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gamification"
    )
    leaderboard = Leaderboard(db_connection)
    leaderboard_data = leaderboard.display_leaderboard()
    db_connection.close()

    return render_template('leaderboard.html', leaderboard_data=leaderboard_data)

# User level route
@app.route('/user_level')
def show_user_level():
    # Retrieve the username from the session
    username = session['username']
    
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gamification"
    )
    cursor = db_connection.cursor()
    cursor.execute("SELECT points FROM users WHERE username = %s", (username,))
    user_points = cursor.fetchone()[0]
    db_connection.close()

    level_system = LevelSystem([100, 200, 300, 400, 500], db_connection)
    user_level_data = level_system.display_user_level(user_points)

    return render_template('user_level.html', user_level_data=user_level_data)

# Game over route
@app.route('/game_over', methods=['GET', 'POST'])
def game_over():
    if request.method == 'POST':
        return redirect(url_for('index'))
    else:
        # Retrieve the username from the session
        username = session['username']
        
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        )

        # Get user points and badges
        current_user = User(username, db_connection)
        
        # Calculate total points earned
        total_points_earned = sum([points for _, _, points in current_user.scenario_results])
        
        # Display game over page with summary
        final_score = f"{current_user.username}, your final score is {total_points_earned} points."
        
        # Close the database connection
        db_connection.close()

        return render_template('game_over.html', scenario_results=current_user.scenario_results, final_score=final_score)

# Main route
@app.route('/')
def index():
    return render_template('game_index.html')

if __name__ == "__main__":
    app.run(debug=True)

