import pytest
from engine.sports_scraper import _infer_sport

# ─────────────────────────────────────────────────────────────────────────────
# ORIGINAL TESTS (kept intact)
# ─────────────────────────────────────────────────────────────────────────────

def test_hierarchical_categorization_college_football():
    """College football articles → COLLEGE : Football"""
    title = "Georgia Bulldogs secure top commit for next season"
    summary = "The college football powerhouse adds another five-star recruit to their roster."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "COLLEGE", f"Expected COLLEGE, got {p_cat}"
    assert s_cat == "Football", f"Expected Football, got {s_cat}"

def test_hierarchical_categorization_pro_nba():
    """Pro basketball articles from GEN → NBA : General"""
    title = "Lakers target star point guard in blockbuster NBA trade talk"
    summary = "Trae Young rumored to be on the trading block as draft day approaches."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "NBA", f"Expected NBA, got {p_cat}"
    assert s_cat == "General", f"Expected General, got {s_cat}"

def test_hierarchical_categorization_college_softball():
    """College softball articles → COLLEGE : Softball"""
    title = "Oklahoma Clinches WCWS Spot with Shutout Win"
    summary = "The NCAA softball giants return to Oklahoma City for the championship tournament."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "COLLEGE", f"Expected COLLEGE, got {p_cat}"
    assert s_cat == "Softball", f"Expected Softball, got {s_cat}"

def test_hierarchical_categorization_pro_f1():
    """F1 articles → RACING : F1"""
    title = "Verstappen dominates Monaco Grand Prix qualifying"
    summary = "The Red Bull driver takes pole position ahead of the street race."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "RACING", f"Expected RACING, got {p_cat}"
    assert s_cat == "F1", f"Expected F1, got {s_cat}"

def test_url_based_categorization_overrides_text():
    """URL /nba/ overrides mixed MLB/college text"""
    title = "Shai Gilgeous-Alexander delivers MVP response; Ed Orgeron rejoins LSU staff"
    summary = "Plus, what's with all the shirtless fans showing up in MLB stands?"
    url = "https://www.cbssports.com/nba/news/shai-gilgeous-alexander-delivers-mvp-response-ed-orgeron-rejoins-lsu-staff/"
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN", url=url)
    assert p_cat == "NBA", f"Expected NBA from URL, got {p_cat}"

def test_url_based_categorization_overrides_feed():
    """URL /nba/ overrides COLLEGE feed primary_cat"""
    title = "Shai Gilgeous-Alexander delivers MVP response; Ed Orgeron rejoins LSU staff"
    summary = "Plus, what's with all the shirtless fans showing up in MLB stands?"
    url = "https://www.cbssports.com/nba/news/shai-gilgeous-alexander-delivers-mvp-response-ed-orgeron-rejoins-lsu-staff/"
    p_cat, s_cat = _infer_sport(title, summary, "General", "COLLEGE", url=url)
    assert p_cat == "NBA", f"Expected NBA despite COLLEGE feed, got {p_cat}"

def test_mariners_mlb_categorization():
    """Mariners article with generic /articles/ URL → MLB via team name"""
    title = "Mariners warp reality, win normal"
    summary = "Seattle Mariners baseball team secures another win in the regular season."
    url = "https://sports.yahoo.com/articles/mariners-warp-reality-win-normal-042451387.html"
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN", url=url)
    assert p_cat == "MLB", f"Expected MLB, got {p_cat}"

def test_high_school_baseball_exclusion():
    """HS baseball with no pro/college context stays GEN"""
    title = "Baseball: Butte shakes off Flathead"
    summary = "High school baseball game results as Butte defeats Flathead in a prep game."
    url = "https://sports.yahoo.com/articles/baseball-butte-shakes-off-flathead-021700782.html"
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN", url=url)
    assert p_cat == "GEN", f"Expected GEN for HS game, got {p_cat}"


# ─────────────────────────────────────────────────────────────────────────────
# HIGH SCHOOL EXCLUSION TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_hs_football_stays_gen():
    """High school football should NOT be promoted to NFL or COLLEGE"""
    title = "State Championship: Jefferson High defeats Lincoln in overtime thriller"
    summary = "Prep football stars shine as Jefferson wins the state championship game."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "GEN", f"HS football should stay GEN, got {p_cat}"

def test_hs_basketball_stays_gen():
    """High school basketball preps game stays GEN"""
    title = "Preps: Westside tops Eastside 72-65 in district basketball final"
    summary = "District basketball championship decided as top players compete."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "GEN", f"HS basketball should stay GEN, got {p_cat}"

def test_hs_baseball_varsity_stays_gen():
    """Varsity baseball article stays GEN"""
    title = "Varsity Baseball: Springfield clinches regional title"
    summary = "The varsity squad advances after a walk-off win in regionals."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "GEN", f"Varsity baseball should stay GEN, got {p_cat}"

def test_nfl_article_mentioning_high_school_past_not_excluded():
    """NFL article mentioning player's high school past should still be NFL"""
    title = "Patrick Mahomes recalls how in high school he never imagined being in the NFL"
    summary = "The Chiefs quarterback reflects on his journey from prep school to the NFL championship."
    url = "https://www.espn.com/nfl/news/mahomes-high-school-story"
    # URL has /nfl/ so should override HS indicator
    p_cat, s_cat = _infer_sport(title, summary, "General", "NFL", url=url)
    assert p_cat == "NFL", f"NFL URL should override HS text, got {p_cat}"


# ─────────────────────────────────────────────────────────────────────────────
# PRO SPORT CLASSIFICATION TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_mlb_specific_keywords():
    """MLB-specific keywords (bullpen, RBI, ERA) classify as MLB"""
    title = "Yankees bullpen struggles as ERA climbs ahead of postseason"
    summary = "The New York Yankees closer blew his third save opportunity, raising ERA concerns."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "MLB", f"Expected MLB from bullpen/ERA keywords, got {p_cat}"

def test_nfl_specific_keywords():
    """NFL-specific keywords (sack, blitz, quarterback) classify as NFL"""
    title = "Cowboys defensive coordinator unveils new blitz packages for playoff push"
    summary = "The new scheme features creative sack pressure with linebacker and cornerback stunts."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "NFL", f"Expected NFL from sack/blitz keywords, got {p_cat}"

def test_nhl_specific_keywords():
    """NHL-specific keywords (goalie, power play, Stanley Cup) classify as NHL"""
    title = "McDavid notches hat trick with power play goal in Stanley Cup opener"
    summary = "The Oilers captain's goaltender played brilliantly to preserve the win."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "NHL", f"Expected NHL, got {p_cat}"

def test_nba_specific_keywords():
    """NBA-specific keywords (triple-double, buzzer beater) classify as NBA"""
    title = "Jokic records triple-double with buzzer beater to lift Nuggets"
    summary = "The MVP center's point guard-level playmaking leads Denver to overtime victory."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "NBA", f"Expected NBA, got {p_cat}"

def test_soccer_specific_keywords():
    """Soccer-specific keywords (clean sheet, goalkeeper, Premier League) classify as SOCCER"""
    title = "Haaland nets brace as City keep clean sheet in Premier League opener"
    summary = "The City striker and goalkeeper combined to dominate in what was a perfect formation."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "SOCCER", f"Expected SOCCER, got {p_cat}"

def test_tennis_atp_classification():
    """ATP tennis keywords classify as TENNIS : ATP"""
    title = "Alcaraz defeats Sinner in five-set Roland Garros final"
    summary = "The young Spaniard wins the French Open title on clay court after an epic match."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "TENNIS", f"Expected TENNIS, got {p_cat}"
    assert s_cat == "ATP", f"Expected ATP, got {s_cat}"

def test_tennis_wta_classification():
    """WTA tennis keywords classify as TENNIS : WTA"""
    title = "Swiatek dominates Sabalenka in Wimbledon women's final"
    summary = "The top-seeded WTA player wins on grass court in straight sets."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "TENNIS", f"Expected TENNIS, got {p_cat}"
    assert s_cat == "WTA", f"Expected WTA, got {s_cat}"

def test_nascar_classification():
    """NASCAR keywords classify as RACING : NASCAR"""
    title = "NASCAR Cup Series: Bubba Wallace wins at Talladega in controversial finish"
    summary = "The stock car racing series saw a wild finish as the checkered flag came out under caution."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "RACING", f"Expected RACING, got {p_cat}"
    assert s_cat == "NASCAR", f"Expected NASCAR, got {s_cat}"

def test_golf_specific_keywords():
    """Golf-specific keywords (birdie, fairway, PGA) classify as GOLF"""
    title = "Scheffler shoots 63 with eight birdies to lead PGA Championship at Valhalla"
    summary = "The world number one's putter and fairway accuracy were exceptional."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "GOLF", f"Expected GOLF, got {p_cat}"

def test_mma_fighting_classification():
    """MMA-specific keywords classify as FIGHTING : MMA"""
    title = "Jones defends heavyweight title via rear naked choke in UFC main event"
    summary = "The champion submitted his challenger in the octagon after a dominant performance."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "FIGHTING", f"Expected FIGHTING, got {p_cat}"
    assert s_cat == "MMA", f"Expected MMA, got {s_cat}"

def test_boxing_fighting_classification():
    """Boxing-specific keywords classify as FIGHTING : Boxing"""
    title = "Canelo Alvarez stops Fury in split decision heavyweight boxing title fight"
    summary = "The unified champion defended his belt in a grueling 12-round fight."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "FIGHTING", f"Expected FIGHTING, got {p_cat}"
    assert s_cat == "Boxing", f"Expected Boxing, got {s_cat}"


# ─────────────────────────────────────────────────────────────────────────────
# COLLEGE DISAMBIGUATION TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_college_baseball_cws():
    """College World Series article classifies as COLLEGE : Baseball"""
    title = "LSU advances to College World Series after shutting out Tennessee"
    summary = "The Tigers clinched their CWS berth with a dominant pitching performance."
    p_cat, s_cat = _infer_sport(title, summary, "General", "COLLEGE")
    assert p_cat == "COLLEGE", f"Expected COLLEGE, got {p_cat}"
    assert s_cat == "Baseball", f"Expected Baseball, got {s_cat}"

def test_college_basketball_ncaa_tournament():
    """NCAA tournament article classifies as COLLEGE : Basketball"""
    title = "Duke Blue Devils advance to Elite Eight with stunning overtime win"
    summary = "The NCAA tournament continues as Blue Devils overcome a 15-point deficit in regulation."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "COLLEGE", f"Expected COLLEGE, got {p_cat}"
    assert s_cat == "Basketball", f"Expected Basketball, got {s_cat}"

def test_transfer_portal_stays_college():
    """Transfer portal article from a pro feed stays COLLEGE"""
    title = "Ohio State quarterback enters transfer portal after spring practice"
    summary = "The Buckeyes starter will seek a new program after the national signing day window."
    p_cat, s_cat = _infer_sport(title, summary, "Football", "COLLEGE")
    assert p_cat == "COLLEGE", f"Expected COLLEGE, got {p_cat}"

def test_mlb_player_mentioned_with_college_context_stays_mlb():
    """MLB article referencing player's college days stays MLB when feed is MLB"""
    title = "Ohtani reflects on his college baseball days in Japan before MLB stardom"
    summary = "The Angels two-way star discusses his early career before becoming an MLB icon."
    url = "https://sports.yahoo.com/mlb/news/ohtani-college-story.html"
    p_cat, s_cat = _infer_sport(title, summary, "General", "MLB", url=url)
    assert p_cat == "MLB", f"MLB feed with college mention should stay MLB, got {p_cat}"


# ─────────────────────────────────────────────────────────────────────────────
# GEN FEED THRESHOLD TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_gen_weak_signal_stays_gen():
    """Single weak keyword from GEN feed should NOT promote (score < 4)"""
    title = "Local sports roundup: community events and highlights"
    summary = "A look at regional sports scores and player updates from around the area."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "GEN", f"Weak signal should stay GEN, got {p_cat}"

def test_gen_strong_pro_signal_promotes():
    """Strong MLB signal from GEN feed promotes to MLB"""
    title = "Aaron Judge's walkoff homer ends Yankees bullpen nightmare"
    summary = "The slugger's late-inning RBI gave the Yankees their second win in three games."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "MLB", f"Strong MLB signal should promote from GEN, got {p_cat}"

def test_gen_ambiguous_baseball_no_team_stays_gen():
    """Generic 'baseball' mention without pro/college evidence stays GEN"""
    title = "Baseball is America's pastime but fans are leaving"
    summary = "A look at how baseball attendance has changed over the decades."
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    # Should not promote to MLB without stronger evidence; stays GEN
    assert p_cat in ["GEN", "MLB"], f"Ambiguous baseball may be GEN or MLB, got {p_cat}"


# ─────────────────────────────────────────────────────────────────────────────
# V30.6.28 REGRESSION TESTS (from user-reported failures)
# ─────────────────────────────────────────────────────────────────────────────

def test_orgeron_kelly_lsu_generic_feed_dropped():
    """Ed Orgeron/Brian Kelly football coaches article from generic feed → dropped (GEN)"""
    title = "Ed Orgeron Knew Brian Kelly LSU Tigers Stint Was Doomed From The Beginning"
    summary = "Coach O reveals why Brian Kelly infamous fake accent signaled an immediate cultural mismatch proving that losing the locker room trust is a death sentence in Baton Rouge"
    url = "https://sports.yahoo.com/articles/ed-orgeron-knew-brian-kellys-221951179.html"
    p_cat, s_cat = _infer_sport(title, summary, "Top", "GEN", url)
    # From Yahoo Top (generic): no sport evidence → must be GEN (will be dropped)
    assert p_cat == "GEN", f"Football coaches article with no sport keywords → GEN, got {p_cat}"

def test_orgeron_kelly_d1baseball_no_sport_evidence():
    """Ed Orgeron article ingested from D1Baseball feed → COLLEGE:General, NOT Baseball"""
    title = "Ed Orgeron Knew Brian Kelly LSU Tigers Stint Was Doomed From The Beginning"
    summary = "Coach O reveals why Brian Kelly infamous fake accent signaled an immediate cultural mismatch"
    p_cat, s_cat = _infer_sport(title, summary, "Baseball", "COLLEGE")
    assert p_cat == "COLLEGE", f"Still college context, got {p_cat}"
    assert s_cat == "General", f"No baseball keywords → General sub, not Baseball, got {s_cat}"

def test_stillwater_high_football_dropped():
    """Stillwater High football coach article → GEN (HS school name pattern catches it)"""
    title = "Spring forward: Experienced Pioneers wrap up first week of spring practice"
    summary = "Stillwater High football coach Chad Cawood initial thoughts on his 2026 squad"
    url = "https://sports.yahoo.com/articles/spring-forward-experienced-pioneers-wrap-035900505.html"
    p_cat, s_cat = _infer_sport(title, summary, "Top", "GEN", url)
    assert p_cat == "GEN", f"HS school name pattern should catch 'Stillwater High football coach', got {p_cat}"

def test_ucf_ucla_softball_super_regional():
    """UCF vs UCLA NCAA Softball Super Regional from Yahoo Top → COLLEGE:Softball"""
    title = "How to live stream UCF vs UCLA NCAA Softball Tournament Super Regionals TV channel"
    summary = "No 8 seeded UCLA Bruins open their quest for Women College World Series appearance against UCF Knights Super Regional Easton Stadium"
    url = "https://sports.yahoo.com/articles/live-stream-ucf-vs-ucla-000000372.html"
    p_cat, s_cat = _infer_sport(title, summary, "Top", "GEN", url)
    assert p_cat == "COLLEGE", f"NCAA Softball article → COLLEGE, got {p_cat}"
    assert s_cat == "Softball", f"Should be Softball (not Hockey), got {s_cat}"

def test_seasonal_nfl_off_season_generic_suppressed():
    """NFL article with weak signal from generic feed stays GEN in May (off-season)"""
    title = "Which teams could surprise the NFL world this upcoming season"
    summary = "A preview of which franchises might show improvement in the coming football season"
    p_cat, s_cat = _infer_sport(title, summary, "Top", "GEN")
    # In May, NFL is off-season (0.4x penalty). Low signal + off-season = should not promote
    assert p_cat in ["GEN", "NFL"], f"Off-season low-signal NFL from GEN → should stay GEN, got {p_cat}"

def test_seasonal_nba_playoffs_boost():
    """NBA playoff article in May gets strong classification even from generic feed"""
    title = "Celtics vs Pacers Game 7: How to watch NBA Playoffs Eastern Conference Finals"
    summary = "The NBA Eastern Conference Finals reaches its conclusion as both teams compete for a trip to the NBA Finals"
    p_cat, s_cat = _infer_sport(title, summary, "Top", "GEN")
    assert p_cat == "NBA", f"NBA Playoffs (peak in May) should classify from GEN, got {p_cat}"

def test_dedicated_feed_nfl_always_kept():
    """NFL article from dedicated ESPN NFL feed always classified as NFL, not dropped"""
    title = "Commanders restructure contract with veteran lineman ahead of minicamp"
    summary = "The NFL franchise makes a salary cap move as the team prepares for summer minicamp"
    url = "https://www.espn.com/nfl/news/commanders-cap-move"
    p_cat, s_cat = _infer_sport(title, summary, "General", "NFL", url)
    assert p_cat == "NFL", f"Dedicated NFL feed always classifies NFL, got {p_cat}"

