
  create view "iris"."public"."iris_silver__dbt_tmp"
    
    
  as (
    with base as (
    select *
    from "iris"."public"."iris_bronze"
)

select
    *,
    case 
      when sepal_width != 0 then sepal_length / sepal_width
      else null
    end as sepal_ratio,
    case
      when petal_width != 0 then petal_length / petal_width
      else null
    end as petal_ratio
from base
  );