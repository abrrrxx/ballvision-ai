from datetime import date, timedelta

from src.simulation.fixtures import generate_group_fixtures
from src.simulation.standings import (
    initialize_group_table,
    update_table,
)
from src.prediction.predictor import predict_match

def simulate_group(group_name, teams):
    fixtures = generate_group_fixtures(teams)

    table = initialize_group_table(teams)
    