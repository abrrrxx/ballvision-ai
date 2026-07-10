from src.prediction.predictor import predict_match
from src.simulation.score_generator import generate_score
from datetime import date


from random import choice


def simulate_knockout_match(
    home_team,
    away_team,
):
    

    prediction = predict_match(
        home_team,
        away_team,
        str(date.today()),
    )
    
    result = prediction["predicted_result"]

    # Knockout matches cannot end in a draw
    if result == "draw":

        if (
            prediction["home_win_probability"]
            >= prediction["away_win_probability"]
        ):
            result = "home_win"

        else:
            result = "away_win"

    home_goals, away_goals = generate_score(result)

    if result == "home_win":
        winner = home_team
    else:
        winner = away_team

    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "winner": winner,
    }

def simulate_knockout_round(fixtures):

    winners = []
    results = []

    for fixture in fixtures:

        result = simulate_knockout_match(
            fixture["home_team"],
            fixture["away_team"],
        )

        winners.append(result["winner"])
        results.append(result)

    return winners, results

def create_next_round(teams):

    fixtures = []

    for i in range(0, len(teams), 2):

        fixtures.append(
            {
                "home_team": teams[i],
                "away_team": teams[i + 1],
            }
        )

    return fixtures

def simulate_knockout_tournament(round_of_32):

    history = {
        "round_of_32": [],
        "round_of_16": [],
        "quarter_finals": [],
        "semi_finals": [],
        "final": [],
        "champion": None,
        "runner_up": None,
    }

    current_round = round_of_32

    stages = [
        "Round of 32",
        "Round of 16",
        "Quarter Finals",
        "Semi Finals",
        "Final",
    ]

    match_numbers = {
        "Round of 32": 73,
        "Round of 16": 89,
        "Quarter Finals": 97,
        "Semi Finals": 101,
        "Final": 103,
    }

    for stage in stages:

        start = match_numbers[stage]

        print("\n")
        print("=" * 70)
        print(stage.upper())
        print("=" * 70)

        for i, fixture in enumerate(current_round):

            print(
                f"Match {start + i}: "
                f"{fixture['home_team']} vs {fixture['away_team']}"
            )

        winners, results = simulate_knockout_round(current_round)

        # Save results
        if stage == "Round of 32":
            history["round_of_32"] = results

        elif stage == "Round of 16":
            history["round_of_16"] = results

        elif stage == "Quarter Finals":
            history["quarter_finals"] = results

        elif stage == "Semi Finals":
            history["semi_finals"] = results

        elif stage == "Final":

            history["final"] = results

            history["champion"] = winners[0]

            final_match = results[0]

            if final_match["winner"] == final_match["home_team"]:
                history["runner_up"] = final_match["away_team"]
            else:
                history["runner_up"] = final_match["home_team"]

            return history

        # Build next round
        current_round = create_next_round(winners)

    return history

   
