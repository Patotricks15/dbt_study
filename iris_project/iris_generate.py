import pandas as pd
from sklearn.datasets import load_iris

# Carrega o dataset Iris
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

# Renomeia as colunas para ficar sem espaços e padronizadas
df.columns = [col.replace(' (cm)', '').replace(' ', '_') for col in df.columns]

# Salva o CSV na pasta 'seeds'
df.to_csv('data/iris_bronze.csv', index=False)
print("Arquivo data/iris_bronze.csv gerado com sucesso!")
