"""Load and prepare FIFA ranking data for feature engineering.

The project expects a CSV at data/fifa_rankings.csv. The loader accepts several
common column names used by public FIFA ranking datasets and returns a simple
DataFrame with normalized team names and numeric ranks.
"""

from pathlib import Path

import pandas as pd
import requests

OUTPUT_PATH = Path(__file__).resolve().parents[2] / "data" / "fifa_rankings.csv"

# Keep URLs in a list so dead public links can be replaced without changing the
# rest of the project. If all downloads fail, the loader uses a small educational
# fallback instead of silently returning all-zero ranking features.
RANKING_URLS: tuple[str, ...] = ()

FALLBACK_RANKINGS: dict[str, int] = {
    "Argentina": 1,
    "France": 2,
    "Spain": 3,
    "England": 4,
    "Brazil": 5,
    "Portugal": 6,
    "Netherlands": 7,
    "Belgium": 8,
    "Italy": 9,
    "Germany": 10,
    "Croatia": 11,
    "Uruguay": 12,
    "Morocco": 13,
    "Colombia": 14,
    "Mexico": 15,
    "United States": 16,
    "Switzerland": 17,
    "Japan": 18,
    "Senegal": 19,
    "Denmark": 20,
    "Austria": 21,
    "Iran": 22,
    "South Korea": 23,
    "Australia": 24,
    "Ukraine": 25,
    "Turkey": 26,
    "Ecuador": 27,
    "Poland": 28,
    "Sweden": 29,
    "Wales": 30,
    "Scotland": 31,
}

TEAM_ALIASES: dict[str, str] = {
    "USA": "United States",
    "US": "United States",
    "United States of America": "United States",
    "Korea Republic": "South Korea",
    "Republic of Korea": "South Korea",
    "IR Iran": "Iran",
    "Türkiye": "Turkey",
    "T?rkiye": "Turkey",
    "England": "England",
    "Côte d'Ivoire": "Ivory Coast",
    "Czech Republic": "Czechia",
    "Curacao": "Curaçao",
    "Cabo Verde": "Cape Verde",
    "Congo DR": "DR Congo",

}

TEAM_COLUMN_CANDIDATES = ["team", "country", "country_full", "nation", "name"]
RANK_COLUMN_CANDIDATES = ["rank", "ranking", "rank_position", "fifa_rank"]
POINTS_COLUMN_CANDIDATES = [
    "total_points",
    "points",
]
DATE_COLUMN_CANDIDATES = ["rank_date", "date", "ranking_date"]


def normalize_team_name(team: object) -> str:
    """Return a consistent team name for matching rankings to match data."""
    normalized = str(team).strip()
    normalized = " ".join(normalized.split())
    return TEAM_ALIASES.get(normalized, normalized)


def download_rankings_data(output_path: Path = OUTPUT_PATH, urls: tuple[str, ...] = RANKING_URLS) -> Path:
    """Download ranking data from the first working configured URL."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        return output_path

    errors = []
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            errors.append(f"{url}: {exc}")
            continue

        output_path.write_bytes(response.content)
        return output_path

    message = "No FIFA ranking CSV found at data/fifa_rankings.csv."
    if errors:
        message += " Download attempts failed: " + " | ".join(errors)
    raise FileNotFoundError(message)


def _find_column(columns: list[str], candidates: list[str]) -> str | None:
    lookup = {column.lower().strip(): column for column in columns}
    for candidate in candidates:
        if candidate in lookup:
            return lookup[candidate]
    return None


def _fallback_rankings() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "team": [normalize_team_name(team) for team in FALLBACK_RANKINGS],
            "rank": list(FALLBACK_RANKINGS.values()),
            "source": "fallback",
        }
    )


def load_rankings_data(path: Path = OUTPUT_PATH, use_fallback: bool = True) -> pd.DataFrame:
    """Load rankings as columns: team, rank, source.

    If the CSV contains ranking dates, the latest row per team is used.
    """
    if not path.exists():
        try:
            download_rankings_data(path)
        except FileNotFoundError:
            if use_fallback:
                return _fallback_rankings()
            raise

    df = pd.read_csv(path)
    team_col = _find_column(df.columns.tolist(), TEAM_COLUMN_CANDIDATES)
    rank_col = _find_column(df.columns.tolist(), RANK_COLUMN_CANDIDATES)
    points_col = _find_column(
    df.columns.tolist(),
    POINTS_COLUMN_CANDIDATES,
    )

    if team_col is None or rank_col is None:
        if use_fallback:
            return _fallback_rankings()
        raise ValueError(
            "Ranking CSV must contain a team column and a rank column. "
            f"Found columns: {list(df.columns)}"
        )

    rankings = df.copy()
    rankings["team"] = rankings[team_col].map(normalize_team_name)
    rankings["rank"] = pd.to_numeric(rankings[rank_col], errors="coerce")
    if points_col is not None:
        rankings["points"] = pd.to_numeric(
        rankings[points_col],
        errors="coerce",
        )
    rankings = rankings.dropna(subset=["team", "rank"])

    date_col = _find_column(rankings.columns.tolist(), DATE_COLUMN_CANDIDATES)
    if date_col is not None:
        rankings["rank_date"] = pd.to_datetime(rankings[date_col], errors="coerce")
        rankings = rankings.sort_values("rank_date").groupby("team", as_index=False).tail(1)
    else:
        rankings = rankings.groupby("team", as_index=False)["rank"].min()

    columns = ["team", "rank"]

    if "points" in rankings.columns:
      columns.append("points")

    rankings = rankings[columns].copy()
    rankings["rank"] = rankings["rank"].astype(float)
    rankings["source"] = "csv"
    return rankings.sort_values("rank").reset_index(drop=True)


def get_ranking_map(path: Path = OUTPUT_PATH) -> dict[str, float]:
    """Return a normalized team-name to rank lookup."""
    rankings = load_rankings_data(path)
    return dict(zip(rankings["team"], rankings["rank"]))


if __name__ == "__main__":
    rankings_df = load_rankings_data()
    print(rankings_df.head(20).to_string(index=False))
    print(f"Loaded {len(rankings_df)} teams from {rankings_df['source'].iloc[0]} rankings.")
