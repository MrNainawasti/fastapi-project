import random
import smtplib
from email.message import EmailMessage
from app.core.config import settings

# OTP Generator
def generate_otp() -> str:
    return str(random.randint(100000, 999999))

# Email Sender
def send_otp_email(receiver_email:str, otp:str):
    sender_email = settings.SENDER_EMAIL
    app_password = settings.EMAIL_APP_PASSWORD

    msg = EmailMessage()
    msg['Subject'] = "Verify Your Account"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(f"""\
        Hello!
        Thankyou for registering. Your verification OTP is: {otp}
        Please do not share it with anyone.
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            print(f"Sucessfully sent OTP email to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
