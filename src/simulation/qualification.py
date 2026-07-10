import pandas as pd

def get_top_two(group_tables):

    qualified = []

    for group_name, table in group_tables.items():

        for position in [0, 1]:

            row = table.iloc[position]

            qualified.append(
                {
                    "team": row["Team"],
                    "group": group_name,
                    "position": position + 1,
                    "points": row["Points"],
                    "goal_difference": row["Goal Difference"],
                    "goals_for": row["Goals For"],
                }
            )

    return qualified

def get_best_third(group_tables):

    third = []

    for group_name, table in group_tables.items():

        row = table.iloc[2]

        third.append(
            {
                "team": row["Team"],
                "group": group_name,
                "position": 3,
                "points": row["Points"],
                "goal_difference": row["Goal Difference"],
                "goals_for": row["Goals For"],
            }
        )

    third.sort(
        key=lambda x: (
            x["points"],
            x["goal_difference"],
            x["goals_for"],
        ),
        reverse=True,
    )

    return third[:8]