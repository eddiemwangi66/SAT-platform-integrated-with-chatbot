from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
import uuid
import mysql.connector
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in a production environment

# Establish MySQL database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Better to use environment variables or other secure methods
    database="login"
)

# Create a cursor to interact with the database
cursor = conn.cursor()

# Create 'phishing_logs' table if it doesn't exist
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

# Index route
@app.route('/phishing', methods=['GET', 'POST'])
def phishing(user=None):
    return render_template('phishing_index.html', user=user)


# send email route
@app.route('/send_email', methods=['GET','POST'])
def send_phishing_email(user=None):
    if request.method == 'POST':
        receiver_email = request.form['email']

        # Set up sender information (better to use environment variables)
        sender_email = "cosymwas254@gmail.com"  # Replace with your email
        sender_password = "blfa psei kxtt fues"  # Avoid storing password in code
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
            
            flash(f"Phishing email sent successfully to {receiver_email}!")
           
             # Ask for user feedback
            user_feedback = request.form.get('user_feedback', '').strip().lower()

            # Log the tracking information to the database with user feedback and reporting status
            log_tracking_info(receiver_email, tracking_id, "Sent", interaction_type=None, feedback=user_feedback, reported=False)

            # Provide training content based on feedback
            if user_feedback == "yes":
                provide_training_content()

             # Ask if the user wants to report the email
            report_email = request.form.get('report_email', '').strip().lower()
            
             # Update the reporting status in the database
            if report_email == "yes":
                log_tracking_info(receiver_email, tracking_id, "Reported", interaction_type=None, feedback=user_feedback, reported=True)
                flash("Thank you for reporting the email. It has been marked as phishing.")

            return redirect(url_for('success_route', email=receiver_email, user=user))  # Redirect to success page after sending email


        except Exception as e:
            app.logger.error(f"Error sending phishing email: {e}")
            flash("An error occurred while sending the phishing email. Please try again later.")

        
            # Log the error status to the database
            log_tracking_info(receiver_email, tracking_id, "Error")
            # Render the error page and pass error_message as parameter
            return render_template('phishing_error.html', user=user, error_message=str(e))

@app.route('/success')
def success(email, user=None):
    return render_template('phishing_success.html', receiver_email=email, user=user)

def log_tracking_info(receiver_email, tracking_id, status, interaction_type=None, feedback=None, reported=False):
    # Log tracking information to the MySQL database
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback = feedback or "No feedback provided"  # Default value if feedback is None
    cursor.execute('''
        INSERT INTO phishing_logs (timestamp, recipient_email, tracking_id, status, interaction_type, feedback, reported)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (timestamp, receiver_email, tracking_id, status, interaction_type, feedback, reported))
    conn.commit()

@app.route('/phishing_training_content')
def provide_training_content(email, user=None):
    # Provide training content based on user feedback
    flash("Training Content:")
    flash("Phishing emails often contain suspicious links or requests for personal information.")
    flash("Please be cautious and verify the authenticity of emails, especially if they request sensitive information.")
    return render_template('phishing_training.html', receiver_email=email, user=user)


if __name__ == '__main__':
    app.run(debug=True)