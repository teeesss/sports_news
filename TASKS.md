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
- [x] Monitor long-term stability of stealth fetches ✅
- [x] Track mobile engagement with 2-row nav ✅

## Classification Hardening (V30.6.27)
- [x] Expanded `_SPORT_KEYWORDS` with 3-5x more sport-specific terms (bullpen/ERA/RBI for MLB, sack/blitz/QB for NFL, power play/goalie for NHL, etc.) ✅
- [x] Added `_HIGH_SCHOOL_INDICATORS` regex — prep/varsity/state championship articles now early-exit to GEN ✅
- [x] Raised GEN feed minimum confidence threshold from 2 → 4 to prevent noise promotions ✅
- [x] Expanded `_COLLEGE_KEYWORDS` with conference names (Big East, Mountain West, Sun Belt, CWS, super regional) ✅
- [x] Fixed NHL team name collisions ("devils"→"new jersey devils", "rangers"→"new york rangers", etc.) ✅
- [x] Added text-validated sport detector for COLLEGE sub_category routing — prevents "overtime" routing basketball articles to Hockey ✅
- [x] Added March Madness bracket keywords (elite eight, sweet sixteen, final four) for basketball sub_category ✅
- [x] Expanded test suite from 8 → 30 tests covering all 10 sport types + HS exclusion + GEN threshold + college disambiguation ✅
- [x] All 30 tests passing ✅

## V30.6.28 - Seasonal Intelligence + Generic Source Drop (2026-05-23)
- [x] Added _SEASON_ACTIVE calendar: sports active by month ✅
- [x] Added _SEASON_PEAK calendar: peak/playoff sports get 2x score boost (NBA/NHL/MLB/COLLEGE/Softball in May) ✅
- [x] Added _GENERIC_SOURCES: Yahoo Top, SBNation, FanSided, Deadspin ✅
- [x] Off-season sports get 0.4x score penalty (NFL in May won't win disambiguation) ✅
- [x] college_dominates guard: when college_signal >= pro_signal*2, suppresses pro-team peak boost (fixes tigers=Detroit vs LSU) ✅
- [x] COLLEGE sub fallback: no longer inherits current_sub blindly; requires word-boundary sport keyword confirmation ✅
- [x] HS school name pattern: catches [School] High [football|coach|etc] constructs ✅
- [x] Drop rule: GEN or COLLEGE:General from generic sources -> skip, not shown ✅
- [x] Regression tests added: all 3 user-reported failures now covered (Orgeron, Stillwater, UCF/UCLA) ✅
- [x] 37/37 tests pass ✅
- [x] Deployed to bmwseals.com/sports-test ✅

## V30.6.29 - College Sport Classification Hardening & Domain Lock (2026-05-23)
- [x] Case-Insensitive Lock: Normalized feed-source lookup to protect locked feeds case-insensitively during persistence reloads. ✅
- [x] Indentation Fix: Corrected nesting of pro vs college boundary scoring so it checks all feeds (including COLLEGE and specific pro leagues) rather than only GEN. ✅
- [x] Regex Word-Boundary Protection: Migrated college sport sub-category checks to regex search with word boundaries and `re.escape()` to avoid substring collisions (e.g. "beginning" matching "inning" for Baseball). ✅
- [x] Regression Testing: Verified 37/37 tests passing cleanly. ✅
- [x] Deployed updates to staging server and verified all systems. ✅

## V30.6.30 - Production Deployment & Documentation Alignment (2026-05-23)
- [x] Promoted V30.6.29 assets from staging to live production site (`bmwseals.com/sports`). ✅
- [x] Standardized `.env` credentials for active production pipeline target. ✅
- [x] Verified full production bundle generation (`build_dist.py`) and secure SFTP deployment (`remote_sync.py`). ✅
- [x] Verified core test suite (44/44 green) against target platform. ✅
- [x] Updated all project-wide architectural, operational, and lifecycle documentation. ✅
