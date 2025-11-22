from data_fetcher.fetch_news import fetch_from_newsapi

def test_fetch_runs():
    # Should return a list even with no API key
    result = fetch_from_newsapi()
    assert isinstance(result, list)
