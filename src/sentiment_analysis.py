from transformers import pipeline
import pandas as pd
from config import CONFIG

class SentimentAnalyzer:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model=CONFIG["SENTIMENT_MODEL"],
            tokenizer=CONFIG["SENTIMENT_MODEL"]
        )
    
    def analyze_sentiment(self, text):
        if not text.strip():
            return {"label": "neutral", "score": 0.0}
        
        result = self.model(text)[0]
        return result
    
    def analyze_dataframe(self, df, text_column="processed_text"):
        print("Performing sentiment analysis...")
        
        # Analyze sentiment for each review
        results = df[text_column].apply(self.analyze_sentiment)
        
        # Extract labels and scores
        df["sentiment_label"] = [r["label"] for r in results]
        df["sentiment_score"] = [r["score"] for r in results]
        
        # Adjust for neutral sentiment
        neutral_mask = (df["sentiment_score"] < (0.5 + CONFIG["NEUTRAL_THRESHOLD"])) & \
                      (df["sentiment_score"] > (0.5 - CONFIG["NEUTRAL_THRESHOLD"]))
        df.loc[neutral_mask, "sentiment_label"] = "neutral"
        
        return df
    
    def aggregate_by_rating(self, df):
        print("Aggregating sentiment by bank and rating...")
        aggregation = {
            "sentiment_score": "mean",
            "sentiment_label": lambda x: x.mode()[0] if not x.mode().empty else "neutral"
        }
        
        grouped = df.groupby(["bank_name", "rating"]).agg(aggregation).reset_index()
        grouped.rename(columns={"sentiment_label": "dominant_sentiment"}, inplace=True)
        
        return grouped