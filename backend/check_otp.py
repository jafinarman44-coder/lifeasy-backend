"""
Check Latest OTP in Database
"""
import sys
sys.path.append('E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend')

from database_prod import SessionLocal
from models import OTPCode
from datetime import datetime

db = SessionLocal()

print("="*60)
print("🔍 LATEST OTP RECORDS")
print("="*60)

# Get last 5 OTPs for the test email
otps = db.query(OTPCode).filter(
    OTPCode.email == "majadar1din@gmail.com"
).order_by(OTPCode.created_at.desc()).limit(5).all()

if otps:
    print(f"\nFound {len(otps)} OTP records:\n")
    for i, otp in enumerate(otps, 1):
        status = "✅ USED" if otp.is_used else "⏳ ACTIVE"
        expired = "❌ EXPIRED" if (otp.expires_at and datetime.utcnow() > otp.expires_at) else "✅ VALID"
        
        print(f"{i}. OTP: {otp.otp}")
        print(f"   Status: {status} | {expired}")
        print(f"   Created: {otp.created_at}")
        print(f"   Expires: {otp.expires_at}")
        print()
else:
    print("\n❌ No OTP records found for majadar1din@gmail.com")

print("="*60)
db.close()
