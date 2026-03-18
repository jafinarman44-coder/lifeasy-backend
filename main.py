from fastapi import FastAPI

app = FastAPI(title="LIFEASY LIVE API")

@app.get("/")
def home():
    return {"status": "LIVE API RUNNING"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/login")
def login(data: dict):
    if data["tenant_id"] == "1001" and data["password"] == "123456":
        return {"token": "demo_token"}
    return {"error": "Invalid credentials"}
