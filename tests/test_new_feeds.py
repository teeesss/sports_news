import asyncio
import feedparser
import pytest
from engine.sports_scraper import FEEDS
from engine.stealth_navigator import StealthNavigator

@pytest.mark.asyncio
async def test_new_feeds_reachability():
    """Verify that new RSS feeds can be fetched and parsed successfully."""
    new_feeds = {
        'CBS - NBA': 'https://www.cbssports.com/rss/headlines/nba/',
        'CBS - NFL': 'https://www.cbssports.com/rss/headlines/nfl/',
        'CBS - MLB': 'https://www.cbssports.com/rss/headlines/mlb/',
        'CBS - NHL': 'https://www.cbssports.com/rss/headlines/nhl/',
        'CBS - NCAAF': 'https://www.cbssports.com/rss/headlines/college-football/',
        'CBS - NCAAB': 'https://www.cbssports.com/rss/headlines/college-basketball/',
        'CBS - Golf': 'https://www.cbssports.com/rss/headlines/golf/',
        'BBC - Soccer': 'https://feeds.bbci.co.uk/sport/football/rss.xml',
        'BBC - F1': 'https://feeds.bbci.co.uk/sport/formula1/rss.xml',
        'NBC - NFL': 'https://profootballtalk.nbcsports.com/feed/'
    }

    nav = StealthNavigator(headless=True)
    await nav.initialize()

    try:
        for name, url in new_feeds.items():
            print(f"Testing reachability of: {name} -> {url}")
            page = await nav.context.new_page()
            try:
                # Go to feed URL
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                content = await page.content()
                
                # Check for XML/RSS tags or pre-wrapped content
                feed = feedparser.parse(content)
                if not feed.entries or len(feed.entries) == 0:
                    # Fallback to direct parse
                    feed = feedparser.parse(url)

                assert len(feed.entries) > 0, f"No entries found in feed {name}"
                print(f"  [SUCCESS] {name} parsed {len(feed.entries)} entries. Sample title: {feed.entries[0].title}")
            except Exception as e:
                pytest.fail(f"Feed {name} failed to load or parse: {e}")
            finally:
                await page.close()
    finally:
        await nav.close()
