"""
LIFEASY V30 PRO - Railway Entry Point
Simple wrapper to start the app with better error handling
"""
import os
import sys

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("="*80)
print("🚀 LIFEASY V30 PRO - Railway Starting...")
print("="*80)

try:
    # Import the main app
    from main_prod import app
    
    print("✅ App imported successfully")
    
    # Get port from Railway
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌐 Starting server on {HOST}:{PORT}")
    
    # Start uvicorn
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
    
except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
    import traceback
    print(f"\nTraceback:\n{traceback.format_exc()}")
    sys.exit(1)
