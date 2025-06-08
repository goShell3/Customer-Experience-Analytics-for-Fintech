"""
Tests for the clean_reviews module.
"""

import pytest
import pandas as pd
from src.data.clean_reviews import clean_text, process_reviews

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

def test_process_reviews():
    """Test the process_reviews function."""
    # Create sample data
    data = {
        'review_text': ['Great app!', 'Terrible experience', 'Okay app'],
        'rating': ['5', '1', '3']
    }
    df = pd.DataFrame(data)
    
    # Process the data
    processed_df = process_reviews(df)
    
    # Check if all expected columns exist
    assert 'cleaned_text' in processed_df.columns
    assert 'sentiment_score' in processed_df.columns
    
    # Check if text was cleaned
    assert processed_df['cleaned_text'].iloc[0] == "great app"
    
    # Check if ratings were converted to numeric
    assert processed_df['rating'].dtype in ['int64', 'float64']
    
    # Check sentiment scores
    assert processed_df['sentiment_score'].iloc[0] == 1  # 5-star review
    assert processed_df['sentiment_score'].iloc[1] == -1  # 1-star review
    assert processed_df['sentiment_score'].iloc[2] == 0  # 3-star review 