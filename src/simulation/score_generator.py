import random

from src.config import RANDOM_STATE

random.seed(RANDOM_STATE)

HOME_WIN_SCORES = [
    (1, 0),
    (2, 0),
    (2, 1),
    (3, 1),
    (3, 2),
    (3, 0),
    (4, 3),
    (4, 1),
]

DRAW_SCORES = [
    (0, 0),
    (1, 1),
    (2, 2),
]

AWAY_WIN_SCORES = [
    (0, 1),
    (0, 2),
    (1, 2),
    (2, 3),
    (1, 3),
    (3, 4),
    (0, 3),
]

def generate_score(prediction):

    if prediction == "home_win":
        return random.choice(HOME_WIN_SCORES)

    elif prediction == "draw":
        return random.choice(DRAW_SCORES)

    else:
        return random.choice(AWAY_WIN_SCORES)
    
def main():

    for _ in range(10):

        print(generate_score("home_win"))

    print()

    for _ in range(10):

        print(generate_score("draw"))

    print()

    for _ in range(10):

        print(generate_score("away_win"))


if __name__ == "__main__":
    main()