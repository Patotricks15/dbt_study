import pandas as pd
from sklearn.datasets import load_iris
import os

iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df["species"] = pd.Categorical.from_codes(iris.target, iris.target_names)

os.makedirs("data/bronze", exist_ok=True)

output_path = "data/bronze/iris.csv"
df.to_csv(output_path, index=False)

print(f"Iris dataset salvo em {output_path}")