import pandas as pd
df = pd.read_parquet("data/iris_bronze.parquet")
print(df.head())
print(df.columns)
