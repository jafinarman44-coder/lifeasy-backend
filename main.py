from fastapi import FastAPI
from database import Base, engine
from auth import router as auth_router

app = FastAPI(title="LIFEASY V30 PRO API")

# DB init
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(auth_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "LIFEASY LIVE API RUNNING"}

@app.get("/health")
def health():
    return {"status": "ok"}
