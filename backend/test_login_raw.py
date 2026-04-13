import requests

url = "https://lifeasy-api.onrender.com/api/auth/v2/login"
data = {
    "email": "majadar1din@gmail.com",
    "password": "01042010"
}

response = requests.post(url, json=data, timeout=30)
print(f"Status: {response.status_code}")
print(f"Response Text: {response.text}")
