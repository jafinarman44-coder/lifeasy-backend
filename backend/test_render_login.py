"""
Test login on Render backend
"""
import requests
import json

# Test login on Render
url = "https://lifeasy-api.onrender.com/api/auth/v2/login"
data = {
    "email": "majadar1din@gmail.com",
    "password": "01042010"
}

print(f"Testing Render backend login:")
print(f"URL: {url}")
print(f"Email: {data['email']}")
print(f"Password: {data['password']}\n")

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {str(e)}")
