# data_fetcher/clean_data.py
import re
from datetime import datetime
from data_fetcher.db_manager import fetch_unprocessed, mark_processed, insert_raw_article
import logging
from bson import ObjectId

logger = logging.getLogger(__name__)

URL_RE = re.compile(r"https?://\S+")

def clean_text(text: str) -> str:
    if not text:
        return ""
    t = URL_RE.sub("", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def normalize_article(doc: dict):
    # Remove junk, ensure fields exist
    content = doc.get("content", "") or doc.get("description", "")
    content_clean = clean_text(content)
    title = doc.get("title", "").strip() if doc.get("title") else ""
    if not title or not doc.get("url"):
        return None
    norm = {
        "title": title,
        "url": doc["url"],
        "publishedAt": doc.get("publishedAt"),
        "source": doc.get("source"),
        "content": content_clean,
        "raw_id": doc.get("_id", None) or None
    }
    return norm

def run_cleaner(limit=200):
    docs = fetch_unprocessed(limit=limit)
    cleaned = []
    for d in docs:
        norm = normalize_article(d)
        if not norm:
            # mark as processed to skip later
            mark_processed(d.get("url") or str(d.get("_id")), {"processed_at": datetime.utcnow()})
            continue
        cleaned.append((d, norm))
    logger.info(f"Cleaner found {len(cleaned)} valid docs to process.")
    return cleaned

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_cleaner()
