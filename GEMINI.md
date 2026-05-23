# Sovereign Sports Intelligence - UI/UX Documentation (Locked)

## 🚨 CRITICAL RULE
**NEVER DO THE FOLLOWING:** Never Remove `database/sports_news.js`. All fixes must be done via script modifications, not file deletion!

## Aesthetics & Colors
- **Background Main**: `#030712` (var--bg-main)
- **Background Card**: `#0b1120` (var--bg-card)
- **Accent (Even)**: `#10b981` (Emerald)
- **Accent (Odd)**: `#6366f1` (Electric Indigo)
- **Gold**: `#f59e0b` (var--gold)
- **Text Main**: `#ffffff` (var--text-main)
- **Text Dim**: `#9ca3af` (var--text-dim)
- **Border**: `#1f2937` (var--border)

## Typography (Institutional)
- **Primary**: 'Outfit', sans-serif (Geometric/Bold/Modern)
- **Scale**: 16px Titles (800 weight) | 12px Summaries | 10px Meta labels.

---

## 🖥️ Desktop Governance
1. **Header Layout**: Split branding (Left) and Stats Bar (Right).
2. **Branding**: `SOVEREIGN SPORTS` on one line, timezone label below with 12px left offset.
3. **Dual-Tone Rails**: High-fidelity alternating rail system:
   - **Even Cards**: 3px Emerald Rail (`#10b981`) + `rgba(16, 185, 129, 0.08)` background tint.
   - **Odd Cards**: 3px Indigo Rail (`#6366f1`) + `rgba(99, 102, 241, 0.08)` background tint.
4. **Navigation Rail**: Single-row horizontal scroller with neon-green underline active state.
5. **Grid Spacing**: `25px` gap between cards; `12px 18px` internal card padding.

---

## 📱 Mobile Governance (High-Density)
1. **Header Layout**: 100% Vertical Centered Stack. Zero horizontal skew.
2. **Branding**: Shrunk to 14px; timezone label centered immediately below with zero margin.
3. **Navigation Filter**: Forced **2-row wrap layout**. No scrolling.
4. **Grid Density**: `12px` gap between cards; `6px 12px` internal card padding.
5. **Zebra Striping**: Even-numbered cards use `rgba(30, 41, 59, 0.47)` background with `0.1` opacity top/bottom borders. Odd cards remain transparent.
6. **Content Governance**: Strict 2-line clamp for both titles and summaries to ensure card height uniformity.

---

## Temporal Governance (Institutional)
- **RSS Parsing**: ALWAYS use `calendar.timegm()` instead of `time.mktime()` for feed timestamps. Feedparser outputs UTC `struct_time`, and `mktime` incorrectly applies machine-local offsets.
- **Persistence Self-Healing**: The scraper MUST implement an automated purge of future-dated articles (`published_at > now`) during the database load phase to prevent "poisoning" the feed with incorrect legacy data.
- **Header Labeling**: The sync header MUST include the current date in `M/D/YY` format next to the EST timezone label to maintain high-fidelity situational awareness.

## Global Rules
- **Content Filter**: `OLYMPICS` is permanently filtered out of navigation and rendering.
- **Favicon**: Custom 'Lightning-S' SVG embedded via data-uri for instant loading.
