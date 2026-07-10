"""
Main entry point for FIFA World Cup Predictor.

Run this app with:
    streamlit run main.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import streamlit as st
from ui.pages import home


def main() -> None:
    """Start the Streamlit user interface."""
    st.set_page_config(
        page_title="FIFA World Cup Predictor",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title("FIFA World Cup Predictor")
    page = st.sidebar.radio(
        "Navigate",
        [
            "Home",
            "Tournament Simulator",
            "Match Predictor",
            "Team Analysis",
            "Analytics Dashboard",
            "Monte Carlo Simulator",
        ],
    )

    if page == "Home":
        home.show()
    else:
        st.info(f"The {page} page has not been built yet.")

    st.sidebar.markdown("---")
    st.sidebar.info(
        "FIFA World Cup Prediction Platform v1.0\n\n"
        "Built with Streamlit and Machine Learning"
    )


if __name__ == "__main__":
    main()
