import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.ui import render_main_ui

if __name__ == "__main__":
    render_main_ui()