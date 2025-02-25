import pandas as pd
import numpy as np
import os

def model(dbt, session):
    silver_csv = os.path.join("data", "silver", "iris_silver.csv")
    df = pd.read_csv(silver_csv)
    
    np.random.seed(42)
    df["split"] = np.where(np.random.rand(len(df)) < 0.7, "train", "test")
    
    os.makedirs("data/gold", exist_ok=True)
    gold_csv = os.path.join("data", "gold", "iris_gold.csv")
    df.to_csv(gold_csv, index=False)
    
    return df
