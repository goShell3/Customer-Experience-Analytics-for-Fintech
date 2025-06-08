"""
Script for cleaning and preprocessing banking app reviews.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_raw_data(file_path: Path) -> pd.DataFrame:
    """
    Load raw reviews data from CSV.
    
    Args:
        file_path: Path to raw reviews CSV file
    
    Returns:
        DataFrame containing raw reviews
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded {len(df)} reviews from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        raise

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate reviews based on review text and app name.
    
    Args:
        df: DataFrame containing reviews
    
    Returns:
        DataFrame with duplicates removed
    """
    initial_count = len(df)
    df = df.drop_duplicates(subset=['review_text', 'app_name'])
    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} duplicate reviews")
    return df

def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing data in reviews.
    
    Args:
        df: DataFrame containing reviews
    
    Returns:
        DataFrame with missing data handled
    """
    initial_count = len(df)
    
    # Drop rows with missing review text or rating
    df = df.dropna(subset=['review_text', 'rating'])
    
    # Log missing data statistics
    missing_stats = df.isnull().sum()
    logger.info("Missing data statistics:")
    for column, count in missing_stats.items():
        if count > 0:
            logger.info(f"  {column}: {count} missing values")
    
    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} rows with missing data")
    
    return df

def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize dates to YYYY-MM-DD format.
    
    Args:
        df: DataFrame containing reviews
    
    Returns:
        DataFrame with normalized dates
    """
    try:
        # Convert to datetime if not already
        df['date'] = pd.to_datetime(df['date'])
        
        # Format as YYYY-MM-DD
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        logger.info("Successfully normalized dates to YYYY-MM-DD format")
        return df
    except Exception as e:
        logger.error(f"Error normalizing dates: {str(e)}")
        raise

def clean_text(text: str) -> str:
    """
    Clean and normalize text data.
    
    Args:
        text: Input text to clean
    
    Returns:
        Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the reviews dataset.
    
    Args:
        df: Raw reviews DataFrame
    
    Returns:
        Processed DataFrame
    """
    # Create a copy to avoid modifying the original
    processed_df = df.copy()
    
    # Clean review text
    processed_df['review_text'] = processed_df['review_text'].apply(clean_text)
    
    # Convert ratings to numeric
    processed_df['rating'] = pd.to_numeric(processed_df['rating'], errors='coerce')
    
    # Add source column
    processed_df['source'] = 'Google Play'
    
    return processed_df

def main():
    """Main function to clean and preprocess reviews."""
    try:
        # Set up paths
        data_dir = Path("../../data")
        raw_dir = data_dir / "raw"
        processed_dir = data_dir / "processed"
        
        # Create processed directory if it doesn't exist
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Load raw data
        raw_file = raw_dir / "raw_reviews.csv"
        df = load_raw_data(raw_file)
        
        # Log initial statistics
        logger.info("\nInitial data statistics:")
        logger.info(f"Total reviews: {len(df)}")
        logger.info(f"Reviews per app:\n{df['app_name'].value_counts()}")
        
        # Remove duplicates
        df = remove_duplicates(df)
        
        # Handle missing data
        df = handle_missing_data(df)
        
        # Normalize dates
        df = normalize_dates(df)
        
        # Preprocess reviews
        df = preprocess_reviews(df)
        
        # Save processed data
        output_file = processed_dir / "cleaned_reviews.csv"
        df.to_csv(output_file, index=False)
        
        # Log final statistics
        logger.info("\nFinal data statistics:")
        logger.info(f"Total reviews after cleaning: {len(df)}")
        logger.info(f"Reviews per app:\n{df['app_name'].value_counts()}")
        logger.info(f"Saved cleaned data to {output_file}")
        
    except Exception as e:
        logger.error(f"Error in preprocessing: {str(e)}")
        raise

if __name__ == "__main__":
    main() 