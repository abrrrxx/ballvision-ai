"""Create leak-free, rolling football features from cleaned match results data."""

from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd

from src.preprocessing.rankings import get_ranking_map, normalize_team_name

CLEANED_DATA_PATH = Path(__file__).resolve().parents[2] / "datasets" / "cleaned_results.csv"
OUTPUT_PATH = Path(__file__).resolve().parents[2] / "datasets" / "engineered_features.csv"


def load_cleaned_data(path: Path = CLEANED_DATA_PATH) -> pd.DataFrame:
    """Load the cleaned match results dataset and sort it by date."""
    return pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)


def _safe_mean(values: deque) -> float:
    return float(np.mean(values)) if values else 0.0


def _safe_rate(values: deque, target_value: int) -> float:
    if not values:
        return 0.5
    return float(sum(1 for value in values if value == target_value) / len(values))


def add_pre_match_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create rolling team-strength features using only prior matches."""
    engineered = df.copy()
    engineered["date"] = pd.to_datetime(engineered["date"])
    engineered = engineered.sort_values("date").reset_index(drop=True)
    engineered["home_advantage"] = 1

    try:
        ranking_map = get_ranking_map()
    except Exception:
        ranking_map = {}

    team_stats = defaultdict(
        lambda: {
            "results_5": deque(maxlen=5),
            "results_10": deque(maxlen=10),
            "goals_scored_5": deque(maxlen=5),
            "goals_scored_10": deque(maxlen=10),
            "goals_conceded_5": deque(maxlen=5),
            "goals_conceded_10": deque(maxlen=10),
            "goal_diff_5": deque(maxlen=5),
            "goal_diff_10": deque(maxlen=10),
            "elo_rating": 1500.0,
            "last_match_date": pd.NaT,
            "matches_played": 0,
        }
    )

    team_to_id = {}
    for team in sorted(set(pd.concat([engineered["home_team"], engineered["away_team"]]).astype(str))):
        team_to_id[team] = len(team_to_id) + 1

    rows = []
    for _, row in engineered.iterrows():
        home_team = str(row["home_team"])
        away_team = str(row["away_team"])
        home_team = normalize_team_name(str(row["home_team"]))
        away_team = normalize_team_name(str(row["away_team"]))
        match_date = row["date"]

        home_stats = team_stats[home_team]
        away_stats = team_stats[away_team]

        # Convert result to a numeric value for rolling form.
        if row["result"] == "home_win":
            result_value = 1
        elif row["result"] == "away_win":
            result_value = -1
        else:
            result_value = 0

        home_form_5 = _safe_mean(home_stats["results_5"])
        away_form_5 = _safe_mean(away_stats["results_5"])
        home_form_10 = _safe_mean(home_stats["results_10"])
        away_form_10 = _safe_mean(away_stats["results_10"])

        home_win_rate_5 = _safe_rate(home_stats["results_5"], 1)
        away_win_rate_5 = _safe_rate(away_stats["results_5"], 1)
        home_win_rate_10 = _safe_rate(home_stats["results_10"], 1)
        away_win_rate_10 = _safe_rate(away_stats["results_10"], 1)

        home_avg_goals_scored_5 = _safe_mean(home_stats["goals_scored_5"])
        away_avg_goals_scored_5 = _safe_mean(away_stats["goals_scored_5"])
        home_avg_goals_conceded_5 = _safe_mean(home_stats["goals_conceded_5"])
        away_avg_goals_conceded_5 = _safe_mean(away_stats["goals_conceded_5"])
        home_avg_goal_diff_5 = _safe_mean(home_stats["goal_diff_5"])
        away_avg_goal_diff_5 = _safe_mean(away_stats["goal_diff_5"])

        home_team_strength = home_avg_goal_diff_5 + home_form_5
        away_team_strength = away_avg_goal_diff_5 + away_form_5
        home_team_strength_delta = home_team_strength - away_team_strength
        home_elo_rating = home_stats["elo_rating"]
        home_team_id = team_to_id.get(home_team, 0)
        away_team_id = team_to_id.get(away_team, 0)
        goal_difference = home_avg_goal_diff_5 - away_avg_goal_diff_5
        away_elo_rating = away_stats["elo_rating"]
        elo_rating_diff = home_elo_rating - away_elo_rating

        rank_diff = 0.0
        home_rank_team = normalize_team_name(home_team)
        away_rank_team = normalize_team_name(away_team)
        if home_rank_team in ranking_map and away_rank_team in ranking_map:
            rank_diff = float(ranking_map[home_rank_team]) - float(ranking_map[away_rank_team])

        home_days_since_last_match = 30
        away_days_since_last_match = 30
        if pd.notna(home_stats["last_match_date"]):
            home_days_since_last_match = (match_date - home_stats["last_match_date"]).days
        if pd.notna(away_stats["last_match_date"]):
            away_days_since_last_match = (match_date - away_stats["last_match_date"]).days

        rows.append(
            {
                "home_recent_form_5": home_form_5,
                "away_recent_form_5": away_form_5,
                "home_recent_form_10": home_form_10,
                "away_recent_form_10": away_form_10,
                "home_win_rate_5": home_win_rate_5,
                "away_win_rate_5": away_win_rate_5,
                "home_win_rate_10": home_win_rate_10,
                "away_win_rate_10": away_win_rate_10,
                "home_avg_goals_scored_5": home_avg_goals_scored_5,
                "away_avg_goals_scored_5": away_avg_goals_scored_5,
                "home_avg_goals_conceded_5": home_avg_goals_conceded_5,
                "away_avg_goals_conceded_5": away_avg_goals_conceded_5,
                "home_avg_goal_diff_5": home_avg_goal_diff_5,
                "away_avg_goal_diff_5": away_avg_goal_diff_5,
                "home_team_strength_delta": home_team_strength_delta,
                "home_team_name": home_team,
                "away_team_name": away_team,

                "home_team": home_team_id,
                "away_team": away_team_id,
                "home_team_win_rate": home_win_rate_5,
                "away_team_win_rate": away_win_rate_5,
                "goal_difference": goal_difference,
                "home_elo_rating": home_elo_rating,
                "away_elo_rating": away_elo_rating,
                "elo_rating_diff": elo_rating_diff,
                "rank_diff": rank_diff,
                "home_days_since_last_match": home_days_since_last_match,
                "away_days_since_last_match": away_days_since_last_match,
            }
        )

        # Update histories after computing the features, so the current match is not leaked.
        home_stats["results_5"].append(result_value)
        away_stats["results_5"].append(-result_value)
        home_stats["results_10"].append(result_value)
        away_stats["results_10"].append(-result_value)
        home_stats["goals_scored_5"].append(int(row["home_score"]))
        away_stats["goals_scored_5"].append(int(row["away_score"]))
        home_stats["goals_scored_10"].append(int(row["home_score"]))
        away_stats["goals_scored_10"].append(int(row["away_score"]))
        home_stats["goals_conceded_5"].append(int(row["away_score"]))
        away_stats["goals_conceded_5"].append(int(row["home_score"]))
        home_stats["goals_conceded_10"].append(int(row["away_score"]))
        away_stats["goals_conceded_10"].append(int(row["home_score"]))
        home_stats["goal_diff_5"].append(int(row["home_score"]) - int(row["away_score"]))
        away_stats["goal_diff_5"].append(int(row["away_score"]) - int(row["home_score"]))
        home_stats["goal_diff_10"].append(int(row["home_score"]) - int(row["away_score"]))
        away_stats["goal_diff_10"].append(int(row["away_score"]) - int(row["home_score"]))
        home_stats["last_match_date"] = match_date
        away_stats["last_match_date"] = match_date
        home_stats["matches_played"] += 1
        away_stats["matches_played"] += 1

        if result_value == 1:
            home_stats["elo_rating"] += 16
            away_stats["elo_rating"] -= 16
        elif result_value == -1:
            home_stats["elo_rating"] -= 16
            away_stats["elo_rating"] += 16
        else:
            home_stats["elo_rating"] += 0
            away_stats["elo_rating"] += 0

    engineered = engineered.drop(columns=["goal_difference"], errors="ignore")
    engineered = pd.concat(
    [engineered.reset_index(drop=True), pd.DataFrame(rows)],
    axis=1,
)

    engineered = engineered.loc[
     :,
     ~engineered.columns.duplicated()
       ].copy()

    team_features = {}

    for team, stats in team_stats.items():

          last_row = engineered[
        (engineered["home_team_name"] == team)
        |
        (engineered["away_team_name"] == team)
        ].iloc[-1]

          if last_row["home_team_name"] == team:
               team_features[team] = {

            "recent_form_5": last_row["home_recent_form_5"],
            "recent_form_10": last_row["home_recent_form_10"],

            "win_rate_5": last_row["home_win_rate_5"],
            "win_rate_10": last_row["home_win_rate_10"],

            "goals_scored_5": last_row["home_avg_goals_scored_5"],
            "goals_conceded_5": last_row["home_avg_goals_conceded_5"],
            "goal_diff_5": last_row["home_avg_goal_diff_5"],

            "elo": last_row["home_elo_rating"],

            "days_since_last_match":
                last_row["home_days_since_last_match"],

            "team_id":
                last_row["home_team"],
        }

          else:

              team_features[team] = {

            "recent_form_5": last_row["away_recent_form_5"],
            "recent_form_10": last_row["away_recent_form_10"],

            "win_rate_5": last_row["away_win_rate_5"],
            "win_rate_10": last_row["away_win_rate_10"],

            "goals_scored_5": last_row["away_avg_goals_scored_5"],
            "goals_conceded_5": last_row["away_avg_goals_conceded_5"],
            "goal_diff_5": last_row["away_avg_goal_diff_5"],

            "elo": last_row["away_elo_rating"],

            "days_since_last_match":
                last_row["away_days_since_last_match"],

            "team_id":
                last_row["away_team"],
        }
    
    return engineered, team_features


def engineer_features(df, return_state=False):
    engineered, team_features = add_pre_match_rolling_features(df)

    if return_state:
      return engineered, team_features

    return engineered

def save_engineered_data(df: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> Path:
    """Save the engineered dataset to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    """Run the full feature engineering pipeline."""
    raw_df = load_cleaned_data()
    engineered_df = engineer_features(raw_df)
    path = save_engineered_data(engineered_df)
    print(f"Engineered dataset saved to: {path}")
    print(engineered_df[["home_team", "away_team", "result", "home_recent_form_5", "away_recent_form_5", "home_advantage"]].head())


if __name__ == "__main__":
    main()





