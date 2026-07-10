from src.feature_engineering.features import (
    engineer_features,
    load_cleaned_data,
)

RAW_DATA = load_cleaned_data()

ENGINEERED_DATA, TEAM_FEATURES = engineer_features(
    RAW_DATA,
    return_state=True,
)