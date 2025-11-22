# ai_processing/ai_processing_pipeline.py
from data_fetcher.db_manager import fetch_unprocessed, mark_processed
from ai_processing.summarizer import extractive_summary
from ai_processing.category_classifier import classify
from ai_processing.sentiment_analyzer import analyze_sentiment
from database.mongo_connection import get_db
from data_fetcher.config import PROCESSED_COLLECTION
from datetime import datetime
import logging
from ai_processing.image_resolver import resolve_image
logger = logging.getLogger(__name__)

def process_one_document(raw_doc):
    content = raw_doc.get("content") or ""
    summary = extractive_summary(content, num_sentences=2)
    category = classify((raw_doc.get("title") or "") + " " + content)
    sentiment = analyze_sentiment(content)
    processed = {
        "title": raw_doc.get("title"),
        "url": raw_doc.get("url"),
        "publishedAt": raw_doc.get("publishedAt"),
        "source": raw_doc.get("source"),
        "summary": summary,
        "category": category,
        "sentiment": sentiment,
        
"image": resolve_image({
    "image": raw_doc.get("image"),
    "urlToImage": raw_doc.get("urlToImage"),
    "url": raw_doc.get("url"),
    "category": category
}),
        "processed_at": datetime.utcnow()
    }
    return processed

def run_processing(limit=100):
    raws = fetch_unprocessed(limit=limit)
    if not raws:
        logger.info("No unprocessed docs found.")
        return 0
    db = get_db()
    coll = db[PROCESSED_COLLECTION]
    processed_count = 0
    for r in raws:
        try:
            proc = process_one_document(r)
            coll.update_one({"url": proc["url"]}, {"$setOnInsert": proc}, upsert=True)
            mark_processed(r.get("url") or str(r.get("_id")), {"processed_at": proc["processed_at"]})
            processed_count += 1
        except Exception:
            logger.exception("Error processing document %s", r.get("url"))
    logger.info(f"Processed {processed_count} articles.")
    return processed_count

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    run_processing()
