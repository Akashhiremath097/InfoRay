"""
database package

Handles:
- MongoDB client initialization
- Central DB access and connection pooling
"""

from .mongo_connection import get_client, get_db
