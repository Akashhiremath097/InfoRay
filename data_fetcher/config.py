# data_fetcher/config.py
from dotenv import load_dotenv
import os

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # optional if you use RSS
NEWSAPI_ENDPOINT = os.getenv("NEWSAPI_ENDPOINT", "https://newsapi.org/v2/top-headlines")
NEWSAPI_COUNTRY = os.getenv("NEWSAPI_COUNTRY", "us")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "news_aggregator")
RAW_COLLECTION = os.getenv("RAW_COLLECTION", "raw_articles")
PROCESSED_COLLECTION = os.getenv("PROCESSED_COLLECTION", "processed_articles")

FETCH_PAGE_SIZE = int(os.getenv("FETCH_PAGE_SIZE", "20"))
