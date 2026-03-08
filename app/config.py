import os
from dotenv import load_dotenv

load_dotenv()

# App Versioning & Branding
APP_TITLE: str = "FitBuddy"
APP_VERSION: str = "2.0.0"

# Server Configuration
HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

# AI & Database Configuration
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./fitbuddy.db")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not GOOGLE_API_KEY:
    raise EnvironmentError(
        "❌  GOOGLE_API_KEY is not set. "
        "Create a .env file with GOOGLE_API_KEY=your_key_here"
    )

class Settings:
    """Settings object to match the usage in run.py."""
    def __init__(self):
        self.APP_TITLE = APP_TITLE
        self.APP_VERSION = APP_VERSION
        self.HOST = HOST
        self.PORT = PORT
        self.DEBUG = DEBUG
        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.DATABASE_URL = DATABASE_URL
        self.GEMINI_MODEL = GEMINI_MODEL

settings = Settings()
