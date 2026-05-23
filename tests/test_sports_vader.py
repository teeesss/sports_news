import pytest
from engine.sports_vader import analyze_article_impact

def test_high_impact_trade_narrative():
    title = "Blockbuster Trade: Star QB traded for three first-round picks"
    summary = "The franchise has completely reset their future after completing a massive trade."
    score = analyze_article_impact(title, summary, "ESPN")
    assert score >= 85

def test_low_impact_narrative():
    title = "Local team has a standard practice on Wednesday"
    summary = "Nothing much happened today, players stretched and ran drills."
    score = analyze_article_impact(title, summary, "Yahoo")
    assert score <= 50
