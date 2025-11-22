# data_fetcher/fetch_rss.py

import feedparser
import logging
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from data_fetcher.db_manager import insert_raw_article

logger = logging.getLogger(__name__)

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.hindustantimes.com/feeds/rss/homepage-news/rssfeed.xml",
    "https://www.indiatoday.in/rss/home",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms"
]


def extract_full_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, timeout=5, headers=headers)
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return text[:5000]
    except Exception:
        return ""


def process_entry(entry, feed_title):
    url = entry.get("link")
    title = entry.get("title", "").strip()
    published = entry.get("published", None)

    if not url or not title:
        return False

    full_text = extract_full_text(url)

    article_doc = {
        "title": title,
        "url": url,
        "publishedAt": published,
        "source": feed_title,
        "content": full_text,
        "fetched_at": datetime.utcnow()
    }

    insert_raw_article(article_doc)
    return True


def fetch_rss():
    total_inserted = 0
    articles_to_process = []

    # STEP 1 — Fetch RSS entries (very fast)
    for feed_url in RSS_FEEDS:
        logger.info(f"Loading feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        feed_title = feed.feed.get("title", "Unknown Source")

        for entry in feed.entries:
            articles_to_process.append((entry, feed_title))

    logger.info(f"Total articles to process: {len(articles_to_process)}")

    # STEP 2 — Multi-thread extraction (super fast)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_entry, entry, source)
                   for entry, source in articles_to_process]

        for f in as_completed(futures):
            if f.result():
                total_inserted += 1

    logger.info(f"RSS fetch completed. Inserted {total_inserted} articles.")
    return total_inserted


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetch_rss()
