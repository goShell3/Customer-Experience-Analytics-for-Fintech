"""
Tests for the theme_analysis module.
"""

import pandas as pd
from pathlib import Path
from src.features.theme_analysis import preprocess_text, identify_themes

def test_preprocess_text():
    text = "The app is slow and crashes often."
    processed = preprocess_text(text)
    assert 'slow' in processed
    assert 'crash' in processed or 'crashes' in processed

def test_identify_themes():
    text = "I have login issues and the app is very slow."
    themes = identify_themes(text)
    assert 'Login Issues' in themes
    assert 'Transaction Speed' in themes 