#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify imports are working correctly.
"""

import os
import sys

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try importing the modules
try:
    from src.data.scrape_reviews import scrape_app_reviews
    from src.data.clean_reviews import load_raw_data, remove_duplicates, preprocess_reviews
    print("Successfully imported all modules!")
except ImportError as e:
    print(f"Import error: {str(e)}")
    print("\nCurrent Python path:")
    for path in sys.path:
        print(f"- {path}") 