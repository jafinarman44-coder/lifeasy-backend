from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers import tenant
from app.routers import otp

app = FastAPI(
    title="LIFEASY SAAS API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LIFEASY SAAS RUNNING"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(tenant.router)
app.include_router(otp.router)
