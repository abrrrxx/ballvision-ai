from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from src.models.trainer import (
    build_pipeline,
    load_engineered_data,
    prepare_training_data,
    split_by_year,
    FEATURE_COLUMNS_NO_TEAM_NAMES,
)

df = load_engineered_data()

train_df, val_df, test_df = split_by_year(df)

X_train, y_train = prepare_training_data(
    train_df,
    FEATURE_COLUMNS_NO_TEAM_NAMES,
)

X_test, y_test = prepare_training_data(
    test_df,
    FEATURE_COLUMNS_NO_TEAM_NAMES,
)
model = build_pipeline(
    LogisticRegression(
        max_iter=2000,
        random_state=42,
        class_weight="balanced",
    ),
    FEATURE_COLUMNS_NO_TEAM_NAMES,
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(classification_report(y_test, predictions))

print("Macro F1:",
      f1_score(
          y_test,
          predictions,
          average="macro",
      ))