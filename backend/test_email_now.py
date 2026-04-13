"""
Test Email Sending - Direct Test
"""
import sys
sys.path.append('E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend')

from utils.email_service import send_otp_email
import random

# Generate test OTP
test_otp = str(random.randint(100000, 999999))
test_email = "majadar1din@gmail.com"

print("="*60)
print("🧪 TESTING EMAIL SENDING")
print("="*60)
print(f"📧 To: {test_email}")
print(f"🔢 OTP: {test_otp}")
print("="*60)

result = send_otp_email(test_email, test_otp)

print("="*60)
if result:
    print("✅ SUCCESS! Check your email inbox (and SPAM folder)")
else:
    print("❌ FAILED! Check error logs above")
print("="*60)
