import pandas as pd

from src.feature_engineering.features import add_pre_match_rolling_features


def test_add_pre_match_rolling_features_adds_expected_columns():
    df = pd.DataFrame(
        [
            {
                "date": "2000-01-01",
                "home_team": "A",
                "away_team": "B",
                "home_score": 2,
                "away_score": 1,
                "result": "home_win",
            },
            {
                "date": "2000-01-02",
                "home_team": "B",
                "away_team": "A",
                "home_score": 0,
                "away_score": 2,
                "result": "away_win",
            },
        ]
    )

    engineered = add_pre_match_rolling_features(df)

    assert "home_recent_form_5" in engineered.columns
    assert "away_recent_form_5" in engineered.columns
    assert "home_advantage" in engineered.columns
    assert "home_elo_rating" in engineered.columns
    assert "away_elo_rating" in engineered.columns
    assert "elo_rating_diff" in engineered.columns
    assert engineered.loc[0, "home_recent_form_5"] == 0.0
    assert engineered.loc[1, "home_recent_form_5"] == -1.0
    assert engineered.loc[0, "home_elo_rating"] == 1500.0
