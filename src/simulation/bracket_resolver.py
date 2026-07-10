import json
from pathlib import Path
BRACKET_FILE = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "round_of_32_bracket.json"
)
ANNEX_FILE = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "annex_c_mapping.json"
)


def load_annex_mapping():

    with open(ANNEX_FILE, encoding="utf-8") as f:
        return json.load(f)
    
def find_correct_mapping(best_third):

    annex = load_annex_mapping()

    qualified_groups = {
        team["group"][-1]
        for team in best_third
    }

    print("\nQualified Third Place Groups:")
    print(sorted(qualified_groups))

    for option, mapping in annex.items():

        groups_in_option = {
            opponent[0]
            for opponent in mapping.values()
        }

        if groups_in_option == qualified_groups:

            print(f"\nMatched FIFA Option {option}")

            return mapping

    raise ValueError(
        "No matching FIFA Annex C option found."
    )    

def load_bracket():

    with open(BRACKET_FILE) as f:
        return json.load(f)
    
def build_slot_map(
    qualified,
    best_third,
):

    slot_map = {}

    for team in qualified:

        slot = (
            team["group"][-1]
            + str(team["position"])
        )

        slot_map[slot] = team["team"]

    for team in best_third:

        slot = (
            team["group"][-1]
            + "3"
        )

        slot_map[slot] = team["team"]

    return slot_map

def create_round_of_32(
    qualified,
    best_third,
):

    slot_map = build_slot_map(
        qualified,
        best_third,
    )

    annex = find_correct_mapping(
        best_third
    )

    bracket = load_bracket()

    fixtures = []

    for match in bracket:

        home_team = slot_map[
            match["home_slot"]
        ]

        # Fixed opponent
        if (
            "away_slot" in match
            and match["away_slot"] is not None
        ):

            away_team = slot_map[
                match["away_slot"]
            ]

        # Third-place opponent
        else:

            third_slot = annex[
                match["home_slot"]
            ]

            away_team = slot_map[
                third_slot
            ]

        fixtures.append(
            {
                "match": match["match"],
                "home_team": home_team,
                "away_team": away_team,
            }
        )

    return fixtures