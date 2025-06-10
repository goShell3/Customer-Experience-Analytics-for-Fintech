"""
Script for analyzing themes in banking app reviews using NLP.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
from ethiopic_nlp import AmharicNLP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
nlp = spacy.load('en_core_web_sm')
amharic_nlp = AmharicNLP()

# Define theme keywords
THEME_KEYWORDS = {
    'Login Issues': ['login', 'password', 'authentication', 'access', 'account'],
    'Transaction Speed': ['slow', 'fast', 'speed', 'transaction', 'transfer'],
    'UI/UX': ['interface', 'design', 'layout', 'screen', 'button'],
    'App Stability': ['crash', 'error', 'bug', 'freeze', 'hang'],
    'Customer Service': ['support', 'service', 'help', 'contact', 'response'],
    'Security': ['secure', 'security', 'safe', 'protection', 'privacy'],
    'Features': ['feature', 'function', 'option', 'tool', 'service']
}

def load_data(file_path: Path) -> pd.DataFrame:
    """Load cleaned reviews data."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} reviews from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def preprocess_text(text: str) -> str:
    """Preprocess text by tokenizing, removing stopwords, and lemmatizing."""
    if not isinstance(text, str):
        return ""
    
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords (both English and Amharic)
    stop_words = set(stopwords.words('english'))
    # Add Amharic stopwords if available
    try:
        amharic_stop_words = set(amharic_nlp.get_stopwords())
        stop_words.update(amharic_stop_words)
    except:
        logger.warning("Could not load Amharic stopwords")
    
    tokens = [t for t in tokens if t not in stop_words]
    
    # Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    
    return ' '.join(tokens)

def identify_themes(text: str) -> List[str]:
    """Identify themes in text based on keyword matching."""
    themes = []
    text = text.lower()
    
    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            themes.append(theme)
    
    return themes

def generate_wordcloud(text: str, bank_name: str, output_dir: Path):
    """Generate and save word cloud for a bank's reviews."""
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=100
    ).generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud - {bank_name}')
    
    # Save word cloud
    output_file = output_dir / f'wordcloud_{bank_name.lower().replace(" ", "_")}.png'
    plt.savefig(output_file)
    plt.close()
    
    logger.info(f"Generated word cloud for {bank_name}")

def analyze_themes(df: pd.DataFrame, output_dir: Path):
    """Analyze themes in reviews and generate visualizations."""
    # Preprocess all reviews
    df['processed_text'] = df['review_text'].apply(preprocess_text)
    
    # Calculate TF-IDF
    vectorizer = TfidfVectorizer(max_features=100)
    tfidf_matrix = vectorizer.fit_transform(df['processed_text'])
    
    # Get feature names
    feature_names = vectorizer.get_feature_names_out()
    
    # Analyze themes for each bank
    themes_by_bank = []
    
    for bank in df['app_name'].unique():
        bank_reviews = df[df['app_name'] == bank]
        
        # Combine all processed reviews for word cloud
        combined_text = ' '.join(bank_reviews['processed_text'])
        generate_wordcloud(combined_text, bank, output_dir)
        
        # Identify themes
        bank_reviews['themes'] = bank_reviews['processed_text'].apply(identify_themes)
        
        # Count theme occurrences
        theme_counts = {}
        for themes in bank_reviews['themes']:
            for theme in themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Get top keywords
        bank_tfidf = tfidf_matrix[bank_reviews.index]
        top_indices = bank_tfidf.mean(axis=0).argsort()[0, -10:][0]
        top_keywords = [feature_names[i] for i in top_indices]
        
        themes_by_bank.append({
            'bank': bank,
            'theme_counts': theme_counts,
            'top_keywords': top_keywords
        })
    
    # Save theme analysis results
    themes_df = pd.DataFrame(themes_by_bank)
    themes_df.to_csv(output_dir / 'themes_by_bank.csv', index=False)
    logger.info("Saved theme analysis results")

def main():
    """Main function to analyze review themes."""
    try:
        # Set up paths
        data_dir = Path("../../data")
        processed_dir = data_dir / "processed"
        output_dir = data_dir / "analysis"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load cleaned reviews
        reviews_file = processed_dir / "cleaned_reviews.csv"
        df = load_data(reviews_file)
        
        # Analyze themes
        analyze_themes(df, output_dir)
        
        logger.info("Theme analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Error in theme analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 