from ai_processing.ai_processing_pipeline import process_one_document

def test_processing_single_doc():
    sample = {
        "title": "AI breakthrough in technology",
        "url": "http://example.com/1",
        "publishedAt": "2025-11-15T12:00:00Z",
        "source": "TestSource",
        "content": "AI has made a huge breakthrough in technology innovation today."
    }

    processed = process_one_document(sample)

    assert processed["summary"] != ""
    assert processed["category"] in ["Politics", "Technology", "Sports", "Health", "Business"]
    assert processed["sentiment"] in ["Positive", "Negative", "Neutral"]
