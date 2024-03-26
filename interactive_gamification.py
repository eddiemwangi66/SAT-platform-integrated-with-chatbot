from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# User class
class User:
    def __init__(self, username, db_conn, avatar="default.jpg"):
        self.username = username
        self.points = 0
        self.badges = []
        self.db_conn = db_conn
        self.avatar = avatar  # Default avatar
        self.initialize_user()
        self.scenario_results = []  # Initialize scenario results list

        
        # Set the user's session username key
        session['username'] = self.username

    def initialize_user(self):
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT, username VARCHAR(255) PRIMARY KEY, points INT, badges TEXT, avatar VARCHAR(255))")
        cursor.execute("INSERT IGNORE INTO users (user_id, username, points, badges, avatar) VALUES (0, %s, 0, '',  %s)", (self.username, self.avatar))
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
        
    def add_scenario_result(self, scenario_name, user_choice, points, result_text=None):
        scenario_result = {
            "scenario_name": scenario_name,
            "user_choice": user_choice,
            "points": points,
            "result_text": result_text
        }
        self.scenario_results.append(scenario_result)

        self.update_database()

        return scenario_result
class Leaderboard:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def display_leaderboard(self, cursor):
        cursor.execute("""SELECT user_id, username, points FROM users ORDER BY points DESC""")
        leaderboard_data = cursor.fetchall()

        # Convert the list of tuples into a list of dictionaries with the keys 'user_id', 'username', and 'points'
        leaderboard_data = [{"user_id": row[0], "username": row[1], "points": row[2]} for row in leaderboard_data]

        # Set initial position to 0
        rank = 0

        for user in leaderboard_data:
            if rank == 0:
                user["id"] = 1
            else:
                if user["points"] > leaderboard_data[rank-1]["points"]:
                    user["id"] = leaderboard_data[rank-1]["id"]
                else:
                    user["id"] = leaderboard_data[rank-1]["id"] + 1
            rank += 1

        return leaderboard_data
# LevelSystem class
class LevelSystem:
    def __init__(self, level_points, db_conn):
        self.level_points = level_points
        self.db_conn = db_conn

    def display_user_level(self, user_points):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT level FROM users WHERE points = %s", (user_points,))
        level = cursor.fetchone()[0]
        next_level_points = self.level_points[level - 1] if level > 0 else 0

        return{"level": level, "next_level_points": next_level_points}

    def get_user_level(self, user_points):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT level FROM users WHERE points = %s", (user_points,))
        level = cursor.fetchone()[0]
        return level

@app.route('/customize_avatar/<username>', methods=['GET', 'POST'])
def customize_avatar(username, db_conn):
    user = User(username, db_conn)
    existing_avatar = user.get_avatar()

    if existing_avatar:
        return f"{username}, you already have an avatar: {existing_avatar}"

    if request.method == 'POST':
        choice = request.form.get('choice')

        if choice == '1':
            predefined_avatars = ["avatar1.jpg", "avatar2.jpg", "avatar3.jpg"]
            avatar_choice = int(request.form.get('avatar_choice'))

            if 1 <= avatar_choice <= len(predefined_avatars):
                selected_avatar = predefined_avatars[avatar_choice - 1]
                user.set_avatar(selected_avatar)
                return f"Avatar set to: {selected_avatar}"
            else:
                return "Invalid choice."

        elif choice == '2':
            custom_avatar_path = request.form.get('custom_avatar_path')
            user.set_avatar(custom_avatar_path)
            return f"{username}'s avatar set to: {custom_avatar_path}"

        else:
            return "Invalid choice."

    return render_template('customize_avatar.html', username=username, predefined_avatars=predefined_avatars)
#phishing scenario
@app.route('/phishing_scenario', methods=['GET', 'POST'])
def phishing_scenario(user=None):
    if request.method == 'GET':
        # Handle GET request
        question, choices = simulate_phishing_scenario()
        return render_template('phishing_scenario.html', question=question, choices=choices, user=user)

    elif request.method == 'POST':
        # Handle POST request
        user_choice = request.form['choice']

        # Retrieve the username from the session
        username = session['username']

        # Connect to MySQL database
        db_connection = mysql.connector.connect(host="localhost",
            user="root",
            password="",
            database="gamification"
        )

        current_user = User(username, db_connection)

        result_text = ""

        if user_choice == 'phishing':
            result_text = "\nYou clicked on the link and entered your credentials. Unfortunately, it was a phishing attempt."
            current_user.earn_points(0)
            current_user.earn_badge("threat")
        elif user_choice == 'ignore':
            result_text = "\nYou ignored the email. Good decision! Always be cautious with unsolicited emails."
            current_user.earn_points(10)
            current_user.earn_badge("Phishing Awareness")
        elif user_choice == 'report':
            result_text = "\nYou reported the email as phishing. Excellent! Reporting suspicious emails helps protect others."
            current_user.earn_points(20)
            current_user.earn_badge("Cyber Hero")
        else:
            result_text = "\nInvalid choice. Please select a valid action."

        # Add scenario result
        scenario_result= {
            "message": [result_text[0], result_text[1:]],
            "result_text": result_text
        }

        return render_template('phishing_scenario.html', scenario_result=scenario_result, user=user)
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
def malware_scenario(user=None):
    if request.method == 'GET':
        # Handle GET request
        question, choices = simulate_malware_scenario()
        return render_template('malware_scenario.html', question=question, choices=choices, user=user)
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

        result_text = ""

        if user_choice == 'malware':
            result_text = "\nYou downloaded and ran the file. Unfortunately, it was malware." \
                          "\nYour computer is now infected. Always be cautious about unexpected downloads."
            current_user.earn_points(0)
            current_user.earn_badge("threat")
        elif user_choice == 'ignore':
            result_text = "\nYou ignored the message. Wise choice! Don't trust unsolicited pop-ups." \
                          "Result: You successfully avoided a potential malware infection."
            current_user.earn_points(10)
            current_user.earn_badge("Phishing Awareness")
        elif user_choice == 'safe':
            result_text = "\nYou closed the pop-up and ran a malware scan. Good decision!" \
                          "\nResult: You successfully avoided a malware infection."
            current_user.earn_points(20)
            current_user.earn_badge("Cyber Hero")

        else:
            result_text = "\nInvalidchoice. Please select a valid action."

        # Add scenario result
        scenario_result = {
            "message": [result_text[0], result_text[1:]],
            "result_text": result_text
        }

        # Close the database connection
        db_connection.close()

        return render_template('malware_scenario.html', scenario_result=scenario_result, user=user)
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
def password_scenario(user=None):
    if request.method == 'GET':
        # Handle GET request
        question, choices = simulate_password_scenario()
        return render_template('password_scenario.html', question=question, choices=choices, user=user)
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
        result_text = ""

        if user_choice == 'insecure':
            result_text = "\nYou used personal information as your password. Unfortunately it's not secure. It can be easily guessed. " \
                          "Result: You are at risk of your password to leak. Always use a strong password that is known to you omly."
            current_user.earn_points(0)
            current_user.earn_badge("threat")
        elif user_choice == 'threat':
            result_text = "\nYou used similar passwords for different accouts. It is not a secure practice if one account is compromised then others are at risk" \
                          "Result: you are at risk if one of the password to the accounts is discovered. Avoid using similar passwords for different accounts"
            current_user.earn_points(0)
            current_user.earn_badge("threat")
            result_text = ""

        elif user_choice == 'secure':
            result_text = "\n You  used a minimum of 10 characters. Great choice!" \
                          "Result: You have chosen a strong password. "
            current_user.earn_points(20)
            current_user.earn_badge("Cyber Hero")

        else:
            result_text = "\nInvalid choice. Please select a valid action."

        # Add scenario result
        current_user.add_scenario_result("Password Scenario", user_choice, current_user.points, result_text)

        # Close the database connection
        db_connection.close()

  # Redirect to the game summary page after handling the user's choice
    return redirect(url_for('game_summary_route', username=session['username'], user=user))
def simulate_password_scenario():
    question = "You are required to setup a password for your account. This account is used in logging into your work office computer. It therefore requires a strong password. What measures will you implement to ensure it remains secure?"
    choices = [
        ("Use personal information as your password e.g your name and date of birth", "insecure"),
        ("Using the same password in all accounts you use to avoid forgetting", "threat"),
        ("Use a password of 10 characters and above, using alphabets, numbers and symbols.", "secure")
    ]
    return question, choices


# Leaderboard route
# Leaderboard route
@app.route('/leaderboard')
def show_leaderboard(user=None):
    with mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        ) as db_connection:
        cursor = db_connection.cursor()
        leaderboard = Leaderboard(db_connection)
        leaderboard_data = leaderboard.display_leaderboard(cursor)

    return render_template('leaderboard.html', leaderboard_data=leaderboard_data, user=user)
# User level route
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

    level_system =LevelSystem([100, 200, 300, 400, 500], db_connection)
    user_level_data = level_system.display_user_level(user_points)

    return render_template('user_level.html', user_level_data=user_level_data)
#game summary route
@app.route('/game_summary/<username>', methods=['GET', 'POST'])
def game_summary(username, user=None):
    if request.method == 'POST':
        # Handle form submission
        pass

    with mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        ) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT username, points FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

    return render_template('game_summary.html', username=user_data[0], points=user_data[1], user=user)

# Game over route
@app.route('/game_over', methods=['GET', 'POST'])
def game_over(user=None):
    if request.method == 'POST':
        scenario_results = session['scenario_results']
        final_score = sum([result['points'] for result in scenario_results])

        with mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        ) as db_connection:

            leaderboard = Leaderboard(db_connection)
            leaderboard_data, total_users = leaderboard.display_leaderboard(db_connection.cursor())

            username = session['username']
            user_level = user_level(db_connection, username)
            user_level_data = user_level.display_user_level()

        session.clear()

        return render_template('game_over.html', scenario_results=scenario_results, final_score=final_score, leaderboard_data=leaderboard_data, user_level_data=user_level_data, user=user)

    else:
        return render_template('game_over.html', scenario_results=[], final_score=0, leaderboard_data=[], user_level_data=[])
@app.route('/game_index', methods=['GET', 'POST'])
def game_index(user=None):
    if request.method == 'POST':
        username = request.form['username']
        avatar = request.form['avatar']

        # Connect to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gamification"
        )

        # Create a new User object with the provided username and avatar
        user = User(username, db_connection, avatar)

        # Close the database connection
        db_connection.close()

        # Redirect the user to the first scenario
        return redirect(url_for('phishing_scenario_route'))

    return render_template('game_index.html', user=None)


if __name__ == "__main__":
    app.run(debug=True)