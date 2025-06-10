import os
import pandas as pd
from google_play_scraper import app, Sort, reviews
from typing import Dict, Optional

class GooglePlayScraper:
    """
    Main class for scraping Google Play Store data.
    Renamed from ScrapData to GooglePlayScraper to avoid any naming conflicts
    """
    
    def __init__(self, package_name: str, app_name: str):
        self.package_name = package_name
        self.app_name = app_name

    def get_app_metadata(self, output_dir: str = "data/metadata") -> None:
        """Get app metadata"""
        os.makedirs(output_dir, exist_ok=True)
        result = app(self.package_name)
        pd.DataFrame([result]).to_csv(
            os.path.join(output_dir, f"{self.app_name}_metadata.csv"),
            index=False
        )

    def get_app_reviews(self, count: int = 400) -> pd.DataFrame:
        """Get app reviews with pagination"""
        reviews_data = []
        token = None
        
        while len(reviews_data) < count:
            batch, token = reviews(
                self.package_name,
                count=min(200, count - len(reviews_data)),
                continuation_token=token
            )
            reviews_data.extend(batch)
            if not token:
                break
                
        return pd.DataFrame([{
            'app': self.app_name,
            'review': r['content'],
            'rating': r['score'],
            'date': r['at'].strftime('%Y-%m-%d')
        } for r in reviews_data])

def scrape_all_apps(apps: Dict[str, str], review_count: int = 400) -> None:
    """Batch scraping function"""
    for name, pkg in apps.items():
        scraper = GooglePlayScraper(pkg, name)
        scraper.get_app_metadata()
        reviews_df = scraper.get_app_reviews(review_count)
        reviews_df.to_csv(f"data/reviews/{name}_reviews.csv", index=False)