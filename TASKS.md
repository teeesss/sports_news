# Tasks

## 🚨 CRITICAL RULE
**NEVER DO THE FOLLOWING:** Never Remove `database/sports_news.js`. All database fixes must be done via script modifications, not file deletion!

## Intelligence Engine (V30.6.15)
- [x] Mirror `StealthNavigator` from `COS_Stock_Plays` to `Sports_News` ✅
- [x] Refactor `sports_scraper.py` to use `StealthNavigator` for all fetches ✅
- [x] Convert `sports_scraper.py` to async to support Playwright ✅
- [x] Verify stealth bypass for blocked sites (ESPN, CaughtOffside) ✅
- [x] Fix outdated URLs for CBS and WTA (replaced dead WTA with Tennis-X) ✅
- [x] Expand registry with new high-fidelity sources ✅
- [x] Hardened SportsVADER with configurable .env knobs ✅
- [x] Implemented Decay-Adjusted "Hot Score" ranking algorithm ✅

## UI/UX Hardening (V30.6.22)
- [x] Standardize Typography to 'Outfit' geometric sans-serif ✅
- [x] Implement Institutional Header (Desktop) with split stats/branding ✅
- [x] Implement High-Density Mobile Header (Centered/Shrunk -33%) ✅
- [x] Reconfigure Mobile Navigation to 2-row wrap layout ✅
- [x] Add Mobile Zebra-Striping for card delineation ✅
- [x] Create custom 'Lightning-S' SVG favicon ✅
- [x] Eliminate source/category badge redundancy ✅
- [x] Implement Dual-Tone Cyber Rails (Emerald/Indigo) for desktop ✅
- [x] Add centered EST label under sync time (Desktop Only) ✅

## Intelligence Hardening (V30.6.23)
- [x] Fix "double-labeling" of sports where `NHL` receives an `NBA` sub-label due to generic keyword crossover (e.g., "playoffs"). ✅
- [x] Ensure `_infer_sport` does not override a specific feed's known sport mapping. ✅
- [x] Implement robust regex word boundaries in `_SPORT_KEYWORDS` to prevent accidental substring matches (e.g., "mcl" in "McLaren"). ✅
- [x] Wipe legacy cache to flush corrupted classifications and push a clean feed payload to production. ✅
- [x] Fix `SyntaxError` in `sports_scraper.py` (missing `except` block in persistent layer loader). ✅
- [x] Implement Open Graph (OG) and Twitter meta tags for Slack link unfurling. ✅
- [x] Generate and deploy premium `og_image.png` for sports portal branding. ✅
- [x] Standardize all timestamps (sync and articles) to Eastern Time (UTC-4) to resolve CST/CDT discrepancy. ✅




## Intelligence Hardening (V30.6.24)
- [x] Streamlined UI by removing manual "SYNC" button to rely on automated scheduling. ✅
- [x] Resolved dead/broken RSS feeds for Jayski, Sportsnet NHL, and Tennis-X. ✅
- [x] Consolidated Marca entries into high-fidelity International English feed. ✅
- [x] Integrated new institutional feeds for College Baseball (D1Baseball), Softball (D1Softball), and Women's Basketball (Swish Appeal). ✅
- [x] Enhanced UI with dedicated "COLLEGE" sub-navigation for granular filtering. ✅
- [x] Implemented "Deep Stealth" mode with multi-phase scrolling and human-like delays. ✅
- [x] Increased global fetch stagger to 8.5s-18.5s to reduce institutional footprint. ✅

## Temporal Hardening (V30.6.25)
- [x] Corrected `sports_scraper.py` timezone logic by replacing `time.mktime` (local) with `calendar.timegm` (UTC) for RSS parsing. ✅
- [x] Implemented "Self-Healing" persistence layer to automatically purge future-dated articles (> now) from `sports_news.js`. ✅
- [x] Refined `web/index.html` header to include current date next to EST sync time for high-fidelity situational awareness. ✅
- [x] Stabilized `timeAgo` function to handle clock drift by defaulting extremely recent or future-dated articles to "1 MINS AGO". ✅
- [x] Verified and deployed cleansed database to production, eliminating the "Boo Weekley" future-date poisoning. ✅

## Premium Feed Ingest & UI Refinement (V30.6.26)
- [x] Integrated 10 premium free RSS feeds for CBS, BBC, and NBC Sports. ✅
- [x] Aligned client hints dynamically with browser user agent version to prevent stealth degradation. ✅
- [x] Upgraded portal styling to high-fidelity Glassmorphism visual theme with custom rail-colored neon glow shadows. ✅
- [x] Implemented source-level slide-down filter panel `[SOURCES ▾]` in `web/index.html` to filter articles by ingestion source (e.g. ESPN, CBS, BBC, D1Baseball, D1Softball, Swish Appeal, Yahoo, etc.). ✅
- [x] Resolved "GEN" misclassification by implementing a two-pass hierarchical classification engine in `engine/sports_scraper.py` to correctly map sports (Football, Baseball, Basketball, Softball, Soccer, Hockey) and College tags, defaulting to General/GEN only when unresolvable. ✅
- [x] Increased COLLEGE article limits to 150 (and global limit to 600) to prevent college baseball and softball articles from being pruned by NCAAF/NCAAB articles. ✅
- [x] Deployed and verified whole release on `bmwseals.com/sports-test` staging endpoint. ✅


## Monitoring
- [ ] Monitor long-term stability of stealth fetches
- [ ] Track mobile engagement with 2-row nav
