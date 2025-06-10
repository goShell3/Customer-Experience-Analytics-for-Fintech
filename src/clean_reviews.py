"""
Script for cleaning and preprocessing bank app reviews.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
import logging
from datetime import datetime
import json

def load_raw_data(json_path='raw_reviews.json'):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def remove_duplicates(df):
    return df.drop_duplicates(subset=['review', 'app'])

def preprocess_reviews(df):
    def clean_text(text):
        text = re.sub(r'[^\\w\\s]', '', text)  # Remove punctuation
        text = re.sub(r'\\s+', ' ', text)      # Remove extra whitespace
        return text.strip().lower()

    df['cleaned_review'] = df['review'].astype(str).apply(clean_text)
    return df