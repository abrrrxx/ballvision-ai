import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT = BASE_DIR / "assets" / "annex_c.txt"
OUTPUT = BASE_DIR / "assets" / "annex_c_mapping.json"

slot_columns = [
    "A1",
    "B1",
    "D1",
    "E1",
    "G1",
    "I1",
    "K1",
    "L1",
]

mapping = {}

with open(INPUT, encoding="utf-8") as f:

    lines = f.readlines()

for line in lines:

    line = line.strip()

    if not line:
        continue

    if line.startswith("Option"):
        continue

    parts = line.split()

    if len(parts) != 9:
        continue

    option = parts[0]

    row = {}

    for slot, opponent in zip(slot_columns, parts[1:]):

        row[slot] = opponent[1] + "3"

    mapping[option] = row

with open(OUTPUT, "w", encoding="utf-8") as f:

    json.dump(mapping, f, indent=4)

print(f"Saved {len(mapping)} options.")