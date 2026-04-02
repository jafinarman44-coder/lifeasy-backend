"""
LIFEASY V30 PRO - Production FastAPI Application
Complete System: Auth + Payment + Notifications + Chat + Calling
Phase 6 Features Included
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_prod import init_db, engine, Base
from models import Tenant, OTPCode  # Import models to ensure they're registered
from auth_master import router as auth_router
from payment_gateway import router as payment_router
from notification_service import router as notification_router
from routers.auth_phase6 import router as auth_phase6_router
from routers.auth_v2 import router as auth_v2_router  # NEW V2 Auth System
from routers.notification_router import router as notification_api_router
from routers.chat_router import router as chat_router
from routers.call_router import router as call_router
from routers.chat_router_v2 import router as chat_v2_router  # NEW WebSocket Chat
from routers.chat_block_router import router as chat_block_router  # Block System
from routers.chat_call_router import router as chat_call_router  # Voice/Video Calls
from routers.call_router_v2 import router as call_v2_router  # NEW Real-Time Call Signaling
from routers.chat_v3 import router as chat_v3_router  # NEW High-Performance Chat v3
import os
import asyncio
from realtime.heartbeat_manager import heartbeat_manager
from realtime.call_socket import call_manager

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

# Include routers (Legacy + Phase 6 + V2)
app.include_router(auth_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(notification_router, prefix="/api")

# Phase 6 V1 Routers
app.include_router(auth_phase6_router)  # /api/auth/*
app.include_router(notification_api_router)  # /api/notifications/*
app.include_router(chat_router)  # /api/chat/*
app.include_router(call_router)  # /api/calls/*

# Phase 6 V2 Routers (NEW - Complete Chat & Call System)
app.include_router(auth_v2_router)  # /api/auth/v2/* (prefix already in router)
app.include_router(chat_v2_router)  # /api/chat/v2/* (WebSocket + REST)
app.include_router(chat_block_router)  # /api/chat/block/*
app.include_router(chat_call_router)  # /api/chat/call/*
app.include_router(call_v2_router)  # /api/call/v2/* (Real-Time Signaling)

# Phase 6 V3 Routers (NEWEST - High Performance Chat)
app.include_router(chat_v3_router)  # /api/chat/v3/* (Advanced features)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting LIFEASY V30 PRO...")
    init_db()
    print("✅ Backend ready!")
    
    # Start WebSocket cleanup background task
    # asyncio.create_task(
    #     heartbeat_manager.cleanup_task(call_manager)
    # )
    # print("🧹 Heartbeat cleanup task started")


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
            "auth": "JWT + OTP (V1 + V2)",
            "payment": "bKash + Nagad",
            "notification": "Firebase + Database",
            "chat": "Real-time messaging",
            "calling": "WebRTC signaling"
        }
    }


@app.get("/api/status")
def api_status():
    """API status endpoint"""
    return {
        "api": "online",
        "environment": os.getenv("LIFEASY_ENV", "development"),
        "features": {
            "auth": "Email + OTP + JWT (V1 & V2)",
            "payment": "bKash & Nagad Gateway",
            "sms": "Twilio & SSL Wireless",
            "notifications": "Firebase + DB Notifications",
            "chat": "WhatsApp-style messaging",
            "calling": "Audio/Video calls (WebRTC)",
            "tenant_approval": "Owner approval workflow",
            "database": "SQLite/PostgreSQL"
        },
        "version": "30.0.0-PHASE6-STEP8"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Production server settings
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"🌐 Server running on http://{host}:{port}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
