from datetime import date, timedelta

from src.prediction.predictor import predict_match
from src.simulation.fixtures import generate_group_fixtures
from src.simulation.score_generator import generate_score
from src.simulation.standings import (
    initialize_group_table,
    update_table,
)

def simulate_group(group_name, teams):
    fixtures = generate_group_fixtures(teams)

    table = initialize_group_table(teams)

    current_date = date(2026, 7, 7)
    print("\n" + "=" * 60)
    print(group_name)
    print("=" * 60)
    print()
    for fixture in fixtures:
        home_team = fixture["home_team"]
        away_team = fixture["away_team"]
        prediction = predict_match(
          home_team,
          away_team,
          str(current_date),
    ) 
        
        home_goals, away_goals = generate_score(
         prediction["predicted_result"]
         )  
        print(
        f"{home_team} vs {away_team} -> {prediction['predicted_result']}")

        table = update_table(
         table,
         home_team,
         away_team,
         home_goals,
         away_goals,
      )
        print(
    f"{home_team:<15} {home_goals} - {away_goals} {away_team}"
     )
        current_date += timedelta(days=1)
        
    table = table.sort_values(
         by=[
        "Points",
        "Goal Difference",
        "Goals For",
         ],
         ascending=False,
      )
    print("\n")

    print("=" * 50)

    print(group_name)

    print("=" * 50)

    print(table.to_string(index=False))
    qualified = table.head(2)

    print("\nQualified for Round of 16:")

    for _, row in qualified.iterrows():
     print(f"✅ {row['Team']}")
    
    return table
    

def main():

 simulate_group(
    "Group A",
    [
        "Spain",
        "Japan",
        "Portugal",
        "Brazil",
    ],
)

if __name__ == "__main__":
    main()