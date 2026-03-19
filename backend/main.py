"""
LIFEASY V30 PRO - Backend Entry Point
This file allows Render to run main_prod by importing it
"""

# Import the production app from main_prod
from main_prod import app

# This makes the app accessible when Render runs: python main.py
# Or: uvicorn main:app --host 0.0.0.0 --port $PORT

if __name__ == "__main__":
    import uvicorn
    import os
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"🌐 LIFEASY V30 PRO API")
    print(f"📖 Running on http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
