"""
KuralCompanion - Hugging Face Spaces Entry Point
This file serves as the main entry point for Hugging Face Spaces deployment
"""

import streamlit as st
import sys
import os

# Add src directory to path for Hugging Face Spaces
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if os.path.exists(src_path):
    sys.path.insert(0, src_path)
else:
    # If src directory doesn't exist, assume we're already in the right place
    pass

# Import and run the main Streamlit app
from streamlit_app import main

if __name__ == "__main__":
    main()
