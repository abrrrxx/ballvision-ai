"""Simple CLI for predicting a match outcome."""

import argparse

from src.prediction.predictor import predict_match


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict a football match result")
    parser.add_argument("home_team", help="Name of the home team")
    parser.add_argument("away_team", help="Name of the away team")
    parser.add_argument("date", help="Match date in YYYY-MM-DD format")
    args = parser.parse_args()

    result = predict_match(args.home_team, args.away_team, args.date)
    print(result)
