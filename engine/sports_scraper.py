import asyncio
import datetime
import json
import logging
import os
import random
import re
import sys
import time
import calendar
from pathlib import Path
from urllib.parse import urlparse

# V28: Hierarchy Leader Error Monitoring
try:
    from engine import error_monitor
except ImportError:
    import error_monitor
error_monitor.init_error_monitor()

# V28: Auto-Dependency Guardian
try:
    try:
        from dependency_mgr import ensure_dependencies
    except ImportError:
        from engine.dependency_mgr import ensure_dependencies
    # ensure_dependencies()
except Exception as e:
    pass

import feedparser
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# V30 Mirror: Import Custom Engines
try:
    from engine.stealth_navigator import StealthNavigator
    from engine.sports_vader import analyze_article_impact
except ImportError:
    from stealth_navigator import StealthNavigator
    from sports_vader import analyze_article_impact

load_dotenv()

# Institutional Paths
ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "database" / "sports_news.js"

# V30.6.15: Institutional Feed Registry
FEEDS = {
    # NBA
    'ESPN - NBA': ('https://www.espn.com/espn/rss/nba/news', 'NBA', 'General'),
    'RealGM - NBA': ('https://basketball.realgm.com/rss/wiretap/0/0.xml', 'NBA', 'Wiretap'),
    'Yahoo - NBA': ('https://sports.yahoo.com/nba/rss/', 'NBA', 'General'),
    'CBS - NBA': ('https://www.cbssports.com/rss/headlines/nba/', 'NBA', 'General'),
    
    # NFL
    'ESPN - NFL': ('https://www.espn.com/espn/rss/nfl/news', 'NFL', 'General'),
    'Yahoo - NFL': ('https://sports.yahoo.com/nfl/rss/', 'NFL', 'General'),
    'CBS - NFL': ('https://www.cbssports.com/rss/headlines/nfl/', 'NFL', 'General'),
    'NBC - NFL': ('https://profootballtalk.nbcsports.com/feed/', 'NFL', 'General'),
    
    # MLB
    'ESPN - MLB': ('https://www.espn.com/espn/rss/mlb/news', 'MLB', 'General'),
    'Yahoo - MLB': ('https://sports.yahoo.com/mlb/rss/', 'MLB', 'General'),
    'CBS - MLB': ('https://www.cbssports.com/rss/headlines/mlb/', 'MLB', 'General'),
    
    # NHL
    'ESPN - NHL': ('https://www.espn.com/espn/rss/nhl/news', 'NHL', 'General'),
    'Yahoo - NHL': ('https://sports.yahoo.com/nhl/rss/', 'NHL', 'General'),
    'The Hockey News': ('https://thehockeynews.com/feed', 'NHL', 'News'),
    'Sportsnet NHL': ('https://www.sportsnet.ca/hockey/nhl/feed', 'NHL', 'Analysis'),
    'Daily Faceoff': ('https://www.dailyfaceoff.com/feed', 'NHL', 'Analysis'),
    'CBS - NHL': ('https://www.cbssports.com/rss/headlines/nhl/', 'NHL', 'General'),
    
    # SOCCER
    'ESPN - Soccer': ('https://www.espn.com/espn/rss/soccer/news', 'SOCCER', 'General'),
    'CaughtOffside': ('https://www.caughtoffside.com/feed/', 'SOCCER', 'Transfer'),
    'Marca - Soccer': ('https://e00-marca.uecdn.es/rss/en/index.xml', 'SOCCER', 'International'),
    'BBC - Soccer': ('https://feeds.bbci.co.uk/sport/football/rss.xml', 'SOCCER', 'General'),
    
    # GOLF
    'ESPN - Golf': ('https://www.espn.com/espn/rss/golf/news', 'GOLF', 'General'),
    'Yahoo - Golf': ('https://sports.yahoo.com/golf/rss/', 'GOLF', 'General'),
    'Bunkered': ('https://www.bunkered.co.uk/rss', 'GOLF', 'General'),
    'Geoff Shackelford': ('https://www.geoffshackelford.com/homepage?format=rss', 'GOLF', 'Analysis'),
    'CBS - Golf': ('https://www.cbssports.com/rss/headlines/golf/', 'GOLF', 'General'),
    
    # TENNIS
    'ESPN - Tennis': ('https://www.espn.com/espn/rss/tennis/news', 'TENNIS', 'General'),
    'Tennis-X': ('http://www.tennis-x.com/tennisxnews.xml', 'TENNIS', 'ATP/WTA'),
    'Essentially Sports - Tennis': ('https://www.essentiallysports.com/category/tennis/feed/', 'TENNIS', 'News'),
    'Tennis Head': ('https://tennishead.net/feed/', 'TENNIS', 'News'),
    'UbiTennis': ('https://www.ubitennis.net/feed/', 'TENNIS', 'News'),
    
    # WWE
    'WrestleView': ('https://www.wrestleview.com/feed/', 'WWE', 'News'),
    'ESPN - WWE': ('https://www.espn.com/espn/rss/wwe/news', 'WWE', 'News'),
    'Fightful': ('https://www.fightful.com/rss', 'WWE', 'News'),
    'Cageside Seats': ('https://www.cagesideseats.com/rss/current.xml', 'WWE', 'News'),
    'PWTorch': ('https://www.pwtorch.com/site/feed/', 'WWE', 'News'),
    
    # FIGHTING
    'Yahoo - MMA': ('https://sports.yahoo.com/mma/rss/', 'FIGHTING', 'MMA'),
    'Yahoo - Boxing': ('https://sports.yahoo.com/boxing/rss/', 'FIGHTING', 'Boxing'),
    'ESPN - MMA': ('https://www.espn.com/espn/rss/mma/news', 'FIGHTING', 'MMA'),
    'Bad Left Hook': ('https://www.badlefthook.com/rss/current.xml', 'FIGHTING', 'Boxing'),
    
    # RACING
    'Motorsport - MotoGP': ('https://www.motorsport.com/rss/motogp/news/', 'RACING', 'MOTOGP'),
    'Autosport - MotoGP': ('https://www.autosport.com/rss/feed/motogp', 'RACING', 'MOTOGP'),
    'Roadracing World': ('https://www.roadracingworld.com/news/category/motogp/feed/', 'RACING', 'MOTOGP'),
    'Motorsport - NASCAR': ('https://www.motorsport.com/rss/nascar-cup/news/', 'RACING', 'NASCAR'),
    'Autosport - NASCAR': ('https://www.autosport.com/rss/feed/nascar', 'RACING', 'NASCAR'),
    'Motorsports Tribune': ('https://motorsportstribune.com/category/nascar/feed/', 'RACING', 'NASCAR'),
    'Yahoo - F1': ('https://sports.yahoo.com/f1/rss/', 'RACING', 'F1'),
    'Yahoo - NASCAR': ('https://sports.yahoo.com/nascar/rss/', 'RACING', 'NASCAR'),
    'Jayski': ('https://www.jayski.com/json/articles/?format=rss', 'RACING', 'NASCAR'),
    'Crash.net MotoGP': ('https://www.crash.net/rss/motogp', 'RACING', 'MOTOGP'),
    'Crash.net NASCAR': ('https://www.crash.net/rss/nascar', 'RACING', 'NASCAR'),
    'BBC - F1': ('https://feeds.bbci.co.uk/sport/formula1/rss.xml', 'RACING', 'F1'),
    
    # COLLEGE
    'Yahoo - NCAAF': ('https://sports.yahoo.com/college-football/rss/', 'COLLEGE', 'Football'),
    'Yahoo - NCAAB': ('https://sports.yahoo.com/college-basketball/rss/', 'COLLEGE', 'Basketball'),
    'D1Baseball': ('https://d1baseball.com/feed/', 'COLLEGE', 'Baseball'),
    'D1Softball': ('https://d1softball.com/feed/', 'COLLEGE', 'Softball'),
    'Extra Inning Softball': ('https://extrainningsoftball.com/feed/', 'COLLEGE', 'Softball'),
    'Swish Appeal': ('https://www.swishappeal.com/rss/current.xml', 'COLLEGE', 'W-Basketball'),
    'CBS - NCAAF': ('https://www.cbssports.com/rss/headlines/college-football/', 'COLLEGE', 'Football'),
    'CBS - NCAAB': ('https://www.cbssports.com/rss/headlines/college-basketball/', 'COLLEGE', 'Basketball'),
    
    # GENERAL / INSTITUTIONAL
    'Yahoo Top': ('https://sports.yahoo.com/rss/', 'GEN', 'Top'),
    'SBNation': ('https://www.sbnation.com/rss/current.xml', 'GEN', 'Analysis'),
    'FanSided': ('https://fansided.com/feed/', 'GEN', 'Opinion'),
    'Deadspin': ('https://deadspin.com/rss', 'GEN', 'News'),
}

_COLLEGE_KEYWORDS = [
    r'college', r'ncaa', r'recruit', r'commit', r'cfb', r'cbb', r'wcws', r'ncaa\.com', 
    r'varsity', r'd1', r'sec network', r'big ten', r'acc', r'sec', r'pac-12', r'big 12',
    r'softball', r'baseball'
]

_SPORT_KEYWORDS = {
    'NBA': [r'nba', r'lebron', r'lakers', r'warriors', r'celtics', r'basketball', r'knicks', r'76ers', r'hoops', r'dunk', r'wnba'],
    'NFL': [r'nfl', r'mahomes', r'super bowl', r'touchdown', r'cowboys', r'quarterback', r'gridiron', r'football', r'interception', r'touchdowns'],
    'MLB': [r'mlb', r'ohtani', r'yankees', r'baseball', r'homerun', r'statcast', r'pitcher', r'ballpark', r'strikeout', r'innings', r'homeruns'],
    'NHL': [r'nhl', r'mcdavid', r'hockey', r'puck', r'stanley cup', r'slapshot', r'skating'],
    'SOCCER': [r'soccer', r'fifa', r'messi', r'ronaldo', r'premier league', r'champions league', r'fwa', r'united', r'transfer', r'la liga', r'bundesliga', r'football club', r'la-liga'],
    'RACING': [r'f1', r'formula 1', r'formulaone', r'nascar', r'motogp', r'verstappen', r'lewis hamilton', r'indycar', r'racing', r'paddock', r'grand prix', r'mclaren'],
    'TENNIS': [r'tennis', r'djokovic', r'federer', r'nadal', r'wimbledon', r'atp', r'wta', r'grand slam'],
    'GOLF': [r'golf', r'tiger woods', r'masters', r'pga', r'lpga', r'mcilroy', r'fairway'],
    'WWE': [r'wwe', r'wrestlemania', r'wrestling', r'smackdown', r'raw', r'tko', r'royal rumble'],
    'FIGHTING': [r'mma', r'ufc', r'boxing', r'mcgregor', r'knockout', r'heavyweight', r'octagon'],
}

_SOFTBALL_KEYWORDS = [r'softball', r'fastpitch', r'wcws', r'd1softball']

def _infer_sport(title, summary, current_sub, primary_cat, url=""):
    text = (title + " " + summary).lower()
    url_lower = url.lower() if url else ""
    
    # 1. Determine if it is College Sports first
    is_college = False
    if url_lower:
        if any(x in url_lower for x in ['/college-football/', '/cfb/', '/college-basketball/', '/cbb/', '/softball/', '/college-baseball/', '/college-', '/ncaa']):
            is_college = True
        elif any(x in url_lower for x in ['/nba/', '/wnba/', '/nfl/', '/mlb/', '/nhl/', '/golf/', '/tennis/', '/wwe/', '/mma/', '/ufc/', '/boxing/', '/f1/', '/nascar/', '/motogp/']):
            is_college = False
        else:
            if primary_cat.upper() == 'COLLEGE':
                is_college = True
            else:
                for ck in _COLLEGE_KEYWORDS:
                    if re.search(r'\b' + ck + r'\b', text):
                        is_college = True
                        break
    else:
        if primary_cat.upper() == 'COLLEGE':
            is_college = True
        else:
            for ck in _COLLEGE_KEYWORDS:
                if re.search(r'\b' + ck + r'\b', text):
                    is_college = True
                    break

    # 2. Determine Sport category
    inferred_sport = None
    
    # Check URL path for explicit sport indicators first
    if url_lower:
        if any(x in url_lower for x in ['/college-football/', '/cfb/']):
            inferred_sport = 'NFL'
        elif any(x in url_lower for x in ['/college-basketball/', '/cbb/']):
            inferred_sport = 'NBA'
        elif '/softball/' in url_lower:
            inferred_sport = 'Softball'
        elif any(x in url_lower for x in ['/college-baseball/', '/baseball/', '/mlb/']) and ('/college-' in url_lower or '/ncaa' in url_lower):
            inferred_sport = 'MLB'
        elif '/nba/' in url_lower or '/wnba/' in url_lower or '/basketball/' in url_lower:
            inferred_sport = 'NBA'
        elif '/nfl/' in url_lower or '/football/' in url_lower:
            inferred_sport = 'NFL'
        elif '/mlb/' in url_lower or '/baseball/' in url_lower:
            inferred_sport = 'MLB'
        elif '/nhl/' in url_lower or '/hockey/' in url_lower:
            inferred_sport = 'NHL'
        elif any(x in url_lower for x in ['/soccer/', '/football/', '/transfer-rumours/']) and not any(x in url_lower for x in ['/nfl/', '/college-football/']):
            inferred_sport = 'SOCCER'
        elif '/golf/' in url_lower:
            inferred_sport = 'GOLF'
        elif '/tennis/' in url_lower:
            inferred_sport = 'TENNIS'
        elif '/wwe/' in url_lower or '/wrestling/' in url_lower:
            inferred_sport = 'WWE'
        elif any(x in url_lower for x in ['/mma/', '/ufc/', '/boxing/', '/fighting/']):
            inferred_sport = 'FIGHTING'
        elif any(x in url_lower for x in ['/f1/', '/formula-1/', '/nascar/', '/motogp/', '/racing/']):
            inferred_sport = 'RACING'

    # Fallback to text keywords if URL path did not yield a specific sport
    if not inferred_sport:
        for sk in _SOFTBALL_KEYWORDS:
            if re.search(r'\b' + sk + r'\b', text):
                inferred_sport = 'Softball'
                break
                
        if not inferred_sport:
            for sport, keywords in _SPORT_KEYWORDS.items():
                found = False
                for k in keywords:
                    if re.search(r'\b' + re.escape(k) + r'\b', text):
                        inferred_sport = sport
                        found = True
                        break
                if found:
                    break

    # 3. Resolve hierarchical routing
    final_sub = current_sub if current_sub else 'General'
    
    if is_college:
        sport_sub_map = {
            'NFL': 'Football',
            'NBA': 'Basketball',
            'MLB': 'Baseball',
            'Softball': 'Softball',
            'NHL': 'Hockey',
            'SOCCER': 'Soccer'
        }
        sub_name = sport_sub_map.get(inferred_sport, inferred_sport)
        if sub_name:
            final_sub = sub_name
        else:
            if current_sub and current_sub.lower() not in ['general', 'news', 'top', 'trending', 'analysis', 'opinion']:
                final_sub = current_sub
            else:
                final_sub = 'General'
        return 'COLLEGE', final_sub
    
    else:
        if inferred_sport:
            if inferred_sport == 'Softball':
                return 'COLLEGE', 'Softball'
            
            if current_sub and current_sub.lower() not in ['general', 'news', 'top', 'trending', 'analysis', 'opinion']:
                final_sub = current_sub
            else:
                if inferred_sport == 'RACING':
                    if any(k in text for k in ['f1', 'formula 1', 'formulaone', 'verstappen', 'hamilton', 'mclaren', 'grand prix', 'paddock']):
                        final_sub = 'F1'
                    elif any(k in text for k in ['nascar', 'jayski', 'cup series', 'cup race']):
                        final_sub = 'NASCAR'
                    elif any(k in text for k in ['motogp', 'moto-gp', 'gp', 'ducati']):
                        final_sub = 'MOTOGP'
                    else:
                        final_sub = 'General'
                elif inferred_sport == 'TENNIS':
                    if any(k in text for k in ['wta', 'women', 'serena', 'swiatek', 'gauff', 'sabalenka']):
                        final_sub = 'WTA'
                    elif any(k in text for k in ['atp', 'men', 'djokovic', 'sinner', 'alcaraz', 'medvedev', 'federer', 'nadal']):
                        final_sub = 'ATP'
                    else:
                        final_sub = 'General'
                elif inferred_sport == 'FIGHTING':
                    if any(k in text for k in ['mma', 'ufc', 'octagon', 'mcgregor', 'jones', 'pereira', 'white']):
                        final_sub = 'MMA'
                    elif any(k in text for k in ['boxing', 'boxer', 'canelo', 'fury', 'usyk', 'ring', 'knockout', 'ko']):
                        final_sub = 'Boxing'
                    else:
                        final_sub = 'General'
                else:
                    final_sub = 'General'
            return inferred_sport, final_sub
        else:
            p_cat = 'GEN' if primary_cat == 'GEN' else primary_cat
            known_sports = ['NBA', 'NFL', 'MLB', 'NHL', 'SOCCER', 'RACING', 'TENNIS', 'GOLF', 'WWE', 'FIGHTING']
            if primary_cat in known_sports:
                p_cat = primary_cat
            return p_cat, final_sub

_JUNK_PATTERNS = re.compile(
    r"(cookies|privacy policy|advertising|subscription|sign up|newsletter|copyright|terms of service|all rights reserved)",
    re.IGNORECASE,
)

_EDITORIAL_KEYWORDS = re.compile(
    r"(trade|injury|signing|game|score|coach|team|player|championship|win|loss|record|historic|season|contract|official|source|report|news|update|vs|beat|defeat|league|star|mvp|roster|draft|pick|playoff|final)",
    re.IGNORECASE,
)

def _clean_text(text):
    if not text: return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ").replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:400] if len(text) > 400 else text

def _is_junk(text):
    if not text or len(text) < 40: return True
    if len(_JUNK_PATTERNS.findall(text[:300])) >= 2: return True
    # Sports-specific relevance check
    editorial_matches = len(_EDITORIAL_KEYWORDS.findall(text))
    if editorial_matches < 1: return True
    return False

async def fetch_feeds():
    # 0. Gating Logic: Avoid rate-limiting (30m cooldown)
    force = "--force" in sys.argv
    if os.path.exists(DB_PATH) and not force:
        file_age_m = (time.time() - os.path.getmtime(DB_PATH)) / 60
        if file_age_m < 30:
            print(f"[!] Intelligence Cache is fresh ({file_age_m:.1f}m old). Skipping sync to protect endpoints. Use --force to override.")
            return
    
    if force:
        print("[*] Force sync requested. Bypassing cooldown.")

    print(f"Starting Sovereign Stealth Mirror Engine...")
    all_articles = []
    
    # V30.6.22: Persistent Intelligence Layer (Load existing articles)
    # 🚨 CRITICAL RULE: NEVER remove or delete database/sports_news.js!
    # If the database needs fixing, use script modifications to correct it in-place.
    try:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                json_str = content.replace("window.sports_news = ", "").strip().rstrip(";")
                all_articles = json.loads(json_str)
                
                # V30.6.25: Self-Healing - Purge Future Dates
                # This fixes the "Future Article" bug caused by previous timezone calculation errors.
                tz_est = datetime.timezone(datetime.timedelta(hours=-4))
                now_est = datetime.datetime.now(tz_est)
                before_count = len(all_articles)
                all_articles = [a for a in all_articles if datetime.datetime.fromisoformat(a['published_at']) <= now_est]
                purged = before_count - len(all_articles)
                if purged > 0:
                    print(f"[*] Self-healing: Purged {purged} articles with future timestamps.")
                
                # V30.6.26: Re-classify existing articles with updated classification logic
                for a in all_articles:
                    feed_info = FEEDS.get(a.get('source'))
                    orig_p_cat = feed_info[1] if feed_info else a.get('primary_category')
                    orig_s_cat = feed_info[2] if feed_info else a.get('sub_category')
                    new_p_cat, new_s_cat = _infer_sport(a['title'], a['summary'], orig_s_cat, orig_p_cat, a.get('url', ''))
                    a['primary_category'] = new_p_cat
                    a['sub_category'] = new_s_cat
                print(f"[*] Loaded {len(all_articles)} valid articles from persistent layer (re-classified).")
    except Exception as e:
        print(f"[!] Persistence error (Likely fresh build): {e}")
    
    # 1. De-clumping & Institutional Staggering
    items = list(FEEDS.items())
    
    # V30.6.22: Targeted Source Filtering (--source)
    source_filter = None
    for arg in sys.argv:
        if arg.startswith("--source="):
            source_filter = arg.split("=")[1].lower()
    
    if source_filter:
        items = [i for i in items if source_filter in i[0].lower() or source_filter in i[1][1].lower()]
        print(f"[*] Targeted sync: Filtered to {len(items)} sources matching '{source_filter}'")

    random.shuffle(items)
    
    final_queue = []
    while items:
        found = False
        for i in range(len(items)):
            source, (url, p_cat, s_cat) = items[i]
            domain = urlparse(url).netloc
            last_domain = urlparse(final_queue[-1][1][0]).netloc if final_queue else None
            if domain != last_domain:
                final_queue.append(items.pop(i))
                found = True
                break
        if not found: final_queue.append(items.pop(0))

    # 2. Stealth Navigator Pool (V30.6.15)
    nav = StealthNavigator(headless=True)
    await nav.initialize()
    
    try:
        for i, (source, (url, primary_cat, sub_cat)) in enumerate(final_queue):
            # Global Randomized Stagger (Institutional Stealth - Increased for V30.6)
            # Simulates a human switching between tabs/sites with a thinking pause
            initial_delay = random.uniform(8.5, 18.5)
            if i > 0: await asyncio.sleep(initial_delay)
            
            print(f"[*] Fetching {source} ({primary_cat}) via Stealth...")
            
            try:
                page = await nav.context.new_page()
                # Use ghost_browse for human-like behavior on every 5th fetch
                response = None
                if i % 5 == 0:
                    response = await nav.ghost_browse(page, url)
                else:
                    response = await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                
                # Retrieve raw XML source text rather than rendered DOM HTML
                if response:
                    content = await response.text()
                else:
                    content = await page.content()
                await page.close()
                
                # V30.6.22: Advanced XML Unwrapping for browser-rendered feeds
                content_lower = content.lower()
                if "<pre" in content_lower and "</pre>" in content_lower:
                    match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL | re.IGNORECASE)
                    if match:
                        content = match.group(1)
                elif "<code" in content_lower and "</code>" in content_lower:
                    match = re.search(r'<code[^>]*>(.*?)</code>', content, re.DOTALL | re.IGNORECASE)
                    if match:
                        content = match.group(1)
                
                # If content looks like HTML but should be XML, try to find the start of XML
                if "<?xml" not in content and "<rss" not in content and "<feed" not in content:
                    # Maybe it's a page with a link to the feed?
                    pass

                feed = feedparser.parse(content)
                
                # If feedparser fails to parse content directly, try fetching again
                if not feed.entries or len(feed.entries) == 0:
                    # Fallback to direct URL fetch (some sites allow this if headers are right)
                    feed = feedparser.parse(url)
                
                if not feed.entries:
                    print(f"    [!] No articles found. Content snippet: {content[:150].replace('\\n', ' ')}...")

                articles_found = 0
                for entry in feed.entries[:10]:
                    title = _clean_text(entry.get('title', ''))
                    summary = _clean_text(entry.get('summary', entry.get('description', '')))
                    link = entry.get('link', '')
                    
                    if not title or _is_junk(title + " " + summary): 
                        continue

                    # V30.6.15: Get real published timestamp
                    pub_date = entry.get('published_parsed', entry.get('updated_parsed'))
                    # Institutional Timezone: Eastern Time (EDT/EST)
                    # We use UTC-4 for EDT (Summer) to ensure 12:30 PM when CST is 11:30 AM.
                    tz_est = datetime.timezone(datetime.timedelta(hours=-4))
                    
                    if pub_date:
                        try:
                            # Convert struct_time to UTC then to EST
                            # V30.6.24 Fix: Use calendar.timegm for UTC struct_time instead of time.mktime
                            epoch = calendar.timegm(pub_date)
                            dt = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).astimezone(tz_est)
                            timestamp = dt.isoformat()
                            hours_old = (time.time() - epoch) / 3600
                        except Exception:
                            timestamp = datetime.datetime.now(tz_est).isoformat()
                            hours_old = 0
                    else:
                        timestamp = datetime.datetime.now(tz_est).isoformat()
                        hours_old = 0

                    impact_score = analyze_article_impact(title, summary, source)
                    
                    # V30.6.26: Hierarchical Categorization
                    article_primary_cat, article_sub_cat = _infer_sport(title, summary, sub_cat, primary_cat, link)
                    
                    # V30.6.15: Calculate Hot Score (Grace Period + Decay)
                    # A 90-rating news item stays at 90 for 4 hours, then decays to ~60 at hour 18.
                    grace_period = float(os.getenv("SPORTSVADER_GRACE_PERIOD", 4))
                    halflife = float(os.getenv("SPORTSVADER_HALFLIFE_HOURS", 24.5))
                    
                    decay_time = max(0, hours_old - grace_period)
                    decayed_score = impact_score * (0.5 ** (decay_time / halflife))

                    all_articles.append({
                        "title": title,
                        "summary": summary,
                        "url": link,
                        "source": source,
                        "primary_category": article_primary_cat,
                        "sub_category": article_sub_cat,
                        "published_at": timestamp,
                        "score": impact_score,
                        "hot_score": decayed_score
                    })
                    articles_found += 1
                
                print(f"    [+] Found {articles_found} articles.")
                
            except Exception as e:
                print(f"    [!] Stealth Fetch failed for {source}: {e}")
                continue

    finally:
        await nav.close()

    # Normalization & Deduplication (Sorted by Hot Score)
    seen_titles = set()
    seen_urls = set()
    unique_articles = []
    
    # Sort by published_at DESC then hot_score DESC to keep freshest and most impactful
    all_articles.sort(key=lambda x: (x.get('published_at', ''), x.get('hot_score', 0)), reverse=True)
    
    # V30.6.22: Per-Category Limiting Logic (Expanded for Institutional Depth)
    cat_counts = {}
    cat_limits = {
        'GEN': 75,
        'COLLEGE': 150
    }
    default_cat_limit = 50
    global_limit = 600
    
    for a in all_articles:
        t_key = a['title'].lower().strip()
        u_key = a['url'].lower().strip()
        p_cat = a['primary_category'].upper()
        
        if t_key not in seen_titles and u_key not in seen_urls:
            # Enforce per-category limits
            current_cat_count = cat_counts.get(p_cat, 0)
            limit = cat_limits.get(p_cat, default_cat_limit)
            
            if current_cat_count < limit:
                seen_titles.add(t_key)
                seen_urls.add(u_key)
                unique_articles.append(a)
                cat_counts[p_cat] = current_cat_count + 1
            
            # Global Break if reached
            if len(unique_articles) >= global_limit:
                break

    # Add sync_time for UI (Forced to Eastern Time)
    if unique_articles:
        tz_est = datetime.timezone(datetime.timedelta(hours=-4))
        unique_articles[0]['sync_time'] = datetime.datetime.now(tz_est).strftime("%I:%M %p")

    # Save Database (V30 Mirror: Variable name MUST be sports_news)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        f.write(f"window.sports_news = {json.dumps(unique_articles, indent=2)};")
    
    print("[OK] SYNC COMPLETE.")

if __name__ == "__main__":
    asyncio.run(fetch_feeds())
