# Sovereign Sports Intelligence

High-fidelity sports intelligence portal providing institutional-grade news and analysis across major global leagues. Aggregates 60+ premium RSS sources, classifies them with a multi-pass hierarchical engine, ranks by hot score, and deploys to production via secure SFTP.

## 🚨 CRITICAL RULE
**NEVER remove `database/sports_news.js`.** All fixes must be done via script modifications, not file deletion!

---

## 🏛️ UI/UX Design System (V30.6.22)
- **Aesthetic**: Institutional Utility / Cyber-Dossier — premium dark mode with glassmorphism.
- **Typography**: `Outfit` Geometric Sans-Serif (Primary).
- **Desktop**: Split-header branding + stats rail. Dual-Tone Cyber Rails — Emerald (even) / Indigo (odd) — with 0.08 background tints.
- **Mobile**: High-density centered layout. 2-row wrap navigation. Zebra-striped cards (`0.47` opacity).
- **Favicon**: Custom `Lightning-S` SVG embedded via data-uri for instant loading.

---

## ⚙️ Intelligence Engine

### Classification
- Two-pass hierarchical engine: domain trust lock → URL path routing → weighted keyword scoring.
- Seasonal `_SEASON_ACTIVE` / `_SEASON_PEAK` calendars apply 2× peak boosts and 0.4× off-season penalties during sport disambiguation.
- College dominance guard: suppresses pro-team score boosts when college signals strongly dominate.
- High school / prep early-exit: prep articles routed to GEN before any sport classification.
- Generic feed noise drop: `GEN` or `COLLEGE:General` from Yahoo Top / SBNation / FanSided / Deadspin are discarded.
- Regex word-boundary matching with `re.escape()` throughout to prevent substring collisions.

### Ranking
- **Hot Score**: Decay-adjusted scoring model. 4-hour grace period, 24.5-hour half-life.
- **SportsVADER**: Custom NLP lexicon (65 institutional terms) injected at runtime.

### Stealth
- **Deep Stealth V30.6.24**: Playwright + `StealthNavigator` with multi-phase scrolling, human-like absorption pauses, and 8.5–18.5s randomized fetch stagger.
- **Client Hints**: `Sec-CH-UA` dynamically aligned with rotated Chrome version strings.

### Temporal Hardening
- All timestamps standardized to Eastern Time (EDT/EST) via `calendar.timegm()`.
- Self-Healing persistence layer: future-dated articles (`published_at > now`) auto-purged on load.

---

## 📡 News Sources (60+)

### 🏀 NBA
| Source | Type |
|--------|------|
| ESPN - NBA | RSS |
| Yahoo - NBA | RSS |
| CBS - NBA | RSS |
| RealGM Wiretap | RSS |

### 🏈 NFL
| Source | Type |
|--------|------|
| ESPN - NFL | RSS |
| Yahoo - NFL | RSS |
| CBS - NFL | RSS |
| NBC ProFootballTalk | RSS |

### ⚾ MLB
| Source | Type |
|--------|------|
| ESPN - MLB | RSS |
| Yahoo - MLB | RSS |
| CBS - MLB | RSS |

### 🏒 NHL
| Source | Type |
|--------|------|
| ESPN - NHL | RSS |
| Yahoo - NHL | RSS |
| CBS - NHL | RSS |
| The Hockey News | RSS |
| Sportsnet NHL | RSS |
| Daily Faceoff | RSS |

### ⚽ Soccer
| Source | Type |
|--------|------|
| ESPN - Soccer | RSS |
| BBC Sport - Football | RSS |
| CaughtOffside | RSS |
| Marca International | RSS |

### ⛳ Golf
| Source | Type |
|--------|------|
| ESPN - Golf | RSS |
| Yahoo - Golf | RSS |
| CBS - Golf | RSS |
| Bunkered | RSS |
| Geoff Shackelford | RSS |

### 🎾 Tennis
| Source | Type |
|--------|------|
| ESPN - Tennis | RSS |
| Tennis-X | RSS |
| Tennis Head | RSS |
| UbiTennis | RSS |
| Essentially Sports - Tennis | RSS |

### 🏎️ Racing (F1 / NASCAR / MotoGP)
| Source | Type |
|--------|------|
| Yahoo - F1 | RSS |
| BBC - F1 | RSS |
| Yahoo - NASCAR | RSS |
| Jayski | RSS |
| Motorsport.com - NASCAR | RSS |
| Autosport - NASCAR | RSS |
| Motorsports Tribune | RSS |
| Crash.net NASCAR | RSS |
| Motorsport.com - MotoGP | RSS |
| Autosport - MotoGP | RSS |
| Crash.net MotoGP | RSS |
| Roadracing World | RSS |

### 🥊 Fighting (MMA / Boxing)
| Source | Type |
|--------|------|
| ESPN - MMA | RSS |
| Yahoo - MMA | RSS |
| Yahoo - Boxing | RSS |
| Bad Left Hook | RSS |

### 🎭 WWE / Wrestling
| Source | Type |
|--------|------|
| ESPN - WWE | RSS |
| WrestleView | RSS |
| Fightful | RSS |
| Cageside Seats | RSS |
| PWTorch | RSS |

### 🎓 College Sports
| Source | Sport | Type |
|--------|-------|------|
| Yahoo - NCAAF | Football | RSS |
| Yahoo - NCAAB | Basketball | RSS |
| CBS - NCAAF | Football | RSS |
| CBS - NCAAB | Basketball | RSS |
| D1Baseball | Baseball | RSS |
| D1Softball | Softball | RSS |
| Extra Inning Softball | Softball | RSS |
| Swish Appeal | W-Basketball | RSS |

### 📰 General / Institutional
| Source | Type |
|--------|------|
| Yahoo Top Sports | RSS |
| SBNation | RSS |
| FanSided | RSS |
| Deadspin | RSS |

> **Note**: General sources (Yahoo Top, SBNation, FanSided, Deadspin) are filtered — articles that cannot be classified into a specific sport are dropped automatically.

---

## 🛠️ Tech Stack
- **Frontend**: HTML5 / Vanilla CSS / JavaScript.
- **Backend**: Python 3.10+ (Async scraping, classification, ranking).
- **Browser Automation**: Playwright via `StealthNavigator`.
- **NLP**: Custom `SportsVADER` + NLTK.
- **Deployment**: Secure SFTP Sync (`paramiko`).

---

## 📂 Project Structure
```
Sports_News/
├── web/                  # Frontend portal (index.html, og_image.png)
├── engine/               # Core intelligence engine
│   ├── sports_scraper.py   # Async RSS ingestion + classification
│   ├── sports_vader.py     # Custom NLP impact scoring
│   ├── stealth_navigator.py # Playwright stealth browser
│   ├── build_dist.py       # Production bundle builder
│   ├── remote_sync.py      # Secure SFTP deployer
│   └── auto_sync.py        # Automated scheduling daemon
├── database/             # Persisted JS data payloads (DO NOT DELETE)
├── tests/                # Regression + integration test suite
├── dist/                 # Built production bundle (git-ignored)
├── GEMINI.md             # UI/UX Governance (locked)
├── CLAUDE.md             # Architecture & Operations
├── TASKS.md              # Project roadmap & history
└── knowledge.md          # Institutional knowledge base
```

---

## 🚀 Operations
| Command | Description |
|---------|-------------|
| `python engine/sports_scraper.py` | Run full RSS sync |
| `python engine/sports_scraper.py --force` | Force sync (bypass 30m cooldown) |
| `python engine/build_dist.py` | Build production bundle |
| `python engine/remote_sync.py --dist` | Deploy to production via SFTP |
| `python engine/auto_sync.py` | Start automated 3-hour sync daemon |
| `python -m pytest tests/` | Run core test suite |

---

## 📊 Current Status (V30.6.30)
- **UI/UX**: Production Ready — Cyber-Dossier V30.6.24.
- **Engine**: Stable — 60+ high-fidelity sources.
- **Classification**: 44/44 tests passing.
- **Stealth**: Hardened — Deep Stealth V30.6.24 active.
- **Production**: Live at `bmwseals.com/sports`.
