import pandas as pd


def initialize_group_table(group_teams):
    """
    Create an empty standings table for one group.
    """

    table = pd.DataFrame(
        {
            "Team": group_teams,
            "Played": 0,
            "Won": 0,
            "Draw": 0,
            "Lost": 0,
            "Goals For": 0,
            "Goals Against": 0,
            "Goal Difference": 0,
            "Points": 0,
        }
    )

    return table

def update_table(
    table,
    home_team,
    away_team,
    home_goals,
    away_goals,
):
    table.loc[
    table["Team"] == home_team,
    "Played"
    ] += 1

    table.loc[
    table["Team"] == away_team,
    "Played"
     ] += 1
    table.loc[
    table["Team"] == home_team,
    "Goals For"
   ] += home_goals

    table.loc[
    table["Team"] == home_team,
    "Goals Against"
] += away_goals

    table.loc[
    table["Team"] == away_team,
    "Goals For"
] += away_goals

    table.loc[
    table["Team"] == away_team,
    "Goals Against"
] += home_goals
    
    table["Goal Difference"] = (
    table["Goals For"]
    - table["Goals Against"]
)
    if home_goals > away_goals:

        table.loc[
        table["Team"] == home_team,
        "Won"
    ] += 1

        table.loc[
        table["Team"] == away_team,
      "Lost"
    ] += 1

        table.loc[
        table["Team"] == home_team,
        "Points"
    ] += 3
       
    elif home_goals < away_goals:
        
        table.loc[
        table["Team"] == away_team,
        "Won"
    ] += 1

        table.loc[
        table["Team"] == home_team,
        "Lost"
    ] += 1

        table.loc[
        table["Team"] == away_team,
        "Points"
    ] += 3
    
    else:
        table.loc[
        table["Team"] == home_team,
        "Draw"
    ] += 1

        table.loc[
        table["Team"] == away_team,
        "Draw"
    ] += 1
        
        table.loc[
        table["Team"] == home_team,
        "Points"
    ] += 1

        table.loc[
        table["Team"] == away_team,
        "Points"
    ] += 1

    table = table.sort_values(
    by=[
        "Points",
        "Goal Difference",
        "Goals For",
    ],
    ascending=False,
)
    return table