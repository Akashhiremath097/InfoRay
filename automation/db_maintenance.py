# automation/db_maintenance.py
from database.mongo_connection import get_db
from data_fetcher.config import RAW_COLLECTION, PROCESSED_COLLECTION
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def cleanup_old_articles(days=30):
    db = get_db()
    cutoff = datetime.utcnow() - timedelta(days=days)
    raw_res = db[RAW_COLLECTION].delete_many({"fetched_at": {"$lt": cutoff}})
    proc_res = db[PROCESSED_COLLECTION].delete_many({"processed_at": {"$lt": cutoff}})
    logger.info(f"Deleted {raw_res.deleted_count} raw and {proc_res.deleted_count} processed old articles.")
