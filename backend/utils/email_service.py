import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")

def send_otp_email(to_email: str, otp: str) -> bool:
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your LIFEASY Verification Code"
        message["From"] = SMTP_FROM
        message["To"] = to_email

        html = f"""
        <html>
        <body>
            <h2>Your LIFEASY OTP Code</h2>
            <p style="font-size:18px; font-weight: bold;">
                Your OTP: <span style="color: #1a73e8;">{otp}</span>
            </p>
            <p>This code is valid for 5 minutes.</p>
        </body>
        </html>
        """

        message.attach(MIMEText(html, "html"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, to_email, message.as_string())
        server.quit()

        print("📧 Email Sent Successfully")
        return True

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        return False
