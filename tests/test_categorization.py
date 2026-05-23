import pytest
from engine.sports_scraper import _infer_sport

def test_hierarchical_categorization_college_football():
    """Verify that college football articles are categorized under COLLEGE : Football"""
    title = "Georgia Bulldogs secure top commit for next season"
    summary = "The college football powerhouse adds another five-star recruit to their roster."
    
    # Run our categorization inference
    # We expect _infer_sport to detect college context and football sport, returning COLLEGE and Football
    # Wait, we will design _infer_sport to return a tuple (primary_category, sub_category)
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "COLLEGE", f"Expected primary category to be COLLEGE, got {p_cat}"
    assert s_cat == "Football", f"Expected sub-category to be Football, got {s_cat}"

def test_hierarchical_categorization_pro_nba():
    """Verify that professional basketball articles are categorized under NBA : General"""
    title = "Lakers target star point guard in blockbuster NBA trade talk"
    summary = "Trae Young rumored to be on the trading block as draft day approaches."
    
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "NBA", f"Expected primary category to be NBA, got {p_cat}"
    assert s_cat == "General", f"Expected sub-category to be General, got {s_cat}"

def test_hierarchical_categorization_college_softball():
    """Verify that college softball articles are categorized under COLLEGE : Softball"""
    title = "Oklahoma Clinches WCWS Spot with Shutout Win"
    summary = "The NCAA softball giants return to Oklahoma City for the championship tournament."
    
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "COLLEGE", f"Expected primary category to be COLLEGE, got {p_cat}"
    assert s_cat == "Softball", f"Expected sub-category to be Softball, got {s_cat}"

def test_hierarchical_categorization_pro_f1():
    """Verify that Formula 1 articles are categorized under RACING : F1"""
    title = "Verstappen dominates Monaco Grand Prix qualifying"
    summary = "The Red Bull driver takes pole position ahead of the street race."
    
    p_cat, s_cat = _infer_sport(title, summary, "General", "GEN")
    assert p_cat == "RACING", f"Expected primary category to be RACING, got {p_cat}"
    assert s_cat == "F1", f"Expected sub-category to be F1, got {s_cat}"
