from setuptools import setup, find_packages

setup(
    name="bank_reviews",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "google-play-scraper",
    ],
    python_requires=">=3.8",
) 