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

1. Scrape reviews:
```bash
python src/data/scrape_reviews.py
```

2. Clean and process data:
```bash
python src/data/clean_reviews.py
```

3. Run analysis notebooks in the `notebooks/` directory.

## Development

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed 