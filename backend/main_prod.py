"""
LIFEASY V30 PRO - Production FastAPI Application
Complete System: Auth + Payment + Notifications + Chat + Calling
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("📦 Loading main_prod.py...")

# Load environment variables
load_dotenv()

print("✅ Environment loaded")

# ============================================
# INITIALIZE FASTAPI APP
# ============================================
app = FastAPI(
    title="LIFEASY V30 PRO API",
    description="Production-ready apartment management system",
    version="30.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

print("✅ FastAPI app initialized")

# ============================================
# CORS CONFIGURATION
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ CORS configured")

# ============================================
# IMPORT AND REGISTER ROUTERS
# ============================================
try:
    from database_prod import init_db
    from models import Tenant, OTPCode
    from auth_master import router as auth_router
    from payment_gateway import router as payment_router
    from notification_service import router as notification_router
    from routers.auth_phase6 import router as auth_phase6_router
    from routers.auth_v2 import router as auth_v2_router
    from routers.notification_router import router as notification_api_router
    from routers.chat_router import router as chat_router
    from routers.call_router import router as call_router
    from routers.chat_router_v2 import router as chat_v2_router
    from routers.chat_block_router import router as chat_block_router
    from routers.chat_call_router import router as chat_call_router
    from routers.call_router_v2 import router as call_v2_router
    from routers.chat_v3 import router as chat_v3_router
    from routers.bill_router import router as bill_router
    from routers.tenant_router import router as tenant_router
    from routers.settings_router import router as settings_router
    from routers.group_router import router as group_router
    from routers.media_router import router as media_router
    
    print("✅ All routers imported successfully")
    
    # Register routers
    app.include_router(auth_router)
    app.include_router(payment_router)
    app.include_router(notification_router)
    app.include_router(bill_router)
    app.include_router(auth_phase6_router)
    app.include_router(notification_api_router)
    app.include_router(chat_router)
    app.include_router(call_router)
    app.include_router(auth_v2_router)
    app.include_router(chat_v2_router)
    app.include_router(chat_block_router)
    app.include_router(chat_call_router)
    app.include_router(call_v2_router)
    app.include_router(chat_v3_router)
    app.include_router(tenant_router)
    app.include_router(settings_router)
    app.include_router(group_router)
    app.include_router(media_router)
    
    print("✅ All routers registered")
    
except Exception as e:
    print(f"❌ ERROR importing routers: {e}")
    import traceback
    traceback.print_exc()
    raise

# ============================================
# STARTUP EVENT
# ============================================
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        print("\n" + "="*80)
        print("🚀 Starting LIFEASY V30 PRO...")
        print(f"📍 Environment: {os.getenv('LIFEASY_ENV', 'development')}")
        print(f"📍 Database: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...")
        print("="*80 + "\n")
        
        init_db()
        print("✅ Database initialized successfully!")
        print("✅ Backend ready!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ CRITICAL STARTUP ERROR!")
        print(f"{'='*80}")
        print(f"Error: {str(e)}")
        import traceback
        print(f"\nTraceback:\n{traceback.format_exc()}")
        print(f"{'='*80}\n")
        raise

# ============================================
# BASIC ENDPOINTS
# ============================================
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
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "environment": os.getenv("LIFEASY_ENV", "development"),
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
        "version": "30.0.0-PHASE6-STEP8",
        "features": {
            "auth": "Email + OTP + JWT (V1 & V2)",
            "payment": "bKash & Nagad Gateway",
            "notifications": "Firebase + DB Notifications",
            "chat": "WhatsApp-style messaging",
            "calling": "Audio/Video calls (WebRTC)"
        }
    }

# ============================================
# PRODUCTION SERVER
# ============================================
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"\n🌐 Server running on http://{host}:{port}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    print(f"🔍 Enhanced logging enabled\n")
    
    uvicorn.run(app, host=host, port=port)

print("✅ main_prod.py loaded successfully")
