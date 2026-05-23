# Sovereign Sports Intelligence

High-fidelity sports intelligence portal providing institutional-grade news and analysis across major global leagues.

## 🚨 CRITICAL RULE
**NEVER DO THE FOLLOWING:** Never Remove `database/sports_news.js`. All fixes must be done via script modifications, not file deletion!

## 🏛️ UI/UX (V30.6.22)
- **Cyber-Dossier Aesthetic**: Premium dark mode with 'Outfit' geometric typography.
- **Dual-Tone Rhythm**: Alternating Emerald/Indigo rails for desktop article isolation.
- **High-Density Mobile**: 2-row wrap navigation and zebra-striped cards for rapid vertical ingestion.

## ⚙️ Intelligence Engine
- **Scraper**: Async/Playwright with `StealthNavigator` (Deep Stealth V30.6.24).
- **Ranking**: Decay-Adjusted "Hot Score" ranking model.
- **Sources**: 55+ high-fidelity sources (incl. College Baseball/Softball & MotoGP).

## 🛠️ Tech Stack
- **Frontend**: HTML5 / Vanilla CSS / JavaScript.
- **Backend**: Python 3.10+ (Scraping & Ranking).
- **Deployment**: Secure SFTP Sync via `./sports.sh`.

## 📂 Project Structure
- `web/`: Frontend portal files.
- `engine/`: Python scrapers and ranking logic.
- `database/`: Locally persisted JS data payloads.
- `GEMINI.md`: UI/UX Governance.
- `TASKS.md`: Project Roadmap.
