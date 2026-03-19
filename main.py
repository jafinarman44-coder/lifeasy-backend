from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import random

app = FastAPI(title="LIFEASY SAAS API")

DB = "lifeasy.db"

# -------- MODELS --------
class LoginData(BaseModel):
    phone: str
    password: str

class OTPData(BaseModel):
    phone: str

class VerifyOTP(BaseModel):
    phone: str
    otp: str

# -------- DB --------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        phone TEXT,
        password TEXT,
        tenant_id TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tenants (
        tenant_id TEXT PRIMARY KEY,
        name TEXT,
        balance REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY,
        tenant_id TEXT,
        amount REAL,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS otp (
        phone TEXT,
        code TEXT
    )
    """)

    # demo tenant
    c.execute("SELECT * FROM tenants WHERE tenant_id='1001'")
    if not c.fetchone():
        c.execute("INSERT INTO tenants VALUES (?,?,?)",
                  ("1001","Test Tenant",5000))

    conn.commit()
    conn.close()

init_db()

# -------- OTP --------
@app.post("/api/send-otp")
def send_otp(data: OTPData):
    otp = str(random.randint(1000,9999))

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("DELETE FROM otp WHERE phone=?", (data.phone,))
    c.execute("INSERT INTO otp VALUES (?,?)", (data.phone, otp))

    conn.commit()
    conn.close()

    print(f"OTP for {data.phone}: {otp}")  # console

    return {"message": "OTP sent"}

@app.post("/api/verify-otp")
def verify_otp(data: VerifyOTP):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT code FROM otp WHERE phone=?", (data.phone,))
    row = c.fetchone()

    if not row or row[0] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    conn.close()
    return {"status": "verified"}

# -------- REGISTER --------
@app.post("/api/register")
def register(data: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (NULL,?,?,?)",
              (data["phone"], data["password"], data["tenant_id"]))

    conn.commit()
    conn.close()

    return {"message": "Registered successfully"}

# -------- LOGIN --------
@app.post("/api/login")
def login(data: LoginData):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT tenant_id FROM users WHERE phone=? AND password=?",
              (data.phone, data.password))

    user = c.fetchone()

    if not user:
        return {"status": "guest"}

    tenant_id = user[0]

    c.execute("SELECT name, balance FROM tenants WHERE tenant_id=?",
              (tenant_id,))
    tenant = c.fetchone()

    conn.close()

    return {
        "status": "success",
        "tenant_id": tenant_id,
        "name": tenant[0],
        "balance": tenant[1]
    }

# -------- DASHBOARD --------
@app.get("/api/dashboard/{tenant_id}")
def dashboard(tenant_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT name, balance FROM tenants WHERE tenant_id=?",
              (tenant_id,))
    tenant = c.fetchone()

    if not tenant:
        raise HTTPException(status_code=404)

    c.execute("SELECT SUM(amount) FROM payments WHERE tenant_id=?",
              (tenant_id,))
    paid = c.fetchone()[0] or 0

    conn.close()

    return {
        "name": tenant[0],
        "due": tenant[1],
        "paid": paid
    }

# -------- PAYMENT (SIMULATED) --------
@app.post("/api/pay")
def pay(data: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO payments VALUES (NULL,?,?,?)",
              (data["tenant_id"], data["amount"], "paid"))

    c.execute("UPDATE tenants SET balance = balance - ? WHERE tenant_id=?",
              (data["amount"], data["tenant_id"]))

    conn.commit()
    conn.close()

    return {"message": "Payment Successful ✅"}

@app.get("/")
def root():
    return {"status": "LIVE SAAS"}
