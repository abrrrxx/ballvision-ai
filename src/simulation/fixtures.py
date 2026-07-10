from itertools import combinations

def generate_group_fixtures(group_teams):
    """
    Generate every match inside one World Cup group.
    """

    fixtures = []

    for home, away in combinations(group_teams, 2):

        fixtures.append(
            {
                "home_team": home,
                "away_team": away,
            }
        )

    return fixtures