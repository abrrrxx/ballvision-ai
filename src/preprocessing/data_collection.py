"""Download a public historical international football results dataset."""

from pathlib import Path

import pandas as pd
import requests

DATA_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "data" / "results.csv"


def download_results_data(output_path: Path = OUTPUT_PATH, url: str = DATA_URL) -> Path:
    """Download the historical results dataset if it is not already present."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"Dataset already exists at: {output_path}")
        return output_path

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    print(f"Downloaded dataset to: {output_path}")
    return output_path


def inspect_dataset(path: Path) -> None:
    """Load the dataset and print its basic structure."""
    df = pd.read_csv(path)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nShape:")
    print(df.shape)


if __name__ == "__main__":
    path = download_results_data()
    inspect_dataset(path)
