# Quickstart Guide

## 🚀 Deployment Workflow
The system uses a unified shell script to handle the full lifecycle from scraping to deployment.

```bash
# Run full sync, build, and deploy
./sports.sh
```

## 🛠️ Local Development

### 1. Requirements
- Python 3.10+
- Playwright Browsers
- `.env` with SFTP credentials

### 2. Manual Commands
- **Scrape**: `python engine/sports_scraper.py`
- **Build**: `python engine/build_dist.py`
- **Deploy**: `python engine/remote_sync.py --dist`

## 🖥️ Portal Configuration
- **Desktop**: 1200px+ (Dual-Tone Rails).
- **Mobile**: < 768px (2-Row Navigation).
- **Favicon**: Embedded SVG (No external assets required).
