from src.simulation.groups import load_groups
from src.simulation.group_stage import simulate_group
from src.simulation.qualification import (
    get_top_two,
    get_best_third,
)
from src.simulation.bracket_resolver import create_round_of_32
from src.simulation.knockout import simulate_knockout_tournament

def simulate_tournament():
    results = {
    "groups": {},
    "knockout": {},
}

    groups = load_groups()

    group_tables = {}

    for group_name, teams in groups.items():

        table = simulate_group(
            group_name,
            teams,
        )

        group_tables[group_name] = table
        results["groups"][group_name] = table

    qualified = get_top_two(group_tables)

    best_third = get_best_third(group_tables)

    round_of_32 = create_round_of_32(
        qualified,
        best_third,
    )
    

    knockout_results = simulate_knockout_tournament(
    round_of_32
    )

    results["knockout"] = knockout_results
    

    return results


def main():

    results = simulate_tournament()

    final = results["knockout"]["final"][0]

    print("\n")
    print("=" * 70)
    print("🏆 FIFA WORLD CUP 2026 FINAL")
    print("=" * 70)

    print(
        f"{final['home_team']} "
        f"{final['home_goals']} - "
        f"{final['away_goals']} "
        f"{final['away_team']}"
    )

    print()

    print(
        f"🏆 Champion: {results['knockout']['champion']}"
    )


if __name__ == "__main__":
    main()