"""
KuralCompanion - Hugging Face Spaces Entry Point
This file serves as the main entry point for Hugging Face Spaces deployment
"""

import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main Streamlit app
from streamlit_app import main

if __name__ == "__main__":
    main()
