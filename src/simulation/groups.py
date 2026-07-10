from pathlib import Path
import json

GROUP_FILE = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "world_cup_groups.json"
)

def load_groups():

    with open(GROUP_FILE) as f:
        return json.load(f)