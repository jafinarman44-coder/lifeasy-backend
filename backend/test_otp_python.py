import requests

url = "http://localhost:8000/api/auth/v2/register-request"
data = {
    "email": "test@example.com",
    "password": "test123",
    "name": "Test User",
    "phone": "+8801712345678"
}

print("Testing OTP Registration...")
print(f"POST {url}")
print(f"Data: {data}")
print()

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
