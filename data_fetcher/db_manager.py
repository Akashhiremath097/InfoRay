# data_fetcher/db_manager.py
import logging

logger = logging.getLogger(__name__)

def insert_raw_article(article: dict):
    # Lazy import to avoid circular import
    from database.mongo_connection import get_db
    from data_fetcher.config import RAW_COLLECTION
    
    db = get_db()
    coll = db[RAW_COLLECTION]

    res = coll.update_one(
        {"url": article.get("url")},
        {"$setOnInsert": article},
        upsert=True
    )
    return res


def fetch_unprocessed(limit=100):
    from database.mongo_connection import get_db
    from data_fetcher.config import RAW_COLLECTION
    
    db = get_db()
    coll = db[RAW_COLLECTION]
    docs = list(coll.find({"processed": {"$ne": True}}).limit(limit))
    return docs


def mark_processed(url, processed_obj):
    from database.mongo_connection import get_db
    from data_fetcher.config import RAW_COLLECTION
    
    db = get_db()
    coll = db[RAW_COLLECTION]
    coll.update_one(
        {"url": url},
        {"$set": {"processed": True, **processed_obj}}
    )
