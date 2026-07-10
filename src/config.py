"""
Configuration settings for FIFA World Cup Predictor
Centralized place for all constants and settings
"""

import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATASETS_DIR = PROJECT_ROOT / "datasets"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
MODELS_DIR = PROJECT_ROOT / "saved_models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Model Configuration
RANDOM_STATE = 42
CROSS_VALIDATION_FOLDS = 5

# Feature Configuration
TARGET_COLUMN = "result"  # "home_win", "draw", "away_win"

# Simulation Settings
NUM_SIMULATIONS = 10000
TOURNAMENT_SIMULATIONS = [100, 1000, 10000, 100000]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# UI Settings
STREAMLIT_CONFIG = {
    "theme": "dark",
    "page_width": "wide",
    "initial_sidebar_state": "expanded",
}
TRAIN_END_YEAR = 2018

VALIDATION_END_YEAR = 2021

PRIMARY_METRIC = "f1_macro"

N_SPLITS = 5

MONTE_CARLO_RUNS = 10000

# Dataset Files
RAW_RESULTS_FILE = DATA_DIR / "results.csv"

CLEANED_RESULTS_FILE = DATASETS_DIR / "cleaned_results.csv"

ENGINEERED_FEATURES_FILE = DATASETS_DIR / "engineered_features.csv"
# Model Files
BASELINE_MODEL_FILE = MODELS_DIR / "logistic_regression_model.pkl"

TUNED_MODEL_FILE = MODELS_DIR / "tuned_logistic_model.pkl"

# Output Files
MODEL_COMPARISON_FILE = OUTPUTS_DIR / "model_comparison.csv"

FEATURE_IMPORTANCE_FILE = OUTPUTS_DIR / "feature_importance.csv"

CV_RESULTS_FILE = OUTPUTS_DIR / "cv_results.csv"