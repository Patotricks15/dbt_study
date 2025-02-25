# models/bronze.py
import pandas as pd
import os

def model(dbt, session):
    csv_path = os.path.join("data", "bronze", "iris.csv")
    
    df = pd.read_csv(csv_path)
    
    df.columns = [col.strip().replace(" ", "_").replace("(", "").replace(")", "") for col in df.columns]
    
    os.makedirs("data/bronze", exist_ok=True)
    clean_csv = os.path.join("data", "bronze", "iris_clean.csv")
    df.to_csv(clean_csv, index=False)
    
    return df
