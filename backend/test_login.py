"""
Test login with REAL credentials
"""
import requests
import json

# Test login
url = "http://localhost:8000/api/auth/v2/login"
data = {
    "email": "majadar1din@gmail.com",
    "password": "01042010"
}

print(f"Testing login with:")
print(f"Email: {data['email']}")
print(f"Password: {data['password']}\n")

response = requests.post(url, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
