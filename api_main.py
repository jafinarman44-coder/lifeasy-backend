"""
LIFEASY V30 PRO - Root Level FastAPI Entry Point
This file allows running the backend from the root directory
"""

# Import the app from backend's main_prod
from backend.main_prod import app

# This makes the app accessible from the root level
# Run with: uvicorn main:app --host 0.0.0.0 --port $PORT

if __name__ == "__main__":
    import uvicorn
    import os
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"🌐 LIFEASY V30 PRO API")
    print(f"📖 Running on http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
