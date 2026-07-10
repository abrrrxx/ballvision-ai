from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.inspection import permutation_importance

from src.config import (
    BASELINE_MODEL_FILE,
    FEATURE_IMPORTANCE_FILE,
    RANDOM_STATE,
)

from src.models.trainer import (
    load_engineered_data,
    prepare_training_data,
    split_by_year,
)

def analyze_feature_importance():
   df = load_engineered_data()

   _,_, test_df = split_by_year(df)

   X_test, y_test = prepare_training_data(test_df)

   model = joblib.load(BASELINE_MODEL_FILE)
   importance = permutation_importance(
    estimator=model,
    X=X_test,
    y=y_test,
    scoring="f1_macro",
    n_repeats=20,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    )

   importance_df = pd.DataFrame(
    {
        "Feature": X_test.columns,
        "Importance": importance.importances_mean,
        "Std": importance.importances_std,
    }
    )
   
   importance_df = importance_df.sort_values(
    "Importance",
    ascending=False,
    )
   
   FEATURE_IMPORTANCE_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
    )

   importance_df.to_csv(
    FEATURE_IMPORTANCE_FILE,
    index=False,
    )
   
   print("\nTop 15 Most Important Features:\n")
   print(importance_df.head(15).to_string(index=False))

   plt.figure(figsize=(10, 7))

   top_features = importance_df.head(15)

   plt.barh(
    top_features["Feature"],
    top_features["Importance"],
    )

   plt.gca().invert_yaxis()

   plt.xlabel("Permutation Importance")
   plt.ylabel("Feature")
   plt.title("Top 15 Feature Importance")

   plt.tight_layout()

   plt.savefig("outputs/feature_importance.png")

   plt.show()

def main():
    analyze_feature_importance()


if __name__ == "__main__":
    main()