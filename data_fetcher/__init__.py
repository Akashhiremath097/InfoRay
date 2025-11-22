# """
# data_fetcher package
# Handles:
# - RSS fetching
# - NewsAPI fetching (optional)
# - Cleaning & normalization
# - Raw DB operations
# """

# # DO NOT IMPORT fetch_news or db_manager here
# # They cause circular imports.

# # Import ONLY functions needed by run_pipeline
# from .fetch_rss import fetch_rss
# from .clean_data import run_cleaner
"""
data_fetcher package
Handles:
- RSS fetching
- Cleaning & normalization
"""

from .fetch_rss import fetch_rss
from .clean_data import run_cleaner
