# Banking App Reviews Analysis

This project analyzes user reviews of banking applications to extract insights and trends.

## Project Structure

```
banking-reviews/
├── data/               # Raw and processed data
│   ├── raw/           # Original, immutable data
│   └── processed/     # Cleaned and transformed data
├── notebooks/         # Jupyter notebooks for analysis
├── src/              # Source code
│   ├── data/         # Data processing scripts
│   ├── features/     # Feature engineering scripts
│   ├── models/       # Model training scripts
│   └── visualization/# Visualization scripts
├── tests/            # Unit tests
├── docs/             # Documentation
├── requirements.txt  # Project dependencies
└── .gitignore       # Git ignore file
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Scrape Reviews
Scrape 400+ reviews for each Ethiopian bank app from Google Play Store:
```bash
python src/data/scrape_reviews.py
```
- Output: `data/raw/raw_reviews.csv`

### 2. Clean and Process Data
Clean the scraped reviews, remove duplicates, handle missing data, and normalize dates:
```bash
python src/data/clean_reviews.py
```
- Output: `data/processed/cleaned_reviews.csv`

### 3. Analyze Themes
Extract common themes and generate word clouds for each bank:
```bash
python src/features/theme_analysis.py
```
- Output: `data/analysis/themes_by_bank.csv` and word cloud images in `data/analysis/`

### 4. Run Jupyter Notebook
Explore and visualize the data:
```bash
cd notebooks
jupyter notebook
```
Open `bank_reviews_analysis.ipynb` for interactive analysis.

### 5. Run Tests
Run all tests to verify functionality:
```bash
pytest tests/
```

## Development

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed # Customer-Experience-Analytics-for-Fintech
