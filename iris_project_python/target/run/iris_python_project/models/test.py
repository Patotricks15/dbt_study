
  
    # models/gold_test.py
import pandas as pd
import os

def model(dbt, session):
    # Obtém a referência do model gold
    gold_relation = dbt.ref("3_gold")
    
    # Monta a query SQL para ler os dados do model gold
    query = f"SELECT * FROM {gold_relation}"
    df = session.execute(query).fetchdf()
    
    # Filtra os dados de teste
    test_df = df[df["split"] == "test"]
    
    # Salva o CSV de teste na camada gold
    os.makedirs("data/gold", exist_ok=True)
    test_csv = os.path.join("data", "gold", "iris_test.csv")
    test_df.to_csv(test_csv, index=False)
    
    return test_df


# This part is user provided model code
# you will need to copy the next section to run the code
# COMMAND ----------
# this part is dbt logic for get ref work, do not modify

def ref(*args, **kwargs):
    refs = {"3_gold": "\"db\".\"main\".\"3_gold\""}
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
    identifier = "test"
    
    def __repr__(self):
        return '"db"."main"."test"'


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
    tmp_name = '__dbt_python_model_df_' + 'test__dbt_tmp'
    con.register(tmp_name, df)
    con.execute('create table "db"."main"."test__dbt_tmp" as select * from ' + tmp_name)
    con.unregister(tmp_name)

  