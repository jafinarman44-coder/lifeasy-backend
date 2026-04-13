"""
Quick Email Test - Verify Gmail SMTP
"""
import sys
sys.path.append('E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend')

from utils.email_service import send_otp_email

print("="*60)
print("🧪 GMAIL SMTP TEST")
print("="*60)

# Send test OTP
test_email = "majadar1din@gmail.com"
test_otp = "999888"

print(f"\n📧 Sending OTP {test_otp} to {test_email}")
print("⏳ Please wait...\n")

result = send_otp_email(test_email, test_otp)

print("="*60)
if result:
    print("✅ SUCCESS!")
    print(f"\n📬 Check your email: {test_email}")
    print("   • Inbox folder")
    print("   • SPAM folder")
    print("   • Sent from: jafinarman44@gmail.com")
else:
    print("❌ FAILED - Check error logs above")
print("="*60)
