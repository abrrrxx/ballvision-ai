"""Prediction utilities for the FIFA World Cup match predictor."""

from pathlib import Path

import joblib
import pandas as pd

from src.feature_engineering.team_state import TEAM_FEATURES
from src.models.trainer import FEATURE_COLUMNS
from src.preprocessing.rankings import (
    get_ranking_map,
    normalize_team_name,
)
from src.config import BASELINE_MODEL_FILE

PREDICTION_COLUMNS = FEATURE_COLUMNS


from pathlib import Path
import joblib

def load_model(model_path=BASELINE_MODEL_FILE):
    print("MODEL PATH:", model_path)
    print("MODEL EXISTS:", Path(model_path).exists())
    return joblib.load(model_path)


MODEL = load_model()


def get_supported_teams() -> set[str]:
    return set(get_ranking_map().keys())


def validate_prediction_teams(home_team: str, away_team: str):

    home_team = normalize_team_name(home_team)
    away_team = normalize_team_name(away_team)

    supported = get_supported_teams()

    if home_team not in supported:
        raise ValueError(f"{home_team} not supported.")

    if away_team not in supported:
        raise ValueError(f"{away_team} not supported.")

    return home_team, away_team


def build_prediction_frame(
    home_team: str,
    away_team: str,
    date: str,
) -> pd.DataFrame:

    home_team, away_team = validate_prediction_teams(
        home_team,
        away_team,
    )

    home = TEAM_FEATURES[home_team]
    away = TEAM_FEATURES[away_team]

    ranking = get_ranking_map()

    prediction_row = pd.DataFrame(
        [
            {
                "home_recent_form_5": home["recent_form_5"],
                "away_recent_form_5": away["recent_form_5"],

                "home_recent_form_10": home["recent_form_10"],
                "away_recent_form_10": away["recent_form_10"],

                "home_win_rate_5": home["win_rate_5"],
                "away_win_rate_5": away["win_rate_5"],

                "home_win_rate_10": home["win_rate_10"],
                "away_win_rate_10": away["win_rate_10"],

                "home_avg_goals_scored_5": home["goals_scored_5"],
                "away_avg_goals_scored_5": away["goals_scored_5"],

                "home_avg_goals_conceded_5": home["goals_conceded_5"],
                "away_avg_goals_conceded_5": away["goals_conceded_5"],

                "home_avg_goal_diff_5": home["goal_diff_5"],
                "away_avg_goal_diff_5": away["goal_diff_5"],

                "home_team_strength_delta":
                    home["goal_diff_5"] - away["goal_diff_5"],

                "home_elo_rating":
                    home["elo"],

                "away_elo_rating":
                    away["elo"],

                "elo_rating_diff":
                    home["elo"] - away["elo"],

                "rank_diff":
                    ranking[home_team] - ranking[away_team],

                "home_days_since_last_match":
                    home["days_since_last_match"],

                "away_days_since_last_match":
                    away["days_since_last_match"],

                "home_advantage": 1,

                "home_team":
                    home["team_id"],

                "away_team":
                    away["team_id"],

                "home_team_win_rate":
                    home["win_rate_5"],

                "away_team_win_rate":
                    away["win_rate_5"],

                "goal_difference":
                    home["goal_diff_5"] - away["goal_diff_5"],
            }
        ]
    )

    return prediction_row[PREDICTION_COLUMNS]


def predict_match(
    home_team: str,
    away_team: str,
    date: str,
):
    """Predict a single football match."""

    home_team, away_team = validate_prediction_teams(
        home_team,
        away_team,
    )

    X = build_prediction_frame(
        home_team,
        away_team,
        date,
    )

    prediction = MODEL.predict(X)[0]

    probabilities = MODEL.predict_proba(X)[0]

    probability_by_class = {
        cls: float(prob)
        for cls, prob in zip(
            MODEL.classes_,
            probabilities,
        )
    }

    return {
        "home_team": home_team,
        "away_team": away_team,
        "date": date,

        "predicted_result": prediction,

        "home_win_probability":
            probability_by_class.get(
                "home_win",
                0.0,
            ),

        "draw_probability":
            probability_by_class.get(
                "draw",
                0.0,
            ),

        "away_win_probability":
            probability_by_class.get(
                "away_win",
                0.0,
            ),

        "probabilities":
            probability_by_class,
    }