"""
Script for scraping banking app reviews from Google Play Store.
"""

import pandas as pd
from google_play_scraper import Sort, reviews
from typing import List, Dict, Any

# App IDs for Ethiopian banking apps
BANK_APPS = {
    'CBE': 'com.cbe.mobilebanking',
    'BOA': 'com.boa.mobilebanking',
    'Dashen': 'com.dashenbank.mobilebanking'
}

def scrape_app_reviews(apps: Dict[str, str], reviews_per_app: int = 400) -> List[Dict[str, Any]]:
    """
    Scrape reviews from Google Play Store for given apps.
    """
    all_reviews = []

    for app_name, app_id in apps.items():
        app_reviews = []
        count = 0
        next_token = None

        while count < reviews_per_app:
            rvs, next_token = reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=200,
                continuation_token=next_token
            )
            for r in rvs:
                app_reviews.append({
                    'app': app_name,
                    'review': r['content'],
                    'rating': r['score'],
                    'date': r['at'].isoformat()
                })
            count += len(rvs)
            if not next_token:
                break

        all_reviews.extend(app_reviews[:reviews_per_app])

    return all_reviews

def save_reviews_to_csv(reviews_data: List[Dict[str, Any]], filename: str = "raw_reviews.csv"):
    df = pd.DataFrame(reviews_data)
    df.to_csv(filename, index=False)
    print(f"[INFO] Saved {len(df)} reviews to {filename}")

def main():
    print("[INFO] Starting scraping process...")
    scraped_data = scrape_app_reviews(BANK_APPS, reviews_per_app=400)
    save_reviews_to_csv(scraped_data)
    print("[INFO] Scraping complete.")

if __name__ == "__main__":
    main()
