# LIFEASY FINAL ENTRY POINT
# Production-ready FastAPI backend for Render deployment

from fastapi import FastAPI

try:
    # Import your real production app
    from main_prod import app
    print("✅ USING MAIN_PROD (REAL BACKEND)")
except Exception as e:
    print("❌ ERROR LOADING MAIN_PROD:", e)
    
    # fallback so Render doesn't crash
    app = FastAPI()

    @app.get("/")
    def root():
        return {"error": "main_prod not loaded", "details": str(e)}
