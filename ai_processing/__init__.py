"""
AI Processing Package

Contains:
- Summarization logic
- Category classification
- Sentiment analysis
- Full AI processing pipeline
"""

from .summarizer import extractive_summary
from .category_classifier import classify
from .sentiment_analyzer import analyze_sentiment
from .ai_processing_pipeline import run_processing, process_one_document
