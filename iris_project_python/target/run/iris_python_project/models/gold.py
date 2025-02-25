
  
    # models/gold.py
import pandas as pd
import numpy as np
import os

def model(dbt, session):
    # Lê o CSV da camada silver
    silver_csv = os.path.join("data", "silver", "iris_silver.csv")
    df = pd.read_csv(silver_csv)
    
    # Cria a coluna 'split' com 70% para treino e 30% para teste
    np.random.seed(42)
    df["split"] = np.where(np.random.rand(len(df)) < 0.7, "train", "test")
    
    # Cria o diretório da camada gold, se necessário, e salva o CSV gold completo
    os.makedirs("data/gold", exist_ok=True)
    gold_csv = os.path.join("data", "gold", "iris_gold.csv")
    df.to_csv(gold_csv, index=False)
    
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
    identifier = "gold"
    
    def __repr__(self):
        return '"db"."main"."gold"'


class dbtObj:
    def __init__(self, load_df_function) -> None:
        self.source = lambda *args: source(*args, dbt_load_df_function=load_df_function)
        self.ref = lambda *args, **kwargs: ref(*args, **kwargs, dbt_load_df_function=load_df_function)
        self.config = config
        self.this = this()
        self.is_incremental = False

# COMMAND ----------




def materialize(df, con):
    try:
        import pyarrow
        pyarrow_available = True
    except ImportError:
        pyarrow_available = False
    finally:
        if pyarrow_available and isinstance(df, pyarrow.Table):
            # https://github.com/duckdb/duckdb/issues/6584
            import pyarrow.dataset
    tmp_name = '__dbt_python_model_df_' + 'gold__dbt_tmp'
    con.register(tmp_name, df)
    con.execute('create table "db"."main"."gold__dbt_tmp" as select * from ' + tmp_name)
    con.unregister(tmp_name)

  