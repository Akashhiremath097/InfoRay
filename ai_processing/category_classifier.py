# ai_processing/category_classifier.py
# Simple rule-based categorizer using keywords for the 5 categories.
CATEGORIES = {
    "Politics": ["election", "senate", "parliament", "president", "minister", "politic", "government"],
    "Technology": ["tech", "iphone", "ai", "machine learning", "software", "hardware", "google", "microsoft"],
    "Sports": ["football", "cricket", "soccer", "nba", "olympic", "score", "match"],
    "Health": ["health", "covid", "vaccine", "disease", "mental health", "hospital"],
    "Business": ["market", "stock", "business", "finance", "economy", "company", "startup"]
}

def classify(text):
    if not text:
        return "Business"  # default fallback
    t = text.lower()
    scores = {k: 0 for k in CATEGORIES}
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in t:
                scores[cat] += 1
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else "Business"
