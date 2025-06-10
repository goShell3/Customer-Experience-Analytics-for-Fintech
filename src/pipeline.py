import pandas as pd
from preprocessing import preprocess_data
from sentiment_analysis import SentimentAnalyzer
from .thematic_analysis import ThemeAnalyzer
from .config import CONFIG
import json

def run_pipeline():
    # Load data
    print("Loading data...")
    df = pd.read_csv(CONFIG["DATA_PATH"])
    
    # Preprocessing
    df = preprocess_data(df)
    
    # Sentiment Analysis
    sentiment_analyzer = SentimentAnalyzer()
    df = sentiment_analyzer.analyze_dataframe(df)
    sentiment_summary = sentiment_analyzer.aggregate_by_rating(df)
    
    # Thematic Analysis
    theme_analyzer = ThemeAnalyzer()
    df, themes = theme_analyzer.analyze_themes(df)
    
    # Save results
    print("Saving results...")
    df.to_csv(CONFIG["OUTPUT_PATH"], index=False)
    sentiment_summary.to_csv("output/sentiment_summary.csv", index=False)
    
    with open(CONFIG["THEMES_OUTPUT_PATH"], "w") as f:
        json.dump(themes, f, indent=2)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()