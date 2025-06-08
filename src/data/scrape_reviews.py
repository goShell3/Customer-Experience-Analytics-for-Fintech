"""
Script for scraping banking app reviews from Google Play Store.
"""

import pandas as pd
from pathlib import Path
from google_play_scraper import Sort, reviews
import time
from datetime import datetime
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# App IDs for Ethiopian banking apps
BANK_APPS = {
    'CBE': 'com.cbe.mobilebanking',
    'BOA': 'com.boa.mobilebanking',
    'Dashen': 'com.dashenbank.mobilebanking'
}

def scrape_app_reviews(app_id: str, app_name: str, count: int = 400) -> List[Dict[str, Any]]:
    """
    Scrape reviews for a specific app.
    
    Args:
        app_id: Google Play Store app ID
        app_name: Name of the banking app
        count: Number of reviews to scrape
    
    Returns:
        List of review dictionaries
    """
    try:
        logger.info(f"Scraping reviews for {app_name} (ID: {app_id})")
        
        # Get reviews with pagination
        result, continuation_token = reviews(
            app_id,
            lang='en',  # English reviews
            country='et',  # Ethiopia
            sort=Sort.NEWEST,
            count=100  # Get 100 reviews per request
        )
        
        all_reviews = result
        
        # Continue scraping until we have enough reviews or no more are available
        while len(all_reviews) < count and continuation_token is not None:
            time.sleep(2)  # Be nice to the API
            result, continuation_token = reviews(
                app_id,
                continuation_token=continuation_token
            )
            all_reviews.extend(result)
            
            logger.info(f"Scraped {len(all_reviews)} reviews for {app_name}")
        
        # Add app name to each review
        for review in all_reviews:
            review['app_name'] = app_name
        
        return all_reviews[:count]  # Return only the requested number of reviews
    
    except Exception as e:
        logger.error(f"Error scraping {app_name}: {str(e)}")
        return []

def main():
    """Main function to scrape reviews for all banking apps."""
    all_reviews = []
    
    for app_name, app_id in BANK_APPS.items():
        try:
            reviews = scrape_app_reviews(app_id, app_name)
            all_reviews.extend(reviews)
            logger.info(f"Successfully scraped {len(reviews)} reviews for {app_name}")
        except Exception as e:
            logger.error(f"Failed to scrape {app_name}: {str(e)}")
    
    if all_reviews:
        # Convert to DataFrame
        df = pd.DataFrame(all_reviews)
        
        # Select and rename columns
        df = df[['app_name', 'content', 'score', 'at']]
        df.columns = ['app_name', 'review_text', 'rating', 'date']
        
        # Convert timestamp to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Save to CSV
        output_dir = Path("../../data/raw")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "raw_reviews.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(df)} reviews to {output_file}")
    else:
        logger.error("No reviews were scraped successfully")

if __name__ == "__main__":
    main() 