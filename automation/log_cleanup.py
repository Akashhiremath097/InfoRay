# automation/log_cleanup.py
import os
import logging
from datetime import datetime, timedelta

from automation.log_cleanup import cleanup_logs
schedule.every().day.at("00:00").do(cleanup_logs)


# Where your logs are stored
DEFAULT_LOG_DIR = "data_fetcher/logs"
DEFAULT_DAYS = 7  # delete logs older than 7 days

logger = logging.getLogger(__name__)

def cleanup_logs(log_dir: str = DEFAULT_LOG_DIR, days: int = DEFAULT_DAYS):
    """
    Delete log files older than `days` days.
    Only removes .log files.
    """
    if not os.path.exists(log_dir):
        logger.warning(f"Log directory not found: {log_dir}")
        return 0

    cutoff = datetime.utcnow() - timedelta(days=days)
    removed_count = 0

    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)

        # Skip non-files
        if not os.path.isfile(file_path):
            continue

        # Only clean .log files
        if not filename.endswith(".log"):
            continue

        try:
            mtime = datetime.utcfromtimestamp(os.path.getmtime(file_path))
            if mtime < cutoff:
                os.remove(file_path)
                removed_count += 1
                logger.info(f"Removed old log file: {filename}")
        except Exception as e:
            logger.exception(f"Error removing log file {filename}: {e}")

    logger.info(f"Log cleanup completed. Deleted {removed_count} files.")
    return removed_count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cleanup_logs()
