"""
Main module for bank reviews collection and analysis.
"""

# from .scrape_reviews import scrape_app_reviews
from .scrape_reviews import ScrapData
from .clean_reviews import (
    load_raw_data,
    remove_duplicates,
    preprocess_reviews,
    handle_missing_data,
    normalize_dates,
    clean_text
)


__all__ = [
    'scrape_app_reviews',
    'load_raw_data',
    'remove_duplicates',
    'preprocess_reviews',
    'handle_missing_data',
    'normalize_dates',
    'clean_text',
    'ScrapData',
]
