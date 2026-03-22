from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router

app = FastAPI(
    title="LIFEASY PRODUCTION API",
    version="1.0.0"
)

# ✅ CORS (mobile app support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROOT
@app.get("/")
def root():
    return {"message": "LIFEASY API RUNNING"}

# ✅ HEALTH
@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ IMPORTANT: AUTH ROUTER INCLUDE
app.include_router(auth_router, prefix="/api")