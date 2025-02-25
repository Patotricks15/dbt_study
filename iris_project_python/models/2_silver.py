# models/silver.py
import pandas as pd
import os

def model(dbt, session):
    bronze_csv = os.path.join("data", "bronze", "iris_clean.csv")
    df = pd.read_csv(bronze_csv)
    

    df["sepal_area"] = df["sepal_length_cm"] * df["sepal_width_cm"]
    df["petal_area"] = df["petal_length_cm"] * df["petal_width_cm"]
    
    os.makedirs("data/silver", exist_ok=True)
    silver_csv = os.path.join("data", "silver", "iris_silver.csv")
    df.to_csv(silver_csv, index=False)
    
    return df
