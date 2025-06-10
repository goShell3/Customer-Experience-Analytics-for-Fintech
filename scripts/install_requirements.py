#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to install project requirements.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install project requirements."""
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        
        # Path to requirements.txt
        requirements_file = project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print(f"Error: requirements.txt not found at {requirements_file}")
            sys.exit(1)
        
        print("Installing project requirements...")
        
        # Install requirements
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            str(requirements_file)
        ])
        
        # Install spacy language model
        print("\nInstalling spacy language model...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "spacy",
            "download",
            "en_core_web_sm"
        ])
        
        print("\nAll requirements installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()