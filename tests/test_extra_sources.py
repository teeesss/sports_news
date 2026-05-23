import asyncio
import sys
import os
import re
import feedparser

# Add engine to path
sys.path.append(os.path.join(os.getcwd(), "engine"))

from stealth_navigator import StealthNavigator

async def test_requested_sources():
    print("Testing SportSpyder and TheScore Final Check...")
    nav = StealthNavigator(headless=True)
    await nav.initialize()
    
    candidates = {
        'SportSpyder NFL': 'https://sportspyder.com/teams/nfl-news/rss',
        'SportSpyder NBA': 'https://sportspyder.com/teams/nba-news/rss',
        'SportSpyder MLB': 'https://sportspyder.com/teams/mlb-news/rss',
        'TheScore Feedburner?': 'http://feeds.feedburner.com/thescore/news'
    }
    
    for name, url in candidates.items():
        print(f"\n[*] Trying: {name} ({url})")
        page = await nav.context.new_page()
        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            content = await page.content()
            feed = feedparser.parse(content)
            print(f"    Entries: {len(feed.entries)}")
            
            if feed.entries:
                print(f"    [OK] Working URL found: {name}")
                print(f"    Sample: {feed.entries[0].title}")
                
        except Exception as e:
            print(f"    [!] Fetch failed for {name}: {e}")
        finally:
            await page.close()
            
    await nav.close()

if __name__ == "__main__":
    asyncio.run(test_requested_sources())
