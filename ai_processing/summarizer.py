# ai_processing/summarizer.py
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import math

# Ensure data present
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def extractive_summary(text, num_sentences=2):
    if not text:
        return ""

    sents = sent_tokenize(text)
    if len(sents) <= num_sentences:
        return " ".join(sents)

    words = [w.lower() for sent in sents for w in word_tokenize(sent) if w.isalpha()]
    freq = Counter(words)
    # score each sentence
    sent_scores = []
    for sent in sents:
        ws = [w.lower() for w in word_tokenize(sent) if w.isalpha()]
        if not ws:
            sent_scores.append((sent, 0))
            continue
        score = sum(freq[w] for w in ws) / math.sqrt(len(ws))
        sent_scores.append((sent, score))
    top = sorted(sent_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
    top_sorted_by_pos = sorted(top, key=lambda x: sents.index(x[0]))
    return " ".join([s for s, _ in top_sorted_by_pos])
