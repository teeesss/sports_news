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

- **2026-05-23 11:38**:
  - `tests/test_categorization.py`: PASS (Hierarchical categorization for COLLEGE Football/Softball, pro NBA, and F1 verified)
  - `tests/test_new_feeds.py`: PASS (CBS, BBC, and NBC Sports RSS reachability verified)
  - `tests/test_registry_contains_new_feeds.py`: PASS (Registry integration verified)
  - `tests/test_stealth_hints.py`: PASS (Client-hints dynamic sync with rotated Chrome version strings verified)
  - `tests/test_ui_styles.py`: PASS (Glassmorphism backdrop-filters and cyber rail shadows verified)
  - `Full Suite`: PASS (11/11 tests pass successfully)
  - Status: PASS.
