import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_sentiment(sentiment_summary):
    """
    Visualize sentiment by bank and rating
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=sentiment_summary,
        x="bank_name",
        y="sentiment_score",
        hue="rating",
        palette="viridis"
    )
    plt.title("Average Sentiment Score by Bank and Rating")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/sentiment_analysis.png")
    plt.close()

def visualize_themes(themes):
    """
    Visualize theme distribution
    """
    theme_counts = {theme: len(keywords) for theme, keywords in themes.items()}
    df = pd.DataFrame.from_dict(theme_counts, orient="index", columns=["count"])
    
    plt.figure(figsize=(10, 6))
    df.sort_values("count", ascending=False).plot(kind="bar", legend=False)
    plt.title("Theme Keyword Counts")
    plt.ylabel("Number of Keywords")
    plt.tight_layout()
    plt.savefig("output/theme_distribution.png")
    plt.close()