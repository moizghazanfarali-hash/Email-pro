import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_personalized_email(to_email, subject, body):
    # .env se data uthana
    SENDER_EMAIL = os.getenv("EMAIL_USER").strip()
    RAW_PASS = os.getenv("EMAIL_PASS")
    
    # Password se spaces khatam karna (Zaroori step!)
    APP_PASSWORD = RAW_PASS.replace(" ", "").strip() if RAW_PASS else ""

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email

    try:
        # SSL connection setup
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Login/Sending Error: {e}")
        return False