import os
import sys

# Get the absolute path of the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root) 