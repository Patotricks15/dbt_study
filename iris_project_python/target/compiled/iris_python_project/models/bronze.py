# models/bronze.py
import pandas as pd
import os

def model(dbt, session):
    # Caminho para o CSV de ingestão (gerado previamente)
    csv_path = os.path.join("data", "bronze", "iris.csv")
    
    # Lê o CSV com pandas
    df = pd.read_csv(csv_path)
    
    # Opcional: renomeia as colunas para remover espaços e caracteres especiais
    df.columns = [col.strip().replace(" ", "_").replace("(", "").replace(")", "") for col in df.columns]
    
    # (Opcional) Salva um CSV "limpo" para referência, se necessário
    os.makedirs("data/bronze", exist_ok=True)
    clean_csv = os.path.join("data", "bronze", "iris_clean.csv")
    df.to_csv(clean_csv, index=False)
    
    return df


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args, **kwargs):
    refs = {}
    key = '.'.join(args)
    version = kwargs.get("v") or kwargs.get("version")
    if version:
        key += f".v{version}"
    dbt_load_df_function = kwargs.get("dbt_load_df_function")
    return dbt_load_df_function(refs[key])


def source(*args, dbt_load_df_function):
    sources = {}
    key = '.'.join(args)
    return dbt_load_df_function(sources[key])


config_dict = {}


class config:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get(key, default=None):
        return config_dict.get(key, default)

class this:
    """dbt.this() or dbt.this.identifier"""
    database = "db"
    schema = "main"
    identifier = "bronze"
    
    def __repr__(self):
        return '"db"."main"."bronze"'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args, **kwargs: ref(*args, **kwargs, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------


