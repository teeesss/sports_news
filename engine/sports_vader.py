print("[*] VADER imports...")
import nltk
print("[*] NLTK imported.")
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load environment variables
load_dotenv()

# Ensure lexicon is downloaded natively
try:
    print("[*] Checking NLTK lexicon...")
    nltk.data.find('sentiment/vader_lexicon.zip')
    print("[*] Lexicon found.")
except LookupError:
    print("[*] Downloading NLTK lexicon...")
    nltk.download('vader_lexicon', quiet=True)
    print("[*] Lexicon downloaded.")

# Sovereign SportsVADER: Institutional-Grade Sports Lexicon (V1.0)
SPORTS_LEXICON = {
    # High-Alpha Transactions
    'trade': 3.5, 'traded': 3.0, 'blockbuster': 4.0, 'signing': 2.5, 'signed': 2.0,
    'extension': 2.5, 'max': 2.0, 'waiver': 1.5, 'acquired': 2.0, 'deal': 1.5,
    'free agent': 2.0, 're-signs': 2.5, 'opt-out': 2.0, 'holdout': -2.5,
    
    # Critical Injuries
    'injury': -2.5, 'injured': -2.5, 'torn': -3.5, 'acl': -4.0, 'mcl': -3.5, 
    'achilles': -4.0, 'fracture': -3.0, 'broken': -3.0, 'surgery': -3.0,
    'out for season': -4.5, 'indefinitely': -3.0, 'concussion': -2.5,
    'questionable': -1.0, 'doubtful': -2.0, 'probable': 0.5,
    
    # Coaching & Leadership
    'fired': -3.5, 'hired': 2.5, 'resigned': -2.0, 'dismissed': -3.0,
    'head coach': 1.0, 'manager': 1.0, 'gm': 1.0, 'front office': 1.0,
    'locker room': -1.5, 'drama': -2.0, 'scandal': -4.0,
    
    # Performance & Achievements
    'championship': 4.5, 'title': 4.0, 'trophy': 4.0, 'mvp': 3.5, 'all-star': 2.5,
    'historic': 3.0, 'record': 3.0, 'breakthrough': 2.5, 'shutout': 2.0,
    'blowout': 2.0, 'dominant': 2.5, 'underdog': 1.5, 'upset': 3.0,
    'clinch': 2.5, 'playoffs': 2.0, 'postseason': 2.0,
    
    # Discipline & Off-Field
    'suspended': -3.5, 'suspension': -3.5, 'arrested': -4.5, 'investigation': -3.0,
    'fined': -1.5, 'ban': -3.5, 'violation': -2.5, 'drug': -3.0, 'ped': -3.5
}

# Domain-Aware Weighting
SOURCE_ALPHA = {
    'ESPN': 1.2,
    'YAHOO': 1.1,
    'GOAL.COM': 1.1,
    'SKY SPORTS': 1.2,
    'REALGM': 1.1,
    'BLEACHER REPORT': 1.0, # Upgraded from 0.9 due to high-density feed
    'CBS SPORTS': 1.1,
    'FOX SPORTS': 1.1,
    'SBNATION': 1.1,
    'DEADSPIN': 1.0,
    'MARCA': 1.1,
    'FANSIDED': 1.0
}

def analyze_article_impact(title: str, summary: str, source: str) -> int:
    """
    Sovereign SportsVADER Engine: Translates sports narrative into a 10-100 impact score.
    Now with configurable knobs from .env.
    """
    sia = SentimentIntensityAnalyzer()
    
    # Configurable Knobs
    base_score_knob = float(os.getenv("SPORTSVADER_BASE_SCORE", 40))
    magnitude_knob = float(os.getenv("SPORTSVADER_MAGNITUDE_WEIGHT", 45))
    breaking_bonus_knob = float(os.getenv("SPORTSVADER_BONUS_BREAKING", 15))
    official_bonus_knob = float(os.getenv("SPORTSVADER_BONUS_OFFICIAL", 10))

    # Initialize Sports Lexicon
    if not getattr(analyze_article_impact, "_SPORTS_INJECTED", False):
        sia.lexicon.update(SPORTS_LEXICON)
        print(f"[INFO] [NLP] Sovereign SportsVADER Lexicons Injected ({len(SPORTS_LEXICON)} terms)")
        analyze_article_impact._SPORTS_INJECTED = True
    else:
        sia.lexicon.update(SPORTS_LEXICON)

    text = f"{title}. {summary}"
    scores = sia.polarity_scores(text)
    magnitude = abs(scores['compound'])
    
    # 1. Base Score calculation
    base_score = base_score_knob + (magnitude * magnitude_knob)
    
    # 2. Institutional Alpha Bonus
    alpha_bonus = 0
    alpha_patterns = {
        r"BREAKING": breaking_bonus_knob,
        r"OFFICIAL": official_bonus_knob,
        r"SOURCES": 5,
        r"FINAL": 10,
        r"URGENT": 12
    }
    for pattern, bonus in alpha_patterns.items():
        if re.search(pattern, text.upper()):
            alpha_bonus += bonus
            
    # 3. Apply Source Multiplier
    source_mult = 1.0
    for s_name, mult in SOURCE_ALPHA.items():
        if s_name.upper() in source.upper():
            source_mult = mult
            break
            
    final_score = (base_score + alpha_bonus) * source_mult
    
    return int(min(max(final_score, 10), 100))
