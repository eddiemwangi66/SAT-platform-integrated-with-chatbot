import smtplib
from email.mime.text import MIMEText
import uuid
import mysql.connector
import datetime
import os

# Create a MySQL database connection and cursor
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="login"
)
cursor = conn.cursor()

# Create the 'phishing_logs' table if it doesn't exist
cursor.execute('''
   CREATE TABLE IF NOT EXISTS phishing_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        recipient_email VARCHAR(255),
        tracking_id VARCHAR(36),
        status VARCHAR(20),
        interaction_type VARCHAR(20),
        feedback VARCHAR(255),
        reported BOOLEAN
    )           
''')
conn.commit()

def send_phishing_email():
    # Get user input for the recipient's email
    receiver_email = input("Enter the recipient's email address: ")

    # Set up sender information
    sender_email = "cosymwas254@gmail.com"  # Replace with your email
    sender_password = "blfa psei kxtt fues"
    smtp_server = "smtp.gmail.com"

    # Create a unique identifier for tracking
    tracking_id = str(uuid.uuid4())

    # Create the email message
    phishing_subject = "Important Account Security Update"
    phishing_body = f"""
    Dear User,

    We have detected suspicious activity on your account. Please click on the following link
    to verify your identity and secure your account:

    https://malicious-website.com/verify?user=target_user&tracking_id={tracking_id}

    If you find this email suspicious, please report it to your IT department.

    Thank you for your cooperation.

    Sincerely,
    Your IT Security Team
    """

    message = MIMEText(phishing_body)
    message["Subject"] = phishing_subject
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, 587) as server:
            # Start TLS for security
            server.starttls()
            # Login to the email account
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())

        print(f"Phishing email sent successfully to {receiver_email}!")

    
        # Ask for user feedback
        user_feedback = input("Was this email suspicious? (Yes/No): ").strip().lower()

        # Log the tracking information to the database with user feedback and reporting status
        log_tracking_info(receiver_email, tracking_id, "Sent", interaction_type=None, feedback=user_feedback, reported=False)


        # Provide training content based on feedback
        if user_feedback == "yes":
            provide_training_content()

        # Ask if the user wants to report the email
        report_email = input("Do you want to report this email as phishing? (Yes/No): ").strip().lower()

        # Update the reporting status in the database
        if report_email == "yes":
            log_tracking_info(receiver_email, tracking_id, "Reported", interaction_type=None, feedback=user_feedback, reported=True)
            print("Thank you for reporting the email. It has been marked as phishing.")


    except Exception as e:
        print(f"Error sending phishing email: {e}")

        # Log the tracking information to the database
        log_tracking_info(receiver_email, tracking_id, "Error", interaction_type=None)

def log_tracking_info(receiver_email, tracking_id, status, interaction_type=None, feedback=None, reported=False):
    # Log tracking information to the MySQL database
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback = feedback or "No feedback provided"  # Default value if feedback is None
    cursor.execute('''
        INSERT INTO phishing_logs (timestamp, recipient_email, tracking_id, status, interaction_type, feedback, reported)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (timestamp, receiver_email, tracking_id, status, interaction_type, feedback, reported))
    conn.commit()
    
def provide_training_content():
    # Provide training content based on user feedback
    print("Training Content:")
    print("Phishing emails often contain suspicious links or requests for personal information.")
    print("Please be cautious and verify the authenticity of emails, especially if they request sensitive information.")

if __name__ == "__main__":
    send_phishing_email()
    # Optionally, you may query the database for analysis purposes
    cursor.execute("SELECT * FROM phishing_logs")
    print("Phishing Logs:")
    for row in cursor.fetchall():
        print(row)

# Close the database connection when done
cursor.close()
conn.close()
