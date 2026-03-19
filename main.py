from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="LIFEASY PRO API")

DB = "lifeasy.db"

# ---------- MODELS ----------
class LoginData(BaseModel):
    tenant_id: str
    password: str

# ---------- DB INIT ----------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id TEXT,
        name TEXT,
        password TEXT,
        balance REAL DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id TEXT,
        amount REAL,
        status TEXT
    )
    """)

    # default user
    c.execute("SELECT * FROM tenants WHERE tenant_id='1001'")
    if not c.fetchone():
        c.execute("INSERT INTO tenants (tenant_id,name,password,balance) VALUES (?,?,?,?)",
                  ("1001","Test User","123456",5000))

    conn.commit()
    conn.close()

init_db()

# ---------- APIs ----------

@app.post("/api/login")
def login(data: LoginData):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT name FROM tenants WHERE tenant_id=? AND password=?",
              (data.tenant_id, data.password))

    user = c.fetchone()
    conn.close()

    if user:
        return {
            "status": "success",
            "name": user[0],
            "tenant_id": data.tenant_id
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid login")


@app.get("/api/dashboard/{tenant_id}")
def dashboard(tenant_id: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT name, balance FROM tenants WHERE tenant_id=?",
              (tenant_id,))
    user = c.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    c.execute("SELECT SUM(amount) FROM payments WHERE tenant_id=? AND status='paid'",
              (tenant_id,))
    paid = c.fetchone()[0] or 0

    conn.close()

    return {
        "name": user[0],
        "due": user[1],
        "paid": paid
    }


@app.post("/api/pay")
def pay(data: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO payments (tenant_id,amount,status) VALUES (?,?,?)",
              (data["tenant_id"], data["amount"], "paid"))

    c.execute("UPDATE tenants SET balance = balance - ? WHERE tenant_id=?",
              (data["amount"], data["tenant_id"]))

    conn.commit()
    conn.close()

    return {"message": "Payment successful ✅"}


@app.get("/")
def root():
    return {"status": "LIVE"}
