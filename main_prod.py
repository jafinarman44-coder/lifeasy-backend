from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LifeEasy API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 🔥 IMPORTANT
app.include_router(auth_router, prefix="/api")
