# Test Results

- **2026-05-08 17:41**:
  - `tests/test_stealth.py`: PASS (CaughtOffside 403 bypass confirmed)
  - `engine/sports_scraper.py`: PASS (Full registry sync successful)
  - `CBS/WTA Fix`: PASS (Updated CBS URL and WTA fallback)
  - `New Sources`: PASS (Yahoo Top, SBNation, Deadspin, Marca, FanSided, Bleacher Report verified)
  - `SportsVADER Config`: PASS (.env knobs successfully integrated)
  - `Hot Score Algorithm`: PASS (Refined Grace-Decay model: 4h Grace + 24.5h Half-Life)
  - Status: 100% success on stealth fetch migration and intelligence ranking optimization.

- **2026-05-11 14:13**:
  - `engine/sports_scraper.py`: PASS (Temporal Hardening: `calendar.timegm` fix verified).
  - `Persistence Check`: PASS (Self-Healing: Purged 12 articles with future timestamps).
  - `UI Verification`: PASS (Header date label and "1 MINS AGO" revert verified).
  - Status: PASS.

- **2026-05-23 11:48**:
  - `tests/test_categorization.py`: PASS (Hierarchical categorization for COLLEGE Football/Softball, pro NBA, F1, and URL-based classification overrides verified)
  - `tests/test_new_feeds.py`: PASS (CBS, BBC, and NBC Sports RSS reachability verified)
  - `tests/test_registry_contains_new_feeds.py`: PASS (Registry integration verified)
  - `tests/test_stealth_hints.py`: PASS (Client-hints dynamic sync with rotated Chrome version strings verified)
  - `tests/test_ui_styles.py`: PASS (Glassmorphism backdrop-filters and cyber rail shadows verified)
  - `Full Suite`: PASS (13/13 tests pass successfully)
  - Status: PASS.

- **2026-05-23 V30.6.27**:
  - `tests/test_categorization.py`: PASS (30/30 — All 10 sport types, HS exclusion, GEN threshold, college disambiguation)
  - New tests added: HS football/basketball/baseball stays GEN; NFL URL overrides HS text; MLB/NFL/NHL/NBA/SOCCER specific keyword routing; ATP/WTA disambiguation; NASCAR/Golf/MMA/Boxing sub-routing; College CWS/NCAA tournament; transfer portal; GEN threshold enforcement
  - Status: **30/30 PASS**.
- **2026-05-23 V30.6.28**:
  - `tests/test_categorization.py`: PASS (37/37 — All tests passing successfully)
  - Coverage: Ed Orgeron (D1Baseball feed no sport evidence falls back to COLLEGE:General), Stillwater High (HS construct excluded), UCF/UCLA Softball Super Regional, seasonal active/peak filters.
  - Status: **37/37 PASS**.

- **2026-05-23 V30.6.30**:
  - `Core test suite`: PASS (44/44 — All tests passing successfully)
  - Coverage: Core sport categorization, seasonal active/peak filters, stealth client-hints, glassmorphism UI styles, registry verification, scraper integration.
  - Status: **44/44 PASS**.
