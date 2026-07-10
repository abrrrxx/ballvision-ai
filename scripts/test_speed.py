from time import perf_counter
from datetime import date

from src.prediction.predictor import predict_match

start = perf_counter()

predict_match(
    "Brazil",
    "Argentina",
    str(date.today())
)

end = perf_counter()

print(f"{end-start:.2f} seconds")