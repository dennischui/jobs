
import smtplib
import ssl
from email.message import EmailMessage

def main():

    # --- Configuration ---
    # Your email and the generated App Password (for Gmail)
    # It is recommended to store these in environment variables for security
    sender_email = "nahyeyenah@gmail.com"
    app_password = "your_app_password" # Use the generated App Password here

    # Recipient email address
    receiver_email = "recipient_email@example.com"

    # Email content
    subject = "Python Notification"
    body = "This is an automated email notification sent from a Python script."

    # --- Create the email message ---
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # --- Send the email via Gmail's SMTP server ---
    try:
        # Create a secure SSL context and connect to the server
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Email notification sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check your email/app password and ensure 2-step verification is enabled.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        main()