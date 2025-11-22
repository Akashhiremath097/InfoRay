# automation/scheduler.py
import schedule
import time
import logging
from run_pipeline import run_full_pipeline

logger = logging.getLogger(__name__)

def job():
    logger.info("Scheduler triggered pipeline.")
    run_full_pipeline()

def start_scheduler(interval_minutes=360):  # default 6 hours
    schedule.clear()
    schedule.every(interval_minutes).minutes.do(job)
    logger.info(f"Scheduler set to run every {interval_minutes} minutes.")
    while True:
        schedule.run_pending()
        time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_scheduler()
