# database/mongo_connection.py
from pymongo import MongoClient
from data_fetcher.config import MONGO_URI, MONGO_DB
import logging

logger = logging.getLogger(__name__)

_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
        logger.info("Mongo client created.")
    return _client

def get_db():
    return get_client()[MONGO_DB]
