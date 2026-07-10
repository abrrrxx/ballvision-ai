"""Clean and prepare the raw international football results dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

RAW_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "results.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "datasets" / "cleaned_results.csv"


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw football results dataset."""
    return pd.read_csv(path)


def preprocess_results_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw dataset and prepare it for modeling."""
    cleaned = df.copy()

    # 1. Convert date to datetime
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    # 2. Standardize text columns
    for column in ["home_team", "away_team", "tournament", "city", "country"]:
        cleaned[column] = cleaned[column].fillna("Unknown").astype(str).str.strip()

    # 3. Convert score columns to numeric values
    cleaned["home_score"] = pd.to_numeric(cleaned["home_score"], errors="coerce")
    cleaned["away_score"] = pd.to_numeric(cleaned["away_score"], errors="coerce")

    # 4. Handle missing values in score columns
    cleaned["home_score"] = cleaned["home_score"].fillna(cleaned["home_score"].median())
    cleaned["away_score"] = cleaned["away_score"].fillna(cleaned["away_score"].median())

    # 5. Create a target label for match outcome
    cleaned["result"] = np.select(
        [
            cleaned["home_score"] > cleaned["away_score"],
            cleaned["home_score"] < cleaned["away_score"],
        ],
        ["home_win", "away_win"],
        default="draw",
    )

    # 6. Create a simple numeric goal difference feature
    cleaned["goal_difference"] = cleaned["home_score"] - cleaned["away_score"]

    # 7. Keep a clean, usable version of the dataset
    cleaned = cleaned.dropna(subset=["date", "home_team", "away_team"])

    return cleaned


def save_cleaned_data(df: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> Path:
    """Save the cleaned dataset to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    """Run the full cleaning pipeline."""
    raw_df = load_raw_data()
    cleaned_df = preprocess_results_data(raw_df)
    path = save_cleaned_data(cleaned_df)
    print(f"Cleaned dataset saved to: {path}")
    print(cleaned_df.head())
    print(cleaned_df[["home_team", "away_team", "home_score", "away_score", "result", "goal_difference"]].head())


if __name__ == "__main__":
    main()
