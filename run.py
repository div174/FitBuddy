"""
FitBuddy – Development server launcher
Usage: python run.py
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"\n⚡ FitBuddy v{settings.APP_VERSION} starting...")
    print(f"   Model : {settings.GEMINI_MODEL}")
    print(f"   DB    : {settings.DATABASE_URL}")
    print(f"   URL   : http://{settings.HOST}:{settings.PORT}\n")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
