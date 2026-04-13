"""
LIFEASY V27 - SMS OTP Service
Send OTP via SMS for mobile verification
Uses Twilio or SSL Wireless for Bangladesh
"""
import os
import random
from typing import Optional

class SMSOTPService:
    """
    Send OTP via SMS
    Supports multiple SMS gateways
    """
    
    def __init__(self):
        # Configuration
        self.provider = os.getenv("SMS_PROVIDER", "mock")  # twilio, ssl_wireless, mock
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.from_number = os.getenv("TWILIO_FROM_NUMBER", "")
        
        # SSL Wireless (Bangladesh)
        self.ssl_user = os.getenv("SSL_WIRELESS_USER", "")
        self.ssl_password = os.getenv("SSL_WIRELESS_PASSWORD", "")
        self.ssl_sid = os.getenv("SSL_WIRELESS_SID", "")
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate numeric OTP"""
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def send_sms(self, phone: str, message: str) -> bool:
        """
        Send SMS message
        Returns True if sent successfully
        """
        try:
            if self.provider == "twilio":
                return self._send_via_twilio(phone, message)
            elif self.provider == "ssl_wireless":
                return self._send_via_ssl(phone, message)
            else:
                # Mock mode for development
                print(f"📱 MOCK SMS to {phone}: {message}")
                return True
        except Exception as e:
            print(f"❌ SMS send failed: {e}")
            return False
    
    def _send_via_twilio(self, phone: str, message: str) -> bool:
        """Send SMS via Twilio"""
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            message = client.messages.create(
                body=message,
                from_=self.from_number,
                to=phone
            )
            
            print(f"✅ Twilio SMS sent: {message.sid}")
            return True
        except Exception as e:
            print(f"❌ Twilio SMS failed: {e}")
            return False
    
    def _send_via_ssl(self, phone: str, message: str) -> bool:
        """Send SMS via SSL Wireless (Bangladesh)"""
        try:
            import requests
            
            url = "https://smsplus.sslwireless.com/api/v3/send-sms"
            
            payload = {
                "api_token": self.ssl_sid,
                "sid": self.ssl_user,
                "csms_id": self.ssl_sid,
                "msisdn": phone,
                "sms_text": message,
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✅ SSL SMS sent to {phone}")
                return True
            else:
                print(f"❌ SSL SMS failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ SSL SMS exception: {e}")
            return False
    
    def send_otp_sms(self, phone: str, otp: str) -> bool:
        """
        Send OTP via SMS
        Formatted message
        """
        message = f"""Your LIFEASY verification code is: {otp}

This code expires in 5 minutes.

Do not share this code with anyone."""
        
        return self.send_sms(phone, message)


# Global instance
sms_service = SMSOTPService()
