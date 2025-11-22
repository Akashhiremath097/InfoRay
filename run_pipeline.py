from data_fetcher import fetch_rss
from data_fetcher import run_cleaner
from ai_processing import run_processing
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_full_pipeline():
    logger.info("Starting RSS fetch...")
    fetch_rss()

    logger.info("Running cleaner...")
    run_cleaner(limit=200)

    logger.info("Running AI processing...")
    run_processing(limit=500)

    logger.info("Pipeline completed.")

if __name__ == "__main__":
    run_full_pipeline()
