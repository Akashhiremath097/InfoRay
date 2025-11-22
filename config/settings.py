# config/settings.py
import os
from dotenv import load_dotenv

# Load .env from the same directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

# --- MongoDB ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "news_aggregator")
RAW_COLLECTION = os.getenv("RAW_COLLECTION", "raw_articles")
PROCESSED_COLLECTION = os.getenv("PROCESSED_COLLECTION", "processed_articles")

# --- News API ---
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_ENDPOINT = os.getenv("NEWSAPI_ENDPOINT", "https://newsapi.org/v2/top-headlines")
NEWSAPI_COUNTRY = os.getenv("NEWSAPI_COUNTRY", "in")
FETCH_PAGE_SIZE = int(os.getenv("FETCH_PAGE_SIZE", 20))

# --- Flask Web App ---
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

# --- Scheduler ---
SCHEDULER_INTERVAL_MINUTES = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", 360))

# --- Cleanup ---
LOG_CLEANUP_DAYS = int(os.getenv("LOG_CLEANUP_DAYS", 7))
DB_CLEANUP_DAYS = int(os.getenv("DB_CLEANUP_DAYS", 30))


def print_settings_summary():
    """Quick debug helper."""
    print("=== SETTINGS LOADED ===")
    print(f"MONGO_URI = {MONGO_URI}")
    print(f"MONGO_DB = {MONGO_DB}")
    print(f"NewsAPI enabled = {bool(NEWSAPI_KEY)}")
    print(f"Flask running at {FLASK_HOST}:{FLASK_PORT}")
    print(f"Scheduler every {SCHEDULER_INTERVAL_MINUTES} minutes")
