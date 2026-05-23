import pytest

def test_index_html_contains_glassmorphism_styles():
    """Verify that index.html contains glassmorphism styling and shadow transitions"""
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Assert that index.html has backdrop-filter on .news-card
    # Currently it shouldn't have this, so it will fail (RED)
    assert 'backdrop-filter: blur(12px)' in html, "backdrop-filter is missing for glassmorphism styling"
    assert 'rgba(16, 185, 129, 0.15)' in html, "Emerald hover glow shadow is missing"
    assert 'rgba(99, 102, 241, 0.15)' in html, "Indigo hover glow shadow is missing"
