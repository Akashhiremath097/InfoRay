import requests
from bs4 import BeautifulSoup
import os
import hashlib
from pathlib import Path
from datetime import datetime

# Local cache directory
CACHE_DIR = Path("web_app/static/thumb_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Category fallback images
CATEGORY_IMAGES = {
    "Technology": "/static/fallbacks/tech.jpg",
    "Sports": "/static/fallbacks/sports.jpg",
    "Health": "/static/fallbacks/health.jpg",
    "Business": "/static/fallbacks/business.jpg",
    "Politics": "/static/fallbacks/politics.jpg",
    "Default": "/static/fallbacks/default.jpg"
}

def hash_url(url: str):
    return hashlib.md5(url.encode()).hexdigest()

def download_and_cache(url: str):
    try:
        img_id = hash_url(url)
        ext = ".jpg"
        local_path = CACHE_DIR / f"{img_id}{ext}"

        if local_path.exists():
            return f"/static/thumb_cache/{img_id}{ext}"

        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
            return f"/static/thumb_cache/{img_id}{ext}"
        return None
    except:
        return None

def extract_og_image(url: str):
    """Scrape OpenGraph image from article page."""
    try:
        r = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]

        # Try Twitter card image
        tw = soup.find("meta", property="twitter:image")
        if tw and tw.get("content"):
            return tw["content"]

        return None
    except:
        return None

def ai_generate_fallback(category: str):
    """
    Generates an AI fallback thumbnail using Lexica API (free).
    """
    try:
        prompt = f"High-quality thumbnail for news about {category}, cinematic, 16:9"
        r = requests.get(
            "https://lexica.art/api/v1/search",
            params={"q": category},
            timeout=6
        )
        data = r.json().get("images", [])
        if data:
            return data[0]["src_small"]
        return None
    except:
        return None

def resolve_image(article):
    """
    FULL IMAGE PIPELINE:
    1. NewsAPI image
    2. OG scraper
    3. Category fallback
    4. AI fallback
    5. Cache downloaded images
    """

    # 1. NewsAPI
    if article.get("image"):
        cached = download_and_cache(article["image"])
        if cached:
            return cached

    # 2. OpenGraph fallback
    og = extract_og_image(article.get("url", ""))
    if og:
        cached = download_and_cache(og)
        if cached:
            return cached

    # 3. Category fallback
    cat = article.get("category", "Default")
    fallback = CATEGORY_IMAGES.get(cat, CATEGORY_IMAGES["Default"])
    return fallback
