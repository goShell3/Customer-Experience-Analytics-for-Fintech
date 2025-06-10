import spacy
import pandas as pd
from config import CONFIG

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Preprocess a single text document
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    doc = nlp(text.lower().strip())
    tokens = []
    
    for token in doc:
        if CONFIG["REMOVE_PUNCT"] and token.is_punct:
            continue
        if token.is_stop and token.text in nlp.Defaults.stop_words:
            continue
        if token.is_space:
            continue
            
        lemma = token.lemma_ if CONFIG["LEMMATIZE"] else token.text
        tokens.append(lemma)
    
    return " ".join(tokens)

def preprocess_data(df, text_column="review_text"):
    """
    Preprocess the entire dataframe
    """
    print("Preprocessing text data...")
    df[text_column] = df[text_column].astype(str)
    df["processed_text"] = df[text_column].apply(preprocess_text)
    return df