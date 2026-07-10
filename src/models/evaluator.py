"""Compare candidate models using chronological train/validation/test splits.

The goal of this file is model selection: train several algorithms on the same
features and choose based on macro F1, not only raw accuracy.
"""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.feature_engineering.features import engineer_features, load_cleaned_data, save_engineered_data
from src.models.trainer import FEATURE_COLUMNS, prepare_training_data, split_by_year

from src.config import (
    ENGINEERED_FEATURES_FILE,
    MODEL_COMPARISON_FILE,
)
CATEGORICAL_FEATURES = ["home_team", "away_team"]
NUMERIC_FEATURES = [col for col in FEATURE_COLUMNS if col not in CATEGORICAL_FEATURES]


def load_data(path: Path = ENGINEERED_FEATURES_FILE) -> pd.DataFrame:
    """Load engineered data, regenerating it if required columns are missing."""
    if path.exists():
        df = pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
        if all(col in df.columns for col in FEATURE_COLUMNS):
            return df

    cleaned_df = load_cleaned_data()
    engineered_df = engineer_features(cleaned_df)
    save_engineered_data(engineered_df, path)
    return engineered_df.sort_values("date").reset_index(drop=True)


def build_pipeline(model) -> Pipeline:
    """Create preprocessing plus estimator for mixed numeric/categorical data."""
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                NUMERIC_FEATURES,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    return make_pipeline(preprocessor, model)


def build_models() -> dict[str, object]:
    """Return candidate models that are useful for a first comparison."""
    return {
        "logistic_regression_balanced": LogisticRegression(
            max_iter=2000,
            random_state=42,
            class_weight="balanced",
        ),
        "random_forest_balanced": RandomForestClassifier(
            n_estimators=150,
            max_depth=10,
            min_samples_leaf=8,
            random_state=42,
            class_weight="balanced",
            n_jobs=1,
        ),
        "extra_trees_balanced": ExtraTreesClassifier(
            n_estimators=150,
            max_depth=10,
            min_samples_leaf=8,
            random_state=42,
            class_weight="balanced",
            n_jobs=1,
        ),
    }


def score_predictions(y_true: pd.Series, y_pred) -> dict[str, float]:
    """Calculate metrics for one split."""
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


def evaluate_models() -> pd.DataFrame:
    """Train and evaluate candidate models, then save a comparison table."""
    df = load_data()
    train_df, validation_df, test_df = split_by_year(df)
    X_train, y_train = prepare_training_data(train_df)
    X_validation, y_validation = prepare_training_data(validation_df)
    X_test, y_test = prepare_training_data(test_df)

    results = []
    for name, model in build_models().items():
        pipeline = build_pipeline(model)
        pipeline.fit(X_train, y_train)

        validation_pred = pipeline.predict(X_validation)
        test_pred = pipeline.predict(X_test)
        validation_scores = score_predictions(y_validation, validation_pred)
        test_scores = score_predictions(y_test, test_pred)

        row = {"model": name}
        row.update({f"validation_{metric}": value for metric, value in validation_scores.items()})
        row.update({f"test_{metric}": value for metric, value in test_scores.items()})
        results.append(row)
        print(f"Completed evaluation for {name}")

    results_df = pd.DataFrame(results).sort_values("validation_f1_macro", ascending=False)
    MODEL_COMPARISON_FILE.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(MODEL_COMPARISON_FILE, index=False)
    print(results_df.to_string(index=False))
    print(f"\nSaved comparison to: {MODEL_COMPARISON_FILE}")
    return results_df


if __name__ == "__main__":
    evaluate_models()

