# src/data_cleaning.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def clean_raw_data(raw_df):
    """
    Tidies wide-formatted scraped tables into machine learning matrices.
    Returns feature matrix X, regression target y_reg, and classification target y_clf.
    """
    # 1. Pivot to Long format for sample generation
    df_long = raw_df.melt(id_vars=["Condition"], var_name="Year", value_name="Price_PHP")
    df_long["Year"] = df_long["Year"].astype(int)
    
    # 2. Convert Data Types and handle structural missing values smoothly
    df_long["Price_PHP"] = pd.to_numeric(df_long["Price_PHP"], errors='coerce')
    df_long["Price_PHP"] = df_long.groupby("Condition")["Price_PHP"].ffill().fillna(0)
    
    # 3. Feature Engineering: One-Hot Encode categorical wear states
    encoder = OneHotEncoder(sparse_output=False)
    encoded_conditions = encoder.fit_transform(df_long[["Condition"]])
    encoded_df = pd.DataFrame(encoded_conditions, columns=encoder.get_feature_names_out(["Condition"]))
    
    # Construct final feature space X
    X = pd.concat([df_long[["Year"]], encoded_df], axis=1)
    
    # 4. Target Generation for Regression (Continuous Valuations)
    y_reg = df_long["Price_PHP"]
    
    # 5. Target Generation for Classification (Price Spikes > 30% over condition median)
    medians = df_long.groupby("Condition")["Price_PHP"].transform("median")
    y_clf = (df_long["Price_PHP"] > (medians * 1.3)).astype(int)
    
    return X, y_reg, y_clf
