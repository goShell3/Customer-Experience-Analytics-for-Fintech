"""
Tests for the clean_reviews module.
"""

import pytest
import pandas as pd
from src.data.clean_reviews import clean_text, preprocess_reviews

def test_clean_text():
    """Test the clean_text function."""
    # Test basic cleaning
    assert clean_text("Hello, World!") == "hello world"
    
    # Test with numbers
    assert clean_text("App version 2.0") == "app version 20"
    
    # Test with special characters
    assert clean_text("Great app!!!") == "great app"
    
    # Test with non-string input
    assert clean_text(None) == ""
    assert clean_text(123) == ""

def test_preprocess_reviews():
    """Test the preprocess_reviews function."""
    # Create sample data
    data = {
        'review_text': ['Great app!', 'Terrible experience', 'Okay app'],
        'rating': ['5', '1', '3'],
        'app_name': ['CBE', 'BOA', 'Dashen'],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03']
    }
    df = pd.DataFrame(data)
    
    # Process the data
    processed_df = preprocess_reviews(df)
    
    # Check if all expected columns exist
    assert 'review_text' in processed_df.columns
    assert 'source' in processed_df.columns
    
    # Check if text was cleaned
    assert processed_df['review_text'].iloc[0] == "great app"
    
    # Check if ratings were converted to numeric
    assert processed_df['rating'].dtype in ['int64', 'float64']
    
    # Check source column
    assert all(processed_df['source'] == 'Google Play') 