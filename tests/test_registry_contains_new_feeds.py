import pytest
from engine.sports_scraper import FEEDS

def test_registry_contains_new_premium_feeds():
    """Verify that the new premium RSS sources are present in the registry"""
    required_keys = [
        'CBS - NBA',
        'CBS - NFL',
        'CBS - MLB',
        'CBS - NHL',
        'CBS - NCAAF',
        'CBS - NCAAB',
        'CBS - Golf',
        'BBC - Soccer',
        'BBC - F1',
        'NBC - NFL'
    ]
    for key in required_keys:
        assert key in FEEDS, f"New premium feed '{key}' is missing from scraper registry"
