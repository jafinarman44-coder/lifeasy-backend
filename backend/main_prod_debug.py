"""
LIFEASY V30 PRO - Production FastAPI Application with Enhanced Error Logging
Complete System: Auth + Payment + Notifications + Chat + Calling
Phase 6 Features Included
"""
import os
import traceback
import sys
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
from routers.bill_router import router as bill_router  # Bills Management
from routers.tenant_router import router as tenant_router  # Tenant Management
from routers.settings_router import router as settings_router  # Settings System
from routers.group_router import router as group_router  # Group Chat & Calls
from routers.media_router import router as media_router  # Media Upload
import asyncio
from realtime.heartbeat_manager import heartbeat_manager
from realtime.call_socket import call_manager

# Load environment variables from .env file
load_dotenv()

# ============================================
# ENHANCED ERROR LOGGING SYSTEM
# ============================================

def log_error(level: str, message: str, exc: Exception = None):
    """Centralized error logging with traceback"""
    timestamp = datetime.now().isoformat()
    log_entry = f"\n{'='*80}\n[{timestamp}] {level}: {message}"
    
    if exc:
        log_entry += f"\n\nEXCEPTION TYPE: {type(exc).__name__}"
        log_entry += f"\nEXCEPTION MESSAGE: {str(exc)}"
        log_entry += f"\n\nFULL TRACEBACK:\n{traceback.format_exc()}"
    
    log_entry += f"\n{'='*80}\n"
    
    # Print to console (visible in Render logs)
    print(log_entry, flush=True)
    
    # Also write to stderr for better visibility
    sys.stderr.write(log_entry)
    sys.stderr.flush()

# Initialize FastAPI app
app = FastAPI(
    title="LIFEASY V30 PRO API",
    description="Production-ready apartment management system with enhanced error logging",
    version="30.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration (Update for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "https://api.lifeasy.com",
        "https://lifeasy.com",
        "*"  # Remove in production, specify exact domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GLOBAL ERROR HANDLER
# ============================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and log them properly"""
    
    # Log the error with full traceback
    log_error(
        "UNHANDLED EXCEPTION",
        f"Request: {request.method} {request.url.path}",
        exc
    )
    
    # Return detailed error in development, generic in production
    env = os.getenv("LIFEASY_ENV", "development")
    
    if env == "development":
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "type": type(exc).__name__,
                "traceback": traceback.format_exc().split('\n'),
                "path": request.url.path,
                "method": request.method
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again.",
                "path": request.url.path,
                "timestamp": datetime.now().isoformat()
            }
        )

# ============================================
# REQUEST LOGGING MIDDLEWARE
# ============================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timing and status"""
    start_time = datetime.now()
    
    # Log incoming request
    print(f"\n📥 [{start_time.strftime('%H:%M:%S')}] {request.method} {request.url.path}", flush=True)
    
    try:
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        
        # Log successful response
        emoji = "✅" if response.status_code < 400 else "❌"
        print(f"{emoji} [{process_time:.2f}s] {request.method} {request.url.path} → {response.status_code}", flush=True)
        
        return response
        
    except Exception as e:
        process_time = (datetime.now() - start_time).total_seconds()
        log_error(
            "REQUEST FAILED",
            f"Request: {request.method} {request.url.path} | Time: {process_time:.2f}s",
            e
        )
        raise

# Include routers (Legacy + Phase 6 + V2)
app.include_router(auth_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(notification_router, prefix="/api")
app.include_router(bill_router, prefix="/api")  # Bills Management

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

# Tenant Router (for tenant-to-tenant features)
app.include_router(tenant_router, prefix="/api/tenants")  # /api/tenants/* (Tenant management)

# Settings Router (WhatsApp-style settings)
app.include_router(settings_router)  # /api/settings/* (Settings system)

# Group Router (Group chat & calls)
app.include_router(group_router)  # /api/groups/* (Group management)

# Media Router (File uploads)
app.include_router(media_router)  # /api/media/* (Media upload)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("\n" + "="*80, flush=True)
    print("🚀 Starting LIFEASY V30 PRO...", flush=True)
    print(f"📍 Environment: {os.getenv('LIFEASY_ENV', 'development')}", flush=True)
    print(f"📍 Database: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...", flush=True)
    print("="*80 + "\n", flush=True)
    
    try:
        init_db()
        print("✅ Database initialized successfully!", flush=True)
    except Exception as e:
        log_error("DATABASE INIT FAILED", "Failed to initialize database", e)
        raise
    
    print("✅ Backend ready!", flush=True)
    
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
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",
        "environment": os.getenv("LIFEASY_ENV", "development"),
        "timestamp": datetime.now().isoformat(),
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
        "version": "30.0.0-PHASE6-STEP8",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    # Production server settings
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"\n🌐 Server running on http://{host}:{port}", flush=True)
    print(f"📖 API Docs: http://{host}:{port}/docs", flush=True)
    print(f"🔍 Enhanced logging enabled\n", flush=True)
    
    uvicorn.run(app, host=host, port=port)
