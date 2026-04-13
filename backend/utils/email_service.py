import os
import smtplib
import requests
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def send_otp_email(to_email: str, otp_code: str) -> bool:
    """
    Send OTP email using Gmail SMTP (primary) with Brevo fallback.
    Gmail is more reliable for delivery.
    """

    # Try Gmail SMTP first (more reliable)
    if SMTP_EMAIL and SMTP_PASSWORD:
        success = _send_via_smtp(to_email, otp_code)
        if success:
            return True
        print("⚠️ SMTP failed, trying Brevo fallback...")
    
    # Fallback to Brevo
    if BREVO_API_KEY:
        return _send_via_brevo(to_email, otp_code)
    
    print("❌ ERROR: No email service configured")
    return False


def _send_via_brevo(to_email: str, otp_code: str) -> bool:
    """Send OTP via Brevo API"""
    if not BREVO_API_KEY:
        return False

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {"name": "LIFEASY", "email": SMTP_EMAIL or "jafinarman44@gmail.com"},
        "to": [{"email": to_email}],
        "subject": "Your LIFEASY OTP Code",
        "htmlContent": f"""
            <h2>Your Verification Code</h2>
            <p>Your OTP is: <strong style='font-size:24px'>{otp_code}</strong></p>
            <p>This code is valid for 5 minutes.</p>
            <br>
            <p>Thank you for using LIFEASY!</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        print("📧 Brevo Response:", r.text)

        return r.status_code == 201

    except Exception as e:
        print("❌ Brevo error:", e)
        return False


def _send_via_smtp(to_email: str, otp_code: str) -> bool:
    """Send OTP via Gmail SMTP (fallback method)"""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        print("❌ SMTP credentials not configured")
        return False

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = 'Your LIFEASY OTP Code'
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 30px; border-radius: 10px;">
                <h2 style="color: #333;">Your Verification Code</h2>
                <div style="background: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                    <p style="font-size: 16px; color: #666; margin: 0;">Your OTP is:</p>
                    <p style="font-size: 36px; font-weight: bold; color: #4CAF50; margin: 10px 0;">{otp_code}</p>
                </div>
                <p style="color: #666;">This code is valid for 5 minutes.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">Thank you for using LIFEASY!</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        
        # Send email
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        server.quit()
        
        print(f"✅ Email sent via SMTP to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ SMTP error: {e}")
        return False
