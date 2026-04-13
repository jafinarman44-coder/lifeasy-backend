"""
SMTP Email Test Script for LIFEASY Backend
Tests direct SMTP connection to verify email sending capability
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection and send test email"""
    
    # Get credentials from environment or use test values
    sender_email = os.getenv("SMTP_EMAIL", "test@gmail.com")
    sender_password = os.getenv("SMTP_PASSWORD", "your-app-password")
    receiver_email = os.getenv("TEST_RECEIVER_EMAIL", sender_email)
    
    print("="*60)
    print("LIFEASY SMTP EMAIL TEST")
    print("="*60)
    print(f"Sender: {sender_email}")
    print(f"Receiver: {receiver_email}")
    print(f"SMTP Server: smtp.gmail.com:587")
    print("="*60)
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "LIFEASY SMTP Test - SUCCESS!"
        
        body = """
        🎉 SUCCESS! 
        
        This is a test email from LIFEASY V30 PRO backend.
        
        If you received this email, it means:
        ✅ SMTP configuration is correct
        ✅ Gmail App Password is valid
        ✅ Your network allows SMTP connections
        ✅ Email OTP functionality will work
        
        Timestamp: SMTP test completed successfully
        """
        
        msg.attach(MIMEText(body, "plain"))
        
        # Connect to SMTP server
        print("\n📧 Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        # Enable TLS encryption
        print("🔒 Starting TLS encryption...")
        server.starttls()
        
        # Login
        print(f"🔑 Logging in as {sender_email}...")
        server.login(sender_email, sender_password)
        
        # Send email
        print(f"📤 Sending test email to {receiver_email}...")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
        # Disconnect
        print("🔌 Disconnecting from SMTP server...")
        server.quit()
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Email sent successfully!")
        print("="*60)
        print("\nCheck your inbox at:", receiver_email)
        print("\nYour OTP email system is ready to use! 🚀")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n" + "="*60)
        print("❌ SMTP AUTHENTICATION ERROR")
        print("="*60)
        print(f"\nError Code: {e.smtp_code}")
        print(f"Error Message: {e.smtp_error}")
        print("\nPossible causes:")
        print("1. Gmail App Password is incorrect")
        print("2. 2-Factor Authentication not enabled on Gmail account")
        print("3. Less secure app access not configured")
        print("\nSolution:")
        print("- Go to: https://myaccount.google.com/apppasswords")
        print("- Generate a new App Password for 'Mail'")
        print("- Update .env file with the new password")
        return False
        
    except smtplib.SMTPConnectError as e:
        print("\n" + "="*60)
        print("❌ SMTP CONNECTION ERROR")
        print("="*60)
        print(f"\nError Code: {e.smtp_code}")
        print(f"Error Message: {e.smtp_error}")
        print("\nPossible causes:")
        print("1. Firewall blocking port 587")
        print("2. ISP blocking SMTP connections")
        print("3. Network restrictions")
        print("\nSolution:")
        print("- Check Windows Firewall settings")
        print("- Try different network (mobile hotspot)")
        print("- Contact ISP about SMTP port blocking")
        return False
        
    except smtplib.SMTPException as e:
        print("\n" + "="*60)
        print("❌ SMTP ERROR")
        print("="*60)
        print(f"\nError: {str(e)}")
        print("\nPossible causes:")
        print("1. Gmail security settings blocking connection")
        print("2. Account requires App Password")
        print("3. Temporary Gmail service issue")
        return False
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ UNEXPECTED ERROR")
        print("="*60)
        print(f"\nError Type: {type(e).__name__}")
        print(f"Error: {str(e)}")
        print("\nThis might indicate:")
        print("1. Network connectivity issues")
        print("2. DNS resolution problems")
        print("3. System-level restrictions")
        return False

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Before running this test:\n")
    print("1. Set up Gmail App Password:")
    print("   → Go to: https://myaccount.google.com/apppasswords")
    print("   → Create App Password for 'Mail'")
    print("   → Copy the 16-character password\n")
    print("2. Update backend/.env file:")
    print("   SMTP_EMAIL=your-email@gmail.com")
    print("   SMTP_PASSWORD=xxxx xxxx xxxx xxxx\n")
    
    response = input("Have you configured SMTP credentials? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        test_smtp_connection()
    else:
        print("\n⚠️  Please configure SMTP credentials first!")
        print("\nQuick Setup Guide:")
        print("1. Enable 2FA on your Google Account")
        print("2. Generate App Password at: https://myaccount.google.com/apppasswords")
        print("3. Add to backend/.env:")
        print("   SMTP_EMAIL=your-email@gmail.com")
        print("   SMTP_PASSWORD=your-16-char-app-password")
        print("   TEST_RECEIVER_EMAIL=test-receiver@gmail.com")
