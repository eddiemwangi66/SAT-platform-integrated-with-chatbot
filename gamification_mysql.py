import mysql.connector
import time

class User:
    def __init__(self, username, db_conn):
        self.username = username
        self.points = 0
        self.badges = []
        self.db_conn = db_conn
        self.initialize_user()

    def initialize_user(self):
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, points INT, badges TEXT)")
        cursor.execute("INSERT IGNORE INTO users (username, points, badges) VALUES (%s, 0, '')", (self.username,))
        self.db_conn.commit()

    def earn_points(self, points):
        self.points += points
        self.update_database()
        print(f"{self.username} earned {points} points! Total points: {self.points}")

    def earn_badge(self, badge_name):
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            self.update_database()
            print(f"{self.username} earned the {badge_name} badge!")

    def update_database(self):
        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE users SET points=%s, badges=%s WHERE username=%s", (self.points, ', '.join(self.badges), self.username))
        self.db_conn.commit()

def simulate_phishing_scenario(user):
    print("You receive an email from your bank asking you to reset your password.")
    time.sleep(1)
    print("What do you want to do?")
    time.sleep(1)

    user_choice = input("1. Click on the link in the email\n2. Ignore the email\n3. Report the email as phishing\nYour choice (enter the corresponding number): ")

    if user_choice == "1":
        print("\nYou clicked on the link and entered your credentials. Unfortunately, it was a phishing attempt.")
        print("Result: You fell victim to a phishing attack. Please be cautious and report such incidents.")
    elif user_choice == "2":
        print("\nYou ignored the email. Good decision! Always be cautious with unsolicited emails.")
        print("Result: You successfully avoided a potential phishing attack.")
        user.earn_points(10)
        user.earn_badge("Phishing Awareness")
    elif user_choice == "3":
        print("\nYou reported the email as phishing. Excellent! Reporting suspicious emails helps protect others.")
        print("Result: You took the right action to prevent a potential phishing attack.")
        user.earn_points(20)
        user.earn_badge("Cyber Hero")
    else:
        print("\nInvalid choice. Please enter a valid number.")
        simulate_phishing_scenario(user)

def main():
    username = input("Enter your username: ")

    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gamification"
    )

    current_user = User(username, db_connection)

    print("Welcome to the Cybersecurity Training Game!")
    time.sleep(1)

    print("\nScenario 1: Phishing Simulation")
    simulate_phishing_scenario(current_user)

    print("\nGame Over! Summary:")
    print(f"{current_user.username}, your final score is {current_user.points} points.")
    if current_user.badges:
        print(f"Badges earned: {', '.join(current_user.badges)}")

    # Close the database connection
    db_connection.close()

if __name__ == "__main__":
    main()
