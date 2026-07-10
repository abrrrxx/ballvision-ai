from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit

from src.models.trainer import (
    build_pipeline,
    load_engineered_data,
    prepare_training_data,
    split_by_year,
)

PARAM_GRID = {
    "logisticregression__C": [0.01,
    0.1,
    5,
    10,
    20,
    50,
    100],
    "logisticregression__solver": ['newton-cg','lbfgs','liblinear','sag','saga'],
    "logisticregression__class_weight": ["balanced", None],
}

def tune_model():
        df = load_engineered_data()

        train_df, validation_df, test_df = split_by_year(df)

        X_train, y_train = prepare_training_data(train_df)
        X_validation, y_validation = prepare_training_data(validation_df)
        X_test, y_test = prepare_training_data(test_df)

        pipeline = build_pipeline(
         LogisticRegression(
        random_state=42,
        max_iter=2000
         )
        )
        
        tscv = TimeSeriesSplit(n_splits=5)
        
        grid_search = GridSearchCV(
         estimator=pipeline,
         param_grid=PARAM_GRID,
         scoring="f1_macro",
         cv=tscv,
         n_jobs=-1,
         verbose=2,
        )
        grid_search.fit(X_train, y_train)
        print("\nBest Parameters:")
        print(grid_search.best_params_)

        print("\nBest Cross Validation Macro F1:")
        print(grid_search.best_score_)

        best_model = grid_search.best_estimator_
        for name, X, y in [
        ("Validation", X_validation, y_validation),
        ("Test", X_test, y_test),
        ]:

         predictions = best_model.predict(X)

        print(f"\n{name} Results")

        print("Accuracy:",
          accuracy_score(y, predictions))

        print("Precision:",
          precision_score(y, predictions,
                          average="macro"))

        print("Recall:",
          recall_score(y, predictions,
                       average="macro"))

        print("Macro F1:",
          f1_score(y, predictions,
                   average="macro")) 

        from src.config import (
    ENGINEERED_FEATURES_FILE,
    TUNED_MODEL_FILE,
)

        TUNED_MODEL_FILE.parent.mkdir(exist_ok=True)

        joblib.dump(best_model, TUNED_MODEL_FILE)

        print(f"\nModel saved to {TUNED_MODEL_FILE}")

def main():

    best_model = tune_model()

    print("Hyperparameter tuning completed successfully.")       


if __name__ == "__main__":
    main()