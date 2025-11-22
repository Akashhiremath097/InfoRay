# ai_processing/sentiment_analyzer.py
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure vader lexicon available
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    if not text:
        return "Neutral"
    scores = sia.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"
