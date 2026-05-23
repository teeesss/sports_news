# Sovereign Sports Intelligence - Architecture & Operations

## 🚨 CRITICAL RULE
**NEVER DO THE FOLLOWING:** Never Remove `database/sports_news.js`. All fixes must be done via script modifications, not file deletion!

## 🏛️ UI/UX Design System (V30.6.22)
- **Aesthetic**: Institutional Utility / Cyber-Dossier.
- **Typography**: 'Outfit' Geometric Sans-Serif (Primary).
- **Desktop Logic**: Split-header rail with **Dual-Tone Cyber Rails** (Emerald/Indigo), 0.08 background tints, and centered EST label under sync time.
- **Mobile Logic**: High-Density centered layout with 2-row navigation and zebra-striped cards (`0.47` opacity).

## ⚙️ Intelligence Engine Migration (V30.6.15)
- **Scraper**: `Async` + `Playwright` via `StealthNavigator` (Deep Stealth V30.6.24).
- **Ranking**: Decay-Adjusted "Hot Score" (Time-sensitive weighting).
- **Categorization**: Strict feed protection and regex word-boundary sport inference.
- **Timezone**: Mandatory Eastern Time (EDT/EST) standardization using `calendar.timegm()` for UTC-to-Local conversion to prevent machine-drift.
- **Self-Healing**: Automated "Future Date Purge" in scraper to invalidate poisoned persistence articles (`published_at > now`).
- **UI Context**: Sync header includes current date `M/D/YY` next to EST label.

- **Registry**: 55+ institutional sources (ESPN, D1Baseball, Swish Appeal, etc.).

## 🛠️ Operations
- **Build Pipeline**: `python engine/build_dist.py` (Local bundle generation).
- **Production Bridge**: `python engine/remote_sync.py --dist` (Secure SFTP sync).
- **Master Entry**: `./sports.sh` (Full lifecycle: Sync -> Build -> Deploy).

## 📂 Key Files
- `web/index.html`: Core UI/UX and rendering logic.
- `engine/sports_scraper.py`: Primary data ingestion.
- `database/sports_news.js`: Live intelligence payload.

## 🛑 Governance
- **Platform Isolation**: Desktop and Mobile rules are strictly separated in CSS to prevent cross-platform layout drift.
- **Permanent Filters**: `OLYMPICS` is blacklisted at the UI rendering level.
- **RSS Priority**: ALWAYS prioritize RSS XML feeds over HTML scraping. It is clean, reliable, and minimizes endpoint block/ban risk.
