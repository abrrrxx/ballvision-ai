from src.simulation.tournament import simulate_tournament

results = simulate_tournament()

print(results.keys())

print()

print(results["groups"].keys())

print()

print(results["knockout"].keys())

print()

print(results["knockout"]["champion"])