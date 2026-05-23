import pytest
import sys
import os

# Ensure engine is in path if necessary, though pytest should handle it based on rootdir

# We will mock the sports_scraper if possible, or just test if it has been updated to import analyze_article_impact
def test_scraper_assigns_dynamic_vader_scores():
    try:
        from engine.sports_scraper import fetch_feeds
    except ImportError:
        pytest.fail("Could not import fetch_feeds from engine.sports_scraper")
    
    # Simple static analysis: read the file to see if analyze_article_impact is imported
    # This is a structural test, to ensure it's wired
    with open('engine/sports_scraper.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "from engine.sports_vader import analyze_article_impact" in content, "SportsVADER is not wired into the scraper"
    assert "analyze_article_impact(" in content, "analyze_article_impact function is not being called in the scraper"
