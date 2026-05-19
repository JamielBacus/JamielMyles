# src/models.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, classification_report


def train_regression_model(X, y_reg):
    """Trains a Random Forest Regressor and outputs error distributions and metrics."""
    X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    print("\n" + "=" * 40)
    print("        REGRESSION EXPERIMENT METRICS        ")
    print("=" * 40)
    print(f"RMSE (Avg Error Vector deviation): ₱{rmse:.2f}")
    print(f"R² (Proportion of variance explained): {r2:.2f}")

    # Extract structural feature importance metrics
    importances = model.feature_importances_
    imp_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance',
                                                                                         ascending=False)
    print("\n--- FEATURE IMPORTANCES ---")
    print(imp_df.to_string(index=False))


def train_classifier_model(X, y_clf):
    """
    Trains an optimized Logistic Regression Classifier.
    Fixed: Increased max_iter to solve convergence and balanced weights for small samples.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y_clf, test_size=0.3, random_state=42, stratify=y_clf)

    # max_iter=1000 allows the algorithm plenty of steps to converge
    # class_weight='balanced' forces the model to pay attention to the rare '1' spikes
    model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("\n" + "=" * 40)
    print("      CLASSIFICATION REPORT (SURGE METRICS)   ")
    print("=" * 40)
    # zero_division=0 clears out the messy warnings if the test partition remains too small to compute safely
    print(classification_report(y_test, preds, target_names=["Stable (0)", "Price Spike (1)"], zero_division=0))