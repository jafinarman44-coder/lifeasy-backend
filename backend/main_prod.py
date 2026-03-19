"""
LIFEASY V30 PRO - Production FastAPI Application
Complete System: Auth + Payment + Notifications
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_prod import init_db, engine, Base
from auth_master import router as auth_router
from payment_gateway import router as payment_router
from notification_service import router as notification_router
import os

# Initialize FastAPI app
app = FastAPI(
    title="LIFEASY V30 PRO API",
    description="Production-ready apartment management system",
    version="30.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration (Update for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://api.lifeasy.com",
        "https://lifeasy.com",
        "*"  # Remove in production, specify exact domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(notification_router, prefix="/api")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting LIFEASY V30 PRO...")
    init_db()
    print("✅ Backend ready!")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "LIFEASY V30 PRO API",
        "version": "30.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "auth": "JWT + OTP",
            "payment": "bKash + Nagad",
            "notification": "Firebase"
        }
    }


@app.get("/api/status")
def api_status():
    """API status endpoint"""
    return {
        "api": "online",
        "environment": os.getenv("LIFEASY_ENV", "development"),
        "features": {
            "auth": "Phone + OTP + JWT",
            "payment": "bKash & Nagad Gateway",
            "sms": "Twilio & SSL Wireless",
            "notifications": "Firebase Cloud Messaging",
            "database": "PostgreSQL"
        },
        "version": "30.0.0-PRO"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Production server settings
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"🌐 Server running on http://{host}:{port}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
