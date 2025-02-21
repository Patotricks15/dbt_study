with base as (
    select *
    from {{ ref('iris_bronze') }}
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
