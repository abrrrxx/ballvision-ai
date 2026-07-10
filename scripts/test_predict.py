from datetime import date

from src.prediction.predictor import predict_match

result = predict_match(
    "Brazil",
    "Jordan",
    str(date.today())
)

print(result)