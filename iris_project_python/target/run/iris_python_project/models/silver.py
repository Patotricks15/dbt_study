
  
    # models/silver.py
import pandas as pd
import os

def model(dbt, session):
    # Caminho para o CSV limpo da camada bronze
    bronze_relation = dbt.ref("bronze")
    query = f"SELECT * FROM {bronze_relation}"
    df = session.execute(query).fetchdf()
    
    # Cria novas colunas de transformação
    # Exemplo: área da sépala e área da pétala
    df["sepal_area"] = df["sepal_length_cm"] * df["sepal_width_cm"]
    df["petal_area"] = df["petal_length_cm"] * df["petal_width_cm"]
    
    # Cria o diretório da camada silver, se necessário
    os.makedirs("data/silver", exist_ok=True)
    silver_csv = os.path.join("data", "silver", "iris_silver.csv")
    df.to_csv(silver_csv, index=False)
    
    return df


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args, **kwargs):
    refs = {"bronze": "\"db\".\"main\".\"bronze\""}
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
    identifier = "silver"
    
    def __repr__(self):
        return '"db"."main"."silver"'


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
    tmp_name = '__dbt_python_model_df_' + 'silver__dbt_tmp'
    con.register(tmp_name, df)
    con.execute('create table "db"."main"."silver__dbt_tmp" as select * from ' + tmp_name)
    con.unregister(tmp_name)

  