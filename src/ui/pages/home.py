"""
Home page for FIFA World Cup Predictor
"""

import streamlit as st


def show():
    """Display the home page"""
    st.title("⚽ FIFA World Cup Prediction Platform")
    st.markdown(
        """
        ### Professional Football Analytics & Tournament Prediction
        
        Welcome to the FIFA World Cup Prediction Platform - a comprehensive
        machine learning system for predicting international football matches
        and simulating entire FIFA World Cup tournaments.
        
        ---
        
        #### 🎯 What Can This Platform Do?
        
        ✅ **Predict Individual Matches** - ML-powered match predictions
        ✅ **Simulate World Cup** - Complete tournament simulations
        ✅ **Team Analysis** - Detailed team statistics and performance
        ✅ **Monte Carlo Simulations** - Statistical tournament predictions
        ✅ **Analytics Dashboard** - Model performance and insights
        
        ---
        
        #### 📊 Latest Model Performance
        
        *Model performance metrics will be displayed here once trained*
        
        ---
        
        #### 🚀 Quick Start
        
        1. Navigate to **Tournament Simulator** to simulate a World Cup
        2. Use **Match Predictor** for specific predictions
        3. Check **Analytics Dashboard** to understand the model
        
        """
    )


if __name__ == "__main__":
    show()
