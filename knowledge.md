# Project Knowledge Base

## UI/UX: The "Cyber-Dossier" Design System

### Rationale
The design shift to **Cyber-Dossier** (Dual-Tone Rails) was driven by the need for high-density, color-coded intelligence delivery. This allows for rapid visual categorization across a 3-column desktop layout.

### Key Principles
1. **Geometric Typography**: Migration to 'Outfit' provided a premium "tech-first" footprint.
2. **Dual-Tone Rhythm (Desktop)**: 
   - Even Cards: Emerald Rail + 0.08 Tint.
   - Odd Cards: Indigo Rail + 0.08 Tint.
   - This prevents "grid fatigue" by creating a rhythmic chromatic pulse.
3. **High-Density Mobile**:
   - Zero horizontal scroll: All navigation wraps into a 2-row static grid.
   - Contrast Delineation: Zebra-striping (`0.47` opacity) with top/bottom micro-borders.

### Technical Implementation
- **Media Queries**: Strict isolation at `768px`. Rules for mobile use `!important` to ensure they override the complex desktop rail logic.
- **Favicon**: Embedded SVG data-uri ensures branding loads instantly without external requests.
- **Content Filtering**: `OLYMPICS` is filtered at the JS render stage to keep the feed focused on core institutional sports intelligence.

## Intelligence: Institutional Deep Stealth (V30.6.24)

### Rationale
Standard headless browsing is increasingly detected by 2026-grade suspect scoring. Deep Stealth mimics the irregular velocity and interaction density of a human analyst.

### Ingestion Methodology: RSS Priority
- **Rule**: ALWAYS prefer and use RSS XML feeds whenever possible as the primary source format.
- **Rationale**: RSS provides a clean, standardized, and structured format. It avoids fragile HTML DOM scraping, ensures long-term layout durability, and has an extremely low risk of triggering IP blocks.

### Implementation Patterns
1. **Multi-Phase Scrolling**: Randomized 2-5 scroll events per page with varying depths and wheel jitter.
2. **Absorption Pauses**: 4-8 second thinking delays after page load to simulate content consumption.
3. **Global Fetch Stagger**: 8.5s - 18.5s randomized intervals between site transitions to prevent IP clustering flags.

## Operational Governance: Temporal Hardening
All timestamps (Scraper, Build, and UI) are strictly standardized to **Eastern Time (EDT/EST)**. This ensures visual parity for stakeholders regardless of the local server's timezone (e.g., CST/CDT drift).

### Key Lessons & Fixes
1. **UTC vs. Local Parsing**: `feedparser` outputs `published_parsed` in UTC. Using `time.mktime()` incorrectly interprets these digits as local time, causing a 3-5 hour phantom offset. ALWAYS use `calendar.timegm()` for UTC `struct_time` conversion.
2. **Persistence Poisoning**: If the scraper generates "future" timestamps (due to bugs), these articles will remain at the top of the feed indefinitely due to the date-descending sort. 
   - **Fix**: The scraper now implements a **Self-Healing Layer** that purges any articles with `published_at > now` during the loading phase.
3. **UI Relative Labels**: "JUST NOW" was found to be too ephemeral/risky for cached views. The system now defaults to **"1 MINS AGO"** for all articles less than 60 seconds old (including future-dated ones) to provide a more concrete reference point.
