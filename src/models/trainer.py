"""Train a leak-free baseline model for match result prediction."""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.feature_engineering.features import engineer_features, load_cleaned_data, save_engineered_data

from src.config import (
    ENGINEERED_FEATURES_FILE,
    BASELINE_MODEL_FILE,
)

FEATURE_COLUMNS = [
    "home_recent_form_5",
    "away_recent_form_5",
    "home_recent_form_10",
    "away_recent_form_10",
    "home_win_rate_5",
    "away_win_rate_5",
    "home_win_rate_10",
    "away_win_rate_10",
    "home_avg_goals_scored_5",
    "away_avg_goals_scored_5",
    "home_avg_goals_conceded_5",
    "away_avg_goals_conceded_5",
    "home_avg_goal_diff_5",
    "away_avg_goal_diff_5",
    "home_team_strength_delta",
    "home_elo_rating",
    "away_elo_rating",
    "elo_rating_diff",
    "rank_diff",
    "home_days_since_last_match",
    "away_days_since_last_match",
    "home_advantage",
    "home_team",
    "away_team",
    "home_team_win_rate",
    "away_team_win_rate",
    "goal_difference",
]
FEATURE_COLUMNS_NO_TEAM_NAMES = [
    feature
    for feature in FEATURE_COLUMNS
    if feature not in ["home_team", "away_team"]
]


def load_engineered_data(
    path: Path = ENGINEERED_FEATURES_FILE
) -> pd.DataFrame:
    """Load the engineered feature dataset, regenerating it if needed."""
    if path.exists():
        df = pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
        if all(col in df.columns for col in FEATURE_COLUMNS):
            return df

    cleaned_df = load_cleaned_data()
    engineered_df = engineer_features(cleaned_df)
    save_engineered_data(engineered_df, path)
    return engineered_df.sort_values("date").reset_index(drop=True)


def prepare_training_data(
    df,
    feature_columns=FEATURE_COLUMNS,
):
    X = df[feature_columns]
    y = df["result"]
    return X, y


def get_feature_types(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Split feature columns into numeric and categorical groups."""
    numeric_columns = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = X.select_dtypes(exclude=["number"]).columns.tolist()
    return numeric_columns, categorical_columns


def build_pipeline(
    model,
    feature_columns=FEATURE_COLUMNS,
    ) -> Pipeline:
    """Build a preprocessing pipeline for mixed numeric and categorical features."""
    numeric_features = [
    col for col in feature_columns
    if col not in ["home_team", "away_team"]
    ]

    categorical_features = [
    col for col in ["home_team", "away_team"]
    if col in feature_columns
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]),
                numeric_features,
            ),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical_features,
            ),
        ]
    )
    return make_pipeline(
        preprocessor,
        model,
    )


def split_by_year(df: pd.DataFrame, train_end_year: int = 2018, val_end_year: int = 2021) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split into chronological train/validation/test sets."""
    train = df[df["date"].dt.year <= train_end_year]
    val = df[(df["date"].dt.year > train_end_year) & (df["date"].dt.year <= val_end_year)]
    test = df[df["date"].dt.year > val_end_year]
    return train, val, test


def train_model() -> tuple[object, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Train a baseline logistic regression model and return evaluation artifacts."""
    df = load_engineered_data()
    train_df, val_df, test_df = split_by_year(df)
    X_train, y_train = prepare_training_data(train_df)
    X_val, y_val = prepare_training_data(val_df)
    X_test, y_test = prepare_training_data(test_df)

    model = build_pipeline(
    LogisticRegression(
        max_iter=2000,
        random_state=42,
        class_weight="balanced",
    )
    )
    model.fit(X_train, y_train)

    for name, X, y in [("validation", X_val, y_val), ("test", X_test, y_test)]:
        predictions = model.predict(X)
        accuracy = accuracy_score(y, predictions)
        print(f"{name.capitalize()} accuracy: {accuracy:.4f}")
        print(classification_report(y, predictions))
        print("Confusion Matrix:")
        print(confusion_matrix(y, predictions))

    return model, X_train, y_train, X_val, y_val, X_test, y_test


def save_model(
    model,
    output_path: Path = BASELINE_MODEL_FILE
) -> Path:
    """Save the trained model to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    import joblib

    joblib.dump(model, output_path)
    return output_path


def main() -> None:
    """Run the training pipeline."""
    model, *_ = train_model()
    path = save_model(model)
    print(f"Model saved to: {path}")


if __name__ == "__main__":
    main()

